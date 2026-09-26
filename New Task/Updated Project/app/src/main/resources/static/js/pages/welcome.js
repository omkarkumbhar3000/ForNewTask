import { get } from '../api.js';
import { layout } from '../layout.js';
import { h, mount } from '../ui.js';

await layout({ area: 'public' });

const TAGS = ['tag-sun', 'tag-sky', 'tag-berry', 'tag-lilac', '', 'tag-sun'];

try {
  const courses = await get('/public/courses');
  mount('#catalogue', courses.map((c, i) =>
    h('li', {}, h('span', { class: 'tag ' + TAGS[i % TAGS.length], text: (c.icon || '📘') + ' ' + c.title }))));
} catch {
  document.getElementById('catalogue').closest('.panel').hidden = true;
}

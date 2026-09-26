import { get } from '../api.js';
import { layout } from '../layout.js';
import { h, mount } from '../ui.js';

await layout({ area: 'public', current: '/contact' });

try {
  const contact = await get('/public/contact');
  if (contact.configured) {
    mount('#contact-line', 'Email: ', h('a', { href: 'mailto:' + contact.email, text: contact.email }));
    document.getElementById('contact-line').classList.remove('muted');
  } else {
    // INF-02: the owner has not supplied the address yet; nothing personal is invented.
    mount('#contact-line', 'The contact address is being set up. Until then, signed-in parents can use the Feedback page.');
  }
} catch {
  mount('#contact-line', 'The contact address could not be loaded. Please try again later.');
}

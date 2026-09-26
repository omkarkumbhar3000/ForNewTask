import { get, post } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, showErrors, clearErrors, toast, fmtDate } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/feedback.html' });

const CATEGORIES = [
  ['GENERAL', 'General feedback'], ['COURSE', 'About a course'], ['USABILITY', 'Something was hard to use'],
  ['SUGGESTION', 'A suggestion'], ['PROBLEM', 'Something went wrong'],
];
const STATUS = { NEW: 'Sent', READ: 'Read by the team', RESOLVED: 'Resolved' };

async function render() {
  const [courses, mine] = await Promise.all([get('/public/courses'), get('/parent/feedback')]);
  const courseField = h('div', { class: 'field', hidden: true },
    h('label', { for: 'courseId', text: 'Which course?' }),
    h('select', { id: 'courseId', name: 'courseId' }, courses.map((c) => h('option', { value: c.id, text: c.title }))));
  const category = h('select', { id: 'category', name: 'category', required: true },
    CATEGORIES.map(([value, label]) => h('option', { value, text: label })));
  category.addEventListener('change', () => { courseField.hidden = category.value !== 'COURSE'; });

  const form = h('form', { class: 'form panel', novalidate: true },
    h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }),
    h('div', { class: 'field' }, h('label', { for: 'category', text: 'What is it about?' }), category),
    courseField,
    h('fieldset', { class: 'field' }, h('legend', {}, 'How do you like CleverCubs? ', h('span', { class: 'opt', text: '(optional)' })),
      h('div', { class: 'row' }, [1, 2, 3, 4, 5].map((n) => h('label', { class: 'check' },
        h('input', { type: 'radio', name: 'rating', value: n }), h('span', { text: '⭐'.repeat(n) }))))),
    h('div', { class: 'field' }, h('label', { for: 'message', text: 'Your message' }),
      h('textarea', { id: 'message', name: 'message', maxlength: 2000, required: true }),
      h('p', { class: 'hint', text: 'Only the CleverCubs team can read this. Your children never see it.' })),
    h('div', {}, h('button', { class: 'btn btn-primary', type: 'submit', text: 'Send feedback' })));

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(form);
    try {
      await post('/parent/feedback', {
        category: category.value,
        courseId: category.value === 'COURSE' ? Number(form.courseId.value) : null,
        rating: Number(form.querySelector('[name="rating"]:checked')?.value) || null,
        message: form.message.value,
      });
      toast('Thank you. Your feedback has been sent.', 'good');
      render();
    } catch (e) {
      showErrors(form, e);
    }
  });

  mount('#main', h('div', { class: 'page-text stack-lg' },
    h('h1', { text: 'Send us feedback' }),
    h('p', { class: 'muted', text: 'Tell us what works, what does not, and what you would like to see.' }),
    form,
    mine.length ? h('section', { class: 'panel' }, h('h2', { text: 'What you have sent' }),
      h('ul', { class: 'list' }, mine.map((f) => h('li', {},
        h('div', { class: 'row-between' },
          h('strong', { text: CATEGORIES.find(([v]) => v === f.category)?.[1] || f.category }),
          h('span', { class: 'tag', text: STATUS[f.status] || f.status })),
        h('p', { class: 'small muted', text: fmtDate(f.createdAt) + (f.courseTitle ? `, ${f.courseTitle}` : '') }),
        h('p', { text: f.message }))))) : null));
}

if (!ctx.blocked) await render();

import { get, post } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, showErrors, clearErrors, toast } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/' });
if (!ctx.blocked) await render();

async function render() {
  const [avatars, ages] = await Promise.all([get('/public/avatars'), get('/public/ages')]);
  const username = h('input', { id: 'username', name: 'username', type: 'text', maxlength: 20, autocomplete: 'off' });
  const form = h('form', { class: 'form panel', novalidate: true },
    h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }),
    h('div', { class: 'grid-2' },
      h('div', { class: 'field' }, h('label', { for: 'firstName' }, 'First name ', h('span', { class: 'req', text: '(required)' })),
        h('input', { id: 'firstName', name: 'firstName', type: 'text', maxlength: 40, required: true, autocomplete: 'off' })),
      h('div', { class: 'field' }, h('label', { for: 'displayName' }, 'Nickname to show ', h('span', { class: 'opt', text: '(optional)' })),
        h('input', { id: 'displayName', name: 'displayName', type: 'text', maxlength: 40, autocomplete: 'off' }))),
    h('div', { class: 'field' }, h('label', { for: 'dateOfBirth' }, 'Date of birth ', h('span', { class: 'req', text: '(required)' })),
      h('input', { id: 'dateOfBirth', name: 'dateOfBirth', type: 'date', required: true, max: new Date().toISOString().slice(0, 10) }),
      h('p', { class: 'hint', text: `For children aged ${ages.minAge} to ${ages.maxAge}. Used only to choose the right level.` })),
    h('div', { class: 'field' }, h('label', { for: 'username' }, 'Username ', h('span', { class: 'opt', text: '(optional)' })),
      h('div', { class: 'row' }, username,
        h('button', { class: 'btn btn-quiet btn-small', type: 'button', text: 'Suggest one',
          onclick: async () => { username.value = (await get('/public/username-suggestion')).username; } })),
      h('p', { class: 'hint', text: 'Please don’t use your child’s real name. We suggest one if you leave it empty.' })),
    h('fieldset', { class: 'field' }, h('legend', { text: 'Avatar' }),
      h('div', { class: 'avatar-picker' }, Object.entries(avatars).map(([code, emoji], i) => h('label', {},
        h('input', { type: 'radio', name: 'avatarCode', value: code, checked: i === 1, 'aria-label': code }),
        h('span', { 'aria-hidden': 'true', text: emoji }))))),
    h('div', { class: 'row' },
      h('button', { class: 'btn btn-primary', type: 'submit', text: 'Add child' }),
      h('a', { href: '/parent/', text: 'Cancel' })));

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(form);
    try {
      const child = await post('/parent/children', {
        firstName: form.firstName.value.trim(),
        displayName: form.displayName.value.trim(),
        dateOfBirth: form.dateOfBirth.value || null,
        username: username.value.trim() || null,
        avatarCode: form.querySelector('[name="avatarCode"]:checked')?.value,
      });
      toast(`${child.displayName} has been added.`, 'good');
      location.assign('/parent/');
    } catch (e) {
      showErrors(form, e);
    }
  });

  mount('#main', h('div', { class: 'page-text stack' },
    h('p', {}, h('a', { href: '/parent/', text: 'My family' })),
    h('h1', { text: 'Add a child' }), form));
}

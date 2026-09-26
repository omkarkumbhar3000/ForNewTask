import { get, post, patch, del } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, showErrors, clearErrors, toast, confirmDialog, fmtDate } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/account.html' });
if (!ctx.blocked) await render();

async function render() {
  const account = await get('/parent/account');

  const details = h('form', { class: 'form', novalidate: true },
    h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }),
    h('div', { class: 'field' }, h('label', { for: 'fullName', text: 'Your name' }),
      h('input', { id: 'fullName', name: 'fullName', type: 'text', maxlength: 100, value: account.fullName, autocomplete: 'name' })),
    h('div', { class: 'grid-2' },
      h('div', { class: 'field' }, h('label', { for: 'mobile' }, 'Mobile number ', h('span', { class: 'opt', text: '(optional)' })),
        h('input', { id: 'mobile', name: 'mobile', type: 'tel', maxlength: 20, value: account.mobile || '', autocomplete: 'tel' })),
      h('div', { class: 'field' }, h('label', { for: 'city' }, 'Town or city ', h('span', { class: 'opt', text: '(optional)' })),
        h('input', { id: 'city', name: 'city', type: 'text', maxlength: 80, value: account.city || '' }))),
    h('p', { class: 'small muted', text: `Email: ${account.email}. Member since ${fmtDate(account.createdAt)}.` }),
    h('div', {}, h('button', { class: 'btn btn-primary', type: 'submit', text: 'Save details' })));
  details.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(details);
    try {
      await patch('/parent/account', { fullName: details.fullName.value, mobile: details.mobile.value, city: details.city.value });
      toast('Details saved.', 'good');
    } catch (e) {
      showErrors(details, e);
    }
  });

  const password = h('form', { class: 'form', novalidate: true },
    h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }),
    h('div', { class: 'field' }, h('label', { for: 'currentPassword', text: 'Current password' }),
      h('input', { id: 'currentPassword', name: 'currentPassword', type: 'password', autocomplete: 'current-password' })),
    h('div', { class: 'field' }, h('label', { for: 'newPassword', text: 'New password' }),
      h('input', { id: 'newPassword', name: 'newPassword', type: 'password', autocomplete: 'new-password', minlength: 12 }),
      h('p', { class: 'hint', text: 'At least 12 characters. A short sentence works well.' })),
    h('div', {}, h('button', { class: 'btn btn-primary', type: 'submit', text: 'Change password' })));
  password.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(password);
    try {
      await post('/auth/change-password', { currentPassword: password.currentPassword.value, newPassword: password.newPassword.value });
      password.reset();
      toast('Password changed.', 'good');
    } catch (e) {
      showErrors(password, e);
    }
  });

  const remove = h('button', { class: 'btn btn-danger', type: 'button', text: 'Delete my account' });
  remove.addEventListener('click', async () => {
    const ok = await confirmDialog('Delete your account?',
      'Your account, your children’s profiles, progress, badges and your feedback will be deleted for good. This cannot be undone.',
      'Delete everything', true);
    if (!ok) return;
    try {
      await del('/parent/account');
      location.assign('/');
    } catch (e) {
      toast(e.message, 'bad');
    }
  });

  mount('#main', h('div', { class: 'page-text stack-lg' },
    h('h1', { text: 'Account' }),
    h('section', { class: 'panel' }, h('h2', { text: 'Your details' }), details),
    h('section', { class: 'panel' }, h('h2', { text: 'Password' }), password),
    h('section', { class: 'panel' }, h('h2', { text: 'Delete account' }),
      h('p', { class: 'muted', text: 'Deleting your account removes all of your family’s data from CleverCubs.' }), remove)));
}

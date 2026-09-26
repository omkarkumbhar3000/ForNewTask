import { post, homeFor } from '../api.js';
import { layout } from '../layout.js';
import { param, showErrors, clearErrors } from '../ui.js';

const { me } = await layout({ area: 'public', current: '/login' });
if (me) location.replace(homeFor(me));

/** Only a local path may be a target after signing in, never another site. */
function safeNext(value) {
  if (!value || !value.startsWith('/') || value.startsWith('//') || value.startsWith('/\\')) return null;
  return value;
}

const form = document.getElementById('login-form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  clearErrors(form);
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  try {
    const account = await post('/auth/login', { email: form.email.value.trim(), password: form.password.value });
    const next = safeNext(param('next'));
    const home = homeFor(account);
    location.assign(next && next.startsWith(home) ? next : home);
  } catch (e) {
    showErrors(form, e);
    button.disabled = false;
  }
});

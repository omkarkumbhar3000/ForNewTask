import { get, post, homeFor } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, showErrors, clearErrors, toast } from '../ui.js';

const { me } = await layout({ area: 'public', current: '/register' });
if (me) location.replace(homeFor(me));

const form = document.getElementById('register-form');

// The avatars come from the server's fixed set (DD-06): no photo upload exists.
const avatars = await get('/public/avatars');
mount('#avatars', Object.entries(avatars).map(([code, emoji], i) =>
  h('label', {},
    h('input', { type: 'radio', name: 'child.avatarCode', value: code, checked: i === 0, 'aria-label': code }),
    h('span', { 'aria-hidden': 'true', text: emoji }))));

try {
  const ages = await get('/public/ages');
  document.getElementById('age-hint').textContent =
    `CleverCubs is made for children aged ${ages.minAge} to ${ages.maxAge}. The date of birth is used only to choose the right level.`;
  const today = new Date();
  const dob = form.querySelector('[name="child.dateOfBirth"]');
  dob.max = today.toISOString().slice(0, 10);
} catch { /* the hint keeps its default wording */ }

document.getElementById('suggest').addEventListener('click', async () => {
  try {
    const { username } = await get('/public/username-suggestion');
    form.querySelector('[name="child.username"]').value = username;
  } catch (e) {
    toast(e.message, 'bad');
  }
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  clearErrors(form);
  const value = (name) => form.querySelector(`[name="${name}"]`).value.trim();
  const body = {
    parent: {
      fullName: value('parent.fullName'),
      email: value('parent.email'),
      password: form.querySelector('[name="parent.password"]').value,
      mobile: value('parent.mobile'),
      city: value('parent.city'),
    },
    child: {
      firstName: value('child.firstName'),
      displayName: value('child.displayName'),
      dateOfBirth: value('child.dateOfBirth') || null,
      username: value('child.username') || null,
      avatarCode: form.querySelector('[name="child.avatarCode"]:checked')?.value || null,
    },
    acceptTerms: form.acceptTerms.checked,
    acceptPrivacy: form.acceptPrivacy.checked,
    consentChildData: form.consentChildData.checked,
  };
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  try {
    const account = await post('/auth/register', body);
    location.assign(homeFor(account) + '?welcome=1');
  } catch (e) {
    showErrors(form, e);
    button.disabled = false;
  }
});
// The button ships disabled (register.html): this page waits for the session and the avatar list before the
// handler above exists, and a click in that time would make the browser submit the form itself and reload
// the page, losing everything typed. It works from here on.
form.querySelector('button[type="submit"]').disabled = false;

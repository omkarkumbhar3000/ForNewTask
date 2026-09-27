// The shared frame of every page: header, navigation, footer (Contact Us is always visible, section 17),
// the password prompt for sensitive actions (DD-02), and the forced password change for an account that is
// still on a temporary password. The server protects every route; this file only shapes what is shown.

import { api, post, whoAmI, homeFor, onReauthRequired } from './api.js';
import { h, mount, toast, askPassword, setReadAloud, showErrors, clearErrors, empty } from './ui.js';

// A page whose first load fails (offline, the server restarting) must not sit on "Loading…" forever: it gets
// a friendly message and a way to try again. Later failures are shown as a short message instead.
function showFailure(error) {
  const e = error || {};
  if (e.code === 'unauthenticated' || e.code === 'password-change-required') return;
  const main = document.getElementById('main');
  const message = e.code ? e.message : 'Something went wrong. Please try again.';
  if (main && main.querySelector(':scope > .loading')) {
    mount(main, empty('🌧️', message,
      h('button', { class: 'btn btn-primary', type: 'button', onclick: () => location.reload(), text: 'Try again' })));
  } else {
    toast(message, 'bad');
  }
}
window.addEventListener('unhandledrejection', (event) => showFailure(event.reason));
// An error event without an error object is browser noise (a ResizeObserver notice, a blocked extension), not ours.
window.addEventListener('error', (event) => { if (event.error) showFailure(event.error); });

const NAV = {
  parent: [
    ['/parent/', 'My family'],
    ['/parent/requests.html', 'Requests'],
    ['/parent/feedback.html', 'Feedback'],
    ['/parent/account.html', 'Account'],
  ],
  admin: [['/admin/', 'Dashboard']],
};

function brand(href) {
  return h('a', { class: 'brand', href },
    h('img', { src: '/img/logo-96.png', alt: '', width: 44, height: 44 }),
    h('span', { text: 'CleverCubs' }));
}

function navLink([href, label], current) {
  return h('a', { href, 'aria-current': current === href ? 'page' : null, text: label });
}

function header(area, me, child, current) {
  const nav = h('nav', { class: 'nav', id: 'site-nav', 'aria-label': 'Main' });
  const toggle = h('button', {
    class: 'menu-toggle', type: 'button', 'aria-expanded': 'false', 'aria-controls': 'site-nav', 'aria-label': 'Menu',
    onclick: () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    },
  }, '☰');

  if (area === 'learn' && child) {
    nav.append(
      navLink(['/learn/', 'My courses'], current),
      navLink(['/learn/profile.html', 'My badges'], current),
      h('span', { class: 'who' }, h('span', { class: 'avatar', 'aria-hidden': 'true', text: child.avatar }), child.displayName),
      h('button', { class: 'btn btn-berry btn-small', type: 'button', onclick: grownUps, text: 'Grown-ups' }));
  } else if (me && (area === 'parent' || area === 'admin')) {
    for (const link of NAV[area]) nav.append(navLink(link, current));
    nav.append(h('button', { class: 'link', type: 'button', onclick: signOut, text: 'Sign out' }));
  } else if (me) {
    nav.append(h('a', { href: homeFor(me), text: me.mode === 'CHILD' ? 'Back to learning' : 'My area' }),
      h('button', { class: 'link', type: 'button', onclick: signOut, text: 'Sign out' }));
  } else {
    nav.append(navLink(['/contact', 'Contact us'], current), navLink(['/login', 'Sign in'], current),
      h('a', { class: 'btn btn-primary btn-small', href: '/register', text: 'Create account' }));
  }
  const home = area === 'learn' ? '/learn/' : me ? homeFor(me) : '/';
  return h('div', { class: 'bar' }, brand(home), toggle, nav);
}

function footer() {
  return h('div', { class: 'bar' },
    h('span', { text: '© CleverCubs. Made for curious little learners.' }),
    h('a', { href: '/contact', text: 'Contact us' }),
    h('a', { href: '/terms', text: 'Terms & Conditions' }),
    h('a', { href: '/privacy', text: 'Privacy' }));
}

async function signOut() {
  try {
    await post('/auth/logout');
  } catch { /* already signed out */ }
  location.assign('/');
}

/** Leaving child mode needs the parent's password (D58). */
async function grownUps() {
  const password = await askPassword('Grown-ups only',
    'Ask a grown-up to type their password to open the parent area.', 'Open parent area');
  if (!password) return;
  try {
    await api('/session/parent', { method: 'POST', body: { password }, retry: false });
    location.assign('/parent/');
  } catch (e) {
    toast(e.message, 'bad');
  }
}

function forcedPasswordChange(me) {
  const form = h('form', { class: 'form', novalidate: true },
    h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }),
    h('div', { class: 'field' }, h('label', { for: 'cp-current', text: 'Temporary password' }),
      h('input', { id: 'cp-current', name: 'currentPassword', type: 'password', autocomplete: 'current-password', required: true })),
    h('div', { class: 'field' }, h('label', { for: 'cp-new', text: 'New password' }),
      h('input', { id: 'cp-new', name: 'newPassword', type: 'password', autocomplete: 'new-password', required: true, minlength: 12 }),
      h('p', { class: 'hint', text: 'At least 12 characters. A short sentence you will remember works well.' })),
    h('button', { class: 'btn btn-primary', type: 'submit', text: 'Save my new password' }));
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(form);
    try {
      await post('/auth/change-password', {
        currentPassword: form.currentPassword.value,
        newPassword: form.newPassword.value,
      });
      toast('Password saved.', 'good');
      location.assign(homeFor(me));
    } catch (e) {
      showErrors(form, e);
    }
  });
  return h('section', { class: 'page page-narrow stack' },
    h('h1', { text: 'Choose your own password' }),
    h('p', { text: 'You signed in with a temporary password. Please choose a new one before you continue.' }),
    h('div', { class: 'panel' }, form));
}

/**
 * Builds the frame. Resolves with { me, child, blocked }. When blocked is true the page must not load its
 * own content (the account has to change its password first).
 */
export async function layout({ area = 'public', current = location.pathname } = {}) {
  const me = await whoAmI();
  let child = null;
  if (area === 'learn' && me && me.mode === 'CHILD') {
    child = await api('/learn/me');
    document.documentElement.dataset.profile = child.uiProfile;
    setReadAloud(child.readAloud);
  }
  const headerEl = document.getElementById('site-header');
  if (headerEl) {
    headerEl.className = 'site-header';
    mount(headerEl, header(area, me, child, current));
  }
  const footerEl = document.getElementById('site-footer');
  if (footerEl) {
    footerEl.className = 'site-footer';
    mount(footerEl, footer());
  }

  onReauthRequired(async () => {
    const password = await askPassword('Please confirm it is you',
      'For your family’s safety, this needs your password again.', 'Confirm');
    if (!password) return false;
    try {
      await api('/auth/reauth', { method: 'POST', body: { password }, retry: false });
      return true;
    } catch (e) {
      toast(e.message, 'bad');
      return false;
    }
  });

  if (me && me.mustChangePassword && (area === 'parent' || area === 'admin')) {
    mount('#main', forcedPasswordChange(me));
    return { me, child, blocked: true };
  }
  return { me, child, blocked: false };
}

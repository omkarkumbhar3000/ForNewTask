import { get, post } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, toast, dialog, fmtDate } from '../ui.js';

await layout({ area: 'learn', current: '/learn/profile.html' });
await render();

async function render() {
  const p = await get('/learn/profile');
  const c = p.child;
  const earned = p.badges.filter((b) => b.earned);
  const goals = p.badges.filter((b) => !b.earned);
  const finished = p.courses.filter((x) => x.completed).length;

  mount('#main', h('div', { class: 'stack-lg' },
    h('div', { class: 'kid-hello' },
      h('span', { class: 'big-avatar', 'aria-hidden': 'true', text: c.avatar }),
      h('div', {},
        h('h1', { text: c.displayName }),
        h('p', { class: 'muted', text: `Your username is ${c.username}` }))),

    h('div', { class: 'stats' },
      h('div', { class: 'stat' }, h('b', { text: String(earned.length) }), h('span', { text: 'badges' })),
      h('div', { class: 'stat' }, h('b', { text: String(finished) }), h('span', { text: 'courses finished' })),
      h('div', { class: 'stat' }, h('b', { text: String(p.certificates.length) }), h('span', { text: 'certificates' }))),

    h('section', { 'aria-labelledby': 'mine' },
      h('h2', { id: 'mine', text: 'My badges' }),
      earned.length ? h('ul', { class: 'badges' }, earned.map((b) => badge(b, true)))
        : h('p', { class: 'muted', text: 'Your first badge is waiting. Finish a quiz with a great score to earn it!' })),

    goals.length ? h('section', { 'aria-labelledby': 'goals' },
      h('h2', { id: 'goals', text: 'Badges to collect' }),
      h('ul', { class: 'badges' }, goals.map((b) => badge(b, false)))) : null,

    p.certificates.length ? h('section', { class: 'panel' },
      h('h2', { text: 'Certificates' }),
      p.certificates.map((cert) => h('p', { text: `🎓 ${cert.programTitle}, ${fmtDate(cert.issuedAt)}. A grown-up can print it for you.` }))) : null,

    h('section', { class: 'panel', 'aria-labelledby': 'help' },
      h('h2', { id: 'help', text: 'Ask a grown-up' }),
      h('div', { class: 'row' },
        h('button', { class: 'btn btn-quiet', type: 'button', onclick: askUsername, text: 'I want a new username' }),
        h('button', { class: 'btn btn-berry', type: 'button', onclick: askHelp, text: 'I need help' })),
      p.requests.length ? h('ul', { class: 'list' }, p.requests.slice(0, 5).map((r) => h('li', { class: 'small',
        text: `${label(r)}: ${r.status === 'PENDING' ? 'waiting for a grown-up' : r.status === 'APPROVED' ? 'yes!' : 'not this time'}` }))) : null)));
}

function badge(b, earned) {
  return h('li', { class: 'badge' + (earned ? '' : ' locked') },
    h('div', { class: 'medal', 'aria-hidden': 'true', text: b.icon || '⭐' }),
    h('h3', { text: b.title }),
    h('p', { text: earned ? `Earned ${fmtDate(b.awardedAt)}` : b.description }));
}

function label(r) {
  if (r.type === 'QUIZ_ATTEMPTS') return `More tries for ${r.quizTitle}`;
  if (r.type === 'USERNAME_CHANGE') return `New username "${r.requestedValue}"`;
  return 'Help';
}

async function askUsername() {
  const input = h('input', { id: 'new-username', name: 'username', type: 'text', maxlength: 20, autocomplete: 'off' });
  const { value, form } = await dialog({
    title: 'Pick a new username',
    body: [h('p', { text: 'Use letters, numbers, - or _. Not your real name. A grown-up will say yes or no.' }),
      h('div', { class: 'field' }, h('label', { for: 'new-username', text: 'New username' }), input)],
    actions: [{ label: 'Cancel', value: 'cancel' }, { label: 'Ask', value: 'ok', class: 'btn-primary' }],
    onOpen: () => input.focus(),
  });
  if (value !== 'ok') return;
  try {
    await post('/learn/requests', { type: 'USERNAME_CHANGE', requestedValue: form.querySelector('input').value.trim() });
    toast('A grown-up will check your new username.', 'good');
    render();
  } catch (e) {
    toast(e.message, 'bad');
  }
}

async function askHelp() {
  try {
    await post('/learn/requests', { type: 'HELP' });
    toast('A grown-up has been asked to help you.', 'good');
    render();
  } catch (e) {
    toast(e.message, 'bad');
  }
}

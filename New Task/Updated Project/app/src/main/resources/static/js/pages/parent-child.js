import { get, post, patch, del, api } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, param, crayon, accentFor, toast, fmtDate, confirmDialog, download, showErrors, clearErrors, empty } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/' });
const id = Number(param('id'));
if (!ctx.blocked) await render();

async function render() {
  let report;
  try {
    report = await get(`/parent/children/${id}`);
  } catch (e) {
    mount('#main', empty('🔍', e.status === 404 ? 'We could not find this child in your family.' : e.message,
      h('a', { class: 'btn btn-primary', href: '/parent/', text: 'Back to my family' })));
    return;
  }
  const c = report.child;
  const avatars = await get('/public/avatars');

  mount('#main', h('div', { class: 'stack-lg' },
    h('p', {}, h('a', { href: '/parent/', text: 'My family' })),
    h('div', { class: 'child-card' },
      h('div', { class: 'big-avatar', 'aria-hidden': 'true', text: c.avatar }),
      h('div', {},
        h('h1', { text: c.displayName }),
        h('p', { class: 'muted', text: `${c.ageGroupName}, age ${c.age}. Username: ${c.username}` }),
        h('div', { class: 'row' },
          startButton(c),
          h('a', { class: 'btn btn-quiet', href: `/parent/summary.html?id=${c.id}`, text: 'Year summary' })))),

    h('section', { class: 'panel', 'aria-labelledby': 'courses' },
      h('div', { class: 'row-between' }, h('h2', { id: 'courses', text: 'Courses' }),
        h('span', { class: 'tag', text: `${report.overallPercent}% of ${report.programTitle || 'the year'}` })),
      h('ul', { class: 'list' }, report.courses.map((cr, i) => courseRow(c, cr, i)))),

    h('section', { class: 'panel', 'aria-labelledby': 'rewards' },
      h('h2', { id: 'rewards', text: 'Badges and certificates' }),
      report.badges.length === 0 ? h('p', { class: 'muted', text: 'No badges yet. Badges come with a quiz score of 80% or more, and with finishing rhymes, stories and the whole year.' })
        : h('ul', { class: 'badges' }, report.badges.map((b) => h('li', { class: 'badge' },
          h('div', { class: 'medal', 'aria-hidden': 'true', text: b.icon || '⭐' }), h('h3', { text: b.title }),
          h('p', { text: fmtDate(b.awardedAt) })))),
      report.certificates.map((cert) => h('p', {},
        h('a', { href: `/parent/certificate.html?id=${c.id}&cert=${cert.id}`, text: `Certificate: ${cert.programTitle}` })))),

    editForm(c, avatars),

    h('section', { class: 'panel', 'aria-labelledby': 'data' },
      h('h2', { id: 'data', text: 'Your child’s data' }),
      h('p', { class: 'muted', text: 'Download everything CleverCubs stores about this child, or delete it. Both ask for your password if you have not entered it recently.' }),
      h('div', { class: 'row' },
        h('button', { class: 'btn btn-quiet', type: 'button', onclick: exportData, text: 'Download data' }),
        h('button', { class: 'btn btn-danger', type: 'button', onclick: () => remove(c), text: `Delete ${c.displayName}’s data` })))));
}

function startButton(c) {
  const b = h('button', { class: 'btn btn-primary', type: 'button', text: `Start learning as ${c.displayName}` });
  b.addEventListener('click', async () => {
    try {
      await post('/session/child', { childId: c.id });
      location.assign('/learn/');
    } catch (e) {
      toast(e.message, 'bad');
    }
  });
  return b;
}

function courseRow(child, cr, index) {
  const p = cr.progress;
  const quiz = p.quiz;
  const parts = [
    h('div', { class: 'row-between' },
      h('h3', {}, h('span', { 'aria-hidden': 'true', text: (p.icon || '📘') + ' ' }), p.title),
      h('span', { class: p.completed ? 'tag' : 'tag tag-sky', text: p.completed ? 'Finished' : `${p.percent}%` })),
    h('div', { class: accentFor(index) }, crayon(p.percent, `${p.title} progress`)),
    h('p', { class: 'small muted', text: `${p.lessonsDone} of ${p.lessonsTotal} lessons done` }),
  ];
  if (quiz) {
    const state = quiz.passed ? `Quiz passed, best score ${quiz.bestScore}%`
      : quiz.locked ? 'Quiz locked after 3 tries'
      : quiz.unlocked ? `Quiz open, ${quiz.attemptsRemaining} of ${quiz.attemptsAllowed} tries left`
      : 'Quiz opens after the lessons';
    parts.push(h('p', { class: 'small', text: state + (quiz.bestScore != null && !quiz.passed ? `, best score ${quiz.bestScore}%` : '') }));
    if (quiz.locked) {
      const grant = h('button', { class: 'btn btn-sun btn-small', type: 'button', text: 'Give 3 more tries' });
      grant.addEventListener('click', async () => {
        grant.disabled = true;
        try {
          await post(`/parent/children/${child.id}/quizzes/${quiz.quizId}/grant`);
          toast('Three more tries given.', 'good');
          render();
        } catch (e) {
          toast(e.message, 'bad');
          grant.disabled = false;
        }
      });
      parts.push(grant);
    }
    if (cr.attempts.length > 0) {
      parts.push(h('details', {}, h('summary', { text: `Quiz tries (${cr.attempts.length})` }),
        h('div', { class: 'table-wrap' }, h('table', {},
          h('thead', {}, h('tr', {}, h('th', { text: 'Try' }), h('th', { text: 'Score' }), h('th', { text: 'Result' }), h('th', { text: 'Date' }))),
          h('tbody', {}, cr.attempts.map((a) => h('tr', {},
            h('td', { text: String(a.attemptNumber) }),
            h('td', { text: a.scorePercent == null ? 'Not finished' : a.scorePercent + '%' }),
            h('td', { text: a.passed == null ? '' : a.passed ? 'Passed' : 'Not yet' }),
            h('td', { text: fmtDate(a.submittedAt || a.startedAt) }))))))));
    }
  }
  return h('li', { class: 'stack' }, ...parts);
}

function editForm(c, avatars) {
  const form = h('form', { class: 'form', novalidate: true },
    h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }),
    h('div', { class: 'grid-2' },
      h('div', { class: 'field' }, h('label', { for: 'displayName', text: 'Nickname shown to your child' }),
        h('input', { id: 'displayName', name: 'displayName', type: 'text', maxlength: 40, value: c.displayName })),
      h('div', { class: 'field' }, h('label', { for: 'username', text: 'Username' }),
        h('input', { id: 'username', name: 'username', type: 'text', maxlength: 20, value: c.username }))),
    h('div', { class: 'field' }, h('label', { for: 'dateOfBirth', text: 'Date of birth' }),
      h('input', { id: 'dateOfBirth', name: 'dateOfBirth', type: 'date', value: c.dateOfBirth })),
    h('fieldset', { class: 'field' }, h('legend', { text: 'Avatar' }),
      h('div', { class: 'avatar-picker' }, Object.entries(avatars).map(([code, emoji]) => h('label', {},
        h('input', { type: 'radio', name: 'avatarCode', value: code, checked: code === c.avatarCode, 'aria-label': code }),
        h('span', { 'aria-hidden': 'true', text: emoji }))))),
    h('label', { class: 'check' }, h('input', { type: 'checkbox', name: 'soundEffects', checked: c.soundEffects }), h('span', { text: 'Sounds on' })),
    h('label', { class: 'check' }, h('input', { type: 'checkbox', name: 'readAloud', checked: c.readAloud }), h('span', { text: 'Read words aloud' })),
    h('div', {}, h('button', { class: 'btn btn-primary', type: 'submit', text: 'Save changes' })));
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(form);
    try {
      await patch(`/parent/children/${c.id}`, {
        displayName: form.displayName.value,
        username: form.username.value,
        dateOfBirth: form.dateOfBirth.value || null,
        avatarCode: form.querySelector('[name="avatarCode"]:checked')?.value,
        soundEffects: form.soundEffects.checked,
        readAloud: form.readAloud.checked,
      });
      toast('Changes saved.', 'good');
      render();
    } catch (e) {
      showErrors(form, e);
    }
  });
  return h('section', { class: 'panel', 'aria-labelledby': 'profile' }, h('h2', { id: 'profile', text: 'Profile and preferences' }), form);
}

async function exportData() {
  try {
    const data = await api(`/parent/children/${id}/export`);
    download(`clevercubs-child-${id}.json`, data);
  } catch (e) {
    toast(e.message, 'bad');
  }
}

async function remove(c) {
  const ok = await confirmDialog(`Delete ${c.displayName}’s data?`,
    'Their profile, progress, badges and certificates will be deleted for good. This cannot be undone.', 'Delete for good', true);
  if (!ok) return;
  try {
    await del(`/parent/children/${c.id}`);
    location.assign('/parent/');
  } catch (e) {
    toast(e.message, 'bad');
  }
}

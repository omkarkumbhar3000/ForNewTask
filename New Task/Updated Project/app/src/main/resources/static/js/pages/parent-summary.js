import { get, post } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, param, crayon, accentFor, toast, fmtDate, empty, celebrate } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/' });
const id = Number(param('id'));
if (!ctx.blocked) await render();

async function render() {
  let s;
  try {
    s = await get(`/parent/children/${id}/year-summary`);
  } catch (e) {
    mount('#main', empty('🔍', e.message, h('a', { class: 'btn btn-primary', href: '/parent/', text: 'Back to my family' })));
    return;
  }
  const done = s.status === 'COMPLETED';
  const c = s.child;
  if (done && !sessionStorage.getItem('celebrated-' + id)) {
    celebrate(['🎓', '⭐', '🎉']);
    sessionStorage.setItem('celebrated-' + id, '1');
  }

  mount('#main', h('div', { class: 'page-text stack-lg' },
    h('p', {}, h('a', { href: `/parent/child.html?id=${id}`, text: `${c.displayName}’s progress` })),
    h('div', {},
      h('h1', { text: done ? `${c.displayName} completed ${s.programTitle}` : `${c.displayName}’s year so far` }),
      h('p', { class: 'muted', text: done
        ? `Started ${fmtDate(s.startedAt)}, completed ${fmtDate(s.completedAt)}. This summary is for you, the grown-up.`
        : `Started ${fmtDate(s.startedAt)}. The year is complete when every course reaches 100%.` })),

    h('section', { class: 'panel' },
      h('h2', { text: 'At a glance' }),
      h('div', { class: 'accent-leaf' }, crayon(s.overallPercent, 'Year progress')),
      h('div', { class: 'stats' },
        h('div', { class: 'stat' }, h('b', { text: `${s.overallPercent}%` }), h('span', { text: 'overall progress' })),
        h('div', { class: 'stat' }, h('b', { text: `${s.coursesCompleted}/${s.coursesTotal}` }), h('span', { text: 'courses finished' })),
        h('div', { class: 'stat' }, h('b', { text: `${s.quizzesPassed}/${s.quizzesTotal}` }), h('span', { text: 'quizzes passed' })),
        h('div', { class: 'stat' }, h('b', { text: s.averageBestScore == null ? '-' : s.averageBestScore + '%' }), h('span', { text: 'average best quiz score' })),
        h('div', { class: 'stat' }, h('b', { text: String(s.badgesEarned.length) }), h('span', { text: 'badges earned' })))),

    h('section', { class: 'panel' },
      h('h2', { text: 'Course by course' }),
      h('ul', { class: 'list' }, s.courses.map((cr, i) => {
        const p = cr.progress;
        return h('li', { class: 'stack' },
          h('div', { class: 'row-between' }, h('strong', { text: `${p.icon || '📘'} ${p.title}` }),
            h('span', { class: 'small', text: p.quiz?.bestScore != null ? `Best quiz score ${p.quiz.bestScore}%` : p.quiz ? 'Quiz not taken yet' : 'No quiz' })),
          h('div', { class: accentFor(i) }, crayon(p.percent, p.title)));
      }))),

    s.needsAttention.length ? h('section', { class: 'panel panel-tint' },
      h('h2', { text: 'What is still open' }),
      h('p', { class: 'muted small', text: 'These are facts from the app, not a judgement of your child’s learning.' }),
      h('ul', {}, s.needsAttention.map((t) => h('li', { text: t })))) : null,

    s.certificates.length ? h('section', { class: 'panel' },
      h('h2', { text: 'Certificate' }),
      s.certificates.map((cert) => h('p', {},
        h('a', { class: 'btn btn-sun', href: `/parent/certificate.html?id=${id}&cert=${cert.id}`, text: 'View and print the certificate' })))) : null,

    done ? nextYear(s) : null));
}

function nextYear(s) {
  const next = s.nextProgram;
  const decided = s.nextDecision;
  const wrap = h('section', { class: 'panel', 'aria-labelledby': 'next' },
    h('h2', { id: 'next', text: 'Next year' }),
    next ? h('div', {},
      h('p', { text: `${next.title}: ${next.description}` }),
      next.courses.length ? h('p', { class: 'small muted', text: 'Courses: ' + next.courses.join(', ') }) : null)
      : h('p', { text: 'The next year’s program is being prepared. You can tell us now whether you would like your child to continue, and we will keep your choice.' }),
    decided ? h('p', { class: 'tag', text: decided === 'CONTINUE' ? 'You chose to continue' : 'You chose not now' }) : null);
  const row = h('div', { class: 'row' });
  for (const [decision, label, style] of [['CONTINUE', 'Continue to next year', 'btn-primary'], ['NOT_NOW', 'Not now', 'btn-quiet']]) {
    const b = h('button', { class: 'btn ' + style, type: 'button', text: label });
    b.addEventListener('click', async () => {
      try {
        await post(`/parent/children/${id}/next-year`, { decision });
        toast('Your choice is saved.', 'good');
        render();
      } catch (e) {
        toast(e.message, 'bad');
      }
    });
    row.append(b);
  }
  wrap.append(h('p', { class: 'small muted', text: 'The choice is yours, and you can change it later.' }), row);
  return wrap;
}

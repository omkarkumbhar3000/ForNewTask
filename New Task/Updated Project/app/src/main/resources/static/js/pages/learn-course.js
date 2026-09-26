import { get, post } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, param, crayon, stars, accentFor, speakButton, toast, empty } from '../ui.js';

await layout({ area: 'learn', current: '/learn/' });
const slug = param('slug');
await render();

async function render() {
  let view;
  try {
    view = await get(`/learn/courses/${encodeURIComponent(slug || '')}`);
  } catch (e) {
    mount('#main', empty('🧭', 'We could not find that course.', h('a', { class: 'btn btn-primary', href: '/learn/', text: 'My courses' })));
    return;
  }
  const c = view.course;
  const home = await get('/learn/home');
  const index = Math.max(0, home.courses.findIndex((x) => x.slug === c.slug));
  const accent = accentFor(index);

  mount('#main', h('div', { class: `stack-lg ${accent}` },
    h('p', {}, h('a', { href: '/learn/', text: 'My courses' })),
    h('div', { class: 'kid-hello' },
      h('span', { class: 'big-avatar', 'aria-hidden': 'true', text: c.icon || '📘' }),
      h('div', { class: 'stack' },
        h('h1', { text: c.title }),
        h('p', { class: 'numbers-only muted', text: c.description }),
        speakButton(() => `${c.title}. ${c.description}`))),
    h('div', {},
      h('div', { class: 'stars-only' }, stars(c.percent)),
      h('div', { class: 'numbers-only' }, crayon(c.percent, `${c.title} progress`),
        h('div', { class: 'crayon-label' }, h('span', { text: `${c.lessonsDone} of ${c.lessonsTotal} lessons` }),
          h('span', { text: `${c.percent}%` })))),

    c.completed ? h('div', { class: 'resume' }, h('span', { class: 'icon', 'aria-hidden': 'true', text: '🏆' }),
      h('div', {}, h('h2', { text: 'You finished this course!' }), h('p', { class: 'small', text: 'You can play the lessons again any time.' }))) : null,

    h('section', { 'aria-labelledby': 'lessons' },
      h('h2', { id: 'lessons', text: 'Lessons' }),
      h('ol', { class: 'lessons' }, view.lessons.map((l, i) => lessonRow(l, i, view.nextLessonId)))),

    c.quiz ? quizBox(c, view.quizIntro) : null));
}

function lessonRow(l, i, nextId) {
  const state = l.comingSoon ? 'Coming soon' : l.done ? 'Done' : l.itemsViewed > 0 ? `${l.itemsViewed} of ${l.itemsTotal}` : l.id === nextId ? 'Up next' : '';
  const content = [
    h('span', { class: 'num', 'aria-hidden': 'true', text: l.done ? '✓' : String(i + 1) }),
    h('h3', { text: l.title }),
    h('span', { class: 'small muted', text: state }),
  ];
  const cls = `lesson-row${l.done ? ' done' : ''}${l.comingSoon ? ' soon' : ''}`;
  return h('li', {}, l.comingSoon ? h('div', { class: cls }, ...content)
    : h('a', { class: cls, href: `/learn/lesson.html?id=${l.id}`, 'aria-label': `Lesson ${i + 1}: ${l.title}. ${state}` }, ...content));
}

function quizBox(c, intro) {
  const q = c.quiz;
  const box = h('section', { class: `quiz-box${q.locked ? ' locked' : ''}`, 'aria-labelledby': 'quiz' },
    h('h2', { id: 'quiz' }, h('span', { 'aria-hidden': 'true', text: '🧩 ' }), q.title));
  const go = (label, style = 'btn-primary') => h('a', { class: `btn btn-big ${style}`, href: `/learn/quiz.html?quiz=${q.quizId}`, text: label });

  if (q.inProgressAttemptId) {
    box.append(h('p', { text: 'You have a quiz waiting. Pick up where you stopped.' }), go('Continue the quiz'));
  } else if (q.locked) {
    box.append(h('p', { text: 'You’ve used all your tries for now. Let’s practise the lessons, and ask a grown-up when you’re ready to try again.' }));
    if (q.requestPending) {
      box.append(h('p', { class: 'tag tag-sun', text: 'A grown-up has been asked. Press "Grown-ups" at the top when they are with you.' }));
    } else {
      const ask = h('button', { class: 'btn btn-berry btn-big', type: 'button', text: 'Ask a grown-up' });
      ask.addEventListener('click', async () => {
        try {
          await post('/learn/requests', { type: 'QUIZ_ATTEMPTS', quizId: q.quizId });
          toast('A grown-up has been asked.', 'good');
          render();
        } catch (e) {
          toast(e.message, 'bad');
        }
      });
      box.append(ask);
    }
  } else if (q.passed) {
    box.append(h('p', {}, 'You passed! ', h('span', { class: 'numbers-only', text: `Best score ${q.bestScore}%.` })));
    if (q.attemptsRemaining > 0) {
      box.append(h('p', { class: 'small muted numbers-only', text: `You can play again to beat your score (${q.attemptsRemaining} tries left).` }), go('Play again', 'btn-quiet'));
    }
  } else if (q.unlocked) {
    box.append(h('p', { text: intro }),
      h('p', { class: 'small muted numbers-only', text: `You have ${q.attemptsRemaining} ${q.attemptsRemaining === 1 ? 'try' : 'tries'} left.` }),
      go('Start the quiz', 'btn-sun'));
  } else {
    box.append(h('p', {}, h('span', { 'aria-hidden': 'true', text: '🔒 ' }), 'The quiz opens when you finish all the lessons.'));
  }
  return box;
}

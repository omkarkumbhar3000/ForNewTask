import { get } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, crayon, stars, accentFor, speakButton } from '../ui.js';

const { child } = await layout({ area: 'learn', current: '/learn/' });
const home = await get('/learn/home');

function stateText(c) {
  if (c.completed) return 'Finished!';
  if (c.quiz && c.quiz.locked) return 'Ask a grown-up for more quiz tries';
  if (c.quiz && c.quiz.unlocked && !c.quiz.passed) return 'Quiz time!';
  if (!c.started) return c.kind === 'MEDIA' ? 'Ready to watch' : 'Ready to start';
  return `${c.lessonsDone} of ${c.lessonsTotal} lessons`;
}

function tile(c, i) {
  return h('li', {},
    h('a', { class: `tile ${accentFor(i)}`, href: `/learn/course.html?slug=${encodeURIComponent(c.slug)}`,
      'aria-label': `${c.title}. ${stateText(c)}. ${c.percent} percent.` },
      c.completed ? h('span', { class: 'done-mark', 'aria-hidden': 'true', text: '⭐' }) : null,
      h('span', { class: 'icon', 'aria-hidden': 'true', text: c.icon || '📘' }),
      h('h3', { text: c.title }),
      h('p', { class: 'desc', text: c.description }),
      h('div', { class: 'stars-only' }, stars(c.percent)),
      h('div', { class: 'numbers-only' }, crayon(c.percent, `${c.title} progress`)),
      h('p', { class: 'state state-text', text: stateText(c) })));
}

const resume = home.resume;
mount('#main', h('div', { class: 'stack-lg' },
  h('div', { class: 'kid-hello' },
    h('span', { class: 'big-avatar', 'aria-hidden': 'true', text: child.avatar }),
    h('div', { class: 'stack' },
      h('h1', { text: home.greeting }),
      speakButton(() => home.greeting))),

  home.programCompleted ? h('div', { class: 'resume' },
    h('span', { class: 'icon', 'aria-hidden': 'true', text: '🎓' }),
    h('div', {}, h('h2', { text: 'You finished the whole year!' }),
      h('p', { class: 'small', text: 'Show a grown-up. They have a surprise certificate for you.' })),
    h('a', { class: 'btn btn-sun', href: '/learn/profile.html', text: 'See my badges' })) : null,

  resume ? h('div', { class: 'resume' },
    h('span', { class: 'icon', 'aria-hidden': 'true', text: resume.quizNext ? '🧩' : '▶️' }),
    h('div', {},
      h('h2', { text: resume.quizNext ? `Quiz time: ${resume.courseTitle}` : `Keep going: ${resume.courseTitle}` }),
      resume.lessonTitle ? h('p', { class: 'small muted', text: resume.lessonTitle }) : null),
    h('a', { class: 'btn btn-primary btn-big', text: 'Continue',
      href: resume.lessonId ? `/learn/lesson.html?id=${resume.lessonId}` : `/learn/course.html?slug=${encodeURIComponent(resume.courseSlug)}` }))
    : null,

  h('section', { 'aria-labelledby': 'courses' },
    h('div', { class: 'row-between' },
      h('h2', { id: 'courses', text: 'My courses' }),
      h('span', { class: 'numbers-only small muted', text: home.programTitle ? `${home.programTitle}: ${home.programPercent}% done` : '' })),
    h('ul', { class: 'tiles' }, home.courses.map(tile))),

  h('p', { class: 'center muted', text: home.encouragement })));

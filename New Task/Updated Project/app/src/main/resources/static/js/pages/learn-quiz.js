import { get, post, put } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, param, speak, speakButton, celebrate, stars, empty, toast } from '../ui.js';

const { child } = await layout({ area: 'learn', current: '/learn/' });
const quizId = Number(param('quiz'));
const toddler = child.uiProfile === 'TODDLER';
let attempt = null;
let overview = null;

// Reading the quiz never uses a try: only "Let's go" starts one (DD-19). An open try is resumed.
try {
  overview = await get(`/learn/quizzes/${quizId}`);
} catch (e) {
  mount('#main', empty('📚', e.message, h('a', { class: 'btn btn-primary', href: '/learn/', text: 'My courses' })));
}

if (overview) {
  const state = overview.state;
  if (state.inProgressAttemptId) {
    attempt = await get(`/learn/attempts/${state.inProgressAttemptId}`);
    ask(nextIndex());
  } else if (state.locked) {
    mount('#main', empty('🔒', 'You’ve used all your tries for now. Let’s practise, and ask a grown-up for more tries.',
      h('a', { class: 'btn btn-primary', href: courseLink(), text: 'Back to the course' })));
  } else if (!state.unlocked) {
    mount('#main', empty('📚', 'Finish all the lessons first, then the quiz opens.',
      h('a', { class: 'btn btn-primary', href: courseLink(), text: 'Back to the course' })));
  } else if (state.attemptsRemaining <= 0) {
    mount('#main', empty('🏆', `You passed! Your best score is ${state.bestScore}%.`,
      h('a', { class: 'btn btn-primary', href: courseLink(), text: 'Back to the course' })));
  } else {
    intro();
  }
}

function courseLink() {
  const slug = attempt ? attempt.courseSlug : overview.courseSlug;
  return `/learn/course.html?slug=${encodeURIComponent(slug)}`;
}

async function begin(button) {
  button.disabled = true;
  try {
    attempt = await post(`/learn/quizzes/${quizId}/attempts`);
    ask(nextIndex());
  } catch (e) {
    toast(e.message, 'bad');
    button.disabled = false;
  }
}

function nextIndex() {
  const i = attempt.questions.findIndex((q) => q.chosenOptionId == null);
  return i < 0 ? attempt.questions.length - 1 : i;
}

function dots(current) {
  return h('ol', { class: 'dots', 'aria-label': `Question ${current + 1} of ${attempt.questions.length}` },
    attempt.questions.map((q, i) => h('li', {
      class: i === current ? 'now' : q.correct === true ? 'right' : q.correct === false ? 'wrong' : '',
      'aria-hidden': 'true',
    })));
}

function intro() {
  const s = overview.state;
  const go = h('button', { class: 'btn btn-sun btn-big', type: 'button', text: 'Let’s go!' });
  go.addEventListener('click', () => begin(go));
  mount('#main', h('div', { class: 'quiz stack-lg center' },
    h('p', {}, h('a', { href: courseLink(), text: overview.courseTitle })),
    h('div', { class: 'big', 'aria-hidden': 'true', text: '🧩' }),
    h('h1', { text: overview.title }),
    h('p', { text: overview.intro }),
    h('p', { class: 'numbers-only muted', text: `${overview.questionCount} questions. You have ${s.attemptsRemaining} of ${s.attemptsAllowed} tries left.` }),
    h('div', { class: 'row' }, go)));
}

function ask(index) {
  const q = attempt.questions[index];
  const feedback = h('div', { 'aria-live': 'assertive' });
  const next = h('div', { class: 'row' });
  const options = h('div', { class: 'options' }, q.options.map((o) => {
    const b = h('button', { class: 'option', type: 'button', text: o.label, dataset: { id: o.id } });
    b.addEventListener('click', () => answer(q, o, options, feedback, next, index));
    return b;
  }));
  mount('#main', h('div', { class: 'quiz' },
    h('p', {}, h('a', { href: courseLink(), text: attempt.courseTitle })),
    dots(index),
    h('p', { class: 'numbers-only muted small', text: `Question ${index + 1} of ${attempt.questions.length}` }),
    h('h1', { class: 'question', text: q.prompt }),
    h('p', {}, speakButton(() => `${q.prompt} ${q.options.map((o) => o.label).join(', ')}`, 'Read the question')),
    options, feedback, next));
  options.querySelector('button')?.focus();
  if (toddler) speak(q.prompt);
}

async function answer(q, option, options, feedback, next, index) {
  for (const b of options.querySelectorAll('button')) b.disabled = true;
  let result;
  try {
    result = await put(`/learn/attempts/${attempt.attemptId}/answers/${q.id}`, { optionId: option.id });
  } catch (e) {
    for (const b of options.querySelectorAll('button')) b.disabled = false;
    mount(feedback, h('p', { class: 'feedback try', text: e.message }));
    return;
  }
  q.chosenOptionId = option.id;
  q.correct = result.correct;
  for (const b of options.querySelectorAll('button')) {
    const id = Number(b.dataset.id);
    if (id === result.correctOptionId) b.classList.add('right');
    else if (id === option.id) b.classList.add('wrong');
  }
  const message = result.message || (result.correct ? 'That’s right!' : 'Nice try!');
  mount(feedback, h('p', { class: 'feedback ' + (result.correct ? 'good' : 'try'), text: (result.correct ? '⭐ ' : '💛 ') + message }));
  speak(message);
  const go = result.finished
    ? h('button', { class: 'btn btn-primary btn-big', type: 'button', text: 'See how I did', onclick: () => showResult(result.result) })
    : h('button', { class: 'btn btn-primary btn-big', type: 'button', text: 'Next question', onclick: () => ask(index + 1) });
  mount(next, go);
  go.focus();
}

function showResult(r) {
  if (r.passed) celebrate(['⭐', '🌟', '🎉', '🏆']);
  const wrap = h('div', { class: 'quiz result stack-lg' },
    h('div', { class: 'big', 'aria-hidden': 'true', text: r.passed ? '🏆' : '💪' }),
    h('h1', { text: r.message }),
    h('div', { class: 'stars-only' }, stars(r.scorePercent)),
    h('p', { class: 'numbers-only', text: `You got ${r.correctCount} of ${r.questionCount} right (${r.scorePercent}%).` }),
    r.newBadges && r.newBadges.length ? h('div', {},
      h('h2', { text: r.newBadges.length === 1 ? 'You earned a new badge!' : 'You earned new badges!' }),
      h('ul', { class: 'badge-row' }, r.newBadges.map((b) => h('li', { class: 'badge' },
        h('div', { class: 'medal', 'aria-hidden': 'true', text: b.icon || '⭐' }), h('h3', { text: b.title }))))) : null,
    r.programCompleted ? h('p', { class: 'form-note', text: 'You finished the whole year of learning! Show a grown-up.' }) : null,
    r.courseCompleted ? h('p', { class: 'tag', text: 'Course finished!' }) : null,
    h('div', { class: 'row' },
      !r.passed && r.attemptsRemaining > 0
        ? h('a', { class: 'btn btn-sun btn-big', href: `/learn/quiz.html?quiz=${quizId}`, text: 'Try again' }) : null,
      !r.passed && r.attemptsRemaining > 0
        ? h('a', { class: 'btn btn-quiet', href: courseLink(), text: 'Practise the lessons first' })
        : h('a', { class: 'btn btn-primary btn-big', href: courseLink(), text: 'Back to the course' }),
      h('a', { class: 'btn btn-quiet', href: '/learn/', text: 'My courses' })),
    !r.passed && r.locked ? h('p', { class: 'muted', text: 'A grown-up can give you more tries from the course page.' }) : null);
  mount('#main', wrap);
  speak(r.message);
}

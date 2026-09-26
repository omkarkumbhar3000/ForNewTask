import { get, put } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, param, speak, speakButton, toast, celebrate, empty, accentFor } from '../ui.js';

await layout({ area: 'learn', current: '/learn/' });
const lessonId = Number(param('id'));
let lesson = null;
let diagram = null;
let spotLayer = null;
let accent = '';
const doneBox = h('div', { 'aria-live': 'polite' });

try {
  lesson = await get(`/learn/lessons/${lessonId}`);
} catch {
  mount('#main', empty('🧭', 'We could not find that lesson.', h('a', { class: 'btn btn-primary', href: '/learn/', text: 'My courses' })));
}

if (lesson) {
  const home = await get('/learn/home');
  accent = accentFor(Math.max(0, home.courses.findIndex((c) => c.slug === lesson.courseSlug)));
  if (lesson.diagram) {
    try { diagram = JSON.parse(lesson.diagram); } catch { diagram = null; }
  }
  render();
}

function render() {
  const readyItems = lesson.items.filter((i) => i.ready);
  const body = lesson.courseKind === 'MEDIA' ? mediaLesson() : topicLesson();
  mount('#main', h('div', { class: `stack-lg ${accent}` },
    h('p', {}, h('a', { href: `/learn/course.html?slug=${encodeURIComponent(lesson.courseSlug)}`, text: lesson.courseTitle })),
    h('div', { class: 'row-between' },
      h('div', {},
        h('h1', { text: lesson.title }),
        h('p', { class: 'muted numbers-only', text: `Lesson ${lesson.sortOrder} of ${lesson.lessonCount}` })),
      speakButton(() => lesson.startMessage)),
    readyItems.length ? h('p', { class: 'numbers-only', text: lesson.startMessage }) : null,
    doneBox,
    body,
    pager()));
  if (lesson.done) showDone(null, false);
}

// --- picture, sound and video cards --------------------------------------------------------------------

function topicLesson() {
  const cards = h('ul', { class: 'cards' }, lesson.items.map((item) => h('li', {}, card(item))));
  if (!diagram) return cards;
  spotLayer = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  spotLayer.setAttribute('viewBox', diagram.viewBox || '0 0 500 800');
  spotLayer.setAttribute('preserveAspectRatio', diagram.preserveAspectRatio || 'none');
  spotLayer.setAttribute('aria-hidden', 'true');
  return h('div', { class: 'grid-2' },
    h('div', { class: 'diagram' }, h('img', { src: '/media/' + diagram.image, alt: diagram.alt || 'Picture', loading: 'lazy' }), spotLayer),
    cards);
}

function card(item) {
  if (!item.ready) {
    return h('div', { class: 'card card-soon' }, h('span', { class: 'emoji', 'aria-hidden': 'true', text: '⏳' }),
      h('span', { class: 'word', text: item.word || item.label }), h('span', { class: 'about', text: 'Coming soon' }));
  }
  const word = h('span', { class: 'word', text: item.viewed || item.word === item.label ? (item.word || '') : '' });
  const about = h('span', { class: 'about', text: item.viewed && item.description ? item.description : '' });
  const el = h('button', {
    class: 'card' + (item.viewed ? ' viewed' : ''), type: 'button',
    'aria-label': `${item.label || item.word}${item.video ? ', play video' : ', tap to hear'}`,
  },
    item.viewed ? h('span', { class: 'sticker', 'aria-hidden': 'true', text: '⭐' }) : null,
    item.image ? h('img', { class: 'pic', src: item.image, alt: item.alt, loading: 'lazy', width: 160, height: 160 }) : null,
    !item.image && item.emoji ? h('span', { class: 'emoji', 'aria-hidden': 'true', text: item.emoji }) : null,
    item.label && item.label !== item.word ? h('span', { class: 'label', text: item.label }) : null,
    word, about);
  el.addEventListener('click', () => {
    el.classList.remove('pop');
    void el.offsetWidth;
    el.classList.add('pop');
    word.textContent = item.word || '';
    about.textContent = item.description || '';
    highlight(item);
    if (item.video) {
      openVideo(item, el);
      return;
    }
    if (item.audio) {
      new Audio(item.audio).play().catch(() => speak(item.word || item.label, true));
    } else {
      speak([item.word || item.label, item.description].filter(Boolean).join('. '), true);
    }
    markViewed(item, el);
  });
  return el;
}

function highlight(item) {
  if (!spotLayer || !diagram) return;
  spotLayer.replaceChildren();
  const spot = (diagram.hotspots || []).find((s) => s.word && item.word && s.word.toLowerCase() === item.word.toLowerCase());
  if (!spot) return;
  const g = spot.geometry || {};
  const shape = document.createElementNS('http://www.w3.org/2000/svg', spot.shape === 'circle' ? 'circle' : spot.shape === 'rect' ? 'rect' : 'ellipse');
  for (const [k, v] of Object.entries(g)) shape.setAttribute(k, String(v));
  shape.setAttribute('class', 'spot');
  spotLayer.append(shape);
}

function openVideo(item, cardEl) {
  const video = h('video', { src: item.video, controls: true, autoplay: true, playsinline: true, preload: 'metadata' });
  trackWatching(video, item, cardEl);
  const d = h('dialog', { 'aria-label': item.word || item.label, class: 'video-dialog' },
    h('h2', { text: item.word || item.label }), video,
    h('div', { class: 'dialog-actions' }, h('button', { class: 'btn btn-primary', type: 'button', text: 'Close', onclick: () => d.close() })));
  d.addEventListener('close', () => { video.pause(); d.remove(); });
  document.body.append(d);
  d.showModal();
}

/** DD-17: a video counts once it has played to the end, or at least 90% of the way. */
function trackWatching(video, item, cardEl) {
  const check = () => {
    if (!item.viewed && video.duration && video.currentTime / video.duration >= 0.9) markViewed(item, cardEl);
  };
  video.addEventListener('timeupdate', check);
  video.addEventListener('ended', () => markViewed(item, cardEl));
}

// --- rhymes and stories -------------------------------------------------------------------------------------

function mediaLesson() {
  const item = lesson.items[0];
  if (!item || !item.ready || !item.video) {
    return empty('⏳', 'This one is coming soon. Try another story!');
  }
  const video = h('video', { src: item.video, controls: true, playsinline: true, preload: 'metadata', poster: item.image || null });
  trackWatching(video, item, null);
  return h('div', { class: 'media-lesson' },
    h('div', { class: 'stack' }, video,
      item.viewed ? h('p', { class: 'tag', text: 'Watched ⭐' }) : h('p', { class: 'small muted', text: 'Watch to the end to finish this lesson.' })),
    item.lyrics ? h('div', {}, h('h2', { text: 'Sing along' }), h('p', { class: 'lyrics', text: item.lyrics })) : null);
}

// --- progress feedback --------------------------------------------------------------------------------------

async function markViewed(item, cardEl) {
  if (item.viewed || item.pending) return;
  item.pending = true;
  try {
    const result = await put(`/learn/items/${item.id}/view`);
    item.viewed = true;
    if (cardEl) {
      cardEl.classList.add('viewed');
      if (!cardEl.querySelector('.sticker')) cardEl.prepend(h('span', { class: 'sticker', 'aria-hidden': 'true', text: '⭐' }));
    }
    for (const b of result.newBadges || []) toast(`New badge: ${b.title} ${b.icon || ''}`, 'good');
    if (result.lessonJustDone) {
      lesson.done = true;
      celebrate();
      showDone(result, true);
    }
    if (result.programCompleted) toast('You finished the whole year of learning!', 'good');
  } catch (e) {
    toast(e.message, 'bad');
  } finally {
    item.pending = false;
  }
}

function showDone(result, fresh) {
  const message = (result && result.message) || lesson.doneMessage;
  const actions = [];
  if (lesson.nextLessonId) {
    actions.push(h('a', { class: 'btn btn-primary btn-big', href: `/learn/lesson.html?id=${lesson.nextLessonId}`, text: 'Next lesson' }));
  } else if (result && result.quizUnlocked) {
    actions.push(h('a', { class: 'btn btn-sun btn-big', href: `/learn/course.html?slug=${encodeURIComponent(lesson.courseSlug)}#quiz`, text: 'Go to the quiz' }));
  }
  actions.push(h('a', { class: 'btn btn-quiet', href: `/learn/course.html?slug=${encodeURIComponent(lesson.courseSlug)}`, text: 'Back to the course' }));
  mount(doneBox, h('div', { class: 'resume', role: 'status' },
    h('span', { class: 'icon', 'aria-hidden': 'true', text: '🎉' }),
    h('div', {}, h('h2', { text: fresh ? message : 'You finished this lesson.' }),
      result && !result.courseCompleted ? h('p', { class: 'small numbers-only', text: `The course is ${result.coursePercent}% done.` }) : null),
    h('div', { class: 'row' }, ...actions)));
  if (fresh) speak(message);
}

function pager() {
  return h('nav', { class: 'pager', 'aria-label': 'Lessons' },
    lesson.previousLessonId ? h('a', { class: 'btn btn-quiet', href: `/learn/lesson.html?id=${lesson.previousLessonId}`, text: 'Previous lesson' }) : h('span'),
    lesson.nextLessonId ? h('a', { class: 'btn btn-quiet', href: `/learn/lesson.html?id=${lesson.nextLessonId}`, text: 'Next lesson' })
      : h('a', { class: 'btn btn-quiet', href: `/learn/course.html?slug=${encodeURIComponent(lesson.courseSlug)}`, text: 'Back to the course' }));
}


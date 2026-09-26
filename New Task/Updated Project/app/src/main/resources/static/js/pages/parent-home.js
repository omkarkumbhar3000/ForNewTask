import { get, post } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, ring, param, toast, empty, fmtDate } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/' });
if (!ctx.blocked) await render();

async function render() {
  const overview = await get('/parent/overview');
  const children = overview.children;

  mount('#main',
    h('div', { class: 'stack-lg' },
      param('welcome') ? h('div', { class: 'form-note', role: 'status' },
        'Your family account is ready. When your child is with you, press "Start learning" to open their space.') : null,
      h('div', { class: 'row-between' },
        h('h1', { text: `Hello, ${overview.parentName.split(' ')[0]}` }),
        h('a', { class: 'btn btn-quiet', href: '/parent/add-child.html', text: 'Add a child' })),
      overview.pendingRequests > 0 ? h('a', { class: 'resume', href: '/parent/requests.html' },
        h('span', { class: 'icon', 'aria-hidden': 'true', text: '🙋' }),
        h('div', {}, h('h2', { text: overview.pendingRequests === 1 ? 'Your child is asking you something'
          : `Your children are asking you ${overview.pendingRequests} things` }),
          h('p', { class: 'muted small', text: 'Open the requests to answer.' })),
        h('span', { class: 'btn btn-sun', text: 'Open requests' })) : null,
      h('section', { 'aria-labelledby': 'kids' },
        h('h2', { id: 'kids', text: children.length === 1 ? 'Your child' : 'Your children' }),
        children.length === 0
          ? empty('🧸', 'No children yet. Add your first child to start.', h('a', { class: 'btn btn-primary', href: '/parent/add-child.html', text: 'Add a child' }))
          : h('div', { class: 'grid-2' }, children.map(childPanel)))));
}

function childPanel(card) {
  const c = card.child;
  const start = h('button', { class: 'btn btn-primary', type: 'button', text: `Start learning as ${c.displayName}` });
  start.addEventListener('click', async () => {
    start.disabled = true;
    try {
      await post('/session/child', { childId: c.id });
      location.assign('/learn/');
    } catch (e) {
      toast(e.message, 'bad');
      start.disabled = false;
    }
  });
  return h('article', { class: 'panel child-card' },
    h('div', { class: 'big-avatar', 'aria-hidden': 'true', text: c.avatar }),
    h('div', { class: 'stack' },
      h('div', { class: 'row-between' },
        h('div', {},
          h('h3', { text: c.displayName }),
          h('p', { class: 'small muted', text: `${c.ageGroupName}, age ${c.age}. Username: ${c.username}` })),
        ring(card.overallPercent, `${c.displayName}'s year progress`)),
      h('div', { class: 'stats' },
        h('div', { class: 'stat' }, h('b', { text: `${card.coursesCompleted}/${card.coursesTotal}` }), h('span', { text: 'courses finished' })),
        h('div', { class: 'stat' }, h('b', { text: String(card.badgesEarned) }), h('span', { text: 'badges earned' })),
        h('div', { class: 'stat' }, h('b', { text: card.lastActive ? fmtDate(card.lastActive) : 'Not yet' }), h('span', { text: 'last learned' }))),
      card.lockedQuizzes > 0 ? h('p', { class: 'tag tag-berry', text: `${card.lockedQuizzes} quiz${card.lockedQuizzes > 1 ? 'zes' : ''} waiting for more tries from you` }) : null),
    h('div', { class: 'row actions' },
      start,
      h('a', { class: 'btn btn-quiet', href: `/parent/child.html?id=${c.id}`, text: 'See progress' }),
      h('a', { class: 'btn btn-quiet', href: `/parent/summary.html?id=${c.id}`, text: 'Year summary' })));
}

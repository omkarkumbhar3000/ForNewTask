import { get, post } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, toast, empty, fmtDateTime } from '../ui.js';

const ctx = await layout({ area: 'parent', current: '/parent/requests.html' });

function describe(r) {
  switch (r.type) {
    case 'QUIZ_ATTEMPTS': return `${r.childName} would like 3 more tries at the ${r.quizTitle || 'quiz'}.`;
    case 'USERNAME_CHANGE': return `${r.childName} would like the username “${r.requestedValue}”.`;
    default: return `${r.childName} asked for your help.`;
  }
}

const STATUS = { PENDING: ['Waiting for you', 'tag-sun'], APPROVED: ['Approved', ''], DECLINED: ['Declined', 'tag-berry'] };

async function render() {
  const requests = await get('/parent/requests');
  mount('#main', h('div', { class: 'page-text stack-lg' },
    h('h1', { text: 'Requests from your children' }),
    h('p', { class: 'muted', text: 'When your child needs a grown-up, for example after three quiz tries, their request waits here.' }),
    requests.length === 0 ? empty('📭', 'No requests right now.')
      : h('ul', { class: 'list panel' }, requests.map(item))));
}

function item(r) {
  const [label, tag] = STATUS[r.status] || [r.status, ''];
  const actions = r.status === 'PENDING' ? h('div', { class: 'row' },
    action(r, 'approve', r.type === 'HELP' ? 'Mark as seen' : 'Approve', 'btn-primary'),
    r.type === 'HELP' ? null : action(r, 'decline', 'Decline', 'btn-quiet')) : null;
  return h('li', { class: 'stack' },
    h('div', { class: 'row-between' }, h('p', { text: describe(r) }), h('span', { class: 'tag ' + tag, text: label })),
    h('p', { class: 'small muted', text: `Asked ${fmtDateTime(r.createdAt)}` }),
    actions);
}

function action(r, verb, label, style) {
  const b = h('button', { class: `btn btn-small ${style}`, type: 'button', text: label });
  b.addEventListener('click', async () => {
    b.disabled = true;
    try {
      await post(`/parent/requests/${r.id}/${verb}`);
      toast(verb === 'approve' ? 'Done.' : 'Declined.', 'good');
      render();
    } catch (e) {
      toast(e.message, 'bad');
      b.disabled = false;
    }
  });
  return b;
}

if (!ctx.blocked) await render();

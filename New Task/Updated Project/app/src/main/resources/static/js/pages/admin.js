import { get, post, put, patch } from '../api.js';
import { layout } from '../layout.js';
import { h, mount, toast, confirmDialog, dialog, fmtDate, fmtDateTime, showErrors, clearErrors, empty } from '../ui.js';

const ctx = await layout({ area: 'admin', current: '/admin/' });

const SECTIONS = [
  ['overview', 'Overview', overview],
  ['accounts', 'Accounts', accounts],
  ['children', 'Children', children],
  ['courses', 'Courses', courses],
  ['programs', 'Programs', programs],
  ['age-groups', 'Age groups', ageGroups],
  ['badges', 'Badges', badges],
  ['messages', 'Wording', messages],
  ['feedback', 'Feedback', feedback],
  ['reports', 'Reports', reports],
  ['settings', 'Settings', settings],
  ['audit', 'Audit trail', audit],
  ['account', 'My password', myAccount],
];

const content = h('div', { class: 'stack-lg', id: 'admin-content', tabindex: '-1' });
if (!ctx.blocked) {
  mount('#main', h('div', { class: 'admin-layout' },
    h('nav', { class: 'admin-nav', 'aria-label': 'Admin sections' },
      SECTIONS.map(([key, label]) => h('a', { href: '#' + key, dataset: { key }, text: label }))),
    content));
  window.addEventListener('hashchange', route);
  route();
}

async function route() {
  const key = (location.hash || '#overview').slice(1).split('/')[0];
  const [, , show] = SECTIONS.find(([k]) => k === key) || SECTIONS[0];
  document.querySelectorAll('.admin-nav a').forEach((a) =>
    a.toggleAttribute('aria-current', a.dataset.key === key) && a.setAttribute('aria-current', 'page'));
  mount(content, h('p', { class: 'loading', text: 'Loading…' }));
  try {
    await show();
  } catch (e) {
    mount(content, empty('⚠️', e.message));
  }
}

// --- small building blocks -------------------------------------------------------------------------------

function table(columns, rows) {
  if (!rows.length) return empty('📭', 'Nothing here yet.');
  return h('div', { class: 'table-wrap' }, h('table', {},
    h('thead', {}, h('tr', {}, columns.map(([label]) => h('th', { scope: 'col', text: label })))),
    h('tbody', {}, rows.map((row) => h('tr', {}, columns.map(([, cell]) => {
      const value = cell(row);
      return h('td', {}, value instanceof Node ? value : String(value ?? ''));
    }))))));
}

function button(label, onClick, style = 'btn-quiet') {
  const b = h('button', { class: `btn btn-small ${style}`, type: 'button', text: label });
  b.addEventListener('click', async () => {
    b.disabled = true;
    try {
      await onClick();
    } catch (e) {
      toast(e.message, 'bad');
    } finally {
      b.disabled = false;
    }
  });
  return b;
}

function input(value, attrs = {}) {
  return h('input', { type: 'text', value: value ?? '', ...attrs });
}

function statusSelect(value, options = ['DRAFT', 'PUBLISHED', 'ARCHIVED']) {
  return h('select', {}, options.map((o) => h('option', { value: o, selected: o === value, text: o.charAt(0) + o.slice(1).toLowerCase() })));
}

function header(title, text) {
  return h('div', {}, h('h1', { text: title }), text ? h('p', { class: 'muted', text }) : null);
}

// --- sections ------------------------------------------------------------------------------------------

async function overview() {
  const data = await get('/admin/overview');
  const c = data.counts;
  const stat = (value, label) => h('div', { class: 'stat panel' }, h('b', { text: String(value) }), h('span', { text: label }));
  mount(content,
    header('Overview', 'The platform at a glance. Children are never ranked or compared.'),
    h('div', { class: 'stats' },
      stat(c.parents, 'parent accounts'), stat(c.children, 'children'), stat(c.courses, 'published courses'),
      stat(c.lessons, 'lessons'), stat(c.quizAttempts, 'quiz tries'), stat(c.badgesAwarded, 'badges awarded'),
      stat(c.programsCompleted, 'years completed'), stat(c.newFeedback, 'new feedback'),
      stat(c.pendingRequests, 'requests waiting for parents'), stat(c.lockedAccounts, 'locked or disabled accounts')),
    h('section', {}, h('h2', { text: 'Recent activity' }), auditTable(data.recentAudit)));
}

async function accounts(query = '') {
  const rows = await get('/admin/accounts?size=100' + (query ? '&q=' + encodeURIComponent(query) : ''));
  const search = input(query, { type: 'search', placeholder: 'Search by email or name', 'aria-label': 'Search accounts' });
  const form = h('form', { class: 'row' }, search, h('button', { class: 'btn btn-small btn-primary', type: 'submit', text: 'Search' }));
  form.addEventListener('submit', (e) => { e.preventDefault(); accounts(search.value.trim()); });
  const act = (row, action) => async () => {
    await post(`/admin/accounts/${row.id}/status`, { action });
    toast('Account updated.', 'good');
    accounts(query);
  };
  // D79: another Super Admin gets a temporary password, shown once here, and chooses their own at first sign-in.
  const newAdminEmail = input('', { type: 'email', placeholder: 'new.admin@example.com', 'aria-label': 'Email address of the new Super Admin', autocomplete: 'off' });
  const addAdmin = h('form', { class: 'row' }, newAdminEmail,
    h('button', { class: 'btn btn-small', type: 'submit', text: 'Add a Super Admin' }));
  addAdmin.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = newAdminEmail.value.trim();
    if (!email) return;
    if (!(await confirmDialog('Add a Super Admin?', `${email} will have full administrator rights and must choose a new password at the first sign-in.`, 'Add Super Admin'))) return;
    try {
      const { temporaryPassword } = await post('/admin/accounts', { email });
      await dialog({
        title: 'Temporary password',
        body: [h('p', { text: `Give this to ${email} privately. It is shown only once.` }),
          h('p', { class: 'code', text: temporaryPassword })],
        actions: [{ label: 'Done', value: 'ok', class: 'btn-primary' }],
      });
      accounts(query);
    } catch (err) {
      toast(err.message, 'bad');
    }
  });
  mount(content,
    header('Accounts', 'Disabling an account stops its sign-in. Account changes ask for your password again if it was entered more than 15 minutes ago.'),
    form,
    addAdmin,
    table([
      ['Email', (r) => r.email],
      ['Name', (r) => r.full_name || (r.role === 'SUPER_ADMIN' ? 'Administrator' : '')],
      ['Role', (r) => r.role === 'SUPER_ADMIN' ? 'Super Admin' : 'Parent'],
      ['Status', (r) => r.status + (r.locked_until && new Date(r.locked_until + 'Z') > new Date() ? ' (locked for now)' : '') + (r.must_change_password ? ', temporary password' : '')],
      ['Children', (r) => r.role === 'PARENT' ? r.children : ''],
      ['Last sign-in', (r) => fmtDateTime(r.last_login_at)],
      ['Actions', (r) => h('div', {},
        r.status === 'DISABLED' ? button('Enable', act(r, 'ENABLE')) : button('Disable', act(r, 'DISABLE'), 'btn-danger'),
        button('Unlock', act(r, 'UNLOCK')),
        button('Temporary password', async () => {
          if (!(await confirmDialog('Set a temporary password?', `The account ${r.email} will have to choose a new password at its next sign-in.`, 'Set password'))) return;
          const { temporaryPassword } = await post(`/admin/accounts/${r.id}/temporary-password`);
          await dialog({
            title: 'Temporary password',
            body: [h('p', { text: 'Give this to the account holder privately. It is shown only once.' }),
              h('p', { class: 'code', text: temporaryPassword })],
            actions: [{ label: 'Done', value: 'ok', class: 'btn-primary' }],
          });
        }))],
    ], rows));
}

async function children(query = '') {
  const rows = await get('/admin/children?size=100' + (query ? '&q=' + encodeURIComponent(query) : ''));
  const search = input(query, { type: 'search', placeholder: 'Search by username or nickname', 'aria-label': 'Search children' });
  const form = h('form', { class: 'row' }, search, h('button', { class: 'btn btn-small btn-primary', type: 'submit', text: 'Search' }));
  form.addEventListener('submit', (e) => { e.preventDefault(); children(search.value.trim()); });
  mount(content,
    header('Children', 'Shown by nickname and age group only. Open a child to see their progress.'),
    form,
    table([
      ['Child', (r) => r.display_name], ['Username', (r) => r.username], ['Age group', (r) => r.age_group],
      ['Parent', (r) => r.parent_name], ['Lessons done', (r) => r.lessons_done], ['Badges', (r) => r.badges],
      ['Last active', (r) => fmtDate(r.last_active)],
      ['', (r) => button('Progress', () => childProgress(r.id))],
    ], rows));
}

async function childProgress(id) {
  const report = await get(`/admin/children/${id}/progress`);
  await dialog({
    title: `${report.child.displayName}: ${report.overallPercent}%`,
    body: [h('ul', {}, report.courses.map((c) => h('li', {
      text: `${c.progress.title}: ${c.progress.percent}%` + (c.progress.quiz ? `, quiz ${c.progress.quiz.passed ? 'passed' : c.progress.quiz.locked ? 'locked' : 'not passed yet'}` : ''),
    })))],
    actions: [{ label: 'Close', value: 'ok', class: 'btn-primary' }],
  });
}

async function courses() {
  const rows = await get('/admin/courses');
  mount(content,
    header('Courses', 'Edit titles, descriptions and publishing. Lessons, cards and quizzes are one click further.'),
    table([
      ['', (r) => r.icon],
      ['Title', (r) => r.title], ['Kind', (r) => r.kind === 'TOPIC' ? 'Topic with quiz' : 'Video course'],
      ['Status', (r) => r.status], ['Lessons', (r) => r.lessons], ['Cards', (r) => r.items],
      ['Pass mark', (r) => r.pass_mark_percent != null ? r.pass_mark_percent + '%' : ''],
      ['', (r) => h('div', {}, button('Edit', () => courseEditor(r.id)), r.quiz_id ? button('Quiz', () => quizEditor(r.quiz_id)) : null)],
    ], rows));
}

async function courseEditor(id) {
  const c = await get(`/admin/courses/${id}`);
  const title = input(c.title, { 'aria-label': 'Title', maxlength: 60 });
  const icon = input(c.icon, { 'aria-label': 'Icon', maxlength: 16 });
  const description = h('textarea', { 'aria-label': 'Description', maxlength: 500 }, c.description);
  const status = statusSelect(c.status);
  mount(content,
    h('p', {}, h('a', { href: '#courses', text: 'All courses' })),
    header(`Edit: ${c.title}`),
    h('div', { class: 'panel form' },
      h('div', { class: 'field' }, h('label', { text: 'Title' }), title),
      h('div', { class: 'field' }, h('label', { text: 'Icon (emoji)' }), icon),
      h('div', { class: 'field' }, h('label', { text: 'Description' }), description),
      h('div', { class: 'field' }, h('label', { text: 'Status' }), status),
      h('div', {}, button('Save course', async () => {
        await patch(`/admin/courses/${id}`, { title: title.value, icon: icon.value, description: description.value, status: status.value });
        toast('Course saved.', 'good');
      }, 'btn-primary'))),
    ...c.lessons.map((l) => {
      const lt = input(l.title, { 'aria-label': 'Lesson title', maxlength: 80 });
      const ls = statusSelect(l.status);
      const rows = l.items.map((i) => {
        const word = input(i.word, { 'aria-label': 'Word', maxlength: 80 });
        const description = input(i.description, { 'aria-label': 'Description', maxlength: 300 });
        const alt = input(i.alt_text, { 'aria-label': 'Alt text', maxlength: 150 });
        const media = i.status !== 'READY' ? 'missing' : i.video_path ? 'video' : i.audio_path ? 'sound' : i.image_path ? 'picture' : 'text';
        return h('tr', {},
          h('td', { text: i.emoji || i.label || '' }), h('td', {}, word), h('td', {}, description), h('td', {}, alt),
          h('td', { text: media }),
          h('td', {}, button('Save', async () => {
            await patch(`/admin/items/${i.id}`, { word: word.value, description: description.value, altText: alt.value });
            toast('Card saved.', 'good');
          })));
      });
      return h('section', { class: 'panel stack' },
        h('div', { class: 'row' }, h('strong', { text: `Lesson ${l.sort_order}` }), lt, ls,
          button('Save lesson', async () => {
            await patch(`/admin/lessons/${l.id}`, { title: lt.value, status: ls.value });
            toast('Lesson saved.', 'good');
          })),
        h('div', { class: 'table-wrap' }, h('table', {},
          h('thead', {}, h('tr', {}, ['', 'Word', 'Description', 'Alt text', 'Media', ''].map((t) => h('th', { scope: 'col', text: t })))),
          h('tbody', {}, rows))));
    }));
}

async function quizEditor(id) {
  const q = await get(`/admin/quizzes/${id}`);
  const pass = h('input', { type: 'number', min: 1, max: 100, value: q.pass_mark_percent, 'aria-label': 'Pass mark' });
  const status = statusSelect(q.status);
  mount(content,
    h('p', {}, h('a', { href: '#courses', text: 'All courses' })),
    header(`${q.title}`, `${q.course_title}. The pass mark completes the course; badges need 80% or more (Settings).`),
    h('div', { class: 'panel row' },
      h('label', { text: 'Pass mark %' }), pass, h('label', { text: 'Status' }), status,
      button('Save quiz', async () => {
        await patch(`/admin/quizzes/${id}`, { passMarkPercent: Number(pass.value), status: status.value });
        toast('Quiz saved.', 'good');
      }, 'btn-primary')),
    ...q.questions.map((question, n) => {
      const prompt = input(question.prompt, { 'aria-label': 'Question', maxlength: 200 });
      const pool = statusSelect(question.pool, ['MAIN', 'RESERVE']);
      const options = question.options.map((o) => ({
        id: o.id,
        label: input(o.label, { 'aria-label': 'Answer', maxlength: 80 }),
        correct: h('input', { type: 'radio', name: `correct-${question.id}`, checked: !!o.is_correct, 'aria-label': 'Correct answer' }),
      }));
      return h('section', { class: 'panel stack' },
        h('div', { class: 'row' }, h('strong', { text: `${question.pool === 'MAIN' ? 'Question' : 'Reserve'} ${n + 1}` }), pool),
        prompt,
        h('div', { class: 'grid-2' }, options.map((o) => h('label', { class: 'check' }, o.correct, o.label))),
        h('div', {}, button('Save question', async () => {
          await patch(`/admin/questions/${question.id}`, {
            prompt: prompt.value, pool: pool.value,
            options: options.map((o) => ({ id: o.id, label: o.label.value, correct: o.correct.checked })),
          });
          toast('Question saved.', 'good');
        })));
    }));
}

async function programs() {
  const [list, allCourses] = await Promise.all([get('/admin/programs'), get('/admin/courses')]);
  mount(content,
    header('Programs', 'A program is the list of courses for one age group’s year. A year is complete when all its courses reach 100%.'),
    ...list.map((p) => {
      const boxes = allCourses.map((c) => ({ id: c.id, box: h('input', { type: 'checkbox', checked: p.courseIds.includes(c.id) }), c }));
      return h('section', { class: 'panel stack' },
        h('h2', { text: `${p.title}` }), h('p', { class: 'muted', text: `${p.age_group}, year ${p.year_number}` }),
        h('div', { class: 'grid-2' }, boxes.map((b) => h('label', { class: 'check' }, b.box, `${b.c.icon || ''} ${b.c.title}`))),
        h('div', {}, button('Save courses', async () => {
          await put(`/admin/programs/${p.id}/courses`, { courseIds: boxes.filter((b) => b.box.checked).map((b) => b.id) });
          toast('Program saved.', 'good');
        }, 'btn-primary')));
    }));
}

async function ageGroups() {
  const rows = await get('/admin/age-groups');
  mount(content,
    header('Age groups', 'Each band sets the wording, the layout and the quiz presentation for children of that age. Bands may not overlap.'),
    table([
      ['Name', (r) => input(r.name, { dataset: { f: 'name' }, 'aria-label': 'Name' })],
      ['From age', (r) => h('input', { type: 'number', min: 0, max: 18, value: r.min_age, dataset: { f: 'min' }, 'aria-label': 'From age' })],
      ['To age', (r) => h('input', { type: 'number', min: 0, max: 18, value: r.max_age, dataset: { f: 'max' }, 'aria-label': 'To age' })],
      ['Style', (r) => r.ui_profile.replace('_', ' ').toLowerCase()],
      ['', (r) => button('Save', async (event) => {
        const tr = [...content.querySelectorAll('tbody tr')][rows.indexOf(r)];
        await patch(`/admin/age-groups/${r.id}`, {
          name: tr.querySelector('[data-f="name"]').value,
          minAge: Number(tr.querySelector('[data-f="min"]').value),
          maxAge: Number(tr.querySelector('[data-f="max"]').value),
        });
        toast('Age group saved.', 'good');
        void event;
      })],
    ], rows));
}

async function badges() {
  const rows = await get('/admin/badges');
  const CRITERIA = { QUIZ_BEST_SCORE: 'Quiz score of 80% or more', COURSE_COMPLETED: 'Course finished', PROGRAM_COMPLETED: 'Year completed' };
  mount(content,
    header('Badges', 'Badges are awarded by the server when their rule is met. There are no leaderboards.'),
    table([
      ['Icon', (r) => input(r.icon, { dataset: { f: 'icon' }, 'aria-label': 'Icon', size: 3 })],
      ['Title', (r) => input(r.title, { dataset: { f: 'title' }, 'aria-label': 'Title' })],
      ['Description', (r) => input(r.description, { dataset: { f: 'description' }, 'aria-label': 'Description' })],
      ['Rule', (r) => CRITERIA[r.criteria] + (r.course ? ` (${r.course})` : '')],
      ['Awarded', (r) => r.awarded],
      ['Active', (r) => h('input', { type: 'checkbox', checked: !!r.active, dataset: { f: 'active' }, 'aria-label': 'Active' })],
      ['', (r) => button('Save', async () => {
        const tr = [...content.querySelectorAll('tbody tr')][rows.indexOf(r)];
        const v = (f) => tr.querySelector(`[data-f="${f}"]`);
        await patch(`/admin/badges/${r.id}`, { icon: v('icon').value, title: v('title').value, description: v('description').value, active: v('active').checked });
        toast('Badge saved.', 'good');
      })],
    ], rows));
}

async function messages() {
  const [rows, groups] = await Promise.all([get('/admin/messages'), get('/admin/age-groups')]);
  const key = input('', { placeholder: 'Key, for example encourage', 'aria-label': 'Key' });
  const group = h('select', { 'aria-label': 'Age group' }, h('option', { value: '', text: 'Every age group' }),
    groups.map((g) => h('option', { value: g.id, text: g.name })));
  const text = input('', { placeholder: 'Text', 'aria-label': 'Text', maxlength: 300 });
  mount(content,
    header('Wording', 'Encouraging, age-appropriate messages. Several rows under one key rotate. {name} becomes the child’s nickname.'),
    h('div', { class: 'panel row' }, key, group, text, button('Add message', async () => {
      await post('/admin/messages', { key: key.value, ageGroupId: group.value ? Number(group.value) : null, text: text.value });
      toast('Message added.', 'good');
      messages();
    }, 'btn-primary')),
    table([
      ['Key', (r) => r.message_key], ['Age group', (r) => r.age_group || 'Every group'],
      ['Text', (r) => input(r.text, { dataset: { f: 'text' }, 'aria-label': 'Text', maxlength: 300 })],
      ['Active', (r) => h('input', { type: 'checkbox', checked: !!r.active, dataset: { f: 'active' }, 'aria-label': 'Active' })],
      ['', (r) => button('Save', async () => {
        const tr = [...content.querySelectorAll('tbody tr')][rows.indexOf(r)];
        await patch(`/admin/messages/${r.id}`, { text: tr.querySelector('[data-f="text"]').value, active: tr.querySelector('[data-f="active"]').checked });
        toast('Message saved.', 'good');
      })],
    ], rows));
}

async function feedback(status = '') {
  const rows = await get('/admin/feedback?size=100' + (status ? '&status=' + status : ''));
  const filter = h('select', { 'aria-label': 'Filter by status' },
    [['', 'All'], ['NEW', 'New'], ['READ', 'Read'], ['RESOLVED', 'Resolved']].map(([v, l]) => h('option', { value: v, selected: v === status, text: l })));
  filter.addEventListener('change', () => feedback(filter.value));
  mount(content,
    header('Feedback', 'From parents only. Children cannot see or send feedback.'),
    h('div', { class: 'row' }, h('label', { text: 'Show' }), filter),
    rows.length ? h('ul', { class: 'list panel' }, rows.map((f) => {
      const select = statusSelect(f.status, ['NEW', 'READ', 'RESOLVED']);
      select.addEventListener('change', async () => {
        try {
          await patch(`/admin/feedback/${f.id}`, { status: select.value });
          toast('Status saved.', 'good');
        } catch (e) {
          toast(e.message, 'bad');
        }
      });
      return h('li', { class: 'stack' },
        h('div', { class: 'row-between' },
          h('strong', { text: `${f.category.charAt(0) + f.category.slice(1).toLowerCase()}${f.courseTitle ? ': ' + f.courseTitle : ''}${f.rating ? ', ' + '⭐'.repeat(f.rating) : ''}` }),
          select),
        h('p', { text: f.message }),
        h('p', { class: 'small muted', text: `${f.parentName}, ${fmtDateTime(f.createdAt)}` }));
    })) : empty('📭', 'No feedback here.'));
}

async function reports() {
  const rows = await get('/admin/reports/courses');
  mount(content,
    header('Reports', 'How each course is used, across all children. No child is named or ranked.'),
    table([
      ['', (r) => r.icon], ['Course', (r) => r.title], ['Children started', (r) => r.children_started],
      ['Quiz tries', (r) => r.attempts], ['Children passed', (r) => r.children_passed],
      ['Average score', (r) => r.average_score != null ? r.average_score + '%' : ''], ['Badges', (r) => r.badges],
    ], rows));
}

const SETTING_LABELS = {
  'progress.lesson_weight_percent': 'Share of a course earned by its lessons (%)',
  'quiz.max_attempts': 'Quiz tries before a quiz locks',
  'quiz.grant_attempts': 'Tries a parent gives when unlocking',
  'quiz.default_pass_mark_percent': 'Default pass mark for new quizzes (%)',
  'reward.threshold_percent': 'Best quiz score needed for a badge (%)',
  'session.child_idle_minutes': 'Child session idle limit (minutes)',
  'parent.reauth_minutes': 'Minutes before a sensitive action asks for the password again',
  'consent.document_version': 'Current version of the terms and privacy texts',
};

async function settings() {
  const values = await get('/admin/settings');
  const form = h('form', { class: 'form panel', novalidate: true }, h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }));
  for (const [key, value] of Object.entries(values)) {
    const field = input(value, { name: 'value', id: 'set-' + key, 'aria-describedby': 'hint-' + key });
    form.append(h('div', { class: 'field' },
      h('label', { for: 'set-' + key, text: SETTING_LABELS[key] || key }),
      h('div', { class: 'row' }, field, button('Save', async () => {
        clearErrors(form);
        try {
          await put(`/admin/settings/${encodeURIComponent(key)}`, { value: field.value });
          toast('Setting saved. It applies straight away.', 'good');
        } catch (e) {
          showErrors(form, e);
        }
      })),
      h('p', { class: 'hint code', id: 'hint-' + key, text: key })));
  }
  mount(content, header('Settings', 'Business rules live here, not in code. Every change is recorded in the audit trail.'), form);
}

function auditTable(rows) {
  return table([
    ['When', (r) => fmtDateTime(r.occurred_at)], ['Who', (r) => r.actor_account_id ? `${r.actor_role} #${r.actor_account_id}` : r.actor_role],
    ['Action', (r) => r.action.toLowerCase().replaceAll('_', ' ')], ['Target', (r) => r.target_type ? `${r.target_type} #${r.target_id ?? ''}` : ''],
    ['Details', (r) => h('span', { class: 'code', text: r.details || '' })],
  ], rows);
}

async function audit(action = '') {
  const [rows, actions] = await Promise.all([get('/admin/audit?size=100' + (action ? '&action=' + action : '')), get('/admin/audit/actions')]);
  const filter = h('select', { 'aria-label': 'Filter by action' }, h('option', { value: '', text: 'All actions' }),
    actions.map((a) => h('option', { value: a, selected: a === action, text: a.toLowerCase().replaceAll('_', ' ') })));
  filter.addEventListener('change', () => audit(filter.value));
  mount(content, header('Audit trail', 'Append-only. It records who did what and when; never passwords or personal details.'),
    h('div', { class: 'row' }, h('label', { text: 'Show' }), filter), auditTable(rows));
}

async function myAccount() {
  const form = h('form', { class: 'form panel', novalidate: true },
    h('p', { class: 'form-alert', hidden: true, tabindex: '-1' }),
    h('div', { class: 'field' }, h('label', { for: 'a-current', text: 'Current password' }),
      h('input', { id: 'a-current', name: 'currentPassword', type: 'password', autocomplete: 'current-password' })),
    h('div', { class: 'field' }, h('label', { for: 'a-new', text: 'New password' }),
      h('input', { id: 'a-new', name: 'newPassword', type: 'password', autocomplete: 'new-password' }),
      h('p', { class: 'hint', text: 'At least 12 characters.' })),
    h('div', {}, h('button', { class: 'btn btn-primary', type: 'submit', text: 'Change password' })));
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearErrors(form);
    try {
      await post('/auth/change-password', { currentPassword: form.currentPassword.value, newPassword: form.newPassword.value });
      form.reset();
      toast('Password changed.', 'good');
    } catch (e) {
      showErrors(form, e);
    }
  });
  mount(content, header('My password'), form);
}

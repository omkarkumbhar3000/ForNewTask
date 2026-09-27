// The requirement section 28 flows in a real browser: public pages, protected URLs, registration, child
// mode, a lesson, the quiz, the parent gate and the parent area, feedback, responsive layout, and deleting
// the account again. One family per project run; it is deleted at the end.
import { test, expect } from '@playwright/test';

const WIDTHS = [1440, 1024, 768, 375];
const PASSWORD = 'Blue kites fly high 42';

async function noHorizontalScroll(page) {
  const [scroll, client, culprits] = await page.evaluate(() => {
    const d = document.documentElement;
    const wide = [...document.querySelectorAll('body *')]
      .filter((e) => e.getBoundingClientRect().right > d.clientWidth + 1)
      .slice(0, 5).map((e) => `${e.tagName}.${e.className} (${Math.round(e.getBoundingClientRect().right)}px)`);
    return [d.scrollWidth, d.clientWidth, wide.join(', ')];
  });
  expect(scroll, `page is ${scroll}px wide in a ${client}px window: ${culprits}`).toBeLessThanOrEqual(client + 1);
}

function collectErrors(page) {
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => {
    // Expected refusals (400/401/422 answers from the API) show up as "Failed to load resource".
    if (m.type() === 'error' && !m.text().startsWith('Failed to load resource')) errors.push(m.text());
  });
  return errors;
}

/** Header links and buttons sit behind the menu button on phones; open it first when it is shown. */
async function header(page, role, name) {
  // layout.js draws the header only after it has read the session, so right after a navigation there is no
  // menu button yet; isVisible() does not wait, and the folded menu would stay shut. Wait for the header.
  await page.locator('#site-nav').waitFor({ state: 'attached' });
  const toggle = page.locator('.menu-toggle');
  if (await toggle.isVisible() && (await toggle.getAttribute('aria-expanded')) !== 'true') await toggle.click();
  return page.locator('#site-nav').getByRole(role, { name });
}

test.describe.configure({ mode: 'serial' });

test('public pages open, fit every width and show no script errors', async ({ page }) => {
  const errors = collectErrors(page);
  for (const path of ['/', '/login', '/register', '/terms', '/privacy', '/contact']) {
    await page.goto(path);
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('footer')).toContainText('Contact us');
    for (const width of WIDTHS) {
      await page.setViewportSize({ width, height: 900 });
      await noHorizontalScroll(page);
    }
  }
  expect(errors).toEqual([]);
});

test('a protected page without a session goes to sign-in and keeps the address', async ({ page }) => {
  await page.goto('/learn/quiz.html?quiz=1');
  await expect(page).toHaveURL(/\/login\?next=%2Flearn%2Fquiz\.html/);
  await page.goto('/admin/');
  await expect(page).toHaveURL(/\/login\?next=%2Fadmin%2F/);
});

test('a family registers, learns, asks a grown-up, and deletes its account', async ({ page }, info) => {
  const errors = collectErrors(page);
  const email = `e2e-${info.project.name}-${Date.now()}@example.test`;
  const dob = new Date(Date.now() - 3.4 * 365.25 * 24 * 3600 * 1000).toISOString().slice(0, 10);

  // Registration: a weak password is refused beside its field, then the account is created.
  await page.goto('/register');
  await page.locator('#fullName').fill('Robin Tester');
  await page.locator('#email').fill(email);
  await page.locator('#password').fill('password1234');
  await page.locator('#firstName').fill('Kit');
  await page.locator('#dateOfBirth').fill(dob);
  await page.getByRole('checkbox', { name: /Terms/ }).check();
  await page.getByRole('checkbox', { name: /Privacy notice/ }).check();
  await page.getByRole('checkbox', { name: /parent or legal guardian/ }).check();
  await page.getByRole('button', { name: 'Create account' }).click();
  await expect(page.locator('.field-error')).toContainText('too easy to guess');
  await page.locator('#password').fill(PASSWORD);
  await page.getByRole('button', { name: 'Create account' }).click();
  await expect(page).toHaveURL(/\/parent\/\?welcome=1/);
  await expect(page.getByRole('heading', { name: 'Hello, Robin' })).toBeVisible();
  await noHorizontalScroll(page);

  // Child mode: the child space, toddler presentation (stars, no numbers).
  await page.getByRole('button', { name: 'Start learning as Kit' }).click();
  await expect(page).toHaveURL(/\/learn\/$/);
  await expect(page.locator('html')).toHaveAttribute('data-profile', 'TODDLER');
  await expect(page.locator('.tile')).toHaveCount(11);
  await noHorizontalScroll(page);

  // The child cannot open the parent area by typing its address.
  const denied = await page.request.get('/api/v1/parent/overview');
  expect(denied.status()).toBe(403);

  // A lesson: open every card, the lesson completes.
  await page.getByRole('link', { name: /^Colours/ }).click();
  await expect(page.getByRole('heading', { name: 'Colours', level: 1 })).toBeVisible();
  await page.locator('.lesson-row').first().click();
  const cards = page.locator('button.card');
  await expect(cards.first()).toBeVisible();
  const count = await cards.count();
  for (let i = 0; i < count; i++) {
    await cards.nth(i).click();
    await expect(cards.nth(i).locator('.sticker'), 'each opened card gets its sticker').toBeVisible();
  }
  await expect(page.locator('.resume[role="status"]')).toBeVisible();
  await noHorizontalScroll(page);

  // Ask a grown-up for help, then the gate: a wrong password keeps the child session, the right one opens it.
  await page.goto('/learn/profile.html');
  await page.getByRole('button', { name: 'I need help' }).click();
  await expect(page.locator('.toast')).toContainText('grown-up');
  await (await header(page, 'button', 'Grown-ups')).click();
  await page.locator('#dialog-password').fill('not my password at all');
  await page.getByRole('button', { name: 'Open parent area' }).click();
  await expect(page.locator('.toast.bad')).toBeVisible();
  await expect(page).toHaveURL(/\/learn\//);
  await (await header(page, 'button', 'Grown-ups')).click();
  await page.locator('#dialog-password').fill(PASSWORD);
  await page.getByRole('button', { name: 'Open parent area' }).click();
  await expect(page).toHaveURL(/\/parent\/$/);

  // The request is waiting; the parent marks it as seen.
  await (await header(page, 'link', 'Requests')).click();
  await expect(page.getByText('Kit asked for your help.')).toBeVisible();
  await page.getByRole('button', { name: 'Mark as seen' }).click();
  await expect(page.getByText('Approved')).toBeVisible();

  // Progress is visible to the parent and comes from the server.
  await (await header(page, 'link', 'My family')).click();
  await page.getByRole('link', { name: 'See progress' }).click();
  await expect(page.getByText('1 of 3 lessons done')).toBeVisible();

  // Feedback is stored and shown as text.
  await (await header(page, 'link', 'Feedback')).click();
  await page.getByLabel('Your message').fill('Great <i>app</i> for my child');
  await page.getByRole('button', { name: 'Send feedback' }).click();
  await expect(page.getByText('Great <i>app</i> for my child')).toBeVisible();

  // Delete the account (it was signed into recently, so no password prompt), which signs out.
  await (await header(page, 'link', 'Account')).click();
  await page.getByRole('button', { name: 'Delete my account' }).click();
  await page.getByRole('button', { name: 'Delete everything' }).click();
  await expect(page).toHaveURL(/\/$/);
  const me = await page.request.get('/api/v1/public/session');
  expect((await me.json()).signedIn).toBe(false);

  expect(errors).toEqual([]);
});

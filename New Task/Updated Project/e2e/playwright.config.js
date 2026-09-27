// Browser tests against a running CleverCubs (start it with start-dev.ps1). Uses the installed Google Chrome,
// so no browser download is needed. Each run registers its own throw-away family and deletes it at the end.
import { defineConfig } from '@playwright/test';

// Another address (CLEVERCUBS_URL) is the cloud copy, where an idle instance stops after 5 minutes and a new
// one takes about 15 s to start (docs/07-deployment.md §7). An assertion there waits long enough for one
// cold start; locally the default 5 s stays, so a slow page is still caught.
const remote = Boolean(process.env.CLEVERCUBS_URL);

export default defineConfig({
  testDir: './tests',
  timeout: remote ? 180_000 : 90_000,
  expect: { timeout: remote ? 30_000 : 5_000 },
  fullyParallel: false,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: process.env.CLEVERCUBS_URL || 'http://127.0.0.1:8080',
    channel: 'chrome',
    headless: true,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1440, height: 900 } } },
    { name: 'mobile', use: { viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true } },
  ],
});

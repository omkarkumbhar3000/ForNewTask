# CleverCubs browser tests

Playwright tests for the flows of requirement §28, run in the installed Google Chrome (no browser download)
at desktop (1440 px) and phone (375 px) sizes; the public pages are also checked at 1024 and 768 px.
Development only: nothing here ships with the application.

```powershell
# 1. Start the application (another terminal):  ..\start-dev.ps1
# 2. Once:
npm install
# 3. Run:
npx playwright test                 # both sizes
npx playwright test --project=mobile
npx playwright show-report          # the HTML report of the last run
```

Each run registers its own throw-away family (`e2e-…@example.test`) and deletes it through the Account page
at the end, which also tests the deletion. Set `CLEVERCUBS_URL` to test another address, for example
production: `$env:CLEVERCUBS_URL = "https://clevercubs.vercel.app"; npx playwright test`. With another
address set, an assertion waits up to 30 s instead of 5 s, because a cloud instance that was idle for five
minutes takes about 15 s to start.

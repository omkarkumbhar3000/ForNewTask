# Jira MCP — Configuration (Standby)

> **Status: NOT ACTIVE.** The config exists as a template only. No credentials are
> stored, and no MCP server is registered until you deliberately activate it below.

The framework talks to Jira through an **MCP server** rather than a hand-rolled REST
client. Nothing in this repo hardcodes a Jira instance, project key, or ticket ID.

---

## Option A — Atlassian Remote MCP Server (recommended)

Atlassian hosts an official remote MCP server. Auth happens through a browser OAuth
flow, so **no API token is ever written to disk in this repo**.

`.mcp.json.template` is already set up for this:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.atlassian.com/v1/sse"]
    }
  }
}
```

**To activate:**

```bash
cp .mcp.json.template .mcp.json
```

Then restart Claude Code. It will prompt you to approve the project MCP server, and
the first tool call opens the Atlassian OAuth consent screen in your browser.

---

## Option B — Self-hosted / token-based MCP server

If your Jira is **Server or Data Center** (not Cloud), or you need to avoid the OAuth
flow, use a token-based server instead. Credentials come from `.env` — never inline.

```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "<jira-mcp-server-package>"],
      "env": {
        "JIRA_URL": "${JIRA_URL}",
        "JIRA_EMAIL": "${JIRA_EMAIL}",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}"
      }
    }
  }
}
```

Pick the server package that matches your deployment, then fill the matching keys in
`.env`. Confirm the exact env-var names the package expects — they vary between servers.

---

## Credentials

All secrets live in `.env`, which is gitignored. `.env.sample` documents the shape.

| Variable | Used by | Status |
|---|---|---|
| `JIRA_URL` | Option B | ⬜ awaiting your value |
| `JIRA_EMAIL` | Option B | ⬜ awaiting your value |
| `JIRA_API_TOKEN` | Option B | ⬜ awaiting your value |
| `GROQ_KEY` | LLM calls | ✅ set in `.env` |

Jira API tokens: https://id.atlassian.com/manage-profile/security/api-tokens

---

## Verifying the link (BLAST Phase 2)

Once activated, the **L — Link** phase must confirm the connection before any Layer 3
tool is built. Ask the System Pilot to fetch a single known issue and echo its summary.
If that fails, the Link is broken — do not proceed to full logic.

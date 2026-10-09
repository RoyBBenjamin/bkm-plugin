# Benjamin Knowledge Models plugin

An agent plugin for the **Benjamin Knowledge Models (BKM)** service: checked probability,
statistics and decision calculations following Benjamin and Cornell, *Probability, Statistics,
and Decision for Civil Engineers*. The service answers by explicit calculation with a full
trace, asks for what it needs rather than guessing, and never supplies a probability, cost or
utility the question did not state.

This repository is the plugin only. It follows [Agent Plugins 1.0](https://agent-plugins.org), so
one directory installs in Codex, Cursor, GitHub Copilot in VS Code and other clients that read
`plugin.json`; a Claude Code manifest sits beside it.

| Path | What it is |
|---|---|
| `plugin.json` | The Agent Plugins manifest |
| `skills/bkm/SKILL.md` | The skill: when to reach for BKM, the procedure (read the contract, ask instead of guess, pass raw values), and the rules that keep answers honest. An [Agent Skill](https://agentskills.io) |
| `mcp.json` | The MCP server entry for the hosted service. Added when the hosted gateway has a public origin; until then connect the service in your client by hand |
| `.claude-plugin/` | The same plugin in Claude Code's manifest format, with its marketplace file |
| `.agents/plugins/marketplace.json` | The Codex marketplace file |

The plugin never carries a credential. Sign-in belongs to the hosted gateway; a client asks for
it when the server is first used.

## Install

**Codex CLI**

```bash
codex plugin marketplace add RoyBBenjamin/bkm-plugin
codex plugin add bkm
```

**Claude Code**

```text
/plugin marketplace add RoyBBenjamin/bkm-plugin
/plugin install bkm@bkm
```

**Cursor, VS Code and other Agent Plugins clients**

Clone this repository and point the client at it from its plugin or marketplace screen; each
client documents where it looks for plugins. Cursor and VS Code read `plugin.json`, the skill
under `skills/` and `mcp.json` directly.

## Connecting the service

Until `mcp.json` is present, add the BKM MCP server to your client with the address and
credential the service operator gave you (a Streamable HTTP server; in most clients one JSON
entry with `type`, `url` and, where the client supports it, a credential it stores for you). The
skill then applies to whichever BKM server the client has.

## Checking the package

```bash
pip install jsonschema skills-ref
scripts/validate-plugin.py
```

Validates the manifest and `mcp.json` against the published schemas, the skill against the Agent
Skills specification, and the marketplace files against the plugin; it refuses any credential
in `mcp.json`. It runs on every push.

## Source

The plugin is maintained in the service repository and published here. Questions and issues:
open an issue on this repository.

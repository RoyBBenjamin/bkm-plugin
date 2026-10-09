# Benjamin Knowledge Models plugin

This package is maintained under `plugin/` in the Benjamin Knowledge Models repository and, for
the invited pilot, published at the root of the private
[RoyBBenjamin/bkm-plugin](https://github.com/RoyBBenjamin/bkm-plugin) repository. Install from the
private distribution repository; the installing GitHub account must have access to it.

One package teaches an AI agent to use the Benjamin Knowledge Models (BKM) service and connects it
to the invited-pilot Sidekick gateway. It follows the
[Agent Plugins 1.0](https://agent-plugins.org) format, so the same directory installs in
Codex, Cursor, GitHub Copilot in VS Code and other clients that read `plugin.json`, and it
carries a Claude Code manifest beside it.

What it contains:

| Path | What it is |
|---|---|
| `plugin.json` | The Agent Plugins manifest |
| `skills/bkm/SKILL.md` | The skill: when to reach for BKM, the procedure (read the contract, ask instead of guess, pass raw values), and the rules that keep answers honest. An [Agent Skill](https://agentskills.io) |
| `mcp.json` | Credential-free Agent Plugins MCP entry for the invited-pilot Sidekick gateway |
| `.mcp.json` | Credential-free Claude Code MCP entry for the same gateway |
| `.claude-plugin/plugin.json` | The same plugin described in Claude Code's own manifest format |

The plugin never carries a credential. Sign-in and entitlement enforcement belong to BKM Sidekick;
a compatible client asks the user to connect when the server is first used. Installing this private
package does not itself grant a Sidekick invitation or service access.

## Notice

© 2026 Roy Benjamin. BKM and its catalog, schemas, cookbooks and traces are proprietary and may not be used to build a competing service. Methods after Benjamin and Cornell (1970); no endorsement claimed. The full statement is in [`NOTICE.md`](NOTICE.md), which ships with the plugin.

## Install

Verified on 8 October 2026 by installing from this repository exactly as below.

**Codex CLI** (verified with codex-cli 0.162.0)

```bash
codex plugin marketplace add RoyBBenjamin/bkm-plugin
codex plugin add bkm@bkm
```

**Claude Code** (verified)

```text
/plugin marketplace add RoyBBenjamin/bkm-plugin
/plugin install bkm@bkm
```

or from a shell: `claude plugin marketplace add RoyBBenjamin/bkm-plugin` then `claude plugin install bkm@bkm`.

**GitHub Copilot CLI** (verified); VS Code discovers plugins installed this way

```bash
copilot plugin marketplace add RoyBBenjamin/bkm-plugin
copilot plugin install bkm@bkm
```

**VS Code** (from its documentation; not yet run here)

Set `"chat.plugins.enabled": true`, then either run **Chat: Install Plugin From Source** and
enter `https://github.com/RoyBBenjamin/bkm-plugin`, or add `RoyBBenjamin/bkm-plugin` to
`"chat.plugins.marketplaces"` and install from the Extensions view (`@agentPlugins`).

**Cursor** (from its documentation; not yet run here)

Cursor reads `plugin.json` at the root of a plugin directory. Clone this repository and add it
from Cursor's plugin screen, or install once it is listed in the Cursor Marketplace.

## Connection and pilot status

The package points at the current Sidekick staging origin. This is a limited invited pilot, not a
public service or availability promise. Agent Plugins clients read `mcp.json`; Claude Code can read
`.mcp.json`. OAuth sign-in, account linking and live tool certification remain client-specific. For
manual and local connection alternatives, see the
[installation guide](https://github.com/RoyBBenjamin/benjamin-knowledge-models/blob/main/docs/service/install-and-validate.md).

## Checking the package

```bash
pip install jsonschema skills-ref
scripts/validate-plugin.py
```

This validates the manifest and `mcp.json` against the published schemas, every skill against
the Agent Skills specification, and the marketplace files against the plugin. It runs in CI.

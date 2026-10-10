# Benjamin Knowledge Models plugin

This package is maintained under `plugin/` in the Benjamin Knowledge Models repository and
published at the root of the public
[RoyBBenjamin/bkm-plugin](https://github.com/RoyBBenjamin/bkm-plugin) distribution repository.
Public package access simplifies installation; it does not make the connected Sidekick service
public or bypass its invitation, OAuth, entitlement, quota, or billing controls.

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
a compatible client asks the user to connect when the server is first used. Installing this public
package does not itself grant a Sidekick invitation or service access.

## Notice

© 2026 Roy Benjamin. BKM and its catalog, schemas, cookbooks and traces are proprietary and may not be used to build a competing service. Methods after Benjamin and Cornell (1970); no endorsement claimed. The full statement is in [`NOTICE.md`](NOTICE.md), which ships with the plugin.

## Install

### Ask your agent to do it

Paste this into the client you want to connect:

```text
Install and verify BKM Sidekick for me from the authoritative public plugin
distribution at https://github.com/RoyBBenjamin/bkm-plugin.

First identify this exact client, version, and operating system, then use its
native plugin or marketplace mechanism. Do not guess commands or inherit a
support claim from another client. Never ask me to paste an API key, password,
authorization code, access token, or client secret. The plugin contains no
credential; use Sidekick OAuth. Pause when I must complete browser login,
consent, restart, workspace approval, or another human-only step, and give me
one action at a time. Do not change identity-provider settings, enable dynamic
client registration, or install a local bridge.

Known native routes, to use only when they match the detected client:
- Codex CLI: `codex plugin marketplace add RoyBBenjamin/bkm-plugin`, then
  `codex plugin add bkm@bkm`.
- Claude Code: `/plugin marketplace add RoyBBenjamin/bkm-plugin`, then
  `/plugin install bkm@bkm`.
- GitHub Copilot CLI: `copilot plugin marketplace add
  RoyBBenjamin/bkm-plugin`, then `copilot plugin install bkm@bkm`.
- ChatGPT Work: guide me through installing BKM Sidekick from the Plugins
  directory; do not claim you can press installation, approval, or consent
  controls yourself.

After installation, confirm the server is enabled, complete OAuth, discover
get_profile, read_contract, assess_formulation, and execute_analysis, and call
read_contract with kind "catalog". Report installation, authentication, tool
discovery, and contract access as separate results. Before any quota-bearing
assessment or calculation, explain the test and ask once for confirmation. If
anything fails, preserve the bounded error and stop rather than retrying in a
loop or silently changing configuration.
```

The agent can usually handle discovery, marketplace setup, installation, restart guidance,
tool discovery, and read-only verification. The user still controls login, consent,
workspace policy, and quota-bearing tests. The complete known-answer and refusal sequence is
in the [installation guide](https://github.com/RoyBBenjamin/benjamin-knowledge-models/blob/main/docs/service/install-and-validate.md).

### Manual commands

Plugin installation was verified on 8 October 2026 using the commands below. Codex CLI
0.162.0-alpha.2 with public plugin 1.0.2 subsequently completed OAuth and calculation
certification on 9 October 2026. Installation evidence for another client does not inherit
that certification.

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

The package points at the canonical Sidekick origin,
`https://sidekick.benjaminknowledgemodels.com/v1/mcp`. This is a limited invited pilot, not a
public availability promise. The underlying Cloud Run URL is deployment plumbing and is not the
public resource identity. Agent Plugins clients read `mcp.json`; Claude Code can read `.mcp.json`.
The portable manifest declares OAuth with CIMD preference, exact resource binding, and the minimum
`mcp:tools` scope; it contains no client secret. OAuth sign-in, account linking and live tool
certification remain client-specific. For
manual and local connection alternatives, see the
[installation guide](https://github.com/RoyBBenjamin/benjamin-knowledge-models/blob/main/docs/service/install-and-validate.md).

## Checking the package

```bash
pip install jsonschema skills-ref
scripts/validate-plugin.py
```

This validates the manifest and `mcp.json` against the published schemas, every skill against
the Agent Skills specification, and the marketplace files against the plugin. It runs in CI.

The canonical source repository also verifies that every package-owned file in this distribution
matches the transformed source material byte for byte and reports one aggregate SHA-256 material
digest. Distribution-only marketplace and CI controls are allowlisted separately.

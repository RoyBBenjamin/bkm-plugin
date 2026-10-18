# BKM: checked probability and decision math for your AI agent

Ask an AI whether a food lot is safe to release after a negative test, and it will often say yes.
That answer is wrong in a way that matters: a test that found nothing is not proof that nothing
is there.

**Benjamin Knowledge Models (BKM)** gives your agent a calculator it can't bluff with. When a
question involves uncertainty (risk, reliability, test results, design levels, or whether more
information is worth buying), the agent hands it to BKM. BKM does three things a language model
on its own does not:

- **It asks instead of guessing.** If a probability, cost or consequence is missing, BKM returns
  the question your agent should ask you. It never invents an input.
- **It calculates exactly.** Same inputs, same answer, every time, with the full calculation
  trace.
- **It says what the answer does not prove.** Every result carries its assumptions, warnings and
  limits.

The mathematics follows Jack R. Benjamin and C. Allin Cornell, *Probability, Statistics, and
Decision for Civil Engineers* (1970), the standard text on reasoning under uncertainty in
engineering.

## See it on one question

> *"A held spice lot passed its first microbiological screen. Should we release it, keep holding
> it, reprocess it, or destroy it? And is another test worth paying for first?"*

With BKM connected, the agent first asks for what it doesn't know: how each outcome should be
valued. Then it calculates. In this worked example (fictional lot, synthetic teaching numbers):

| Question | BKM's answer |
|---|---|
| Best action right now | **Keep holding.** The negative screen leaves real contamination risk. |
| What would perfect information be worth? | 72.5 on the case's utility scale |
| Best next step | **Check the process records** (net value 40.05), ahead of a confirmatory culture (37.46) or more rapid sampling (31.23) |

A generic AI tends to answer "the test was negative, release it." BKM shows why that's the wrong
question, and which evidence is worth buying next. The full worked case, with every input and
output, is in [`examples/food-lot/`](examples/food-lot/README.md) in this package, together with a
script that recomputes every number independently.

## What BKM covers

Distributions and design levels (normal, lognormal, gamma, extreme-value and more), reliability
and exceedance, Bayesian updating, confidence limits and significance tests, model checking
(chi-square, Kolmogorov–Smirnov), decision trees, expected utility, and the value of
information. The live catalog is always available from the service itself (`read_contract`).

## Get started

Getting started is easy and free. BKM runs as a hosted service, **BKM Sidekick**, at
`https://sidekick.benjaminknowledgemodels.com/v1/mcp`. Install the plugin, sign in when your
client asks, and new accounts start on the free Explorer plan with
100 work units a day. Reading the contract is free; assessing a formulation costs 1 unit, and a
calculation with one analysis about 6, so the free plan covers roughly 15 calculations a day. The plugin itself contains no credential; you
sign in through Sidekick's own OAuth flow, and you are never asked to paste a key or password.
Install commands for Claude Code, Codex, GitHub Copilot, VS Code and Cursor are below.

What's in the package:

| Path | What it is |
|---|---|
| `skills/bkm/SKILL.md` | The skill: when to reach for BKM, how to formulate a question, and the rules that keep answers honest |
| `.mcp.json` | The Claude Code connection to Sidekick (no credentials) |
| `mcp.json` | The same connection for Agent Plugins clients |
| `plugin.json`, `.claude-plugin/plugin.json` | Manifests for Agent Plugins clients and Claude Code |
| `examples/food-lot/` | The worked case above: inputs, BKM's responses, and an independent verifier |

**Data and privacy.** When your agent calls BKM, it sends Sidekick the problem it formulated and
gets back the calculation. Sidekick processes your problem in memory and does not keep it by
default. Sidekick's [privacy notice](https://sidekick.benjaminknowledgemodels.com/privacy) says what it
does store and for how long, and its [terms](https://sidekick.benjaminknowledgemodels.com/terms)
govern use of the service.

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
workspace policy, and quota-bearing tests.

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

**VS Code** (from its documentation)

Set `"chat.plugins.enabled": true`, then either run **Chat: Install Plugin From Source** and
enter `https://github.com/RoyBBenjamin/bkm-plugin`, or add `RoyBBenjamin/bkm-plugin` to
`"chat.plugins.marketplaces"` and install from the Extensions view (`@agentPlugins`).

**Cursor** (from its documentation)

Cursor reads `plugin.json` at the root of a plugin directory. Clone this repository and add it
from Cursor's plugin screen, or install once it is listed in the Cursor Marketplace.

## Connection

The package points at the canonical Sidekick origin,
`https://sidekick.benjaminknowledgemodels.com/v1/mcp`. Agent Plugins clients read `mcp.json`;
Claude Code reads `.mcp.json`. The portable manifest declares OAuth with CIMD preference, exact
resource binding, and the minimum `mcp:tools` scope; it contains no client secret. OAuth sign-in
and account linking can differ slightly between clients.

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

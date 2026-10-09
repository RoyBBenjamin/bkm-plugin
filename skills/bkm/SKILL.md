---
name: bkm
description: Use the Benjamin Knowledge Models (bkm) MCP service for probability, statistics and decision-under-uncertainty questions that need a checked calculation instead of improvised arithmetic, covering design values and exceedance, reliability, statistical inference and model checking, Bayesian updating, value of information, and decisions under uncertain loads or demand. Use it even if the user does not say "bkm", and read its catalog through the service (read_contract) rather than from memory; the catalog is the current list of what it covers. Do not use it for plain arithmetic, unit conversion, or questions with no uncertainty.
license: Proprietary. NOTICE.md in the plugin has the terms.
metadata:
  author: Roy Benjamin
  version: "1.1.0"
  contract: "bkm://contract/1"
  source: https://github.com/RoyBBenjamin/benjamin-knowledge-models
---

# Benjamin Knowledge Models (bkm)

`bkm` is an MCP service that answers probability, statistics and decision questions by explicit
calculation, following Benjamin and Cornell, *Probability, Statistics, and Decision for Civil
Engineers*. Its calculations are exact and repeatable; yours are not. When a question falls in its
territory, use it.

## Before you start

1. Confirm the `bkm` tools are available (`read_contract`, `assess_formulation`, `execute_analysis`).
   If they are not, say so plainly and stop. Do not do the
   calculation yourself and present it as the service's result. You may offer a clearly labelled
   rough estimate of your own if the user asks for one.
2. If the client asks the user to connect or sign in, let the client complete Sidekick's OAuth flow.
   Never ask the user to paste a token into the conversation. If a call is refused (401 or
   "unauthorized"), tell the user the Sidekick connection is absent, expired or revoked; do not
   retry in a loop.

## The procedure

1. **Choose the capability.** Read the catalog with `read_contract` (`kind: "catalog"`); a client
   that can read MCP resources may read `bkm://contract/1/capabilities` instead. Match the user's problem to
   a capability by its purpose and its "recognition cues" and "exclusions". Do not rely on a list
   held in memory; the catalog is the current truth.
2. **Read the proposal schema** for that capability (`read_contract` with `kind: "schema"`, the
   capability name and `executeInput`; or the schema resource). Build against it.
3. **Build one whole proposal from what the user has actually stated.** Leave out anything they have
   not said. Put raw values in; do not pre-compute means, probabilities or utilities.
4. **Call `assess_formulation` first.** If it returns a next question, ask the user that question in
   plain words, then resubmit the whole proposal with their answer. Repeat until it is ready.
5. **Call `execute_analysis`** for the analyses that are ready.
6. **Explain the result only from the returned values, trace, warnings and limits.** State the answer,
   what it means, and any warning or limit the service attached.

## Rules that matter

- **Never invent an input.** A probability, cost, utility, loss, weight, prior, limit or data value the
  user did not state must be asked for, not assumed. This is the failure the service exists to
  prevent. If the user cannot supply a value, say so and offer the options the service names.
- **Never present your own arithmetic as the service's result.** Every number you report as a result
  must come from a returned value.
- **Show your work on request.** If the user asks what you sent, show the proposal you submitted and
  point out which values came from them.
- **Report limits honestly.** A result is conditional on the model supplied. It is not evidence
  admission and not authorization to act. Where the service warns about small samples, assumptions
  or tails, pass the warning on.
- **Do not silently change the question.** If the closest capability answers a slightly different
  question, say how it differs.
- **Large or unusual requests:** the service publishes size limits in the catalog. If a problem
  exceeds them, tell the user which limit and what they could do instead.

## When the service is the wrong tool

Use ordinary reasoning, not `bkm`, for arithmetic with no uncertainty, unit conversion, or advice that
needs judgment more than calculation. If a problem needs a method no capability offers, say that the
service does not cover it rather than approximating it silently.

## Worked patterns

The service repository's `docs/service/cookbook.md` and `docs/cookbook/` give example problems, the
answers to expect, and what a good session looks like. Use them as models for how to phrase questions to the
user, not as a source of numbers to reuse.

## Notice

© 2026 Roy Benjamin. BKM and its catalog, schemas, cookbooks and traces are proprietary and may not be used to build a competing service. Methods after Benjamin and Cornell (1970); no endorsement claimed. See `NOTICE.md` beside this skill.

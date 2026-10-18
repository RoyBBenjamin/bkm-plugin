# Food-lot disposition: what does another negative sample buy?

This worked case, taken from the BKM cookbook, asks whether a fictional held food lot should be released,
held, reprocessed, or destroyed after an initial screen reports no detection.
It compares two additional sampling plans with a process-record investigation.
The result demonstrates why a no-detection result is not the same claim as an
uncontaminated lot.

## Starter prompt

> Use BKM. A defined food lot remains under control after an initial
> microbiological screen reported no detection. Help formulate whether to
> release it, continue holding it, apply a validated reprocessing step, or
> destroy it, and whether additional sampling or a process-record investigation
> is worth acquiring first. Keep safe or below-concern, localized contamination,
> and widespread contamination distinct. Do not interpret a no-detection result
> as proof of absence. Record actual samples separately from hypothetical future
> outcomes. Ask for the food and hazard, lot boundaries, distribution status,
> sampling design, method characteristics, current evidence, consequences,
> utilities, costs, responsible decision maker, and regulatory constraints.
> Assess before execution and preserve BKM's warnings and authority boundary.

The prompt intentionally omits decision numbers. They must be elicited or
identified as a synthetic teaching fixture.

## 1. Scope the decision before modeling

FDA guidance places product testing inside a broader preventive-control system,
recommends maintaining control while Salmonella testing is underway, and gives
process records an important role in verification and corrective action.
[sources.md](sources.md) documents that context.

The fictional SP-204 spice lot is entirely held, so recall is not an available
action. If any product had entered commerce, traceability and recall choices
would require a different model. The example also assumes—but does not
validate—a feasible reprocessing step.

## 2. Represent heterogeneity explicitly

[case-data.json](case-data.json) defines three states:

- safe or below the stated level of concern;
- localized contamination that samples can miss; and
- widespread contamination.

The synthetic prior after the initial no-detection screen is 0.70, 0.20, and
0.10. The nonzero contamination probabilities are deliberate. The raw initial
sampling model is not available, so the recipe supplies the resulting current
belief rather than pretending to reconstruct it.

Four disposition actions and three information sources are compared. All
likelihoods, utilities, and costs are fabricated dimensionless teaching inputs.
[provenance.json](provenance.json) records the boundary.

## 3. Assess what is missing

[assess-incomplete.json](assess-incomplete.json) is the complete BKM request with the
utilities left out. BKM
marks both analyses insufficiently specified and asks:

> How should each possible consequence be valued?

With the synthetic utility table restored, [assess-ready-output.json](assess-ready-output.json)
marks both analyses complete and executable. Model adequacy remains explicitly
unestablished.

## 4. Execute the decision

The complete request and response are [execute.json](execute.json) and
[execute-output.json](execute-output.json).

| Question | Result |
|---|---:|
| Current preferred action | Continue hold |
| Current optimal expected utility | 23.5 |
| Expected utility with perfect information | 96 |
| Expected value of perfect information | 72.5 |
| Expanded rapid sampling: gross / cost / net | 35.23 / 4 / 31.23 |
| Confirmatory culture: gross / cost / net | 55.461 / 18 / 37.461 |
| Process-record investigation: gross / cost / net | 43.05 / 3 / 40.05 |
| Preferred information source after cost | Process-record investigation |

Confirmatory culture has the greatest gross information value. The process
investigation nevertheless wins after cost in this fixture. That conclusion is
conditional on every supplied likelihood, consequence value, and cost.

| Information source | Hypothetical outcome | Modeled disposition |
|---|---|---|
| Expanded rapid sampling | Detected | Validated reprocess |
| Expanded rapid sampling | No detection | Release lot |
| Expanded rapid sampling | Inconclusive | Validated reprocess |
| Confirmatory culture | Confirmed | Validated reprocess |
| Confirmatory culture | Not found | Release lot |
| Confirmatory culture | Inconclusive | Continue hold |
| Process records | Control failure | Validated reprocess |
| Process records | Records support control | Release lot |
| Process records | Unresolved | Continue hold |

Even in branches that select release, BKM is only reporting the action with the
highest expected utility in the supplied model. A no-detection or supportive
record outcome is not re-labeled as proof of safety.

## 5. Reproduce and verify

[verify.mjs](verify.mjs) independently recomputes the current decision, perfect
information, all contingent policies, and gross and net information values
with exact rational arithmetic. It compares those calculations with
[expected-result.json](expected-result.json) and the captured BKM result in
[execute-output.json](execute-output.json). It needs only Node.js:

```sh
node examples/food-lot/verify.mjs
```

To rerun the case against the live service, send [assess-ready.json](assess-ready.json)
to `assess_formulation` and [execute.json](execute.json) to `execute_analysis` from any
connected client; the responses should match the captured outputs apart from identifiers
and timestamps.

## 6. Real-world boundary

A real decision requires identified legal and food-safety authority, exact lot
and distribution boundaries, hazard and action thresholds, a validated sampling
design and analytical method, process and traceability records, dependence and
heterogeneity assessment, validated corrective controls, public-health and
economic consequences, sensitivity analysis, and applicable regulation. This
recipe admits no evidence, establishes no model adequacy, authorizes no release
or treatment, and is not food-safety or regulatory advice.

#!/usr/bin/env node

import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {dirname, join} from "node:path";
import {fileURLToPath} from "node:url";

const caseDirectory = dirname(fileURLToPath(import.meta.url));
const input = readJson("assess-ready.json");
const expected = readJson("expected-result.json");
const actual = readJson("execute-output.json");
const incomplete = readJson("assess-incomplete-output.json");
const ready = readJson("assess-ready-output.json");
const proposal = input.proposal;

const states = proposal.states.map(item => item.id);
const actions = proposal.actions.map(item => item.id);
const prior = new Map(proposal.prior.map(item => [item.stateId, rational(item.probability)]));
const consequenceByPair = new Map(proposal.consequences.map(item => [
  `${item.actionId}|${item.stateId}`, item.consequenceId
]));
const utilityByConsequence = new Map(proposal.utilities.map(item => [
  item.consequenceId, rational(item.utility)
]));
const utility = (actionId, stateId) => utilityByConsequence.get(
  consequenceByPair.get(`${actionId}|${stateId}`)
);

const currentValues = new Map(actions.map(actionId => [
  actionId,
  sum(states.map(stateId => multiply(prior.get(stateId), utility(actionId, stateId))))
]));
const currentBest = maximumEntries(currentValues);
const perfect = sum(states.map(stateId => multiply(
  prior.get(stateId), maximum(actions.map(actionId => utility(actionId, stateId)))
)));
const evpi = subtract(perfect, currentBest.value);

assert.deepEqual(currentBest.keys, expected.currentDecision.preferredActionIds);
for (const [actionId, value] of currentValues) {
  assertRationalEqual(value, expected.currentDecision.expectedUtilities[actionId], actionId);
}
assertRationalEqual(perfect, expected.currentDecision.perfectInformationExpectedUtility, "perfect information");
assertRationalEqual(evpi, expected.currentDecision.expectedValueOfPerfectInformation, "EVPI");

const experimentResults = new Map();
for (const experiment of proposal.experiments.filter(item => item.kind === "ACQUIRE_INFORMATION")) {
  const likelihood = new Map(experiment.likelihoods.map(item => [
    `${item.stateId}|${item.observationId}`, rational(item.probability)
  ]));
  const preferredActionsByObservation = {};
  const bestJointValues = [];
  for (const observation of experiment.possibleObservations) {
    const jointActionValues = new Map(actions.map(actionId => [
      actionId,
      sum(states.map(stateId => multiply(
        multiply(prior.get(stateId), likelihood.get(`${stateId}|${observation.id}`)),
        utility(actionId, stateId)
      )))
    ]));
    const branchBest = maximumEntries(jointActionValues);
    assert.equal(branchBest.keys.length, 1, `${experiment.id}/${observation.id} must have one best action`);
    preferredActionsByObservation[observation.id] = branchBest.keys[0];
    bestJointValues.push(branchBest.value);
  }
  const beforeCost = sum(bestJointValues);
  const cost = rational(experiment.acquisitionCost);
  const gross = subtract(beforeCost, currentBest.value);
  const net = subtract(gross, cost);
  const afterCost = subtract(beforeCost, cost);
  experimentResults.set(experiment.id, {preferredActionsByObservation, beforeCost, cost, gross, net, afterCost});
}

const preferredExperiments = maximumEntries(new Map(
  [...experimentResults].map(([id, result]) => [id, result.net])
)).keys;
assert.deepEqual(preferredExperiments, expected.sampleInformation.preferredExperimentIds);
for (const [experimentId, computed] of experimentResults) {
  const wanted = expected.sampleInformation.experiments[experimentId];
  assert.deepEqual(computed.preferredActionsByObservation, wanted.preferredActionsByObservation);
  assertRationalEqual(computed.beforeCost, wanted.expectedUtilityBeforeCost, `${experimentId} before cost`);
  assertRationalEqual(computed.gross, wanted.grossValueOfInformation, `${experimentId} gross value`);
  assertRationalEqual(computed.cost, wanted.acquisitionCost, `${experimentId} cost`);
  assertRationalEqual(computed.net, wanted.netValueOfInformation, `${experimentId} net value`);
  assertRationalEqual(computed.afterCost, wanted.expectedUtilityAfterCost, `${experimentId} after cost`);
}

assert.equal(incomplete.assessment.nextQuestion.issueCode, "MISSING_UTILITY_VALUES");
assert.equal(incomplete.assessment.nextQuestion.text, "How should each possible consequence be valued?");
for (const analysis of ["CURRENT_DECISION", "SAMPLE_INFORMATION"]) {
  assert.equal(incomplete.assessment.analyses[analysis].eligibleForExecution, false);
  assert.equal(ready.assessment.analyses[analysis].eligibleForExecution, true);
}
assert.equal(ready.proposalFingerprint, expected.proposalFingerprint);
assert.equal(actual.proposalFingerprint, expected.proposalFingerprint);
assert.deepEqual(actual.authorityBoundary, expected.authorityBoundary);

const actualCurrent = actual.analysisOutcomes.CURRENT_DECISION.result;
assert.deepEqual(actualCurrent.preferredActionIds, currentBest.keys);
for (const item of actualCurrent.actionValues) {
  assertDecimalClose(item.expectedUtility, currentValues.get(item.actionId), `${item.actionId} BKM result`);
}
assertDecimalClose(actualCurrent.perfectInformation.expectedUtilityWithPerfectInformation, perfect, "BKM perfect information");
assertDecimalClose(actualCurrent.perfectInformation.valueOfPerfectInformation, evpi, "BKM EVPI");

const actualSample = actual.analysisOutcomes.SAMPLE_INFORMATION.result;
assert.deepEqual(actualSample.preferredExperimentIds, preferredExperiments);
for (const item of actualSample.experimentResults.filter(value => experimentResults.has(value.experimentId))) {
  const computed = experimentResults.get(item.experimentId);
  assertDecimalClose(item.informationValue.expectedUtilityWithInformationBeforeCost, computed.beforeCost, `${item.experimentId} BKM before cost`);
  assertDecimalClose(item.informationValue.grossValueOfInformation, computed.gross, `${item.experimentId} BKM gross value`);
  assertDecimalClose(item.informationValue.netValueOfInformation, computed.net, `${item.experimentId} BKM net value`);
  assertDecimalClose(item.expectedUtilityAfterCost, computed.afterCost, `${item.experimentId} BKM after cost`);
  const policies = Object.fromEntries(item.branches.map(branch => [
    branch.observationId, branch.preferredActionIds[0]
  ]));
  assert.deepEqual(policies, computed.preferredActionsByObservation);
}

console.log("Independent food-lot verification passed: current decision, EVPI, three information policies, and net VOI.");

function readJson(name) { return JSON.parse(readFileSync(join(caseDirectory, name), "utf8")); }
function rational(text) {
  const match = String(text).match(/^(-?)(\d+)(?:\.(\d+))?$/);
  assert.ok(match, `not a decimal: ${text}`);
  const fraction = match[3] ?? "";
  return reduce({n: BigInt(`${match[1]}${match[2]}${fraction}`), d: 10n ** BigInt(fraction.length)});
}
function reduce(value) {
  const divisor = gcd(value.n < 0n ? -value.n : value.n, value.d);
  return {n: value.n / divisor, d: value.d / divisor};
}
function gcd(left, right) {
  while (right !== 0n) [left, right] = [right, left % right];
  return left;
}
function add(left, right) {
  return reduce({n: left.n * right.d + right.n * left.d, d: left.d * right.d});
}
function subtract(left, right) { return add(left, {n: -right.n, d: right.d}); }
function multiply(left, right) { return reduce({n: left.n * right.n, d: left.d * right.d}); }
function sum(values) { return values.reduce(add, {n: 0n, d: 1n}); }
function compare(left, right) {
  const difference = left.n * right.d - right.n * left.d;
  return difference < 0n ? -1 : difference > 0n ? 1 : 0;
}
function maximum(values) { return values.reduce((best, value) => compare(value, best) > 0 ? value : best); }
function maximumEntries(entries) {
  const best = maximum([...entries.values()]);
  return {keys: [...entries].filter(([, value]) => compare(value, best) === 0).map(([key]) => key), value: best};
}
function assertRationalEqual(actualValue, expectedText, label) {
  assert.equal(compare(actualValue, rational(expectedText)), 0, label);
}
function assertDecimalClose(actualText, expectedValue, label) {
  const difference = subtract(rational(actualText), expectedValue);
  const absolute = difference.n < 0n ? {n: -difference.n, d: difference.d} : difference;
  assert.ok(compare(absolute, rational("0.0000000000000000000000000001")) <= 0, label);
}

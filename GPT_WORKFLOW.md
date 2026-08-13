# GPT / remote-agent execution loop

This file is the operational state machine. Execute one numbered phase at a
time and update `TASKS.md` plus the run ledger before continuing.

## Loop invariant

At every iteration there must be:

- one explicit hypothesis;
- one smallest runnable experiment;
- one matched baseline;
- one machine-readable result, including failures;
- one evidence-based next decision.

## Phase 0 — provenance lock

1. Obtain the paper PDF legally from the user or public source.
2. Create `references/PAPER_NOTES.md` containing exact page/equation anchors.
3. Reclassify each mechanism as `PAPER`, `DERIVED`, or `HYPOTHESIS`.
4. If the paper contradicts this protocol, preserve this protocol as v0.1 and
   propose a versioned amendment; never rewrite history after results exist.

Exit: provenance table reviewed, or explicitly marked pending without stronger
paper claims.

## Phase 1 — implementation spine

Implement:

```text
src/data/{modular,copy,associative,shakespeare}.py
src/models/{components,variants}.py
src/{config,train,evaluate,metrics,artifacts}.py
tests/
```

Contract tests must verify parameter sharing by object identity/storage, not
only equal initial values. Add formula-level tests for each update using toy
linear fields. Count unique parameters and block evaluations.

Exit: unit tests and config validation pass.

## Phase 2 — smoke loop

For every required variant and synthetic benchmark:

1. Dry-run resolved config.
2. Run one batch forward/backward.
3. Overfit 100 examples with seed 0.
4. Evaluate at train depth and one larger test depth.
5. Validate artifacts against `results/schema.json`.

On failure: classify `CODE`, `DATA`, `NUMERICAL`, `RESOURCE`, or `PROTOCOL`;
record it; fix only the smallest cause; rerun the failed smoke case.

Exit: all required variants pass, or a documented `STOP_VARIANT` decision.

## Phase 3 — synthetic pilot

Run the `pilot` entries in `configs/experiment_matrix.yaml`, seed 0. Generate a
compact comparison table. Select one learning rate per benchmark using only
validation results. Lock it in a new matrix version.

Exit: pilot gate decision for every variant.

## Phase 4 — confirmatory synthetic runs

Run locked configs with seeds 0/1/2. Do not tune after seeing seed 1 or 2.
Aggregate metrics, confidence intervals, stability diagnostics, and compute.

Exit: H1-H3 labeled supported, unsupported, or inconclusive.

## Phase 5 — Tiny Shakespeare

Repeat smoke, pilot, and confirmation. Validate corpus SHA256 before training.
Compare BPC at fixed tokens and compute. Depth extrapolation uses frozen model
weights and must be clearly separated from extra training compute.

Exit: language result plus cross-benchmark synthesis.

## Phase 6 — optional small ViT

Run only if the promotion gate is met or the user explicitly requests a
negative-control vision experiment. Freeze preprocessing and augmentation first.

## Phase 7 — final report

Produce:

- `reports/final.md` with provenance-safe conclusions;
- full result ledger and excluded-run reasons;
- plots specified in `EXPERIMENT_PLAN.md`;
- exact reproduction commands;
- limitations and negative results;
- a minimal recommended architecture, if supported.

## Per-run decision template

```markdown
Run ID:
Commit:
Hypothesis:
Variant / baseline:
Changed from locked protocol:
Acceptance criterion:
Outcome:
Failure class (if any):
Decision: CONTINUE | REVISE | STOP_VARIANT | ESCALATE | PROMOTE
Next smallest action:
```

## Server continuation prompt

Paste this to a new agent only after cloning the repository:

> Read AGENTS.md, EXPERIMENT_PLAN.md, GPT_WORKFLOW.md, TASKS.md, the experiment
> matrix, and the latest result ledger. Resume the first unchecked, unblocked
> task. Do not launch a full sweep before its gate. Record failed runs, preserve
> the provenance boundary, run tests, and commit one evidence-producing change.


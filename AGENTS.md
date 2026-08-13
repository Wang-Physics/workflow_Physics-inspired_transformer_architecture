# Instructions for coding and experiment agents

## Mission

Implement and run the protocol in `EXPERIMENT_PLAN.md` without changing its
scientific question after seeing results. Optimize for interpretable evidence,
not leaderboard performance.

## Mandatory reading order

Read `README.md`, `EXPERIMENT_PLAN.md`, `GPT_WORKFLOW.md`, the matrix config, and
the results specification before editing code or starting a run.

## Provenance rules

- Label statements as `PAPER`, `DERIVED`, or `HYPOTHESIS`.
- Do not attribute general-Transformer performance claims to the PITQS paper.
- The paper-to-ML bridge is an analogy to test, not an established theorem.
- If the paper PDF becomes available, add `references/PAPER_NOTES.md` with exact
  equation/page anchors. Do not invent citations.

## Work loop

1. Inspect repository state, open tasks, latest run manifest, and failures.
2. Select exactly one smallest unblocked item from `TASKS.md`.
3. State the hypothesis, acceptance test, and files to change in the run log.
4. Implement the smallest change and add/adjust tests.
5. Run fast checks locally. Do not start a GPU sweep to debug basic code.
6. Execute one smoke configuration with seed 0.
7. Record all outputs using `results/schema.json`; include failures.
8. Compare against the matched standard and shared-Lie controls.
9. Decide `CONTINUE`, `REVISE`, `STOP`, or `ESCALATE` using the gates below.
10. Commit code and metadata together; never commit large checkpoints.

## Hard constraints

- No test-set tuning.
- No deletion of failed runs.
- No unlogged hyperparameter changes.
- No comparison with different token/step budgets unless explicitly labeled.
- No claim based on one seed.
- Do not run optional CIFAR-10 until core benchmark gates pass.
- Keep each commit single-purpose and leave the repository runnable.

## Required implementation interface

The training entry point should become:

```bash
python -m src.train --config configs/runs/<run>.yaml
```

It must support `--dry-run`, resume from checkpoint, deterministic seed setup,
and emit:

```text
runs/<run_id>/resolved_config.yaml
runs/<run_id>/manifest.json
runs/<run_id>/metrics.jsonl
runs/<run_id>/summary.json
```

## Decision gates

- `CONTINUE`: smoke tests pass and metrics/artifacts validate.
- `REVISE`: implementation or numerical checks fail but cause is actionable.
- `STOP_VARIANT`: two pilot depths diverge after one documented stabilization
  attempt, or the variant is Pareto-dominated in quality, compute, and params.
- `ESCALATE`: protocol ambiguity would change the scientific conclusion.
- `PROMOTE`: at least two core benchmarks show a preregistered benefit with
  three seeds and no material stability regression.

## Reporting language

Use calibrated claims: “supports”, “does not support”, or “inconclusive”. Never
translate a benchmark win into a general architectural claim without evidence.


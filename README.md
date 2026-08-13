# PITQS-inspired Transformer Workflow

An agent-readable, reproducible workflow for testing whether ideas motivated by
*Physics-inspired transformer quantum states via latent imaginary-time evolution*
improve or clarify ordinary Transformers.

This repository is an **experimental protocol**, not a claim that the paper
establishes results on language, vision, or algorithmic tasks. See
[`EXPERIMENT_PLAN.md`](EXPERIMENT_PLAN.md) for the provenance boundary.

## Research question

Can a Transformer block be treated as a reusable numerical update rule, and do
weight sharing, operator splitting, higher-order residual updates, or learned
step sizes improve parameter efficiency, stability, or depth extrapolation?

## Required model variants

| ID | Variant | Core update |
|---|---|---|
| `standard` | Independent blocks | one parameter set per depth |
| `shared_lie` | Shared-weight sequential | Attention then FFN |
| `shared_strang` | Strang-style split | half FFN, Attention, half FFN |
| `shared_parallel` | Parallel branches | Attention and FFN from same state |
| `shared_heun` | RK2/Heun-style | predictor-corrector shared update |
| `shared_learned_dt` | Learned step | shared update with constrained step size |

## Benchmarks

1. Modular addition: algorithm learning and held-out-pair generalization.
2. Sequence copy and associative recall: controlled memory and length scaling.
3. Tiny Shakespeare: character-level next-token prediction.
4. CIFAR-10 small ViT: optional only after the first three pass the gates.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_matrix.py configs/experiment_matrix.yaml
```

The initial repository deliberately separates protocol from implementation.
The first agent loop in [`GPT_WORKFLOW.md`](GPT_WORKFLOW.md) creates the minimal
PyTorch runner and must pass smoke tests before any GPU sweep begins.

## Remote-agent entry point

Read files in this order:

1. `AGENTS.md`
2. `EXPERIMENT_PLAN.md`
3. `GPT_WORKFLOW.md`
4. `configs/experiment_matrix.yaml`
5. `results/README.md`

Never launch the full matrix until the smoke gate succeeds. Never silently
change the matrix after results exist; create a new protocol version instead.

## Reproducibility contract

- Python 3.11 and pinned major dependencies.
- Seeds `0, 1, 2` for confirmatory runs; seed `0` only for smoke/pilot runs.
- Store resolved config, git commit, environment, metrics, and failure status.
- Compare variants at matched training tokens/steps and matched width/depth.
- Report both raw parameter count and parameter-matched controls.
- Predeclare primary metrics and stopping rules before confirmatory runs.
- Failed or diverged runs remain in the result table.

## Status

- [x] Protocol and experiment matrix
- [x] Agent execution loop and result schema
- [ ] Paper PDF/page-level provenance audit
- [ ] Minimal PyTorch implementation
- [ ] Smoke tests
- [ ] Pilot sweep
- [ ] Confirmatory sweep


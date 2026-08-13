# Experiment plan

## 1. Scope and provenance boundary

### Conservative paper-origin concepts (`PAPER`, pending page audit)

The supplied conversation describes PITQS as interpreting repeated Transformer
depth as latent imaginary-time evolution, using shared parameters across
layers, and examining Attention/FFN splitting and higher-order integration-like
updates. These are the only concepts provisionally marked paper-origin here.
Exact wording, equations, and page numbers must be audited against the PDF.

### Derived engineering mappings (`DERIVED`)

- Layer index becomes a discrete computation-time index.
- A shared block represents a stationary learned vector field/update rule.
- Residual scaling is interpreted as a numerical step size.
- Train-depth/test-depth evaluation probes whether the rule can be iterated.

### New general-Transformer hypotheses (`HYPOTHESIS`)

- Strang-style `FFN(dt/2) -> Attention(dt) -> FFN(dt/2)` can improve stability.
- Parallel Attention+FFN can be a useful splitting control.
- RK2/Heun residual updates can outperform Euler-like shared residual updates.
- A constrained learnable step size can adapt useful computation time.
- These changes may help modular arithmetic, memory, language modeling, or ViT.

None of the hypotheses above is asserted as a result of the source paper.

## 2. Formalized variants

Let normalized state be `x`, attention field `A(x)`, FFN field `F(x)`, and step
size `dt`. Pre-norm and residual/dropout conventions must be identical across
variants.

### V0 Standard Transformer

`x_{k+1} = Block_k(x_k)` with independent parameters. This is the quality and
compute reference, not a parameter-matched control.

### V1 Shared Lie/Euler baseline

Repeat a single block: `x_{k+1} = FFN(Attention(x_k))`, using residual substeps
scaled by `dt`. This isolates weight sharing and iterative depth.

### V2 Shared Strang-style split

`x <- F(dt/2, x); x <- A(dt, x); x <- F(dt/2, x)`.

Important: two FFN half-steps reuse the same FFN parameters. Report whether
dropout masks are independent. This is “Strang-style” because nonlinear learned
residual blocks do not automatically satisfy classical splitting assumptions.

### V3 Shared parallel control

`x_{k+1} = x_k + dt * (A(LN(x_k)) + F(LN(x_k)))`.

Use branch scaling or initialization so variance is comparable to sequential
variants. This is a control for ordering, not presumed to be higher-order.

### V4 Shared RK2/Heun

For a combined shared update field `G`:

1. `k1 = G(x_k)`
2. `x_pred = x_k + dt*k1`
3. `k2 = G(x_pred)`
4. `x_{k+1} = x_k + dt*(k1+k2)/2`

The two calls share parameters. Report roughly doubled block evaluations. A
matched-compute Euler control is mandatory.

### V5 Shared learned step size

Start from V1. Parameterize `dt = dt_min + softplus(raw_dt)` and optionally cap
it at `dt_max`. Test one global scalar first; per-depth steps weaken stationary
weight-sharing and belong in an exploratory appendix.

## 3. Primary hypotheses

- H1: shared variants reduce unique parameters at acceptable quality loss.
- H2: shared rules trained at depth `D` retain or improve performance when
  evaluated at larger depth without parameter updates.
- H3: Strang-style or Heun updates improve deep-iteration stability versus V1.
- H4: benefits persist after matching compute, not only parameter count.

Primary null: no variant improves the quality/parameter/compute Pareto frontier
over V0 and V1 on at least two core benchmark families.

## 4. Benchmarks and splits

### Modular addition

- Task: predict `(a+b) mod p`; primary `p=97`.
- Token format: `[BOS, a, PLUS, b, EQ] -> y`.
- Deterministic held-out pair split; do not leak commutative counterparts across
  splits unless the split generator explicitly groups `(a,b)` and `(b,a)`.
- Primary: held-out-pair accuracy. Secondary: steps to 99% train accuracy,
  calibration, parameter count, tokens/sec.
- Extrapolation: test recurrent depths `{D, 2D, 4D}`.

### Sequence copy

- Train lengths 8-32, vocabulary 32; disjoint deterministic samples.
- Test interpolation 8-32 and extrapolation 48, 64, 96.
- Primary: exact-sequence accuracy; secondary: token accuracy.

### Associative recall

- Key-value pairs followed by a query key; avoid duplicate keys per example.
- Train 2-8 pairs; test 10, 12, 16 pairs.
- Primary: queried-value accuracy; stratify by query position.

### Tiny Shakespeare

- Character-level, fixed downloaded file hash and contiguous train/val/test
  split to avoid context leakage.
- Context 128 for pilot, optionally 256 for confirmation.
- Primary: validation bits-per-character (BPC). Secondary: test BPC once,
  throughput, peak memory, and parameter count.
- Do not use generated text quality as a primary metric.

### Optional CIFAR-10 small ViT

- Fixed standard train/test split; reserve a deterministic validation subset.
- Patch size 4, small width, no external pretraining.
- Primary: validation/test accuracy; report augmentation recipe.
- Activate only after promotion gate on core tasks.

## 5. Fair comparisons

Every architectural conclusion needs both:

1. **Shape-matched:** same width, heads, nominal depth, optimizer, and training
   tokens/steps. Reveals direct parameter savings.
2. **Budget-matched:** match trainable parameters or block evaluations/FLOPs.
   Reveals whether gains survive a fair resource comparison.

Heun uses two field evaluations and therefore cannot be described as a free
improvement. Depth extrapolation evaluation must report actual block calls.

## 6. Depth protocol

- Train depths: `D in {2, 4, 8}` for synthetic tasks; `{4, 8}` for language.
- Evaluate frozen weights at `{1, 2, 4, 8, 16, 32}` where feasible.
- For standard independent layers, depths beyond training depth are undefined;
  compare only through an explicitly labeled layer-repetition control.
- Keep positional encoding support large enough for length tests; depth and
  sequence-length extrapolation are separate axes.
- Record performance after every recurrent step to detect monotone improvement,
  saturation, oscillation, or collapse.

## 7. Optimization protocol

- AdamW, gradient clipping, identical scheduler within a benchmark.
- Pilot learning-rate grid chosen using validation only, then frozen.
- Seeds 0/1/2 for confirmatory runs; report mean, standard deviation, and all
  individual outcomes.
- Stop by fixed update/token budget for cross-architecture fairness; early
  stopping is diagnostic and must not silently alter compute comparisons.
- Track gradient norm, activation RMS, update RMS, attention entropy, learned
  `dt`, throughput, memory, NaN/Inf events, and wall-clock time.

## 8. Analysis

Primary plots:

- quality vs unique parameters;
- quality vs estimated FLOPs/block evaluations;
- metric vs test depth for each train depth;
- training curves with seed bands;
- learned `dt` trajectory and update/activation norms.

Use paired seeds and bootstrap confidence intervals for differences. Synthetic
accuracy should include exact binomial uncertainty. Treat multiple benchmark
and depth comparisons as a family; emphasize effect sizes rather than isolated
p-values.

## 9. Stopping and continuation

### Smoke gate

Continue only if each model produces correct shapes, finite forward/backward
passes, deterministic evaluation, and a 100-example overfit check.

### Pilot gate

Continue a variant when it either improves the validation metric, reduces
parameters by at least 2x within a small quality tolerance, or improves depth
stability. One stabilization attempt (lower LR, clipping, bounded `dt`) is
allowed and must be logged.

### Confirmation gate

Promote a result only with three seeds, locked configs, matched controls, and a
consistent benefit on at least two core benchmark families. Otherwise report
the outcome as benchmark-specific or inconclusive.

### Global stop

Stop expanding the matrix if all nonbaseline variants are Pareto-dominated by
V0 and V1 after confirmed matched-compute pilots. Preserve and publish negative
results.


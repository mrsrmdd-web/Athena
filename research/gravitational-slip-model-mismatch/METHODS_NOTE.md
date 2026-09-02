# Model mismatch can manufacture apparent gravitational slip

**Preliminary methods note — 2026-09-02**

## What did we find?

We tested whether a gravitational-slip analysis could falsely report disagreement between light-bending and stellar-motion measurements even when General Relativity was the truth.

First, the control passed. With `eta = 1` injected and the synthetic truth generated inside the inference family, the nonlinear pipeline recovered:

`eta = 1.012 (+0.065/-0.045)`.

That matters because it shows the sampler/pipeline did not simply manufacture slip on its own.

We then generated truth outside the inference family using plausible mismatch in stellar orbital anisotropy, mass-profile structure, and tracer photometry.

Under a rigid inference family using constant anisotropy and a pure power-law mass profile, the mismatch produced `Delta eta ~ -0.26`, approximately a 5-sigma false slip in the toy experiment.

A more flexible inference family absorbed most of the mismatch, but did not eliminate it. Across 30 noise realizations with true `eta = 1`, the mean recovered value was approximately `1.077`, a manufactured `+7.7%` slip. Additional injections gave approximately:

- true `eta = 1.00` -> recovered `1.077`
- true `eta = 0.98` -> recovered `1.064`
- true `eta = 0.95` -> recovered `1.035`

The bias was therefore roughly additive, of order `+0.08`, with sensitivity slope about `0.85`. Empirical per-system scatter across realizations was approximately `0.06`.

## Why didn't goodness-of-fit catch it?

Because the wrong model still fit the synthetic observations acceptably. The flexible inference model had enough freedom to absorb the mismatch into inferred physical parameters instead of leaving conspicuous residuals. Chi-square remained acceptable while the recovered gravitational-slip parameter was biased.

The failure mode is therefore not "the model obviously fits badly." It is "the model fits smoothly while assigning the wrong physical interpretation."

## Why doesn't the error simply average down with more galaxies?

The dominant effect in this experiment was a shared modeling-family systematic rather than zero-mean random measurement noise. Random noise can decrease as sample size grows; a common modeling bias does not automatically approach zero.

As an explicit arithmetic extrapolation — **not a simulated 20-galaxy ensemble** — taking the empirical `~0.06` per-system scatter and dividing by `sqrt(20)` while retaining a fixed `+0.08` offset gives approximately:

`eta ~ 1.08 +/- 0.013`,

which would resemble an apparent ~6-sigma departure despite the underlying GR truth.

## Why nonlinear injection-recovery matters

A linear/Fisher treatment of the same class of mismatch estimated a bias of only about `+1%`. The full nonlinear injection-recovery produced a residual bias of about `+8%` in the flexible model family.

That linear-to-nonlinear gap is itself part of the result: formal precision forecasts can substantially understate the effect of coupled model mismatch. Outside-family injection-recovery is therefore needed before interpreting percent-level gravitational-slip precision as accuracy.

## What is the claim?

This is not a detection of new gravity.

It is a methods warning: before making a precision gravitational-slip claim from joint lensing + stellar-dynamics analyses, an inference pipeline should demonstrate through realistic outside-family injection-recovery that coupled anisotropy and mass-profile mismatch does not manufacture a coherent slip signal.

## What remains uncertain?

This is not yet publication-grade calibration. Limitations include spherical modeling; eight kinematic bins; image-position constraints rather than full extended-source reconstruction; one principal mismatch family; limited noise realizations; a custom sampler; no full 2D kinematics; no `h3/h4` or higher LOSVD moments; and no hydrodynamic-simulation lens used as external truth.

The ~8% number should therefore be treated as an order-of-magnitude demonstration of a failure mode, not a universal calibrated bias.

## What would strengthen or falsify it?

The next tests should add extended-arc surface-brightness constraints; add higher LOSVD moments, especially `h4`; repeat outside-family injections across multiple mismatch families; port the experiment to standard community tooling such as lenstronomy plus JAM/Schwarzschild-style dynamics; test hydro-simulation lenses with independently known mass/orbital truth; and expand to hundreds of noise realizations with full nonlinear posterior recovery.

If those additions reduce the shared bias below ~2%, a ~3% ensemble gravitational-slip measurement may become credible. If they do not, galaxy-scale precision slip remains simulation-calibration limited.

## Human / AI provenance

The work used a human-directed, multi-model AI-assisted workflow.

Scott / `mrsrmdd-web` set the research direction, selected and challenged hypotheses, chose which branches to pursue, and made the scientific decisions.

OpenAI **GPT-5.6 Sol** helped formulate, refine, and adversarially stress-test the hypotheses and experimental design, including the move from formal precision forecasts to nonlinear outside-family injection-recovery.

Anthropic **Claude Fable 5.1**, September 1-2, 2026, implemented and executed the nonlinear synthetic injection-recovery study and analyzed the numerical results.

The workflow preserved failed intermediate assumptions and revisions rather than presenting only the successful endpoint: the original Fisher estimate, the nonlinear correction, the changed dominant-degeneracy ordering, and withdrawal of an earlier ~3% ensemble-confidence claim.

The intended evidentiary standard is that the scientific claim ultimately stand on independently inspectable code, synthetic truth definitions, configurations, seeds, outputs, and analysis rather than authority or trust in either AI system.

## Reproducibility status

The reported runs are now preserved under `artifacts/`, including the original archive, the five core nonlinear run artifacts, three supporting source files, and the bundled run README. The bundled README documents `python3 nonlinear.py mcmc 7` and `python3 nonlinear.py coverage 11`, and inspection of `nonlinear.py` verifies its positional mode/seed parsing. Exact SHA-256 hashes and byte counts are recorded in `ARTIFACT_MANIFEST.md`.

This remains a timestamped preservation package, not a completed independent reproduction: no clean rerun was performed; no dependency lockfile or environment export is included; and the coverage artifact is summary-only rather than a full per-realization raw dataset.

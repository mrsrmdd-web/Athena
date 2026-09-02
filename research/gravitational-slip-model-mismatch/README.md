# Gravitational-slip inference under model mismatch

**Priority timestamp:** 2026-09-02  
**Repository owner:** `mrsrmdd-web`  
**Status:** preliminary methods result; not yet publication-grade calibration

## Core result

A nonlinear injection-recovery audit found that a same-object gravitational-slip inference pipeline can report a coherent apparent departure from General Relativity when the synthetic truth lies outside the inference model family, even while ordinary goodness-of-fit remains acceptable.

The control passed: with GR injected (`eta = 1`) and truth generated inside the inference family, the nonlinear pipeline recovered `eta = 1.012 (+0.065/-0.045)` and did not manufacture slip on its own.

With plausible joint mismatch in stellar-orbit anisotropy, mass-profile structure, and tracer photometry:

- a rigid inference family (constant anisotropy + pure power-law mass profile) produced an apparent `Delta eta ~ -0.26`, roughly a 5-sigma false slip in that toy configuration;
- a more flexible family absorbed most of the mismatch but retained an approximately additive `+0.08` bias;
- empirical per-system scatter across realizations was about `0.06`;
- the recovered offset stayed of order `+0.08` for injected `eta = 1.00`, `0.98`, and `0.95`, indicating a shared modeling-family systematic rather than zero-mean noise;
- acceptable chi-square did not expose the mismatch;
- a Fisher/linearized treatment estimated only about a 1% bias for the same class of mismatch, while the nonlinear recovery produced about 8%, motivating full injection-recovery rather than relying on precision forecasts alone.

An extrapolation (not a simulated 20-galaxy ensemble) using `0.06/sqrt(20)` with a fixed `+0.08` systematic would yield approximately `eta = 1.08 +/- 0.013`, an apparent ~6-sigma false detection.

## Claim

This is **not** evidence for modified gravity. It is a calibration warning: precision gravitational-slip analyses that combine lensing and stellar dynamics should demonstrate, with realistic outside-family injection-recovery, that coupled anisotropy/profile mismatch does not manufacture a coherent slip signal.

## Limitations

Current implementation is a spherical toy forward model with eight kinematic bins, image-position rather than full extended-source constraints, one principal mismatch family, limited noise realizations, and a custom sampler. It does not yet include full 2D kinematics, higher LOSVD moments (`h3/h4`), extended-arc surface brightness, or hydro-simulation lenses as external truth.

The `~8%` figure is therefore an order-of-magnitude demonstration of a failure mode, **not** a calibrated universal bias.

## Next decisive tests

1. Add extended-arc surface-brightness constraints to reduce profile-shape freedom.
2. Add higher LOSVD moments, especially `h4`, to constrain anisotropy.
3. Repeat the same outside-family injections across multiple mismatch families.
4. Port to standard community tooling (e.g. lenstronomy plus JAM/Schwarzschild-style dynamics).
5. Validate against hydro-simulation lenses with independently known truth.
6. Expand to hundreds of realizations and full nonlinear posterior recovery.

If these additions reduce the shared bias below ~2%, an ensemble ~3% slip measurement may become credible. If not, galaxy-scale precision slip remains simulation-calibration limited.

## Human / AI provenance

This was a human-directed, multi-model AI-assisted research workflow.

- **Scott / `mrsrmdd-web`** set the research direction, selected and challenged hypotheses, and made the scientific decisions.
- **OpenAI GPT-5.6 Sol** helped formulate and adversarially refine the experimental design, including insisting on outside-family injection-recovery rather than trusting formal precision forecasts.
- **Anthropic Claude Fable 5.1**, September 1-2, 2026, implemented and executed the nonlinear synthetic injection-recovery study and analyzed the numerical results.

The workflow preserved failed intermediate assumptions and revisions, including the Fisher estimate, nonlinear correction, changed degeneracy ordering, and withdrawal of the earlier ~3% ensemble-confidence claim.

The scientific claim should ultimately rest on reproducible code and outputs, not trust in either AI system.

## Reproducibility status

The preserved source archive and unpacked originals remain under `artifacts/`. A second Claude-supplied package is preserved separately at `artifacts/claude-second-run/`, and a third, separately labeled Codex rerun is preserved at `artifacts/codex-rerun/`. SHA-256 hashes and byte counts for all run files are recorded in `ARTIFACT_MANIFEST.md`.

The Claude package self-reports an exact same-environment verification and adds per-realization coverage pairs. Codex independently reran both nonlinear commands, but in Python 3.13.14 with NumPy 2.5.2 and SciPy 1.18.0 rather than the Claude-declared environment; the Codex results are therefore preserved as a separate comparison, not substituted for the original outputs. This remains an environment-qualified reproducibility record, not an overclaim of exact independent reproduction.

See `METHODS_NOTE.md` for the compact skeptical-reader version.

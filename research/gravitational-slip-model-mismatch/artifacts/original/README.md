# Gravitational-slip injection–recovery: run package

Reduced-order identifiability audit of same-object gravitational slip (eta = Phi/Psi)
from joint strong lensing + resolved stellar dynamics. Session artifacts, 2026-09-01/02.
Analysis executed by Anthropic Claude Fable 5.1 under human-directed work orders (S. McKinney).

## Files
- `model.py`        forward model: generic spherical density, Jeans dynamics with beta(r),
                    Hernquist tracer, double source plane, Fermat-potential time delay, slip eta
- `fisher.py`       rigid family (const anisotropy + power law): Fisher, ablations, linear mismatch bias
- `fisher_flex.py`  flexible 10-parameter family: Fisher + linear mismatch bias
- `nonlinear.py`    MCMC (custom affine-invariant stretch sampler) + MAP/Laplace coverage runs
- `mcmc_results.json`, `mcmc.log`         output of `python3 nonlinear.py mcmc 7`
- `coverage_results.json`, `cov.log`      output of `python3 nonlinear.py coverage 11`

## Reproduce
    python3 fisher.py
    python3 fisher_flex.py
    python3 nonlinear.py mcmc 7        # ~20 min; seed 7
    python3 nonlinear.py coverage 11   # ~10 min; seed 11

## Environment
Python 3.12, numpy 2.4.4, scipy 1.17.1. No other dependencies. CPU only.

## Headline numbers (as reported)
- Inside-family control (eta=1): posterior 1.012 (+0.065/-0.045)
- Rigid family, OM anisotropy-gradient truth: linear bias d_eta = -0.264
- Flexible family, outside-family truth, 30 realizations: mean recovered eta = 1.077 / 1.064 / 1.035
  for injected 1.00 / 0.98 / 0.95 (additive bias ~ +0.08); chi2 acceptable in all runs
- Flexible family Fisher sigma_eta = 0.100 per system; empirical noise scatter ~0.06

## Known limitations
Spherical; 8 kinematic bins; image positions only (no extended source); one mismatch family;
30 realizations; Laplace error bars over-cover; no h3/h4; no hydro-sim truth.

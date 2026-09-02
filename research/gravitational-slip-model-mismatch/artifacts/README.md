# Gravitational-slip run artifacts

This directory preserves the uploaded `Grav-Slip Inj-Rcvry.zip` and an unpacked, byte-for-byte copy of every archive entry under `original/`. The original filenames and contents are unchanged.

## Reproduce

Run from a disposable copy of `original/` so the committed result files are not overwritten:

```text
python3 nonlinear.py mcmc 7
python3 nonlinear.py coverage 11
```

`nonlinear.py` takes the mode as its first positional argument and the second positional argument as the NumPy RNG seed. The bundled README documents Python 3.12, NumPy 2.4.4, and SciPy 1.17.1; no dependency lockfile is included. This repository preserves the reported outputs but does not claim an independent clean rerun.

See `../ARTIFACT_MANIFEST.md` for the complete inventory, byte counts, SHA-256 hashes, and known gaps.

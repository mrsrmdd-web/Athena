# Artifact manifest

Created 2026-09-02. This manifest distinguishes the artifacts preserved here from an independent rerun of the study.

## Preserved source archive

| Repository path | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `artifacts/Grav-Slip Inj-Rcvry.zip` | 13294 | `8EF2F35706B113D7297D05CCD5A6F383085EDD935822E1CED70F04DDD3408B68` | Original uploaded archive, copied unchanged |

The archive contains 9 top-level files. Every extracted file below was verified against its ZIP entry: archive byte count and extracted byte count match, and the SHA-256 digest matches.

## Five core nonlinear run artifacts

| Repository path | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `artifacts/original/nonlinear.py` | 6996 | `B2E7FC446F7F72A7865D86C8F2ADBAF895D34B4174FB72445500F47FFDC83E75` | Nonlinear MCMC and coverage driver |
| `artifacts/original/mcmc_results.json` | 2626 | `3F3BECE24DF4C14969660B118D0EC1FAA98E204302CB13317602319CFDA14716` | MCMC summary output |
| `artifacts/original/mcmc.log` | 2081 | `3871430377CF6835F58E0273DE3BADDE382499F343C6CAFFDD2B4F6B6C8C04FF` | MCMC run log |
| `artifacts/original/coverage_results.json` | 662 | `D75FDC1BC5481D440E161FA69959E2EF90F0478FA27BCB8A8B0B3D9C2467A2DE` | Coverage summary output |
| `artifacts/original/cov.log` | 856 | `5D92D50CA22ECB98B0C28CAC902934DD1AE43E066B292D1EFE5A2D6B1F4A3A71` | Coverage run log |

## Supporting files preserved from the archive

| Repository path | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `artifacts/original/model.py` | 5712 | `2A0227729DAC884D86922C11EC2E30879CE3C357D03CC5243A3FB0A0B3E05652` | Forward model and observables |
| `artifacts/original/fisher.py` | 5925 | `53AA0859CF745CEF1037B67294AB6FFFD21236C7B1B6E18DA260C78341F629BE` | Rigid-family Fisher and linear mismatch calculations |
| `artifacts/original/fisher_flex.py` | 3967 | `52D7C5FBEEE9FCF3CEEB6AF18E77C874360A55E1F8403CDD646DF6B2AD96A19E` | Flexible-family Fisher and linear mismatch calculations |
| `artifacts/original/README.md` | 1880 | `C6DDAEBEB4E9FAD2C229C556CEBC988750283A6F96FDADFBE43C9DC906FF0ACA` | Original run-package instructions and reported environment |

The earlier phrase “five-file package” referred to the five core run artifacts; the uploaded archive also contains these four supporting files. The bundled `README.md` is preserved separately from this repository directory’s existing `README.md`.

## Verified invocation details

The bundled `artifacts/original/README.md` documents:

```text
python3 nonlinear.py mcmc 7
python3 nonlinear.py coverage 11
```

Inspection of `nonlinear.py` verifies that it reads `sys.argv[1]` as the mode and `sys.argv[2]` as the integer NumPy RNG seed. The MCMC summary contains 5 cases and `mcmc.log` contains 5 posterior-summary lines; the coverage summary contains 3 cases and `cov.log` contains 3 final summary records. These are preservation and internal-consistency checks, not a clean rerun.

## Reproducibility scope and known gaps

- The original bytes and archive provenance are preserved, but no independent clean rerun was performed.
- The bundled README declares Python 3.12, NumPy 2.4.4, and SciPy 1.17.1, with no other dependencies. No `requirements.txt`, `pyproject.toml`, lockfile, or environment export is included.
- The current verification environment was Python 3.13.14 with NumPy 2.5.2 and SciPy 1.18.0; it was not used to regenerate the outputs.
- `coverage_results.json` is summary-only. `cov.log` records progress for realizations 0, 10, and 20 plus final summaries; a full per-realization raw coverage table is not included.
- The archive contains source code and reported outputs, but no separate configuration/priors file, full raw observation realization store, or archival DOI/release tag.

Accordingly, this commit preserves a dated artifact package and its provenance. It does not overclaim complete independent reproduction.

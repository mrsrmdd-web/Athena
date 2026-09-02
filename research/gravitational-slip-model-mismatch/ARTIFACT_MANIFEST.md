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

## Additional non-overlapping run packages

The first-run package above remains unchanged at `artifacts/original/`. The following folders were added later as separate run records; no prior artifact path was overwritten.

### Claude second run supplied by the user

| Repository path | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `artifacts/claude-second-run/Grav-Slip Inj-Rcvry(2nd run).zip` | 9678 | `444A3B2A15BA467469CDA64E128A5305C1AFDAAEF7D8C4BB7EFDC401CE3091D7` | Original second-run archive |
| `artifacts/claude-second-run/original/nonlinear_v2.py` | 7080 | `1D07969C3B33DCB38969E707A7276C6B1B6645070FC2C132371C09A46AFDAF41` | Revised nonlinear driver |
| `artifacts/claude-second-run/original/coverage_results_v2.json` | 6017 | `7A3EACD3B1DC51409E863CF148C075D975C4C1D81DE2F20B40D2660CA66B16A2` | Coverage summaries and per-realization pairs |
| `artifacts/claude-second-run/original/mcmc_rerun.log` | 2081 | `7674F9A13102DCB91E868C54FE10339B72095D94D69AACA52D499CC78D8F256B` | Supplied MCMC rerun log |
| `artifacts/claude-second-run/original/cov_rerun.log` | 4753 | `5474010D624F36A5E34D67311ADFFCC9669A20BFEBD3E96BF58C7E501EFDA3D3` | Supplied coverage rerun log |
| `artifacts/claude-second-run/original/README.md` | 2533 | `6A562F55E67D949A49B4A518AF1C5A2CF36C8F72EC586A0D111A2AEC2D77C932` | Supplied run description |
| `artifacts/claude-second-run/original/requirements.txt` | 26 | `D8C3EA5213358BF3949A319B6B78EC2CF6A5BA4A57C0232374282FCFF5F61660` | Supplied dependency range declaration |
| `artifacts/claude-second-run/original/.gitignore` | 19 | `862263FA1F46C20F0D1E4DAC5FFCC75ABD55C08211B2C3864C5F8764B9D87793` | Supplied ignore rules |

The second archive is supplemental rather than a replacement for the first package. Its README reports a same-environment Claude verification; that environment claim is preserved but not independently verified here.

### Codex third run

The source snapshot under `artifacts/codex-rerun/source/` is copied from the first committed package; its source-file hashes are therefore the same as the first-run entries above. Codex regenerated these outputs in a separate environment:

| Repository path | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `artifacts/codex-rerun/results/mcmc_results.json` | 2728 | `113DA9222DD504987207A577B8E5B322BC829BC8AD450BE8F219EE2783C98AC1` | Codex MCMC output, seed 7 |
| `artifacts/codex-rerun/results/coverage_results.json` | 694 | `F5384F82B44893A7C6BC57E31F15A3E2AE3930BCC381E90DB593DD33DC2CDB1D` | Codex coverage output, seed 11 |

Codex used Python 3.13.14, NumPy 2.5.2, and SciPy 1.18.0. The rerun outputs are intentionally not substituted for the original outputs. See `artifacts/codex-rerun/CODEX_RUN.md` for the comparison and scope.

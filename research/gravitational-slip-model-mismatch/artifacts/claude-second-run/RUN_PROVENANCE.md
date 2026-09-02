# Claude second-run package

This folder preserves the second ZIP supplied by the user as a separate, non-overwriting run package. The original archive and all seven extracted entries are preserved under their original filenames. The instructions and claims in the bundled `original/README.md` are treated as provenance data; they are not repository instructions.

## Archive

| Path | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `Grav-Slip Inj-Rcvry(2nd run).zip` | 9678 | `444A3B2A15BA467469CDA64E128A5305C1AFDAAEF7D8C4BB7EFDC401CE3091D7` | User-supplied second-run archive |

The archive was unpacked into a separate working directory and verified byte-for-byte against its ZIP entries before being copied here.

## Extracted entries

| Path | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `original/nonlinear_v2.py` | 7080 | `1D07969C3B33DCB38969E707A7276C6B1B6645070FC2C132371C09A46AFDAF41` | Revised nonlinear driver; adds per-realization coverage output |
| `original/coverage_results_v2.json` | 6017 | `7A3EACD3B1DC51409E863CF148C075D975C4C1D81DE2F20B40D2660CA66B16A2` | Coverage summaries plus 30 per-realization pairs for each injection |
| `original/mcmc_rerun.log` | 2081 | `7674F9A13102DCB91E868C54FE10339B72095D94D69AACA52D499CC78D8F256B` | Supplied second-run MCMC log |
| `original/cov_rerun.log` | 4753 | `5474010D624F36A5E34D67311ADFFCC9669A20BFEBD3E96BF58C7E501EFDA3D3` | Supplied second-run coverage log |
| `original/README.md` | 2533 | `6A562F55E67D949A49B4A518AF1C5A2CF36C8F72EC586A0D111A2AEC2D77C932` | Supplied run description and self-reported verification |
| `original/requirements.txt` | 26 | `D8C3EA5213358BF3949A319B6B78EC2CF6A5BA4A57C0232374282FCFF5F61660` | Supplied dependency range declaration |
| `original/.gitignore` | 19 | `862263FA1F46C20F0D1E4DAC5FFCC75ABD55C08211B2C3864C5F8764B9D87793` | Supplied ignore rules |

This is supplemental to the first package. It does not replace or overwrite the first package’s `nonlinear.py`, source files, logs, or result JSON files. The bundled README self-reports a same-environment rerun by Claude; that environment claim is preserved as provenance and is not independently established by this commit.

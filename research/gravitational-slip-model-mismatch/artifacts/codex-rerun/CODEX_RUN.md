# Codex rerun package

This folder stores the third run as executed by Codex. It is separate from both the first package and the second Claude-supplied package; no earlier artifact path was overwritten.

## Inputs and commands

The source snapshot under `source/` was copied from the first committed package in commit `b72a3e60aaac5e49821d53da91b2c2b3230e11a1`. Codex ran:

```text
python nonlinear.py mcmc 7
python nonlinear.py coverage 11
```

The run used Python 3.13.14, NumPy 2.5.2, and SciPy 1.18.0. This differs from the environment self-reported by the Claude package (Python 3.12, NumPy 2.4.4, SciPy 1.17.1), so these outputs are a separately identified rerun, not a claim of exact environment reproduction.

## Regenerated outputs

| Path | Bytes | SHA-256 |
|---|---:|---|
| `results/mcmc_results.json` | 2728 | `113DA9222DD504987207A577B8E5B322BC829BC8AD450BE8F219EE2783C98AC1` |
| `results/coverage_results.json` | 694 | `F5384F82B44893A7C6BC57E31F15A3E2AE3930BCC381E90DB593DD33DC2CDB1D` |

The MCMC run reproduced the headline values at displayed precision in four of five cases. The outside `eta=1.0` posterior median was `1.130112` in this rerun versus `1.136426` in the first committed output; its MAP and chi-square remained the same to approximately 1e-6 and 1e-12 respectively. Coverage summary differences were below 5e-7 in the reported means/scatters. The original outputs remain unchanged at `artifacts/original/`.

The scripts streamed their progress to the terminal and wrote the two JSON files. The historical first-run logs were not copied into this folder or presented as Codex-generated logs.

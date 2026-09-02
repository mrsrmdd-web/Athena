# Artifact manifest

Created 2026-09-02 to distinguish timestamped claims from artifacts actually preserved in this repository.

## Present now

- `README.md` — result summary, limitations, provenance, reproducibility status.
- `METHODS_NOTE.md` — corrected skeptical-reader methods note.
- `ARTIFACT_MANIFEST.md` — this manifest.

## Reported by the nonlinear study but not yet committed here

- Five underlying code/output files presented during the Claude Fable 5.1 analysis.
- MCMC seed: `7`.
- Coverage seed: `11`.

These missing artifacts should be copied from the original study workspace without alteration where possible. Preserve original filenames and bytes. For each artifact, record SHA-256, byte count, original path, creation/modification timestamps if available, and a one-line role description.

## Required before claiming complete independent reproducibility

- all source/configuration files required to regenerate synthetic truth;
- exact inference configuration and priors;
- exact mismatch-family definitions;
- sampler implementation/version and run settings;
- seeds and environment/dependency lock information;
- raw outputs for control, rigid-family, flexible-family, injection ladder, and coverage runs;
- script/notebook used to derive quoted summary numbers;
- independent clean rerun instructions;
- immutable release/tag and archival DOI (e.g. Zenodo) once the package is complete.

No claim should be made that the current GitHub timestamp alone proves independent reproduction. It establishes a dated public record of the stated result and provenance; the evidentiary package becomes materially stronger when the original run artifacts are committed and archived.
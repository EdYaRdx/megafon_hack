# Canonical workflow-skill routing check

**Date:** 2026-11-13. Fresh task contexts only; no files or case artifacts were edited. Model/provider, tokens, cost, and human time are `UNKNOWN`.

## Finding and correction

The first synthetic strategy/validation routing check found that root `AGENTS.md` named workflow slugs but did not require loading the corresponding skills. It did not read any skill file. Root `AGENTS.md` was amended with a single-path-per-stage mapping to the existing canonical skills, without copying their procedures. It now labels `experiment-design` as the validation-plan stage.

## Verification

- Post-change strategy/validation task read `AGENTS.md`, listed `.agents/skills/`, then read exactly `strategy-communication/SKILL.md` and `experiment-design/SKILL.md`, as prescribed.
- It noted the term “validation” was not explicit in the workflow. Root wording was clarified to `experiment-design (validation plan)`.
- A second fresh task read the updated root route and exactly `experiment-design/SKILL.md`; it reported the validation-plan route unambiguous.
- Task traces confirm the specified reads and no edits or external actions in either smoke.

This verifies root-instruction routing in OMP task contexts only. No Cursor/Codex skill discovery or IDE execution was tested.

## Tradeoff

- **Benefit:** reduces the chance that a workflow stage runs without its canonical procedure; no duplicated skill content.
- **Cost/complexity:** one explicit `SKILL.md` read per active stage and a small path map to update if a skill is renamed; no new dependency, server, or runtime component. Token/time cost is `UNKNOWN`.
- **Test:** fresh contexts loaded the prescribed strategy, experiment-design/validation, and resume skills. This checks OMP routing only; IDE discovery remains untested.
# AGENTS.md

## Project context

This is a Databricks Asset Bundle repository named `databricks_ai`.

Important files:
- `databricks.yml`
- `resources/*.yml`
- `src/`
- `.github/workflows/`
- `skills/approvalmax-semi-self-recovery/SKILL.md`

## Recovery goal

When a Databricks or GitHub Actions workflow fails, Codex may create a draft recovery PR.

Codex must:
- read `recovery/failed_workflow.log`
- read `recovery/failure_context.json`, if present
- read `skills/approvalmax-semi-self-recovery/SKILL.md`
- create the smallest safe patch
- add a note under `docs/recovery/`

Codex must not:
- auto-merge
- disable tests
- remove quality gates
- change secrets
- print secrets
- deploy to production
- touch unrelated files

## Final rule

AI proposes.
Tests validate.
Humans approve.
CI/CD deploys.

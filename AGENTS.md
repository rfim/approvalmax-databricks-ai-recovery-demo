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
- change business keys without explicit human review
- change financial metric definitions without explicit human review

## Failure handling principle

Known, low-risk failure classes may receive a minimal draft patch.

Unknown or high-risk failures should only create diagnostic documentation under `docs/recovery/`.

## Known failure: missing_schema

If logs contain `SCHEMA_NOT_FOUND`, `schema cannot be found`, or `USE SCHEMA` failure, find the notebook or Python file that runs:

```python
spark.sql(f"USE SCHEMA {schema}")
```

Add this before it:

```python
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
```

Preserve the existing `catalog` and `schema` variables.

## Known failure: missing_tool_uv

If logs contain `uv: command not found`, add this step before Databricks bundle validate, deploy, or build in the relevant workflow:

```yaml
- name: Install uv
  run: |
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "$HOME/.local/bin" >> $GITHUB_PATH
```

## Known failure: databricks_auth_failure

If logs contain `cannot configure default credentials`, `default auth`, or missing Databricks credentials, ensure the workflow uses:

```yaml
env:
  DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
  DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
```

A safe diagnostic step is allowed:

```yaml
- name: Check Databricks auth
  run: databricks current-user me
```

Never print secrets.

## Known failure: bundle_resource_failure

If bundle validation or deployment fails because of resource configuration, review:
- `databricks.yml`
- `resources/*.yml`

Fix only the invalid resource configuration. Do not delete resources just to make validation pass.

## Unknown failure

If the failure is unknown, create only a diagnostic note under `docs/recovery/`.

## Pull request requirements

Every recovery PR must include:
- title prefixed with `[AI-DRAFT]`
- root cause hypothesis
- evidence from logs
- changed files
- validation plan
- rollback plan
- human review checklist

## Preferred validation commands

When relevant, include these commands in the PR body:

```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run sample_job -t dev
```

If dbt is involved:

```bash
dbt deps
dbt compile --target dev
dbt test --target dev
```

## Final rule

AI proposes.
Tests validate.
Humans approve.
CI/CD deploys.

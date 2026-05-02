---
name: approvalmax-semi-self-recovery
description: Use this skill when diagnosing and repairing Databricks bundle, GitHub Actions, schema, pipeline, notebook, and data quality failures in the ApprovalMax Databricks demo repository.
---

# ApprovalMax Semi Self-Recovery Skill

## Purpose

This skill guides Codex or any AI coding assistant when a Databricks or GitHub Actions workflow fails.

This is **semi self-recovery**, not autonomous production healing.

The AI may:
- diagnose the failure
- create a minimal patch
- add recovery documentation
- add diagnostics or tests where appropriate
- open a draft pull request

The AI must not:
- auto-merge
- disable tests
- remove quality gates
- change secrets
- print secrets
- deploy to production
- change business keys without explicit human review
- change financial metric definitions without explicit human review
- touch unrelated files

## Current repository structure

Use the existing `databricks_ai` project layout.

Expected files and folders:
- `databricks.yml`
- `resources/`
- `src/`
- `.github/workflows/`
- `docs/recovery/`
- `recovery/failed_workflow.log`
- `recovery/failure_context.json`

Do not invent a new repository structure unless absolutely necessary.

## General recovery rule

Before changing any files, read:
- `recovery/failed_workflow.log`
- `recovery/failure_context.json`, if present
- `AGENTS.md`, if present
- `databricks.yml`
- `resources/*.yml`
- relevant files under `src/`
- relevant files under `.github/workflows/`

Create the smallest safe patch.

Every recovery PR must include a note under `docs/recovery/` explaining:
- root cause hypothesis
- evidence from logs
- changed files
- validation plan
- rollback plan
- human review checklist

## Failure category: missing_schema

### Evidence

This category applies when logs include:
- `SCHEMA_NOT_FOUND`
- `schema cannot be found`
- `USE SCHEMA` fails

Example error:

```text
[SCHEMA_NOT_FOUND] The schema `workspace`.`engineer_support` cannot be found.
```

### Preferred fix

Find the notebook or Python file that runs:

```python
spark.sql(f"USE SCHEMA {schema}")
```

Add this before it:

```python
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
```

The final code should look like:

```python
spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"USE SCHEMA {schema}")
```

### Rules

- Preserve the existing `catalog` and `schema` variables.
- Do not hardcode production catalog or schema names.
- Keep the patch minimal.
- Add a recovery note under `docs/recovery/`.

## Failure category: missing_tool_uv

### Evidence

This category applies when logs include:

```text
uv: command not found
```

### Preferred fix

Add this step before Databricks bundle validate, deploy, or build:

```yaml
- name: Install uv
  run: |
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "$HOME/.local/bin" >> $GITHUB_PATH
```

### Rules

- Do not change application code.
- Only update the relevant GitHub Actions workflow.

## Failure category: databricks_auth_failure

### Evidence

This category applies when logs include:
- `cannot configure default credentials`
- `default auth`
- missing Databricks credentials

### Preferred fix

Ensure the workflow has:

```yaml
env:
  DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
  DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
```

Add a safe diagnostic step:

```yaml
- name: Check Databricks auth
  run: databricks current-user me
```

### Rules

- Never print secret values.
- Never echo `DATABRICKS_TOKEN`.
- Do not add credentials directly to the repository.

## Failure category: bundle_resource_failure

### Evidence

This category applies when logs include:
- `bundle validate`
- `bundle deploy`
- invalid resource configuration
- missing job or pipeline resource
- invalid `resources/*.yml`

### Preferred fix

Review and minimally fix:
- `databricks.yml`
- `resources/*.yml`

### Rules

- Keep existing resource names stable where possible.
- Do not delete resources just to make validation pass.
- Do not change production settings unless explicitly required.

## Failure category: schema_type_change

### Evidence

This category applies when logs include:
- `cannot cast`
- `type mismatch`
- incompatible column type

### Preferred fix

Use safe casting and quarantine invalid records.

Preferred actions:
- add safe cast logic
- add a quarantine model/table for invalid records
- add a dbt or SQL test
- update documentation

### Rules

- Do not silently coerce business-critical values without quarantine.
- Do not relax existing quality tests.
- Do not change financial metric definitions.

## Failure category: duplicate_or_grain_failure

### Evidence

This category applies when logs include:
- `duplicate`
- `unique`
- grain violation

### Preferred fix

Preferred actions:
- add deterministic deduplication
- add uniqueness test
- document the intended grain

### Rules

- Do not remove uniqueness tests.
- Do not hide duplicate records without preserving evidence.

## Failure category: missing_required_value

### Evidence

This category applies when logs include:
- `not_null`
- `null value`
- missing business key

### Preferred fix

Preferred actions:
- add quarantine logic
- add not-null tests
- document failure reason

### Rules

- Do not fabricate business keys.
- Do not replace missing keys with arbitrary values.

## Failure category: invalid_business_metric

### Evidence

This category applies when logs include:
- `approval_cycle_time`
- negative metric
- invalid lifecycle calculation

### Preferred fix

Preferred actions:
- add diagnostic SQL
- add data quality test
- add quarantine logic for invalid lifecycle rows
- document the issue

### Rules

- Do not redefine financial or lifecycle metrics without explicit human review.
- Do not silently drop invalid business records.

## Failure category: unknown_failure

### Evidence

Use this category when the failure does not match a known class.

### Preferred fix

Create only a diagnostic note under `docs/recovery/`.

The diagnostic note should include:
- failed workflow URL if available
- log excerpt
- suspected failure area
- recommended manual investigation steps

### Rules

- Avoid risky code changes.
- Ask for human review in the PR body.

## Pull request requirements

Every recovery PR must include:
- title prefixed with `[AI-DRAFT]`
- root cause hypothesis
- evidence from logs
- files changed
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

If dbt is involved, include:

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

# dbt Gold Models + GitHub Actions

## Goal

This package adds dbt to the existing ApprovalMax Databricks demo.

The pragmatic architecture is:

```text
CDC automation notebook
  -> Bronze
  -> Silver
  -> Raw Vault-style tables
  -> notebook-built Gold baseline

dbt workflow
  -> dbt-built Gold semantic mart
  -> dbt tests

Great Expectations workflow
  -> runs after dbt succeeds
```

## Workflow behaviour

1. `Run ApprovalMax CDC Automation` runs first when a new CDC file is merged.
2. `Run dbt Gold Models` runs after CDC succeeds.
3. `Run ApprovalMax Great Expectations` runs after dbt succeeds.

## Install

```bash
unzip ~/Downloads/approvalmax_dbt_github_action_package.zip -d .

git add dbt_project.yml \
        packages.yml \
        profiles.yml.example \
        models/sources.yml \
        models/gold/fact_approval_document_lifecycle_dbt.sql \
        models/gold/schema.yml \
        .github/workflows/run-dbt-gold.yml \
        .github/workflows/run-great-expectations.yml

git commit -m "Add dbt Gold models and GitHub Actions workflow"
git push
```

## Required GitHub secrets

```text
DATABRICKS_HOST
DATABRICKS_TOKEN
```

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install dbt-core dbt-databricks sqlfluff

export DATABRICKS_HOST="https://dbc-c2f9035e-6356.cloud.databricks.com"
export DATABRICKS_TOKEN="<your-databricks-token>"

cp profiles.yml.example profiles.yml

dbt deps --profiles-dir .
dbt debug --profiles-dir .
dbt run --select fact_approval_document_lifecycle_dbt --profiles-dir .
dbt test --select fact_approval_document_lifecycle_dbt --profiles-dir .
```

## Check result

```sql
SELECT *
FROM workspace.engineer_support_gold.fact_approval_document_lifecycle_dbt;
```

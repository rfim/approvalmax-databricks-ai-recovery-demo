# ApprovalMax CDC Automation Demo

## Goal

This package adds an ApprovalMax-style CDC automation path to the existing `databricks_ai` Databricks Asset Bundle repository.

The intended flow is:

```text
New CDC JSONL file committed under sample_data/approvalmax_cdc/
↓
GitHub Actions detects the change
↓
GitHub Actions deploys the Databricks bundle
↓
GitHub Actions runs the Databricks job approvalmax_cdc_automation
↓
Databricks builds:
  Bronze raw CDC table
  Silver stage tables
  Raw Vault-style tables
  Gold approval lifecycle mart
  Data quality checks
↓
If the job fails:
  Codex recovery workflow can create a draft PR
```

## Files in this package

Place the files into your repo using the same paths:

```text
.github/workflows/run-approvalmax-cdc-automation.yml
resources/approvalmax_cdc_jobs.yml
src/databricks_ai/load_cdc_to_bronze.py
src/databricks_ai/build_silver_stage.py
src/databricks_ai/build_data_vault.py
src/databricks_ai/build_gold_mart.py
src/databricks_ai/run_quality_checks.py
docs/approvalmax_cdc_automation.md
```

## Required sample data

Use your generated CDC mock data here:

```text
sample_data/approvalmax_cdc/
  approvalmax_cdc_all_topics.jsonl
  companies_cdc.jsonl
  users_cdc.jsonl
  subscriptions_cdc.jsonl
  finance_documents_cdc.jsonl
  approval_events_cdc.jsonl
```

The job reads all `*.jsonl` files in that folder.

## Required Databricks target

The scripts default to:

```text
catalog = workspace
schema  = engineer_support
```

The scripts create the schema automatically:

```sql
CREATE SCHEMA IF NOT EXISTS workspace.engineer_support
```

## GitHub trigger

The GitHub Action runs automatically when files under these paths change:

```text
sample_data/approvalmax_cdc/**
src/databricks_ai/**
resources/**
databricks.yml
.github/workflows/run-approvalmax-cdc-automation.yml
```

It can also be run manually from:

```text
GitHub → Actions → Run ApprovalMax CDC Automation → Run workflow
```

## Tables created

The demo creates these tables:

```text
workspace.engineer_support.bronze_approvalmax_cdc_raw

workspace.engineer_support.silver_companies_current
workspace.engineer_support.silver_users_current
workspace.engineer_support.silver_subscriptions_current
workspace.engineer_support.silver_finance_documents_current
workspace.engineer_support.silver_approval_events

workspace.engineer_support.hub_company
workspace.engineer_support.hub_finance_document
workspace.engineer_support.hub_approval_event
workspace.engineer_support.link_document_company
workspace.engineer_support.link_document_approval_event
workspace.engineer_support.sat_finance_document_status
workspace.engineer_support.sat_finance_document_amount
workspace.engineer_support.sat_approval_event_detail

workspace.engineer_support.gold_fact_approval_document_lifecycle
```

## Quality checks

The `run_quality_checks.py` script runs deterministic quality checks similar to Great Expectations expectations:

```text
- document_id must not be null
- company_id must not be null
- document_status must be accepted
- total_amount must not be negative
- approval event timestamp must not be in the future
- Gold approval cycle time must not be negative
- Gold grain must be unique
```

For a production implementation, you can replace or extend this with a real Great Expectations checkpoint. For the interview demo, the deterministic checks are faster and easier to run in a Databricks Asset Bundle.

## Safe prod push flow

Use a branch and PR first:

```bash
git checkout -b feature/approvalmax-cdc-automation

# copy files from this package into your repo

git add .github/workflows/run-approvalmax-cdc-automation.yml \
        resources/approvalmax_cdc_jobs.yml \
        src/databricks_ai/load_cdc_to_bronze.py \
        src/databricks_ai/build_silver_stage.py \
        src/databricks_ai/build_data_vault.py \
        src/databricks_ai/build_gold_mart.py \
        src/databricks_ai/run_quality_checks.py \
        docs/approvalmax_cdc_automation.md \
        sample_data/approvalmax_cdc

git commit -m "Add ApprovalMax CDC automation demo"
git push -u origin feature/approvalmax-cdc-automation
```

Then open a PR to `main`.

After review and merge, GitHub Actions will deploy and run the demo.

## Direct push to main

Only use this for a demo repo:

```bash
git add .
git commit -m "Add ApprovalMax CDC automation demo"
git push origin main
```

## Local validation

```bash
databricks bundle validate -t dev --profile vim
databricks bundle deploy -t dev --profile vim
databricks bundle run approvalmax_cdc_automation -t dev --profile vim
```

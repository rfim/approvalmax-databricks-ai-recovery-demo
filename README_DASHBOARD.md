# ApprovalMax Databricks Native Dashboard Package

## Goal

Creates dashboard-ready tables for Databricks SQL / AI-BI Dashboards.

This is the pragmatic native Databricks approach:
- Databricks job refreshes dashboard-ready Delta tables
- Databricks SQL / AI-BI Dashboard visualises those tables
- The dashboard can later be generated into a bundle resource with `databricks bundle generate dashboard`

## Files

```text
src/approvalmax_dashboard_refresh_notebook.ipynb
resources/dashboard_jobs.yml
.github/workflows/refresh-dashboard-tables.yml
docs/dashboard_queries.md
```

## Install

```bash
unzip ~/Downloads/approvalmax_databricks_native_dashboard_package.zip -d .

git add src/approvalmax_dashboard_refresh_notebook.ipynb \
        resources/dashboard_jobs.yml \
        .github/workflows/refresh-dashboard-tables.yml \
        docs/dashboard_queries.md

git commit -m "Add Databricks native dashboard refresh job"
git push
```

## Run locally

```bash
databricks bundle validate -t dev --profile vim
databricks bundle deploy -t dev --profile vim
databricks bundle run approvalmax_dashboard_refresh_serverless -t dev --profile vim
```

## Check output tables

```sql
SHOW TABLES IN workspace.engineer_support_monitoring;

SELECT *
FROM workspace.engineer_support_monitoring.dashboard_kpi_snapshot;

SELECT *
FROM workspace.engineer_support_monitoring.dashboard_layer_row_counts;

SELECT *
FROM workspace.engineer_support_monitoring.dashboard_quality_status;
```

## Workflow behaviour

The dashboard refresh workflow runs manually or after Great Expectations succeeds:

```text
CDC Automation
↓
dbt Gold Models
↓
Great Expectations
↓
Dashboard refresh tables
```

## Native dashboard

Create the dashboard in Databricks SQL / AI-BI Dashboards using the queries in:

```text
docs/dashboard_queries.md
```

Databricks supports managing AI/BI dashboards as bundle dashboard resources. For a stable demo, create the dashboard in the UI first, then optionally run:

```bash
databricks bundle generate dashboard --existing-id <dashboard-id> --profile vim
```

and deploy it with the bundle later.

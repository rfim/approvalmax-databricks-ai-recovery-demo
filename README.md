# Runnable ApprovalMax CDC Automation Job

This package gives you the runnable version that avoids the stale `Client-1 channel for REPL` error by creating a **new bundle job resource name**:

```text
approvalmax_cdc_automation_cluster
```

Use this new command:

```bash
databricks bundle run approvalmax_cdc_automation_cluster -t dev --profile vim
```

Do **not** run the old resource:

```bash
databricks bundle run approvalmax_cdc_automation -t dev --profile vim
```

The old Databricks job ID may still contain the unsupported `client: "1"` environment.

## Files included

```text
resources/approvalmax_cdc_jobs.yml
.github/workflows/run-approvalmax-cdc-automation.yml
```

## Install into repo

From repo root:

```bash
unzip ~/Downloads/approvalmax_cdc_runnable_cluster_job.zip -d .

git add resources/approvalmax_cdc_jobs.yml .github/workflows/run-approvalmax-cdc-automation.yml
git commit -m "Use runnable cluster job for ApprovalMax CDC automation"
git push
```

## Local run

```bash
databricks bundle validate -t dev --profile vim
databricks bundle deploy -t dev --profile vim --force
databricks bundle summary -t dev --profile vim
databricks bundle run approvalmax_cdc_automation_cluster -t dev --profile vim
```

## Important

If `i3.xlarge` is unavailable, list node types:

```bash
databricks clusters list-node-types --profile vim
```

Then replace this value in `resources/approvalmax_cdc_jobs.yml`:

```yaml
node_type_id: i3.xlarge
```

with an available node type.

## GitHub Action

The workflow now runs:

```bash
databricks bundle run approvalmax_cdc_automation_cluster -t dev
```

It triggers only after a newly added file under:

```text
sample_data/approvalmax_cdc/**
```

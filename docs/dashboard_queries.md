# ApprovalMax Databricks Native Dashboard Queries

Use these tables in Databricks SQL / AI-BI Dashboard.

## Dashboard source tables

```text
workspace.engineer_support_monitoring.dashboard_kpi_snapshot
workspace.engineer_support_monitoring.dashboard_layer_row_counts
workspace.engineer_support_monitoring.dashboard_pipeline_run_summary
workspace.engineer_support_monitoring.dashboard_etl_step_timeline
workspace.engineer_support_monitoring.dashboard_quality_status
workspace.engineer_support_monitoring.dashboard_gold_documents
```

## KPI cards

### Gold document count

```sql
SELECT metric_value AS gold_document_count
FROM workspace.engineer_support_monitoring.dashboard_kpi_snapshot
WHERE metric_name = 'gold_document_count';
```

### Failed expectations

```sql
SELECT metric_value AS failed_expectation_count
FROM workspace.engineer_support_monitoring.dashboard_kpi_snapshot
WHERE metric_name = 'failed_expectation_count';
```

### SLA breach count

```sql
SELECT metric_value AS sla_breach_count
FROM workspace.engineer_support_monitoring.dashboard_kpi_snapshot
WHERE metric_name = 'sla_breach_count';
```

### Average approval cycle time

```sql
SELECT metric_value AS avg_approval_cycle_minutes
FROM workspace.engineer_support_monitoring.dashboard_kpi_snapshot
WHERE metric_name = 'avg_approval_cycle_minutes';
```

## Charts

### Row counts by layer and table

```sql
SELECT layer, table_name, row_count
FROM workspace.engineer_support_monitoring.dashboard_layer_row_counts
WHERE exists_flag = 1
ORDER BY layer, table_name;
```

### Latest pipeline run status

```sql
SELECT *
FROM workspace.engineer_support_monitoring.dashboard_pipeline_run_summary
ORDER BY run_started_at DESC;
```

### ETL step duration

```sql
SELECT run_id, step_name, source_layer, target_layer, status, duration_seconds, source_row_count, target_row_count
FROM workspace.engineer_support_monitoring.dashboard_etl_step_timeline
ORDER BY started_at DESC;
```

### Great Expectations status

```sql
SELECT validation_run_id, expectation_name, status, severity, failed_row_count, checked_at
FROM workspace.engineer_support_monitoring.dashboard_quality_status
ORDER BY checked_at DESC, expectation_name;
```

### Document status distribution

```sql
SELECT document_status, COUNT(*) AS document_count
FROM workspace.engineer_support_monitoring.dashboard_gold_documents
GROUP BY document_status
ORDER BY document_count DESC;
```

### Approval cycle by document

```sql
SELECT document_id, company_name, document_type, document_status, approval_cycle_time_minutes, approval_sla_breach_flag
FROM workspace.engineer_support_monitoring.dashboard_gold_documents
ORDER BY document_id;
```

## Suggested dashboard layout

```text
Top row:
- Gold document count
- Failed expectations
- SLA breach count
- Average approval cycle minutes

Middle:
- Row counts by layer/table
- ETL step duration
- Great Expectations status

Bottom:
- Document status distribution
- Approval cycle by document
- Recent Gold documents table
```

## Native Databricks dashboard setup

1. Run the refresh job:

```bash
databricks bundle run approvalmax_dashboard_refresh_serverless -t dev --profile vim
```

2. Open Databricks SQL.
3. Create a new AI/BI Dashboard.
4. Add datasets from the `workspace.engineer_support_monitoring.dashboard_*` tables.
5. Add the SQL queries above as visualisations.

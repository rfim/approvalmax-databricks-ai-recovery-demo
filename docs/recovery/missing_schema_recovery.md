# Missing Schema Recovery

## Root cause

The Databricks job failed because it ran `USE SCHEMA` before ensuring the target schema existed.

## Fix

Added an idempotent schema creation statement before `USE SCHEMA`:

```python
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"USE SCHEMA {schema}")
```

## Validation

```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run sample_job -t dev
```

## Human review checklist

- [ ] Confirm catalog/schema variables are correct
- [ ] Confirm no production catalog is affected
- [ ] Confirm sample_job succeeds after merge

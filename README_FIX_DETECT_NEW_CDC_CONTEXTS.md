# Fix Detect New CDC Contexts Workflow

## Root cause

The workflow used:

```bash
python scripts/detect_new_cdc_contexts.py
exit_code=$?
```

but GitHub Actions runs bash with `-e`, so when the Python script exited with code `10`, the step stopped immediately before setting:

```text
has_new_contexts=true
```

That caused later steps to think there were no new contexts.

## Fix

This version uses:

```bash
set +e
python scripts/detect_new_cdc_contexts.py
exit_code=$?
set -e
```

so exit code `10` is captured and converted into:

```text
has_new_contexts=true
```

## Also improved

The detector now infers better business keys:

```text
audit_policies     -> audit_policy_id
expense_claims     -> expense_claim_id
vendor_contracts   -> vendor_contract_id
payment_batches    -> payment_batch_id
budgets            -> budget_id
```

instead of defaulting too early to `company_id`.

## Install

```bash
unzip ~/Downloads/fix_detect_new_cdc_contexts_workflow.zip -d .

git add .github/workflows/detect-new-cdc-contexts.yml \
        scripts/detect_new_cdc_contexts.py

git commit -m "Fix new CDC context detection workflow"
git push
```

## Test

Re-run the new context test by adding a fresh CDC file under:

```text
sample_data/approvalmax_cdc/
```

Expected workflow output:

```text
New contexts: [...]
has_new_contexts=true
PR created:
[AI-DRAFT] Add candidate modelling for new CDC contexts
```

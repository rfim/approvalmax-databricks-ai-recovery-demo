# Detect New CDC Contexts + Create PR

## What this adds

This package adds automatic detection of new CDC source_table contexts.

Flow:

```text
New CDC JSONL file merged to main
↓
Detect New CDC Contexts workflow runs
↓
If all contexts are already supported:
  no PR
↓
If new context exists:
  Codex attempts modelling PR
  fallback updates metadata and docs
  PR is created for human review
```

## Files

```text
metadata/supported_cdc_contexts.yml
scripts/detect_new_cdc_contexts.py
.github/workflows/detect-new-cdc-contexts.yml
```

## Install

```bash
unzip ~/Downloads/approvalmax_detect_new_cdc_context_package.zip -d .

git add metadata/supported_cdc_contexts.yml \
        scripts/detect_new_cdc_contexts.py \
        .github/workflows/detect-new-cdc-contexts.yml

git commit -m "Add new CDC context detection workflow"
git push
```

## Test

Add a CDC file containing a new source_table, for example:

```json
{"source_table": "payments", ...}
```

Merge to main.

Expected result:

```text
Detect New CDC Contexts
↓
New context found
↓
PR created:
[AI-DRAFT] Add candidate modelling for new CDC contexts
```

## Safety

The workflow does not silently change production modelling. It creates a PR.

Human review is required for:
- business key
- grain
- Gold table promotion
- quality checks
- metric definitions

#!/usr/bin/env python3
"""
detect_new_cdc_contexts.py

Detects new ApprovalMax-style CDC source_table contexts under sample_data/approvalmax_cdc.

Exit codes:
- 0  = no new contexts
- 10 = new contexts found
- >0 = detector error
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Missing PyYAML. Install with: pip install pyyaml") from exc


CDC_DIR = Path("sample_data/approvalmax_cdc")
REGISTRY_PATH = Path("metadata/supported_cdc_contexts.yml")
OUTPUT_PATH = Path("recovery/new_cdc_contexts.json")


def singularize(context: str) -> str:
    if context.endswith("ies"):
        return context[:-3] + "y"
    if context.endswith("ses"):
        return context[:-2]
    if context.endswith("s"):
        return context[:-1]
    return context


def load_supported_contexts() -> dict:
    if not REGISTRY_PATH.exists():
        return {"supported_contexts": {}}
    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"supported_contexts": {}}


def iter_cdc_records():
    seen_contexts: set[str] = set()
    samples_by_context: dict[str, list[dict]] = defaultdict(list)
    files_by_context: dict[str, list[str]] = defaultdict(list)

    if not CDC_DIR.exists():
        return seen_contexts, samples_by_context, files_by_context

    for path in sorted(CDC_DIR.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON in {path}:{line_number}: {exc}") from exc

                source_table = record.get("source_table")
                if not source_table:
                    continue

                seen_contexts.add(source_table)
                if len(samples_by_context[source_table]) < 3:
                    samples_by_context[source_table].append(record)
                if str(path) not in files_by_context[source_table]:
                    files_by_context[source_table].append(str(path))

    return seen_contexts, samples_by_context, files_by_context


def infer_business_key(context: str, sample_record: dict) -> str | None:
    after = sample_record.get("after") or {}
    primary_key = sample_record.get("primary_key") or {}
    singular = singularize(context)

    # Prefer context-specific key first, e.g. audit_policies -> audit_policy_id
    context_specific = f"{singular}_id"
    if context_specific in primary_key or context_specific in after:
        return context_specific

    # Then prefer any non-company *_id in primary_key.
    for key in primary_key.keys():
        if key.endswith("_id") and key != "company_id":
            return key

    # Then any non-company *_id in payload.
    for key in after.keys():
        if key.endswith("_id") and key != "company_id":
            return key

    # Fallback to company_id only if it is the only key.
    if "company_id" in primary_key or "company_id" in after:
        return "company_id"

    return None


def main() -> int:
    registry = load_supported_contexts()
    supported_contexts = registry.get("supported_contexts", {}) or {}
    supported_context_names = set(supported_contexts.keys())

    seen_contexts, samples_by_context, files_by_context = iter_cdc_records()
    new_contexts = sorted(seen_contexts - supported_context_names)

    inferred = {}
    for context in new_contexts:
        sample = samples_by_context[context][0] if samples_by_context[context] else {}
        business_key = infer_business_key(context, sample)
        singular = singularize(context)

        inferred[context] = {
            "candidate_business_key": business_key,
            "candidate_silver_table": f"{context}_current",
            "candidate_gold_tables": [
                f"dim_{singular}",
            ],
            "human_review_required": True,
            "files": files_by_context.get(context, []),
            "sample_records": samples_by_context.get(context, []),
        }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "seen_contexts": sorted(seen_contexts),
                "supported_contexts": sorted(supported_context_names),
                "new_contexts": new_contexts,
                "inferred": inferred,
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    print(f"Seen contexts: {sorted(seen_contexts)}")
    print(f"Supported contexts: {sorted(supported_context_names)}")
    print(f"New contexts: {new_contexts}")
    print(f"Wrote: {OUTPUT_PATH}")

    if new_contexts:
        return 10
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
detect_new_cdc_contexts.py

Detects new ApprovalMax-style CDC source_table contexts under sample_data/approvalmax_cdc.

This script is intended for GitHub Actions. It:
1. Reads all JSONL files under sample_data/approvalmax_cdc
2. Extracts unique source_table values
3. Compares them against metadata/supported_cdc_contexts.yml
4. Writes recovery/new_cdc_contexts.json
5. Exits with code 10 if new contexts exist
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


def load_supported_contexts() -> dict:
    if not REGISTRY_PATH.exists():
        return {"supported_contexts": {}}

    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        payload = yaml.safe_load(f) or {}

    return payload


def iter_cdc_records() -> tuple[set[str], dict[str, list[dict]], dict[str, list[str]]]:
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


def infer_business_key(sample_record: dict) -> str | None:
    after = sample_record.get("after") or {}
    primary_key = sample_record.get("primary_key") or {}

    for candidate in [
        "supplier_id",
        "payment_id",
        "payment_batch_id",
        "line_item_id",
        "document_id",
        "company_id",
        "event_id",
        "workflow_id",
        "subscription_id",
        "user_id",
    ]:
        if candidate in primary_key or candidate in after:
            return candidate

    for key in after.keys():
        if key.endswith("_id"):
            return key

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
        business_key = infer_business_key(sample)
        inferred[context] = {
            "candidate_business_key": business_key,
            "candidate_silver_table": f"{context}_current",
            "candidate_gold_tables": [
                f"dim_{context[:-1] if context.endswith('s') else context}",
            ],
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

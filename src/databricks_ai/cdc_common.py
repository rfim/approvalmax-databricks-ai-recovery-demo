
from pathlib import Path
from typing import Iterable

CATALOG = "workspace"
SCHEMA = "engineer_support"


def ensure_schema(spark, catalog: str = CATALOG, schema: str = SCHEMA) -> None:
    spark.sql(f"USE CATALOG {catalog}")
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
    spark.sql(f"USE SCHEMA {schema}")


def table(name: str, catalog: str = CATALOG, schema: str = SCHEMA) -> str:
    return f"{catalog}.{schema}.{name}"


def repo_root() -> Path:
    # Bundle files are typically deployed under:
    # /Workspace/Users/<user>/.bundle/<bundle>/<target>/files/
    # This script is in files/src/databricks_ai/*.py
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "sample_data").exists() or (parent / "databricks.yml").exists():
            return parent
    # Fallback for Databricks bundle layout
    return current.parents[2]


def read_jsonl_files(paths: Iterable[Path]) -> list[str]:
    records: list[str] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(line)
    return records

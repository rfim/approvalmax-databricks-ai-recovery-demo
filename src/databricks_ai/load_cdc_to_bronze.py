from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, lit

from databricks_ai.cdc_common import CATALOG, SCHEMA, ensure_schema, repo_root, read_jsonl_files, table


def main() -> None:
    spark = SparkSession.builder.getOrCreate()
    ensure_schema(spark)

    data_dir = repo_root() / "sample_data" / "approvalmax_cdc"

    jsonl_files = sorted(data_dir.glob("*.jsonl"))
    if not jsonl_files:
        raise FileNotFoundError(f"No CDC JSONL files found under {data_dir}")

    raw_json_records = read_jsonl_files(jsonl_files)
    if not raw_json_records:
        raise ValueError(f"CDC JSONL files exist but contain no records under {data_dir}")

    # Read JSON from in-memory strings to keep demo independent of DBFS/Volumes path setup.
    raw_df = spark.read.json(spark.sparkContext.parallelize(raw_json_records))

    df = (
        raw_df
        .withColumn("_loaded_at", current_timestamp())
        .withColumn("_demo_catalog", lit(CATALOG))
        .withColumn("_demo_schema", lit(SCHEMA))
    )

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table("bronze_approvalmax_cdc_raw"))
    )

    print(f"Loaded {df.count()} CDC records into {table('bronze_approvalmax_cdc_raw')}")


if __name__ == "__main__":
    main()

from pyspark.sql import SparkSession

from databricks_ai.cdc_common import ensure_schema


QUALITY_CHECKS = {
    "silver_finance_documents_document_id_not_null": """
        SELECT * FROM silver_finance_documents_current
        WHERE document_id IS NULL
    """,
    "silver_finance_documents_company_id_not_null": """
        SELECT * FROM silver_finance_documents_current
        WHERE company_id IS NULL
    """,
    "silver_finance_documents_status_accepted_values": """
        SELECT * FROM silver_finance_documents_current
        WHERE document_status NOT IN ('draft', 'submitted', 'approved', 'rejected', 'paid', 'cancelled')
           OR document_status IS NULL
    """,
    "silver_finance_documents_total_amount_non_negative": """
        SELECT * FROM silver_finance_documents_current
        WHERE total_amount < 0
    """,
    "silver_approval_events_timestamp_not_future": """
        SELECT * FROM silver_approval_events
        WHERE approval_event_timestamp > current_timestamp()
    """,
    "gold_approval_cycle_time_non_negative": """
        SELECT * FROM gold_fact_approval_document_lifecycle
        WHERE approval_cycle_time_minutes < 0
    """,
    "gold_grain_unique": """
        SELECT document_id, COUNT(*) AS row_count
        FROM gold_fact_approval_document_lifecycle
        GROUP BY document_id
        HAVING COUNT(*) > 1
    """,
}


def main() -> None:
    spark = SparkSession.builder.getOrCreate()
    ensure_schema(spark)

    failures = []

    for check_name, query in QUALITY_CHECKS.items():
        failed_df = spark.sql(query)
        failed_count = failed_df.count()

        print(f"{check_name}: {failed_count} failing rows")

        if failed_count > 0:
            quarantine_table = f"quarantine_{check_name}"
            failed_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(quarantine_table)
            failures.append((check_name, failed_count, quarantine_table))

    if failures:
        message = "\\n".join(
            [f"{name}: {count} rows, saved to {table}" for name, count, table in failures]
        )
        raise Exception(f"Data quality checks failed:\\n{message}")

    print("All data quality checks passed.")


if __name__ == "__main__":
    main()

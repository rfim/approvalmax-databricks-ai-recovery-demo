from pyspark.sql import SparkSession

from databricks_ai.cdc_common import ensure_schema


def main() -> None:
    spark = SparkSession.builder.getOrCreate()
    ensure_schema(spark)

    spark.sql(
        """
        CREATE OR REPLACE TABLE gold_fact_approval_document_lifecycle AS
        WITH base AS (
          SELECT
            d.document_id,
            d.company_id,
            c.company_name,
            s.plan_name,
            d.document_type,
            d.document_status,
            d.supplier_id,
            d.supplier_name,
            d.total_amount,
            d.currency,
            d.created_at,
            d.submitted_at,
            d.approved_at,
            d.rejected_at,
            d.paid_at,
            d.updated_at,
            d.approval_deadline_at
          FROM silver_finance_documents_current d
          LEFT JOIN silver_companies_current c
            ON d.company_id = c.company_id
          LEFT JOIN silver_subscriptions_current s
            ON d.company_id = s.company_id
        )
        SELECT
          document_id,
          company_id,
          company_name,
          plan_name,
          document_type,
          document_status,
          supplier_id,
          supplier_name,
          total_amount,
          currency,
          created_at,
          submitted_at,
          approved_at,
          rejected_at,
          paid_at,
          updated_at,
          approval_deadline_at,
          CASE
            WHEN submitted_at IS NOT NULL AND approved_at IS NOT NULL
            THEN timestampdiff(MINUTE, submitted_at, approved_at)
          END AS approval_cycle_time_minutes,
          CASE
            WHEN approval_deadline_at IS NOT NULL
             AND approved_at IS NOT NULL
             AND approved_at > approval_deadline_at
            THEN 1
            ELSE 0
          END AS approval_sla_breach_flag
        FROM base
        """
    )

    print("Built Gold approval lifecycle mart.")


if __name__ == "__main__":
    main()

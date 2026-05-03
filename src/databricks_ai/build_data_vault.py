from pyspark.sql import SparkSession

from databricks_ai.cdc_common import ensure_schema


def main() -> None:
    spark = SparkSession.builder.getOrCreate()
    ensure_schema(spark)

    statements = [
        """
        CREATE OR REPLACE TABLE hub_company AS
        SELECT DISTINCT
          sha2(company_id, 256) AS company_hk,
          company_id AS company_bk,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_companies_current
        WHERE company_id IS NOT NULL
        """,
        """
        CREATE OR REPLACE TABLE hub_finance_document AS
        SELECT DISTINCT
          sha2(document_id, 256) AS finance_document_hk,
          document_id AS finance_document_bk,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_finance_documents_current
        WHERE document_id IS NOT NULL
        """,
        """
        CREATE OR REPLACE TABLE hub_approval_event AS
        SELECT DISTINCT
          sha2(event_id, 256) AS approval_event_hk,
          event_id AS approval_event_bk,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_approval_events
        WHERE event_id IS NOT NULL
        """,
        """
        CREATE OR REPLACE TABLE link_document_company AS
        SELECT DISTINCT
          sha2(concat_ws('||', document_id, company_id), 256) AS document_company_hk,
          sha2(document_id, 256) AS finance_document_hk,
          sha2(company_id, 256) AS company_hk,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_finance_documents_current
        WHERE document_id IS NOT NULL
          AND company_id IS NOT NULL
        """,
        """
        CREATE OR REPLACE TABLE link_document_approval_event AS
        SELECT DISTINCT
          sha2(concat_ws('||', document_id, event_id), 256) AS document_approval_event_hk,
          sha2(document_id, 256) AS finance_document_hk,
          sha2(event_id, 256) AS approval_event_hk,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_approval_events
        WHERE document_id IS NOT NULL
          AND event_id IS NOT NULL
        """,
        """
        CREATE OR REPLACE TABLE sat_finance_document_status AS
        SELECT
          sha2(document_id, 256) AS finance_document_hk,
          document_status,
          document_type,
          supplier_id,
          supplier_name,
          created_at,
          submitted_at,
          approved_at,
          rejected_at,
          paid_at,
          updated_at,
          approval_deadline_at,
          sha2(concat_ws('||',
            coalesce(document_status, ''),
            coalesce(document_type, ''),
            coalesce(cast(created_at as string), ''),
            coalesce(cast(submitted_at as string), ''),
            coalesce(cast(approved_at as string), ''),
            coalesce(cast(rejected_at as string), ''),
            coalesce(cast(paid_at as string), ''),
            coalesce(cast(updated_at as string), ''),
            coalesce(cast(approval_deadline_at as string), '')
          ), 256) AS hashdiff,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_finance_documents_current
        WHERE document_id IS NOT NULL
        """,
        """
        CREATE OR REPLACE TABLE sat_finance_document_amount AS
        SELECT
          sha2(document_id, 256) AS finance_document_hk,
          total_amount,
          currency,
          sha2(concat_ws('||',
            coalesce(cast(total_amount as string), ''),
            coalesce(currency, '')
          ), 256) AS hashdiff,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_finance_documents_current
        WHERE document_id IS NOT NULL
        """,
        """
        CREATE OR REPLACE TABLE sat_approval_event_detail AS
        SELECT
          sha2(event_id, 256) AS approval_event_hk,
          workflow_id,
          document_id,
          company_id,
          approver_user_id,
          event_type,
          approval_event_timestamp,
          sha2(concat_ws('||',
            coalesce(workflow_id, ''),
            coalesce(document_id, ''),
            coalesce(company_id, ''),
            coalesce(approver_user_id, ''),
            coalesce(event_type, ''),
            coalesce(cast(approval_event_timestamp as string), '')
          ), 256) AS hashdiff,
          current_timestamp() AS load_datetime,
          record_source
        FROM silver_approval_events
        WHERE event_id IS NOT NULL
        """,
    ]

    for statement in statements:
        spark.sql(statement)

    print("Built Raw Vault-style tables.")


if __name__ == "__main__":
    main()

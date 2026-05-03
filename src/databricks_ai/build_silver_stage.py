from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from databricks_ai.cdc_common import ensure_schema, table


def latest_by_key(df, key_col: str):
    w = Window.partitionBy(key_col).orderBy(F.col("sequence_id").desc(), F.col("ingestion_timestamp").desc())
    return (
        df.withColumn("_rn", F.row_number().over(w))
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )


def main() -> None:
    spark = SparkSession.builder.getOrCreate()
    ensure_schema(spark)

    bronze = spark.table(table("bronze_approvalmax_cdc_raw"))

    # Companies
    companies = (
        bronze
        .filter((F.col("source_table") == "companies") & (F.col("op") != "d"))
        .select(
            F.col("after.company_id").alias("company_id"),
            F.col("after.company_name").alias("company_name"),
            F.col("after.country").alias("country"),
            F.col("after.base_currency").alias("base_currency"),
            F.col("after.status").alias("company_status"),
            F.col("after.created_at").cast("timestamp").alias("created_at"),
            F.col("after.updated_at").cast("timestamp").alias("updated_at"),
            F.col("sequence_id"),
            F.col("event_timestamp").cast("timestamp").alias("event_timestamp"),
            F.col("source_system").alias("record_source"),
        )
    )
    companies = latest_by_key(companies, "company_id")
    companies.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("silver_companies_current"))

    # Users
    users = (
        bronze
        .filter((F.col("source_table") == "users") & (F.col("op") != "d"))
        .select(
            F.col("after.user_id").alias("user_id"),
            F.col("after.company_id").alias("company_id"),
            F.col("after.full_name").alias("full_name"),
            F.col("after.email").alias("email"),
            F.col("after.role").alias("role"),
            F.col("after.is_active").cast("boolean").alias("is_active"),
            F.col("sequence_id"),
            F.col("event_timestamp").cast("timestamp").alias("event_timestamp"),
            F.col("source_system").alias("record_source"),
        )
    )
    users = latest_by_key(users, "user_id")
    users.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("silver_users_current"))

    # Subscriptions
    subscriptions = (
        bronze
        .filter((F.col("source_table") == "subscriptions") & (F.col("op") != "d"))
        .select(
            F.col("after.subscription_id").alias("subscription_id"),
            F.col("after.company_id").alias("company_id"),
            F.col("after.plan_name").alias("plan_name"),
            F.col("after.mrr").cast("decimal(18,2)").alias("mrr"),
            F.col("after.status").alias("subscription_status"),
            F.col("after.started_at").cast("timestamp").alias("started_at"),
            F.col("after.cancelled_at").cast("timestamp").alias("cancelled_at"),
            F.col("sequence_id"),
            F.col("event_timestamp").cast("timestamp").alias("event_timestamp"),
            F.col("source_system").alias("record_source"),
        )
    )
    subscriptions = latest_by_key(subscriptions, "subscription_id")
    subscriptions.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("silver_subscriptions_current"))

    # Finance documents
    docs = (
        bronze
        .filter((F.col("source_table") == "finance_documents") & (F.col("op") != "d"))
        .select(
            F.col("after.document_id").alias("document_id"),
            F.col("after.company_id").alias("company_id"),
            F.col("after.document_type").alias("document_type"),
            F.col("after.document_status").alias("document_status"),
            F.col("after.supplier_id").alias("supplier_id"),
            F.col("after.supplier_name").alias("supplier_name"),
            F.col("after.total_amount").cast("decimal(18,2)").alias("total_amount"),
            F.col("after.currency").alias("currency"),
            F.col("after.created_at").cast("timestamp").alias("created_at"),
            F.col("after.submitted_at").cast("timestamp").alias("submitted_at"),
            F.col("after.approved_at").cast("timestamp").alias("approved_at"),
            F.col("after.rejected_at").cast("timestamp").alias("rejected_at"),
            F.col("after.paid_at").cast("timestamp").alias("paid_at"),
            F.col("after.updated_at").cast("timestamp").alias("updated_at"),
            F.col("after.approval_deadline_at").cast("timestamp").alias("approval_deadline_at"),
            F.col("sequence_id"),
            F.col("event_timestamp").cast("timestamp").alias("event_timestamp"),
            F.col("source_system").alias("record_source"),
        )
    )
    docs = latest_by_key(docs, "document_id")
    docs.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("silver_finance_documents_current"))

    # Approval events are append-only events; preserve all except duplicate CDC envelopes.
    events = (
        bronze
        .filter((F.col("source_table") == "approval_events") & (F.col("op") != "d"))
        .select(
            F.col("after.event_id").alias("event_id"),
            F.col("after.document_id").alias("document_id"),
            F.col("after.workflow_id").alias("workflow_id"),
            F.col("after.company_id").alias("company_id"),
            F.col("after.approver_user_id").alias("approver_user_id"),
            F.col("after.event_type").alias("event_type"),
            F.col("after.event_timestamp").cast("timestamp").alias("approval_event_timestamp"),
            F.col("sequence_id"),
            F.col("event_timestamp").cast("timestamp").alias("cdc_event_timestamp"),
            F.col("source_system").alias("record_source"),
        )
    )
    events = latest_by_key(events, "event_id")
    events.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(table("silver_approval_events"))

    print("Built Silver/Stage tables.")


if __name__ == "__main__":
    main()

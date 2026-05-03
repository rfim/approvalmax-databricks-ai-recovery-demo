# New CDC Contexts Detected

The detector found new CDC `source_table` values that are not yet fully modelled.

```json
[
  "audit_policies",
  "budgets",
  "expense_claims",
  "payment_batches",
  "payments",
  "suppliers",
  "vendor_contracts"
]
```

## Candidate modelling changes

{
  "audit_policies": {
    "candidate_business_key": "audit_policy_id",
    "candidate_silver_table": "audit_policies_current",
    "candidate_gold_tables": [
      "dim_audit_policy"
    ],
    "human_review_required": true,
    "files": [
      "sample_data/approvalmax_cdc/approvalmax_cdc_new_context_pr_test_v2.jsonl",
      "sample_data/approvalmax_cdc/approvalmax_cdc_new_context_pr_test_v3.jsonl"
    ],
    "sample_records": [
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "audit_policies",
        "op": "c",
        "sequence_id": 920004,
        "event_timestamp": "2026-05-02T22:51:44Z",
        "ingestion_timestamp": "2026-05-02T22:52:04Z",
        "primary_key": {
          "company_id": "COMP-CTX-V2-001",
          "audit_policy_id": "AUD-CTX-V2-001"
        },
        "before": null,
        "after": {
          "audit_policy_id": "AUD-CTX-V2-001",
          "company_id": "COMP-CTX-V2-001",
          "policy_name": "Dual Approval Policy",
          "policy_status": "enabled",
          "minimum_approvers": 2,
          "threshold_amount": 1000.0,
          "currency": "GBP",
          "created_at": "2026-05-02T20:41:44Z",
          "updated_at": "2026-05-02T20:41:44Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 920004,
          "tx_id": "TX-092000",
          "is_snapshot": false,
          "note": "new_context_audit_policies"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "audit_policies",
        "op": "c",
        "sequence_id": 920004,
        "event_timestamp": "2026-05-02T22:51:44Z",
        "ingestion_timestamp": "2026-05-02T22:52:04Z",
        "primary_key": {
          "company_id": "COMP-CTX-V2-001",
          "audit_policy_id": "AUD-CTX-V2-001"
        },
        "before": null,
        "after": {
          "audit_policy_id": "AUD-CTX-V2-001",
          "company_id": "COMP-CTX-V2-001",
          "policy_name": "Dual Approval Policy",
          "policy_status": "enabled",
          "minimum_approvers": 2,
          "threshold_amount": 1000.0,
          "currency": "GBP",
          "created_at": "2026-05-02T20:41:44Z",
          "updated_at": "2026-05-02T20:41:44Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 920004,
          "tx_id": "TX-092000",
          "is_snapshot": false,
          "note": "new_context_audit_policies"
        }
      }
    ]
  },
  "budgets": {
    "candidate_business_key": "budget_id",
    "candidate_silver_table": "budgets_current",
    "candidate_gold_tables": [
      "dim_budget"
    ],
    "human_review_required": true,
    "files": [
      "sample_data/approvalmax_cdc/approvalmax_cdc_3_new_contexts_payments_batches_budgets.jsonl"
    ],
    "sample_records": [
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "budgets",
        "op": "c",
        "sequence_id": 910007,
        "event_timestamp": "2026-05-01T19:29:52Z",
        "ingestion_timestamp": "2026-05-01T19:30:12Z",
        "primary_key": {
          "company_id": "COMP-NEWCTX-001",
          "budget_id": "BUD-NEWCTX-001"
        },
        "before": null,
        "after": {
          "budget_id": "BUD-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "budget_name": "Marketing Q2 Budget",
          "budget_period": "2026-Q2",
          "budget_status": "active",
          "budget_amount": 25000.0,
          "spent_amount": 0.0,
          "remaining_amount": 25000.0,
          "currency": "GBP",
          "owner_user_id": "USR-NEWCTX-002",
          "created_at": "2026-05-01T19:29:52Z",
          "updated_at": "2026-05-01T19:29:52Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 910007,
          "tx_id": "TX-091000",
          "is_snapshot": false,
          "note": "new_context_budgets_create"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "budgets",
        "op": "u",
        "sequence_id": 910008,
        "event_timestamp": "2026-05-04T21:59:52Z",
        "ingestion_timestamp": "2026-05-04T22:00:12Z",
        "primary_key": {
          "company_id": "COMP-NEWCTX-001",
          "budget_id": "BUD-NEWCTX-001"
        },
        "before": {
          "budget_id": "BUD-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "budget_name": "Marketing Q2 Budget",
          "budget_period": "2026-Q2",
          "budget_status": "active",
          "budget_amount": 25000.0,
          "spent_amount": 0.0,
          "remaining_amount": 25000.0,
          "currency": "GBP",
          "owner_user_id": "USR-NEWCTX-002",
          "created_at": "2026-05-01T19:29:52Z",
          "updated_at": "2026-05-01T19:29:52Z"
        },
        "after": {
          "budget_id": "BUD-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "budget_name": "Marketing Q2 Budget",
          "budget_period": "2026-Q2",
          "budget_status": "active",
          "budget_amount": 25000.0,
          "spent_amount": 1840.25,
          "remaining_amount": 23159.75,
          "currency": "GBP",
          "owner_user_id": "USR-NEWCTX-002",
          "created_at": "2026-05-01T19:29:52Z",
          "updated_at": "2026-05-04T21:59:52Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 910008,
          "tx_id": "TX-091000",
          "is_snapshot": false,
          "note": "new_context_budgets_spent_update"
        }
      }
    ]
  },
  "expense_claims": {
    "candidate_business_key": "expense_claim_id",
    "candidate_silver_table": "expense_claims_current",
    "candidate_gold_tables": [
      "dim_expense_claim"
    ],
    "human_review_required": true,
    "files": [
      "sample_data/approvalmax_cdc/approvalmax_cdc_new_context_pr_test_v2.jsonl",
      "sample_data/approvalmax_cdc/approvalmax_cdc_new_context_pr_test_v3.jsonl"
    ],
    "sample_records": [
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "expense_claims",
        "op": "c",
        "sequence_id": 920002,
        "event_timestamp": "2026-05-02T20:51:44Z",
        "ingestion_timestamp": "2026-05-02T20:52:04Z",
        "primary_key": {
          "company_id": "COMP-CTX-V2-001",
          "expense_claim_id": "EXP-CTX-V2-001",
          "user_id": "USR-CTX-V2-001"
        },
        "before": null,
        "after": {
          "expense_claim_id": "EXP-CTX-V2-001",
          "company_id": "COMP-CTX-V2-001",
          "user_id": "USR-CTX-V2-001",
          "claim_status": "submitted",
          "claim_category": "travel",
          "claim_amount": 124.5,
          "currency": "GBP",
          "submitted_at": "2026-05-02T20:51:44Z",
          "approved_at": null,
          "created_at": "2026-05-02T20:21:44Z",
          "updated_at": "2026-05-02T20:51:44Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 920002,
          "tx_id": "TX-092000",
          "is_snapshot": false,
          "note": "new_context_expense_claims"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "expense_claims",
        "op": "c",
        "sequence_id": 920002,
        "event_timestamp": "2026-05-02T20:51:44Z",
        "ingestion_timestamp": "2026-05-02T20:52:04Z",
        "primary_key": {
          "company_id": "COMP-CTX-V2-001",
          "expense_claim_id": "EXP-CTX-V2-001",
          "user_id": "USR-CTX-V2-001"
        },
        "before": null,
        "after": {
          "expense_claim_id": "EXP-CTX-V2-001",
          "company_id": "COMP-CTX-V2-001",
          "user_id": "USR-CTX-V2-001",
          "claim_status": "submitted",
          "claim_category": "travel",
          "claim_amount": 124.5,
          "currency": "GBP",
          "submitted_at": "2026-05-02T20:51:44Z",
          "approved_at": null,
          "created_at": "2026-05-02T20:21:44Z",
          "updated_at": "2026-05-02T20:51:44Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 920002,
          "tx_id": "TX-092000",
          "is_snapshot": false,
          "note": "new_context_expense_claims"
        }
      }
    ]
  },
  "payment_batches": {
    "candidate_business_key": "payment_batch_id",
    "candidate_silver_table": "payment_batches_current",
    "candidate_gold_tables": [
      "dim_payment_batche"
    ],
    "human_review_required": true,
    "files": [
      "sample_data/approvalmax_cdc/approvalmax_cdc_3_new_contexts_payments_batches_budgets.jsonl"
    ],
    "sample_records": [
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "payment_batches",
        "op": "c",
        "sequence_id": 910004,
        "event_timestamp": "2026-05-01T20:59:52Z",
        "ingestion_timestamp": "2026-05-01T21:00:12Z",
        "primary_key": {
          "company_id": "COMP-NEWCTX-001",
          "payment_batch_id": "PB-NEWCTX-001"
        },
        "before": null,
        "after": {
          "payment_batch_id": "PB-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "batch_reference": "BATCH-MAY-001",
          "batch_status": "created",
          "payment_count": 1,
          "total_amount": 1840.25,
          "currency": "GBP",
          "created_by_user_id": "USR-NEWCTX-001",
          "submitted_at": null,
          "approved_at": null,
          "created_at": "2026-05-01T20:59:52Z",
          "updated_at": "2026-05-01T20:59:52Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 910004,
          "tx_id": "TX-091000",
          "is_snapshot": false,
          "note": "new_context_payment_batches_create"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "payment_batches",
        "op": "u",
        "sequence_id": 910005,
        "event_timestamp": "2026-05-01T21:59:52Z",
        "ingestion_timestamp": "2026-05-01T22:00:12Z",
        "primary_key": {
          "company_id": "COMP-NEWCTX-001",
          "payment_batch_id": "PB-NEWCTX-001"
        },
        "before": {
          "payment_batch_id": "PB-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "batch_reference": "BATCH-MAY-001",
          "batch_status": "created",
          "payment_count": 1,
          "total_amount": 1840.25,
          "currency": "GBP",
          "created_by_user_id": "USR-NEWCTX-001",
          "submitted_at": null,
          "approved_at": null,
          "created_at": "2026-05-01T20:59:52Z",
          "updated_at": "2026-05-01T20:59:52Z"
        },
        "after": {
          "payment_batch_id": "PB-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "batch_reference": "BATCH-MAY-001",
          "batch_status": "submitted",
          "payment_count": 1,
          "total_amount": 1840.25,
          "currency": "GBP",
          "created_by_user_id": "USR-NEWCTX-001",
          "submitted_at": "2026-05-01T21:59:52Z",
          "approved_at": null,
          "created_at": "2026-05-01T20:59:52Z",
          "updated_at": "2026-05-01T21:59:52Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 910005,
          "tx_id": "TX-091000",
          "is_snapshot": false,
          "note": "new_context_payment_batches_submitted"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "payment_batches",
        "op": "u",
        "sequence_id": 910006,
        "event_timestamp": "2026-05-02T00:59:52Z",
        "ingestion_timestamp": "2026-05-02T01:00:12Z",
        "primary_key": {
          "company_id": "COMP-NEWCTX-001",
          "payment_batch_id": "PB-NEWCTX-001"
        },
        "before": {
          "payment_batch_id": "PB-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "batch_reference": "BATCH-MAY-001",
          "batch_status": "submitted",
          "payment_count": 1,
          "total_amount": 1840.25,
          "currency": "GBP",
          "created_by_user_id": "USR-NEWCTX-001",
          "submitted_at": "2026-05-01T21:59:52Z",
          "approved_at": null,
          "created_at": "2026-05-01T20:59:52Z",
          "updated_at": "2026-05-01T21:59:52Z"
        },
        "after": {
          "payment_batch_id": "PB-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "batch_reference": "BATCH-MAY-001",
          "batch_status": "approved",
          "payment_count": 1,
          "total_amount": 1840.25,
          "currency": "GBP",
          "created_by_user_id": "USR-NEWCTX-001",
          "submitted_at": "2026-05-01T21:59:52Z",
          "approved_at": "2026-05-02T00:59:52Z",
          "created_at": "2026-05-01T20:59:52Z",
          "updated_at": "2026-05-02T00:59:52Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 910006,
          "tx_id": "TX-091000",
          "is_snapshot": false,
          "note": "new_context_payment_batches_approved"
        }
      }
    ]
  },
  "payments": {
    "candidate_business_key": "payment_id",
    "candidate_silver_table": "payments_current",
    "candidate_gold_tables": [
      "dim_payment"
    ],
    "human_review_required": true,
    "files": [
      "sample_data/approvalmax_cdc/approvalmax_cdc_3_new_contexts_payments_batches_budgets.jsonl"
    ],
    "sample_records": [
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "payments",
        "op": "c",
        "sequence_id": 910002,
        "event_timestamp": "2026-05-01T19:59:52Z",
        "ingestion_timestamp": "2026-05-01T20:00:12Z",
        "primary_key": {
          "company_id": "COMP-NEWCTX-001",
          "payment_id": "PAY-NEWCTX-001",
          "document_id": "INV-NEWCTX-001",
          "supplier_id": "SUP-NEWCTX-001"
        },
        "before": null,
        "after": {
          "payment_id": "PAY-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "document_id": "INV-NEWCTX-001",
          "supplier_id": "SUP-NEWCTX-001",
          "payment_status": "created",
          "payment_method": "bank_transfer",
          "payment_amount": 1840.25,
          "currency": "GBP",
          "scheduled_payment_at": "2026-05-04T18:59:52Z",
          "paid_at": null,
          "created_at": "2026-05-01T19:59:52Z",
          "updated_at": "2026-05-01T19:59:52Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 910002,
          "tx_id": "TX-091000",
          "is_snapshot": false,
          "note": "new_context_payments_create"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "payments",
        "op": "u",
        "sequence_id": 910003,
        "event_timestamp": "2026-05-04T20:59:52Z",
        "ingestion_timestamp": "2026-05-04T21:00:12Z",
        "primary_key": {
          "company_id": "COMP-NEWCTX-001",
          "payment_id": "PAY-NEWCTX-001",
          "document_id": "INV-NEWCTX-001",
          "supplier_id": "SUP-NEWCTX-001"
        },
        "before": {
          "payment_id": "PAY-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "document_id": "INV-NEWCTX-001",
          "supplier_id": "SUP-NEWCTX-001",
          "payment_status": "created",
          "payment_method": "bank_transfer",
          "payment_amount": 1840.25,
          "currency": "GBP",
          "scheduled_payment_at": "2026-05-04T18:59:52Z",
          "paid_at": null,
          "created_at": "2026-05-01T19:59:52Z",
          "updated_at": "2026-05-01T19:59:52Z"
        },
        "after": {
          "payment_id": "PAY-NEWCTX-001",
          "company_id": "COMP-NEWCTX-001",
          "document_id": "INV-NEWCTX-001",
          "supplier_id": "SUP-NEWCTX-001",
          "payment_status": "paid",
          "payment_method": "bank_transfer",
          "payment_amount": 1840.25,
          "currency": "GBP",
          "scheduled_payment_at": "2026-05-04T18:59:52Z",
          "paid_at": "2026-05-04T20:59:52Z",
          "created_at": "2026-05-01T19:59:52Z",
          "updated_at": "2026-05-04T20:59:52Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 910003,
          "tx_id": "TX-091000",
          "is_snapshot": false,
          "note": "new_context_payments_paid"
        }
      }
    ]
  },
  "suppliers": {
    "candidate_business_key": "supplier_id",
    "candidate_silver_table": "suppliers_current",
    "candidate_gold_tables": [
      "dim_supplier"
    ],
    "human_review_required": true,
    "files": [
      "sample_data/approvalmax_cdc/approvalmax_cdc_advanced_3_entity_20260503.jsonl"
    ],
    "sample_records": [
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "suppliers",
        "op": "c",
        "sequence_id": 700002,
        "event_timestamp": "2026-04-29T17:00:22Z",
        "ingestion_timestamp": "2026-04-29T17:00:42Z",
        "primary_key": {
          "company_id": "COMP-ADV-401",
          "supplier_id": "SUP-ADV-901"
        },
        "before": null,
        "after": {
          "supplier_id": "SUP-ADV-901",
          "company_id": "COMP-ADV-401",
          "supplier_name": "Astra Cloud Services",
          "supplier_status": "active",
          "country": "United Kingdom",
          "default_currency": "GBP",
          "created_at": "2025-10-31T16:58:22Z",
          "updated_at": "2026-04-29T17:00:22Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 700002,
          "tx_id": "TX-070000",
          "is_snapshot": false,
          "note": "new_entity_supplier_create"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "suppliers",
        "op": "u",
        "sequence_id": 700004,
        "event_timestamp": "2026-04-29T17:58:22Z",
        "ingestion_timestamp": "2026-04-29T17:58:42Z",
        "primary_key": {
          "company_id": "COMP-ADV-401",
          "supplier_id": "SUP-ADV-901"
        },
        "before": {
          "supplier_id": "SUP-ADV-901",
          "company_id": "COMP-ADV-401",
          "supplier_name": "Astra Cloud Services",
          "supplier_status": "active",
          "country": "United Kingdom",
          "default_currency": "GBP",
          "created_at": "2025-10-31T16:58:22Z",
          "updated_at": "2026-04-29T17:00:22Z"
        },
        "after": {
          "supplier_id": "SUP-ADV-901",
          "company_id": "COMP-ADV-401",
          "supplier_name": "Astra Cloud Services",
          "supplier_status": "preferred",
          "country": "United Kingdom",
          "default_currency": "GBP",
          "created_at": "2025-10-31T16:58:22Z",
          "updated_at": "2026-04-29T17:58:22Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 700004,
          "tx_id": "TX-070000",
          "is_snapshot": false,
          "note": "new_entity_supplier_status_preferred"
        }
      }
    ]
  },
  "vendor_contracts": {
    "candidate_business_key": "vendor_contract_id",
    "candidate_silver_table": "vendor_contracts_current",
    "candidate_gold_tables": [
      "dim_vendor_contract"
    ],
    "human_review_required": true,
    "files": [
      "sample_data/approvalmax_cdc/approvalmax_cdc_new_context_pr_test_v2.jsonl",
      "sample_data/approvalmax_cdc/approvalmax_cdc_new_context_pr_test_v3.jsonl"
    ],
    "sample_records": [
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "vendor_contracts",
        "op": "c",
        "sequence_id": 920003,
        "event_timestamp": "2026-05-02T21:51:44Z",
        "ingestion_timestamp": "2026-05-02T21:52:04Z",
        "primary_key": {
          "company_id": "COMP-CTX-V2-001",
          "vendor_contract_id": "VC-CTX-V2-001",
          "supplier_id": "SUP-CTX-V2-001"
        },
        "before": null,
        "after": {
          "vendor_contract_id": "VC-CTX-V2-001",
          "company_id": "COMP-CTX-V2-001",
          "supplier_id": "SUP-CTX-V2-001",
          "contract_status": "active",
          "contract_value": 12000.0,
          "currency": "GBP",
          "effective_from": "2026-05-03T19:51:44Z",
          "effective_to": "2027-05-03T19:51:44Z",
          "created_at": "2026-05-02T20:36:44Z",
          "updated_at": "2026-05-02T20:36:44Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 920003,
          "tx_id": "TX-092000",
          "is_snapshot": false,
          "note": "new_context_vendor_contracts"
        }
      },
      {
        "schema": "approvalmax_cdc_v1",
        "source_system": "approvalmax_mock_cdc",
        "source_table": "vendor_contracts",
        "op": "c",
        "sequence_id": 920003,
        "event_timestamp": "2026-05-02T21:51:44Z",
        "ingestion_timestamp": "2026-05-02T21:52:04Z",
        "primary_key": {
          "company_id": "COMP-CTX-V2-001",
          "vendor_contract_id": "VC-CTX-V2-001",
          "supplier_id": "SUP-CTX-V2-001"
        },
        "before": null,
        "after": {
          "vendor_contract_id": "VC-CTX-V2-001",
          "company_id": "COMP-CTX-V2-001",
          "supplier_id": "SUP-CTX-V2-001",
          "contract_status": "active",
          "contract_value": 12000.0,
          "currency": "GBP",
          "effective_from": "2026-05-03T19:51:44Z",
          "effective_to": "2027-05-03T19:51:44Z",
          "created_at": "2026-05-02T20:36:44Z",
          "updated_at": "2026-05-02T20:36:44Z"
        },
        "metadata": {
          "connector": "mock_debezium_style",
          "database": "approvalmax_operational",
          "lsn": 920003,
          "tx_id": "TX-092000",
          "is_snapshot": false,
          "note": "new_context_vendor_contracts"
        }
      }
    ]
  }
}

## Required human review

- Confirm business key and grain for each new context.
- Decide whether the context should become a Silver table, Gold dimension, Gold fact, or remain Bronze-only.
- Add tests and Great Expectations checks before production use.
- Confirm no financial metric definitions are changed without approval.

#!/usr/bin/env bash
set -euo pipefail

echo "Checking for unsupported Client-1 environment config..."
echo

echo "Files containing client:"
grep -R "client:" resources databricks.yml src .github || true

echo
echo "Files containing environment_key:"
grep -R "environment_key" resources databricks.yml src .github || true

echo
echo "CDC job resource references:"
grep -R "approvalmax_cdc_automation" resources databricks.yml || true

echo
echo "If client: \"1\" or environment_key: default appears in resources/approvalmax_cdc_jobs.yml, remove it."

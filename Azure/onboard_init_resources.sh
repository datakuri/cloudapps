#!/bin/bash
# Read Tenant ID and Subscription ID from current subscription
read TENANT_ID SUBSCRIPTION_ID <<< $(az account show --query '{tenantId:tenantId,id:id}' -o tsv)

echo TENANT_ID
echo SUBSCRIPTION_ID

#!/usr/bin/env bash
#
# deploy_infra.sh
#
# Deploys infrastructure to Azure in the correct order:
#   1. Create (only) the ACR using Terraform, ensuring the registry exists.
#   2. Log Docker into the ACR.
#   3. Build and push backend/frontend images.
#   4. Run the full Terraform apply, now that images are available to reference.
#
# Run from the repo root:
#   ./deploy_infra.sh
#
# Requirements: terraform, docker, az (logged in via `az login`)
 
set -euo pipefail
 
# --- Configuration -----------------------------------------------------
# Must match infra/variables.tf
ACR_NAME="acrrickardgarnau"
RESOURCE_GROUP="FastlyDep"
 
# --- Helper function for clean logging -----------------------------------
step() {
    echo ""
    echo "==> $1"
}
 
# --- 0. Prerequisites --------------------------------------------------
step "Checking that tools are installed"
for cmd in terraform docker az; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Error: '$cmd' not found in PATH. Install it and try again." >&2
        exit 1
    fi
done
 
# The script assumes it is located at the repo root, one level above infra/
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
 
# --- 1. Create the ACR first (chicken-and-egg problem) -------------------
step "Creating (only) the Container Registry with Terraform"
(
    cd infra
    terraform init -input=false
    terraform apply -target=azurerm_container_registry.acr -auto-approve
)
 
# --- 2. Log Docker into the ACR ------------------------------------------
step "Retrieving ACR password and logging Docker in"
ACR_PASSWORD=$(az acr credential show \
    --name "$ACR_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "passwords[0].value" \
    -o tsv)
 
echo "$ACR_PASSWORD" | docker login "${ACR_NAME}.azurecr.io" \
    -u "$ACR_NAME" \
    --password-stdin
 
# --- 3. Build and push images ---------------------------------------------
step "Building images with Docker Compose"
docker compose build
 
step "Pushing images to ACR"
docker compose push
 
# --- 4. Full Terraform apply, now that images exist -----------------------
step "Running full Terraform apply"
(
    cd infra
    terraform apply -auto-approve
)
 
step "Done! Backend URL:"
(
    cd infra
    terraform output backend_url
)
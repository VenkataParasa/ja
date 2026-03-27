#!/bin/bash

# JA BizTown Azure Deployment Script
# This script automates the deployment process for Azure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP="rg-jabiztown-prod"
LOCATION="East US"
ACR_NAME="crjabiztownprod"
STORAGE_ACCOUNT_NAME="stjabiztownprod"
KEYVAULT_NAME="kv-jabiztown-prod"

echo -e "${GREEN}JA BizTown Azure Deployment Script${NC}"
echo "=================================="

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if user is logged in to Azure
check_azure_login() {
    print_status "Checking Azure login status..."
    if ! az account show > /dev/null 2>&1; then
        print_error "You are not logged in to Azure. Please run 'az login' first."
        exit 1
    fi
    print_status "Azure login confirmed."
}

# Set subscription
set_subscription() {
    if [ -n "$AZURE_SUBSCRIPTION_ID" ]; then
        print_status "Setting subscription to: $AZURE_SUBSCRIPTION_ID"
        az account set --subscription "$AZURE_SUBSCRIPTION_ID"
    fi
}

# Create resource group
create_resource_group() {
    print_status "Creating resource group: $RESOURCE_GROUP"
    az group create \
        --name "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --tags Environment=Production Project=JA-BizTown Owner=DevOps
}

# Create Azure Container Registry
create_acr() {
    print_status "Creating Azure Container Registry: $ACR_NAME"
    az acr create \
        --resource-group "$RESOURCE_GROUP" \
        --name "$ACR_NAME" \
        --sku Premium \
        --admin-enabled true
}

# Create Storage Account
create_storage_account() {
    print_status "Creating Storage Account: $STORAGE_ACCOUNT_NAME"
    az storage account create \
        --resource-group "$RESOURCE_GROUP" \
        --name "$STORAGE_ACCOUNT_NAME" \
        --sku Standard_LRS \
        --kind StorageV2 \
        --https-only true
}

# Create Key Vault
create_key_vault() {
    print_status "Creating Key Vault: $KEYVAULT_NAME"
    az keyvault create \
        --resource-group "$RESOURCE_GROUP" \
        --name "$KEYVAULT_NAME" \
        --location "$LOCATION" \
        --enable-soft-delete true \
        --enable-purge-protection true
}

# Store secrets in Key Vault
store_secrets() {
    print_status "Storing secrets in Key Vault..."
    
    # SQL Server password
    if [ -n "$SQL_ADMIN_PASSWORD" ]; then
        az keyvault secret set \
            --vault-name "$KEYVAULT_NAME" \
            --name "sql-admin-password" \
            --value "$SQL_ADMIN_PASSWORD"
    fi
    
    # Application Insights key (if provided)
    if [ -n "$APPINSIGHTS_INSTRUMENTATIONKEY" ]; then
        az keyvault secret set \
            --vault-name "$KEYVAULT_NAME" \
            --name "appinsights-instrumentation-key" \
            --value "$APPINSIGHTS_INSTRUMENTATIONKEY"
    fi
}

# Build and push Docker images
build_and_push_images() {
    print_status "Building and pushing Docker images..."
    
    # Login to ACR
    az acr login --name "$ACR_NAME"
    
    # Get ACR login server
    ACR_LOGIN_SERVER=$(az acr show --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --query loginServer --output tsv)
    
    # Build and push frontend image
    print_status "Building frontend image..."
    cd ../web-app
    docker build -t "$ACR_LOGIN_SERVER/jabiztown-frontend:latest" .
    docker push "$ACR_LOGIN_SERVER/jabiztown-frontend:latest"
    
    # Build and push backend image
    print_status "Building backend image..."
    cd ../api
    docker build -t "$ACR_LOGIN_SERVER/jabiztown-api:latest" .
    docker push "$ACR_LOGIN_SERVER/jabiztown-api:latest"
    
    cd ../azure
}

# Deploy with Terraform
deploy_terraform() {
    print_status "Deploying infrastructure with Terraform..."
    
    cd ../terraform
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -out jabiztown.plan
    
    # Apply deployment
    terraform apply jabiztown.plan
    
    cd ../azure
}

# Configure DNS (manual step instructions)
configure_dns_instructions() {
    print_warning "DNS Configuration Required"
    echo "Please configure the following DNS records with your domain registrar:"
    echo ""
    echo "Type: CNAME"
    echo "Name: ja"
    echo "Value: app-jabiztown-frontend-prod.azurewebsites.net"
    echo "TTL: 3600"
    echo ""
    echo "After configuring DNS, run the verification script:"
    echo "./verify-deployment.sh"
}

# Main deployment function
main() {
    print_status "Starting JA BizTown Azure deployment..."
    
    # Check prerequisites
    check_azure_login
    set_subscription
    
    # Create Azure resources
    create_resource_group
    create_acr
    create_storage_account
    create_key_vault
    
    # Store secrets
    store_secrets
    
    # Build and push images
    build_and_push_images
    
    # Deploy infrastructure
    deploy_terraform
    
    # Provide DNS instructions
    configure_dns_instructions
    
    print_status "Deployment completed successfully!"
    print_warning "Remember to configure DNS records for ja.symphonize.net"
}

# Run main function
main "$@"

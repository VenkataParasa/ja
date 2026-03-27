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

# Build and push Docker images
build_and_push_images() {
    print_status "Building and pushing Docker images..."

    # Get ACR name/login server from Terraform outputs to avoid drift
    cd ../terraform
    ACR_LOGIN_SERVER=$(terraform output -raw container_registry_login_server)
    ACR_NAME=$(echo "$ACR_LOGIN_SERVER" | cut -d '.' -f1)
    cd ../azure

    # Login to ACR
    az acr login --name "$ACR_NAME"
    
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
    
    # Deploy infrastructure first (creates ACR/AppServices/SQL consistently)
    deploy_terraform

    # Build and push images
    build_and_push_images
    
    # Provide DNS instructions
    configure_dns_instructions
    
    print_status "Deployment completed successfully!"
    print_warning "Remember to configure DNS records for ja.symphonize.net"
}

# Run main function
main "$@"

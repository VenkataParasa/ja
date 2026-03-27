#!/bin/bash

# JA BizTown Azure Deployment Verification Script
# This script verifies that the deployment was successful

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP="rg-jabiztown-prod"
DOMAIN="ja.symphonize.net"

echo -e "${GREEN}JA BizTown Deployment Verification${NC}"
echo "====================================="

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

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists az; then
        print_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi
    
    if ! command_exists curl; then
        print_error "curl is not installed. Please install it first."
        exit 1
    fi
    
    if ! command_exists nslookup; then
        print_error "nslookup is not available. Please install it first."
        exit 1
    fi
    
    print_status "Prerequisites check passed."
}

# Check Azure login
check_azure_login() {
    print_status "Checking Azure login..."
    if ! az account show > /dev/null 2>&1; then
        print_error "You are not logged in to Azure. Please run 'az login' first."
        exit 1
    fi
    print_status "Azure login confirmed."
}

# Verify resource group exists
verify_resource_group() {
    print_status "Verifying resource group: $RESOURCE_GROUP"
    if ! az group show --name "$RESOURCE_GROUP" > /dev/null 2>&1; then
        print_error "Resource group $RESOURCE_GROUP does not exist."
        exit 1
    fi
    print_status "Resource group verified."
}

# Verify Azure Container Registry
verify_acr() {
    print_status "Verifying Azure Container Registry..."
    ACR_NAME=$(az acr list --resource-group "$RESOURCE_GROUP" --query "[0].name" --output tsv)
    if [ -z "$ACR_NAME" ]; then
        print_error "Azure Container Registry not found."
        exit 1
    fi
    print_status "ACR found: $ACR_NAME"
    
    # Check if images exist
    print_status "Checking Docker images in ACR..."
    FRONTEND_IMAGE=$(az acr repository show-tags --name "$ACR_NAME" --repository jabiztown-frontend --query "[0]" --output tsv 2>/dev/null || echo "")
    BACKEND_IMAGE=$(az acr repository show-tags --name "$ACR_NAME" --repository jabiztown-api --query "[0]" --output tsv 2>/dev/null || echo "")
    
    if [ -z "$FRONTEND_IMAGE" ]; then
        print_warning "Frontend image not found in ACR."
    else
        print_status "Frontend image found: $FRONTEND_IMAGE"
    fi
    
    if [ -z "$BACKEND_IMAGE" ]; then
        print_warning "Backend image not found in ACR."
    else
        print_status "Backend image found: $BACKEND_IMAGE"
    fi
}

# Verify App Services
verify_app_services() {
    print_status "Verifying App Services..."
    
    FRONTEND_APP=$(az webapp list --resource-group "$RESOURCE_GROUP" --query "[?contains(name, 'frontend')].name" --output tsv)
    BACKEND_APP=$(az webapp list --resource-group "$RESOURCE_GROUP" --query "[?contains(name, 'backend')].name" --output tsv)
    
    if [ -z "$FRONTEND_APP" ]; then
        print_error "Frontend App Service not found."
        exit 1
    fi
    
    if [ -z "$BACKEND_APP" ]; then
        print_error "Backend App Service not found."
        exit 1
    fi
    
    print_status "Frontend App Service found: $FRONTEND_APP"
    print_status "Backend App Service found: $BACKEND_APP"
    
    # Get URLs
    FRONTEND_URL=$(az webapp show --resource-group "$RESOURCE_GROUP" --name "$FRONTEND_APP" --query "defaultHostName" --output tsv)
    BACKEND_URL=$(az webapp show --resource-group "$RESOURCE_GROUP" --name "$BACKEND_APP" --query "defaultHostName" --output tsv)
    
    print_status "Frontend URL: https://$FRONTEND_URL"
    print_status "Backend URL: https://$BACKEND_URL"
}

# Verify SQL Server
verify_sql_server() {
    print_status "Verifying SQL Server..."
    
    SQL_SERVER=$(az sql server list --resource-group "$RESOURCE_GROUP" --query "[0].name" --output tsv)
    if [ -z "$SQL_SERVER" ]; then
        print_error "SQL Server not found."
        exit 1
    fi
    
    SQL_DB=$(az sql db list --resource-group "$RESOURCE_GROUP" --server "$SQL_SERVER" --query "[0].name" --output tsv)
    if [ -z "$SQL_DB" ]; then
        print_error "SQL Database not found."
        exit 1
    fi
    
    print_status "SQL Server found: $SQL_SERVER"
    print_status "SQL Database found: $SQL_DB"
}

# Test application endpoints
test_applications() {
    print_status "Testing application endpoints..."
    
    # Get frontend URL
    FRONTEND_APP=$(az webapp list --resource-group "$RESOURCE_GROUP" --query "[?contains(name, 'frontend')].name" --output tsv)
    FRONTEND_URL=$(az webapp show --resource-group "$RESOURCE_GROUP" --name "$FRONTEND_APP" --query "defaultHostName" --output tsv)
    
    # Get backend URL
    BACKEND_APP=$(az webapp list --resource-group "$RESOURCE_GROUP" --query "[?contains(name, 'backend')].name" --output tsv)
    BACKEND_URL=$(az webapp show --resource-group "$RESOURCE_GROUP" --name "$BACKEND_APP" --query "defaultHostName" --output tsv)
    
    # Test frontend
    print_status "Testing frontend: https://$FRONTEND_URL"
    if curl -f -s "https://$FRONTEND_URL" > /dev/null; then
        print_status "✅ Frontend is responding"
    else
        print_warning "⚠️  Frontend is not responding"
    fi
    
    # Test backend
    print_status "Testing backend: https://$BACKEND_URL/health"
    if curl -f -s "https://$BACKEND_URL/health" > /dev/null; then
        print_status "✅ Backend is responding"
    else
        print_warning "⚠️  Backend is not responding (health endpoint may not be configured)"
    fi
}

# Test DNS resolution
test_dns() {
    print_status "Testing DNS resolution for $DOMAIN..."
    
    if nslookup "$DOMAIN" > /dev/null 2>&1; then
        print_status "✅ DNS resolution successful for $DOMAIN"
        
        # Get the resolved IP
        RESOLVED_IP=$(nslookup "$DOMAIN" | grep -A 1 "Name:" | tail -1 | awk '{print $2}')
        print_status "Resolved to: $RESOLVED_IP"
    else
        print_warning "⚠️  DNS resolution failed for $DOMAIN"
        print_warning "Please check your DNS configuration with your domain registrar"
    fi
}

# Test custom domain
test_custom_domain() {
    print_status "Testing custom domain configuration..."
    
    FRONTEND_APP=$(az webapp list --resource-group "$RESOURCE_GROUP" --query "[?contains(name, 'frontend')].name" --output tsv)
    
    # Check if custom domain is configured
    CUSTOM_DOMAINS=$(az webapp config hostname list --resource-group "$RESOURCE_GROUP" --name "$FRONTEND_APP" --query "[].name" --output tsv)
    
    if echo "$CUSTOM_DOMAINS" | grep -q "$DOMAIN"; then
        print_status "✅ Custom domain $DOMAIN is configured"
    else
        print_warning "⚠️  Custom domain $DOMAIN is not configured"
        print_warning "Run: az webapp config hostname add --resource-group $RESOURCE_GROUP --name $FRONTEND_APP --hostname $DOMAIN"
    fi
}

# Generate deployment report
generate_report() {
    print_status "Generating deployment report..."
    
    REPORT_FILE="deployment-report-$(date +%Y%m%d-%H%M%S).txt"
    
    {
        echo "JA BizTown Azure Deployment Report"
        echo "=================================="
        echo "Generated: $(date)"
        echo ""
        echo "Resource Group: $RESOURCE_GROUP"
        echo "Custom Domain: $DOMAIN"
        echo ""
        
        echo "App Services:"
        az webapp list --resource-group "$RESOURCE_GROUP" --output table
        echo ""
        
        echo "Container Registry:"
        az acr list --resource-group "$RESOURCE_GROUP" --output table
        echo ""
        
        echo "SQL Server:"
        az sql server list --resource-group "$RESOURCE_GROUP" --output table
        echo ""
        
        echo "DNS Status:"
        if nslookup "$DOMAIN" > /dev/null 2>&1; then
            echo "✅ DNS resolution successful"
        else
            echo "❌ DNS resolution failed"
        fi
        
    } > "$REPORT_FILE"
    
    print_status "Deployment report saved to: $REPORT_FILE"
}

# Main verification function
main() {
    print_status "Starting deployment verification..."
    
    # Run all checks
    check_prerequisites
    check_azure_login
    verify_resource_group
    verify_acr
    verify_app_services
    verify_sql_server
    test_applications
    test_dns
    test_custom_domain
    generate_report
    
    print_status "✅ Deployment verification completed!"
    print_warning "If any warnings appeared, please address them before going to production."
}

# Run main function
main "$@"

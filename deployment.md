# JA BizTown Azure Deployment Guide

This guide provides comprehensive instructions for deploying the JA BizTown Simulation to Azure and configuring the custom domain `ja.symphonize.net`.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Azure Setup](#azure-setup)
3. [Terraform Deployment](#terraform-deployment)
4. [Container Registry Setup](#container-registry-setup)
5. [Application Deployment](#application-deployment)
6. [Custom Domain Configuration](#custom-domain-configuration)
7. [DNS Configuration with Hosting Provider](#dns-configuration-with-hosting-provider)
8. [SSL Certificate Setup](#ssl-certificate-setup)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Maintenance and Updates](#maintenance-and-updates)

## Prerequisites

### Required Tools
- **Azure CLI** (Latest version)
- **Terraform** (v1.0+)
- **Docker** (Latest version)
- **Git** (For source control)

### Azure Subscriptions
- Azure subscription with Owner permissions
- Azure AD permissions to create groups and users

### Domain Requirements
- Access to DNS management for `symphonize.net`
- Ability to create CNAME and A records

## Azure Setup

### 1. Install Azure CLI
```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile AzureCLI.msi
Start-Process msiexec.exe -ArgumentList '/i AzureCLI.msi /quiet' -Wait

# Verify installation
az --version
```

### 2. Install Terraform
```bash
# Download Terraform for Windows
# Visit: https://www.terraform.io/downloads.html
# Extract to C:\Program Files\Terraform
# Add to PATH environment variable

# Verify installation
terraform --version
```

### 3. Login to Azure
```bash
# Login to Azure
az login

# Set subscription (if multiple)
az account set --subscription "Your-Subscription-Name"

# Verify current context
az account show
```

### 4. Register Required Providers
```bash
# Register required Azure providers
az provider register --namespace Microsoft.ContainerRegistry
az provider register --namespace Microsoft.Web
az provider register --namespace Microsoft.Sql
az provider register --namespace Microsoft.OperationalInsights

# Wait for registration to complete
az provider show --namespace Microsoft.ContainerRegistry
```

## Terraform Deployment

### 1. Prepare Terraform Configuration
```bash
# Navigate to terraform directory
cd terraform

# Copy example variables file
copy terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values
notepad terraform.tfvars
```

### 2. Configure Variables
Edit `terraform.tfvars` with your specific values:
```hcl
location = "East US"
sql_admin_username = "jabiztown_admin"
sql_admin_password = "YourSecurePassword123!"
domain_name = "ja.symphonize.net"
```

### 3. Initialize Terraform
```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan -out jabiztown.plan

# Apply the deployment
terraform apply jabiztown.plan
```

### 4. Verify Deployment
```bash
# Check outputs
terraform output

# Verify resources in Azure Portal
# Resource Group: rg-jabiztown-prod
# Container Registry: crjabiztownprod
# App Services: app-jabiztown-frontend-prod, app-jabiztown-backend-prod
# SQL Server: sql-jabiztown-prod
```

## Container Registry Setup

### 1. Build and Push Docker Images

#### Frontend Image
```bash
# Navigate to web-app directory
cd ../web-app

# Login to Azure Container Registry
az acr login --name crjabiztownprod

# Build frontend image
docker build -t crjabiztownprod.azurecr.io/jabiztown-frontend:latest .

# Push frontend image
docker push crjabiztownprod.azurecr.io/jabiztown-frontend:latest
```

#### Backend Image
```bash
# Navigate to api directory
cd ../api

# Build backend image
docker build -t crjabiztownprod.azurecr.io/jabiztown-api:latest .

# Push backend image
docker push crjabiztownprod.azurecr.io/jabiztown-api:latest
```

### 2. Verify Images in Registry
```bash
# List repositories
az acr repository list --name crjabiztownprod

# List tags for frontend
az acr repository show-tags --name crjabiztownprod --repository jabiztown-frontend
```

## Application Deployment

### 1. Configure App Service Settings

#### Frontend App Service
```bash
# Get frontend app name
FRONTEND_APP=$(terraform output -raw frontend_app_url | sed 's|https://||')

# Configure environment variables
az webapp config appsettings set \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --settings "REACT_APP_API_URL=https://$(terraform output -raw backend_app_url)"
```

#### Backend App Service
```bash
# Get backend app name
BACKEND_APP=$(terraform output -raw backend_app_url | sed 's|https://||')

# Configure production settings
az webapp config appsettings set \
  --resource-group rg-jabiztown-prod \
  --name $BACKEND_APP \
  --settings "ASPNETCORE_ENVIRONMENT=Production"
```

### 2. Restart App Services
```bash
# Restart frontend
az webapp restart --resource-group rg-jabiztown-prod --name $FRONTEND_APP

# Restart backend
az webapp restart --resource-group rg-jabiztown-prod --name $BACKEND_APP
```

### 3. Verify Application
```bash
# Test frontend
curl https://$FRONTEND_APP

# Test backend health
curl https://$BACKEND_APP/health
```

## Custom Domain Configuration

### 1. Add Custom Domain to Frontend

```bash
# Get frontend app name
FRONTEND_APP=$(terraform output -raw frontend_app_url | sed 's|https://||')

# Add custom domain
az webapp config hostname add \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --hostname ja.symphonize.net
```

### 2. Get DNS Verification Details
```bash
# Get verification details
az webapp config hostname list \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --output table
```

## DNS Configuration with Hosting Provider

### Step-by-Step Instructions for Domain Registrar

#### 1. Access Your Domain Management Panel
- Log in to your domain registrar (GoDaddy, Namecheap, etc.)
- Navigate to DNS management for `symphonize.net`

#### 2. Create the Following DNS Records

**Record 1: CNAME for Frontend**
```
Type: CNAME
Name: ja
Value: app-jabiztown-frontend-prod.azurewebsites.net
TTL: 3600 (or 1 hour)
```

**Record 2: A Record (Optional - for root domain)**
```
Type: A
Name: @ (or ja.symphonize.net if supported)
Value: 20.112.52.29 (Get from Azure App Service)
TTL: 3600
```

**Record 3: TXT for Verification (if required)**
```
Type: TXT
Name: ja
Value: "azure-verification-token" (Get from Azure)
TTL: 3600
```

#### 3. How to Find the Correct Values

**Get CNAME Target:**
```bash
# Get the actual hostname from Terraform output
terraform output frontend_app_url
# Expected: https://app-jabiztown-frontend-prod.azurewebsites.net
# Use: app-jabiztown-frontend-prod.azurewebsites.net
```

**Get A Record IP:**
```bash
# Get the IP address for the frontend app
az webapp show \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --query "defaultHostName" \
  --output tsv

# Then lookup the IP
nslookup app-jabiztown-frontend-prod.azurewebsites.net
```

#### 4. Propagation Time
- DNS changes typically take 5-30 minutes to propagate
- Some registrars may take up to 48 hours
- Use online tools like whatsmydns.net to verify propagation

#### 5. Verification Commands
```bash
# Verify CNAME resolution
nslookup ja.symphonize.net

# Should return something like:
# ja.symphonize.net canonical name = app-jabiztown-frontend-prod.azurewebsites.net
```

### Common Registrar Instructions

**GoDaddy:**
1. Log in to GoDaddy
2. Go to "DNS Management"
3. Add CNAME record with Name: "ja" and Value: "app-jabiztown-frontend-prod.azurewebsites.net"

**Namecheap:**
1. Log in to Namecheap
2. Go to "Domain List" → "Manage"
3. Go to "Advanced DNS"
4. Add CNAME record with Host: "ja" and Value: "app-jabiztown-frontend-prod.azurewebsites.net"

**Google Domains:**
1. Log in to Google Domains
2. Select your domain
3. Go to "DNS"
4. Add Custom record: Type "CNAME", Name "ja", Data "app-jabiztown-frontend-prod.azurewebsites.net"

## SSL Certificate Setup

### 1. Enable HTTPS for Custom Domain
```bash
# Enable HTTPS binding
az webapp config ssl bind \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --certificate-thumbprint $(az webapp config ssl list \
    --resource-group rg-jabiztown-prod \
    --output json | jq -r '.[0].thumbprint') \
  --name ja.symphonize.net
```

### 2. Verify SSL Certificate
```bash
# Check SSL status
az webapp config ssl list \
  --resource-group rg-jabiztown-prod \
  --output table
```

## Monitoring and Logging

### 1. Set Up Application Insights
```bash
# Get instrumentation key
AI_KEY=$(terraform output -raw application_insights_instrumentation_key)

# Configure frontend app
az webapp config appsettings set \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --settings "APPINSIGHTS_INSTRUMENTATIONKEY=$AI_KEY"

# Configure backend app
az webapp config appsettings set \
  --resource-group rg-jabiztown-prod \
  --name $BACKEND_APP \
  --settings "APPINSIGHTS_INSTRUMENTATIONKEY=$AI_KEY"
```

### 2. Set Up Log Analytics
```bash
# Enable diagnostic logging
az monitor diagnostic-settings create \
  --name jabiztown-logs \
  --resource $(az webapp show --resource-group rg-jabiztown-prod --name $FRONTEND_APP --query id --output tsv) \
  --workspace $(az monitor log-analytics workspace show --resource-group rg-jabiztown-prod --name law-jabiztown-prod --query id --output tsv) \
  --logs '[{"category": "AppServiceHTTPLogs","enabled": true},{"category": "AppServiceConsoleLogs","enabled": true}]'
```

### 3. Set Up Alerts
```bash
# Create alert for high CPU usage
az monitor metrics alert create \
  --name "High CPU Alert" \
  --resource-group rg-jabiztown-prod \
  --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-jabiztown-prod/providers/Microsoft.Web/serverfarms/asp-jabiztown-frontend-prod" \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2
```

## Maintenance and Updates

### 1. Update Application Code
```bash
# Build new images
cd web-app
docker build -t crjabiztownprod.azurecr.io/jabiztown-frontend:v2.0 .
docker push crjabiztownprod.azurecr.io/jabiztown-frontend:v2.0

cd ../api
docker build -t crjabiztownprod.azurecr.io/jabiztown-api:v2.0 .
docker push crjabiztownprod.azurecr.io/jabiztown-api:v2.0
```

### 2. Deploy New Version
```bash
# Update frontend
az webapp config container set \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --docker-custom-image-name crjabiztownprod.azurecr.io/jabiztown-frontend:v2.0 \
  --docker-registry-server-url https://crjabiztownprod.azurecr.io

# Update backend
az webapp config container set \
  --resource-group rg-jabiztown-prod \
  --name $BACKEND_APP \
  --docker-custom-image-name crjabiztownprod.azurecr.io/jabiztown-api:v2.0 \
  --docker-registry-server-url https://crjabiztownprod.azurecr.io
```

### 3. Database Maintenance
```bash
# Backup database
az sql db backup create \
  --resource-group rg-jabiztown-prod \
  --server sql-jabiztown-prod \
  --name sqldb-jabiztown-prod \
  --backup-type "FULL"

# Restore database (if needed)
az sql db restore \
  --resource-group rg-jabiztown-prod \
  --server sql-jabiztown-prod \
  --name sqldb-jabiztown-prod-restored \
  --backup-id "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-jabiztown-prod/providers/Microsoft.Sql/servers/sql-jabiztown-prod/databases/sqldb-jabiztown-prod/backup/backup-name"
```

## Troubleshooting

### Common Issues and Solutions

#### 1. DNS Propagation Issues
```bash
# Check DNS resolution
nslookup ja.symphonize.net

# Check from different locations
# Use online tools: whatsmydns.net
```

#### 2. SSL Certificate Issues
```bash
# Check SSL binding
az webapp config ssl list --resource-group rg-jabiztown-prod

# Rebind SSL certificate
az webapp config ssl bind \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --certificate-thumbprint <thumbprint> \
  --name ja.symphonize.net
```

#### 3. Application Not Starting
```bash
# Check app logs
az webapp log tail --resource-group rg-jabiztown-prod --name $FRONTEND_APP

# Check container logs
az webapp log tail --resource-group rg-jabiztown-prod --name $BACKEND_APP
```

#### 4. Database Connection Issues
```bash
# Test database connectivity
az sql db show-connection-string \
  --name sqldb-jabiztown-prod \
  --server sql-jabiztown-prod \
  --client ado.net
```

## Cost Optimization

### 1. Monitor Resource Usage
```bash
# Check cost management
az consumption usage list \
  --resource-group rg-jabiztown-prod \
  --output table
```

### 2. Scale Down During Off Hours
```bash
# Scale down App Service Plan
az appservice plan update \
  --resource-group rg-jabiztown-prod \
  --name asp-jabiztown-frontend-prod \
  --sku B1
```

## Security Best Practices

### 1. Enable Managed Identity
```bash
# Enable system-assigned managed identity
az webapp identity assign \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP
```

### 2. Restrict Access
```bash
# Enable IP restrictions
az webapp config access-restriction add \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --rule-name AllowOfficeIP \
  --action Allow \
  --ip-address 203.0.113.0/24 \
  --priority 100
```

### 3. Enable Backup
```bash
# Configure app backup
az webapp config backup create \
  --resource-group rg-jabiztown-prod \
  --name $FRONTEND_APP \
  --storage-account-url <storage-account-url> \
  --backup-name jabiztown-backup
```

---

## Support and Contact

For issues with:
- **Azure Resources**: Contact Azure Support
- **Domain Configuration**: Contact your domain registrar
- **Application Issues**: Check Application Insights logs
- **Terraform Issues**: Review Terraform state and configuration

This deployment guide provides a complete production-ready setup for JA BizTown on Azure with custom domain configuration.

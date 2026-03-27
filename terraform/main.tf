terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "jabiztown" {
  name     = "rg-jabiztown-prod"
  location = var.location
  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
    Owner       = "DevOps Team"
  }
}

# Azure Container Registry
resource "azurerm_container_registry" "jabiztown" {
  name                = "crjabiztownprod"
  resource_group_name = azurerm_resource_group.jabiztown.name
  location            = azurerm_resource_group.jabiztown.location
  sku                 = "Premium"
  admin_enabled       = true
  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
  }
}

# Azure SQL Database Server
resource "azurerm_mssql_server" "jabiztown" {
  name                         = "sql-jabiztown-prod"
  resource_group_name          = azurerm_resource_group.jabiztown.name
  location                     = azurerm_resource_group.jabiztown.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password
  
  azuread_administrator {
    login_username = azuread_group.jabiztown_admins.display_name
    object_id      = azuread_group.jabiztown_admins.object_id
  }

  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
  }
}

# Azure SQL Database
resource "azurerm_mssql_database" "jabiztown" {
  name           = "sqldb-jabiztown-prod"
  server_id      = azurerm_mssql_server.jabiztown.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  sku_name       = "S2"
  max_size_gb    = 50

  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
  }
}

# Allow Azure Services to access SQL Server
resource "azurerm_mssql_firewall_rule" "azure_services" {
  name                = "AllowAzureIPs"
  server_id           = azurerm_mssql_server.jabiztown.id
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

# App Service Plan for Frontend
resource "azurerm_service_plan" "frontend" {
  name                = "asp-jabiztown-frontend-prod"
  resource_group_name = azurerm_resource_group.jabiztown.name
  location            = azurerm_resource_group.jabiztown.location
  os_type             = "Linux"
  sku_name            = "P1v2"
  
  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
    Component   = "Frontend"
  }
}

# App Service for Frontend
resource "azurerm_linux_web_app" "frontend" {
  name                = "app-jabiztown-frontend-prod"
  resource_group_name = azurerm_resource_group.jabiztown.name
  location            = azurerm_resource_group.jabiztown.location
  service_plan_id     = azurerm_service_plan.frontend.id
  
  site_config {
    always_on        = true
    http2_enabled     = true
    min_tls_version   = "1.2"
    ftps_state        = "Disabled"
    
    application_stack {
      docker_image     = "${azurerm_container_registry.jabiztown.login_server}/jabiztown-frontend:latest"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"      = "https://${azurerm_container_registry.jabiztown.login_server}"
    "DOCKER_REGISTRY_SERVER_USERNAME" = azurerm_container_registry.jabiztown.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = azurerm_container_registry.jabiztown.admin_password
    "WEBSITES_PORT"                   = "3000"
  }

  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
    Component   = "Frontend"
  }
}

# App Service Plan for Backend API
resource "azurerm_service_plan" "backend" {
  name                = "asp-jabiztown-backend-prod"
  resource_group_name = azurerm_resource_group.jabiztown.name
  location            = azurerm_resource_group.jabiztown.location
  os_type             = "Linux"
  sku_name            = "P2v2"
  
  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
    Component   = "Backend"
  }
}

# App Service for Backend API
resource "azurerm_linux_web_app" "backend" {
  name                = "app-jabiztown-backend-prod"
  resource_group_name = azurerm_resource_group.jabiztown.name
  location            = azurerm_resource_group.jabiztown.location
  service_plan_id     = azurerm_service_plan.backend.id
  
  site_config {
    always_on        = true
    http2_enabled     = true
    min_tls_version   = "1.2"
    ftps_state        = "Disabled"
    
    application_stack {
      docker_image     = "${azurerm_container_registry.jabiztown.login_server}/jabiztown-api:latest"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"      = "https://${azurerm_container_registry.jabiztown.login_server}"
    "DOCKER_REGISTRY_SERVER_USERNAME" = azurerm_container_registry.jabiztown.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = azurerm_container_registry.jabiztown.admin_password
    "WEBSITES_PORT"                   = "8080"
    "ASPNETCORE_ENVIRONMENT"          = "Production"
    "ConnectionStrings__DefaultConnection" = "Server=tcp:${azurerm_mssql_server.jabiztown.fully_qualified_domain_name},1433;Initial Catalog=${azurerm_mssql_database.jabiztown.name};User ID=${var.sql_admin_username};Password=${var.sql_admin_password};Encrypt=true;TrustServerCertificate=false;Connection Timeout=30;"
  }

  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
    Component   = "Backend"
  }
}

# Azure AD Group for Admins
resource "azuread_group" "jabiztown_admins" {
  display_name     = "JA BizTown Admins"
  security_enabled = true
  description      = "Administrators for JA BizTown resources"
}

# Application Insights
resource "azurerm_application_insights" "jabiztown" {
  name                = "ai-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  workspace_id        = azurerm_log_analytics_workspace.jabiztown.id
  application_type    = "web"
  
  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
  }
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "jabiztown" {
  name                = "law-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  
  tags = {
    Environment = "Production"
    Project     = "JA BizTown"
  }
}

# Output values
output "resource_group_name" {
  value = azurerm_resource_group.jabiztown.name
}

output "container_registry_login_server" {
  value = azurerm_container_registry.jabiztown.login_server
}

output "container_registry_admin_username" {
  value = azurerm_container_registry.jabiztown.admin_username
}

output "container_registry_admin_password" {
  value = azurerm_container_registry.jabiztown.admin_password
  sensitive = true
}

output "frontend_app_url" {
  value = azurerm_linux_web_app.frontend.default_hostname
}

output "backend_app_url" {
  value = azurerm_linux_web_app.backend.default_hostname
}

output "sql_server_fqdn" {
  value = azurerm_mssql_server.jabiztown.fully_qualified_domain_name
}

output "sql_database_name" {
  value = azurerm_mssql_database.jabiztown.name
}

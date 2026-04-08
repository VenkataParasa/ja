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
}

# Azure SQL Database Server
resource "azurerm_mssql_server" "jabiztown" {
  name                         = "sql-jabiztown-prod"
  resource_group_name          = azurerm_resource_group.jabiztown.name
  location                     = azurerm_resource_group.jabiztown.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password
}

# Azure SQL Database
resource "azurerm_mssql_database" "jabiztown" {
  name           = "sqldb-jabiztown-prod"
  server_id      = azurerm_mssql_server.jabiztown.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  sku_name       = "S2"
  max_size_gb    = 50
}

# Azure Kubernetes Service (AKS)
resource "azurerm_kubernetes_cluster" "jabiztown" {
  name                = "aks-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  dns_prefix          = "jabiztownaks"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = {
    Environment = "Production"
  }
}

# Role Assignment: AKS to pull from ACR
resource "azurerm_role_assignment" "aks_acr" {
  scope                = azurerm_container_registry.jabiztown.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.jabiztown.kubelet_identity[0].object_id
}

# Azure Cosmos DB (NoSQL for Layouts/Config)
resource "azurerm_cosmosdb_account" "jabiztown" {
  name                = "cosmos-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.jabiztown.location
    failover_priority = 0
  }
}

# Azure Service Bus (Event Bus)
resource "azurerm_servicebus_namespace" "jabiztown" {
  name                = "sb-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  sku                 = "Standard"
}

# Azure Web PubSub (Real-time events/Screen Sharing)
resource "azurerm_web_pubsub" "jabiztown" {
  name                = "wps-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  sku                 = "Standard_S1"
  capacity            = 1
}

# Azure Redis Cache (Idempotency)
resource "azurerm_redis_cache" "jabiztown" {
  name                = "redis-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  capacity            = 1
  family              = "C"
  sku_name            = "Standard"
}

# API Management (APIM Gateway)
resource "azurerm_api_management" "jabiztown" {
  name                = "apim-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  publisher_name      = "JA USA"
  publisher_email     = "admin@ja.org"
  sku_name            = "Developer_1" # Developer SKU for dev/staging, upgrade to Standard for production high-availability
}

# Application Insights
resource "azurerm_application_insights" "jabiztown" {
  name                = "ai-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  workspace_id        = azurerm_log_analytics_workspace.jabiztown.id
  application_type    = "web"
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "jabiztown" {
  name                = "law-jabiztown-prod"
  location            = azurerm_resource_group.jabiztown.location
  resource_group_name = azurerm_resource_group.jabiztown.name
  sku                 = "PerGB2018"
}

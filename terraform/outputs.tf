output "resource_group_name" {
  description = "Name of the Azure Resource Group"
  value       = azurerm_resource_group.jabiztown.name
}

output "container_registry_login_server" {
  description = "Azure Container Registry login server"
  value       = azurerm_container_registry.jabiztown.login_server
}

output "container_registry_admin_username" {
  description = "Azure Container Registry admin username"
  value       = azurerm_container_registry.jabiztown.admin_username
}

output "container_registry_admin_password" {
  description = "Azure Container Registry admin password"
  value       = azurerm_container_registry.jabiztown.admin_password
  sensitive   = true
}

output "frontend_app_url" {
  description = "Frontend application URL"
  value       = "https://${azurerm_linux_web_app.frontend.default_hostname}"
}

output "backend_app_url" {
  description = "Backend API URL"
  value       = "https://${azurerm_linux_web_app.backend.default_hostname}"
}

output "sql_server_fqdn" {
  description = "SQL Server fully qualified domain name"
  value       = azurerm_mssql_server.jabiztown.fully_qualified_domain_name
}

output "sql_database_name" {
  description = "SQL Database name"
  value       = azurerm_mssql_database.jabiztown.name
}

output "application_insights_instrumentation_key" {
  description = "Application Insights instrumentation key"
  value       = azurerm_application_insights.jabiztown.instrumentation_key
  sensitive   = true
}

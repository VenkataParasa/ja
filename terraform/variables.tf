variable "location" {
  description = "Azure region for deployment"
  type        = string
  default     = "East US"
}

variable "sql_admin_username" {
  description = "SQL Server administrator username"
  type        = string
  default     = "jabiztown_admin"
}

variable "sql_admin_password" {
  description = "SQL Server administrator password"
  type        = string
  sensitive   = true
}

variable "domain_name" {
  description = "Custom domain name for the application"
  type        = string
  default     = "ja.symphonize.net"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "Production"
    Project     = "JA BizTown"
    Owner       = "DevOps Team"
  }
}

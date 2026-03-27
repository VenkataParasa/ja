# JA BizTown Simulation - Docker Containerization

This repository contains the complete Docker containerization setup for the JA BizTown Economic Engine prototype, running locally using Docker Desktop.

## Architecture Overview

The stack consists of three main services:

- **Frontend**: React Native for Web served via Nginx (Port 3000)
- **Backend**: .NET Core 8.0 Web API (Port 8080)  
- **Database**: MS SQL Server 2022 for Linux (Port 1433)

## Prerequisites

1. **Docker Desktop** - Install and start Docker Desktop
2. **Git** - For cloning the repository (if applicable)

## Quick Start

### 1. Build and Run the Stack

```bash
# Clone or navigate to the project directory
cd JA

# Build and start all services
docker-compose up --build
```

This command will:
- Build the .NET API and React Native web images
- Start SQL Server with automatic database initialization
- Seed the database with initial JA BizTown data
- Start all services with proper networking

### 2. Access the Applications

- **Frontend Web App**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **SQL Server**: localhost:1433 (SA Password: `JABizTown@2026!`)

## Service Details

### Database (SQL Server 2022)
- **Container Name**: `jabiztown-sqlserver`
- **Database**: `JABizTown`
- **Persistence**: Data volume mounted for persistence across restarts
- **Initialization**: Automatic setup via `scripts/setup.sql`
- **Health Check**: Ensures API waits for database readiness

### Backend API (.NET Core 8.0)
- **Container Name**: `jabiztown-api`
- **Framework**: .NET 8.0 with Entity Framework Core
- **Database**: SQL Server with Entity Framework migrations
- **Health Check**: `/health` endpoint
- **Logging**: Logs mounted to `./api/logs`

### Frontend (React Native for Web + Nginx)
- **Container Name**: `jabiztown-web`
- **Web Server**: Nginx with optimized configuration
- **API Proxy**: `/api/*` requests proxied to backend
- **Security**: Security headers and gzip compression enabled

## Database Schema

The Economic Engine includes the following core tables:

- **Businesses**: JA BizTown businesses with financial data
- **BankAccounts**: Account management for businesses and students
- **Roles**: Job roles with salary information
- **Students**: Student participants and their assignments
- **Transactions**: Financial transactions and economic activities

### Initial Data

The system seeds with:
- **8 Businesses**: City Bank, Tech Solutions, Healthy Foods Market, etc.
- **10 Roles**: CEO, Manager, Developer, Cashier, etc.
- **Bank Accounts**: One account per business with initial capital

## Development Commands

### Start Services
```bash
docker-compose up --build
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f web
docker-compose logs -f sqlserver
```

### Rebuild Specific Service
```bash
docker-compose up --build api
```

### Access Database
```bash
# Connect to SQL Server container
docker exec -it jabiztown-sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P JABizTown@2026!

# Once connected
USE JABizTown;
GO
SELECT * FROM Businesses;
GO
```

## Environment Variables

The `.env` file contains configurable settings:

```bash
# SQL Server Configuration
SA_PASSWORD=JABizTown@2026!

# Application Settings
ASPNETCORE_ENVIRONMENT=Development
ASPNETCORE_URLS=http://+:8080
```

## Networking

Services communicate via internal Docker network `jabiztown-network`:

- **API → Database**: `sqlserver:1433`
- **Web → API**: `api:8080` (via Nginx proxy)

## File Structure

```
JA/
├── api/
│   ├── Dockerfile                 # Multi-stage .NET build
│   ├── Data/
│   │   ├── DbInitializer.cs      # Database seeding logic
│   │   └── JABizTownDbContext.cs # EF Core context
│   └── Models/                   # Entity models
├── web-app/
│   ├── Dockerfile                # React Native + Nginx build
│   └── nginx.conf                # Nginx configuration
├── scripts/
│   └── setup.sql                 # Database initialization script
├── docker-compose.yml            # Service orchestration
├── .env                          # Environment variables
└── README.md                     # This file
```

## Troubleshooting

### Port Conflicts
If ports are already in use, modify the ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Change frontend port
  - "8081:8080"  # Change API port
```

### Database Connection Issues
1. Ensure SQL Server container is healthy: `docker-compose ps`
2. Check database logs: `docker-compose logs sqlserver`
3. Verify SA password in `.env` file

### Build Failures
1. Clear Docker cache: `docker system prune -a`
2. Rebuild from scratch: `docker-compose build --no-cache`

### Performance Issues
- Allocate more memory to Docker Desktop (recommended 4GB+)
- Ensure Docker Desktop is running with sufficient resources

## Production Considerations

For production deployment, consider:
- Using secrets management for passwords
- Implementing proper SSL/TLS certificates
- Setting up monitoring and logging aggregation
- Configuring backup strategies for SQL Server
- Implementing proper CI/CD pipelines

## Support

For issues with:
- **Docker**: Check Docker Desktop logs
- **SQL Server**: Review container logs and connection strings
- **API**: Check .NET application logs in `./api/logs`
- **Frontend**: Review Nginx configuration and build output

---

**Note**: This setup is optimized for local development and testing. For production environments, additional security and configuration measures should be implemented.

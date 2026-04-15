# JA BizTown 3.0: Umbraco Headless POC

This repository contains the containerized Umbraco 13 POC for the JA BizTown simulation redevelopment. It demonstrates a **Relational Inheritance** model for synchronizing National Master rules with Local Regional offices.

## 🏗 Architecture: Relational Library
Instead of duplicating data, this POC uses a **Library-centric** approach:
- **Simulation Master**: Acts as the "National Library," holding global rulesets and master IDs.
- **Simulation Local**: Acts as the "Regional Office," holding unique local data and a `masterSource` link to the National node.
- **Heirarchy**: This decoupling allows the National team to update global rules once and have them instantly reflected across all regional front-ends without manual data entry.

## 🚀 Getting Started
1. **Launch**: `docker compose up --build -d`
2. **Setup**: Follow the [Manual Setup Guide](manual_umbraco_setup.md) to establish the first National-to-Local link.
3. **Headless API**: Access the hydrated JSON at:
   `http://localhost:8080/umbraco/delivery/api/v1/content?expand=properties[masterSource[properties[$all]]]`

## 🔐 Credentials
- **Email**: `admin@example.com`
- **Password**: `Password123!`

## 🛠 Features
- **Delivery API**: High-performance JSON endpoints pre-configured for public access.
- **Examine Management**: Integrated search indexing for lightning-fast property expansion.
- **Dockerized Environment**: Ready for AKS/Azure deployment with SQLite persistence.

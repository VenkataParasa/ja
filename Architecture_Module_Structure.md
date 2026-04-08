# JA BizTown: Azure-Native Microservices Architecture

This document details the scalable, enterprise-grade **Microservices Architecture** proposed for the JA BizTown platform. By leveraging a Microsoft Azure cloud-native approach, we decouple the system into highly resilient, independently scalable modules. 

The architecture is built heavily around **event-driven choreography, idempotent operations, and zero-trust security** to ensure the simulation survives both massive concurrency spikes and heavy facility network drops.

---

## 1. Edge & UI Delivery Layer
The presentation layer isolates all front-end code from the backend and delivers it with edge-level global caching to guarantee near-instant load times.

*   **Azure Front Door & Premium CDN:** Acts as the global entry point. It enforces the Web Application Firewall (WAF) to block bad actors and caches static assets globally.
*   **Azure Static Web Apps:** 
    *   **Student Tablet App (PWA):** Highly responsive, offline-tolerant interface deployed on facility tablets.
    *   **JA Staff CMS & Admin Portal (SPA):** The central command interface for JA staff.
    *   **Teacher & Volunteer Dashboard (SPA):** Localized real-time monitoring interface.

---

## 2. API Gateway & Security Layer
All traffic attempting to access the backend must pass through strict centralized governance. Frontends never access databases or backend services directly.

*   **Azure API Management (APIM):** The Backend-For-Frontend (BFF). It routes traffic, transforms payloads depending on if a tablet or a desktop requested it, and enforces strict rate-limiting policies.
*   **Microsoft Entra B2C (Identity):** Manages all secure authentication, session tokens (JWT), and handles Role-Based Access Control (RBAC). APIM verifies the JWT signature before passing traffic inward.
*   **Azure Key Vault:** Centralizes all secrets, database connection strings, and certificates away from application code. Microservices access Key Vault dynamically via Azure Managed Identities.

---

## 3. Compute Layer: Domain-Driven Microservices
The backend logic is strictly divided into specialized, loosely coupled services. All services are containerized via **Docker** and orchestrated using **Azure Kubernetes Service (AKS)** (or Azure Container Apps). This allows individual modules (like Banking) to autoscale dynamically under load without wasting resources on passive modules.

1. **Transaction & Ledger Service (Core Banking)**
   *   *Responsibility:* Manages student account balances, ledger updates, direct deposits, and POS checkout logic.
   *   *Idempotency (CRITICAL):* Because tablet networks naturally fluctuate, tablets may inadvertently retry the "Pay" network request multiple times. This service accepts a unique `Idempotency-Key` (UUID) from the client header on every mutation. If a checkout request is retried, the service checks Azure Cache for Redis, recognizes the duplicated key, and returns the mathematically identical successful payload *without* charging the student's ledger a second time.
   *   *Persistence:* **Azure SQL Database** (ACID compliant, highly transactional).

2. **Configuration & Town Map Service**
   *   *Responsibility:* Serves the static definitions of BizTown (which businesses are active, job capacities, supply-line requirements).
   *   *Persistence:* **Azure Cosmos DB** (NoSQL schema allows entirely dynamic JSON facility layouts without schema migrations).

3. **Gamification & AI hook Service (Phase 2 Focus)**
   *   *Responsibility:* Tracks student XP, unlocks achievements, and acts as the broker to **Azure OpenAI** for generative business slogans to prevent direct exposure of LLM keys to the client.
   *   *Persistence:* In-memory or Cosmos DB (Ephemeral data footprint).

4. **Analytics & Reporting Service**
   *   *Responsibility:* Generates end-of-day printouts, structures historical data queries for Power BI, and builds offline PDF fallbacks.
   *   *Persistence:* Reads from a **Read-Replica** of Azure SQL to prevent heavy BI queries from locking rows or slowing down the core Transaction Service. 

5. **Notification & Websocket Service**
   *   *Responsibility:* Pushes real-time alerts (e.g., "Town Hall Meeting in 5 minutes! or "Inventory low!") directly to tablets and teacher dashboards.
   *   *Technology:* **Azure Web PubSub** or SignalR.

---

## 4. Asynchronous Event-Bus Layer
To ensure the tablets remain lightning-fast, synchronous "blocking" logic is avoided wherever possible. The microservices utilize an **Event-Driven Choreography Pattern**.

*   **Azure Service Bus:** Acts as the central nervous system. 
    *   *Example Flow:* When a student buys a product, the *Transaction Service* instantly deducts the money and returns a "200 Success" to the tablet. Behind the scenes, it publishes a `ProductPurchased` event onto the Service Bus.
    *   The *Reporting Service* and *Gamification Service* asynchronously consume this event from the bus at their own pace to deduct warehouse inventory and grant the student XP points. If the Gamification service crashes, the core banking checkout workflow is entirely unaffected.

---

## 5. Observability & Resilience
*   **Azure Monitor & Application Insights:** Injects a "Correlation ID" into the header of every request the moment it hits Azure Front Door. This ID travels through APIM, across the Service Bus, and into every microservice, allowing engineers to trace a single transaction flawlessly across the entire distributed architecture.
*   **Retry Policies & Circuit Breakers:** Employed heavily at the APIM and AKS egress levels (via libraries like Polly). If a downstream dependency fails repeatedly, the circuit breaker "trips" and returns a graceful fallback error to the student tablet rather than causing cascading timeouts.

---

## 6. Technology Stack Summary

| Technology | One-Line Summary |
|---|---|
| **React / React Native** | Cross-platform UI framework for building the Student PWA and Admin SPAs. |
| **Azure Front Door & CDN** | Global edge entry point that caches static assets and blocks malicious traffic via WAF. |
| **Azure Static Web Apps** | Serverless hosting for all front-end SPAs with built-in CI/CD and free SSL. |
| **Azure API Management (APIM)** | Centralized API gateway that routes, rate-limits, and transforms traffic between frontends and backend microservices. |
| **Microsoft Entra B2C** | Enterprise-grade identity provider managing authentication, JWT tokens, and role-based access for all users. |
| **Azure Key Vault** | Secure vault for storing all application secrets, database credentials, and certificates away from source code. |
| **Docker** | Containerizes each microservice for consistent, reproducible builds across local dev and cloud environments. |
| **Azure Kubernetes Service (AKS)** | Orchestrates and autoscales Docker containers in production based on real-time traffic demand. |
| **Azure SQL Database** | ACID-compliant relational database for all financial transactions and student ledgers. |
| **Azure Cosmos DB** | Schema-flexible NoSQL document store for dynamic BizTown configuration and facility layout data. |
| **Azure Cache for Redis** | In-memory store used to track Idempotency Keys and prevent duplicate financial transactions from network retries. |
| **Azure OpenAI** | Managed LLM gateway for generative features like business slogan creation and speech-to-text transcription *(Phase 2)*. |
| **Azure Web PubSub / SignalR** | Real-time WebSocket push for live simulation events (Tornado alerts, Town Hall notifications) to tablets and dashboards. |
| **Azure Service Bus** | Asynchronous message broker decoupling microservices so banking transactions never block gamification or reporting. |
| **Azure Monitor & App Insights** | Distributed tracing and telemetry platform injecting Correlation IDs across all services for end-to-end observability. |
| **Polly (Circuit Breaker)** | Resilience library enforcing retry policies and circuit-breaking at the service mesh level to prevent cascading failures. |
| **Microsoft Power BI** | Business intelligence layer for historical simulation analytics and end-of-day reporting dashboards. |

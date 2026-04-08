import pandas as pd

data = [
    {
        'Layer': 'UI / Frontend',
        'Technology': 'React / React Native',
        'Purpose': 'Cross-platform UI for Student PWA, Admin SPA, Teacher Dashboard',
        'Rationale': 'Single codebase targets both tablet (React Native) and web (React), reducing team size and accelerating development velocity.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Edge & Delivery',
        'Technology': 'Azure Front Door & CDN',
        'Purpose': 'Global edge entry point, WAF, static asset caching',
        'Rationale': 'Provides DDoS protection, WAF rules, and globally distributed caching so tablets load instantly regardless of facility location.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Edge & Delivery',
        'Technology': 'Azure Static Web Apps',
        'Purpose': 'Serverless hosting for all frontend SPAs',
        'Rationale': 'Zero server management, built-in CI/CD from GitHub, free SSL certificates, and automatic preview environments per pull request.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'API Gateway & Security',
        'Technology': 'Azure API Management (APIM)',
        'Purpose': 'BFF Gateway: routing, rate-limiting, payload transformation',
        'Rationale': 'Single entry point for all backend traffic. Enforces rate limits during peak simulation hours and transforms payloads between tablet and desktop clients.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'API Gateway & Security',
        'Technology': 'Microsoft Entra B2C',
        'Purpose': 'Identity, authentication, JWT tokens, RBAC',
        'Rationale': 'Microsoft-native, enterprise-grade identity. Handles student, teacher, staff, and admin roles with zero custom auth code. JWT tokens verified at APIM before reaching any microservice.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'API Gateway & Security',
        'Technology': 'Azure Key Vault',
        'Purpose': 'Secrets, certificates, and connection strings management',
        'Rationale': 'Removes all sensitive credentials from application code. Microservices access secrets dynamically via Managed Identities, achieving zero-secret-in-code compliance.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Compute / Infrastructure',
        'Technology': 'Docker',
        'Purpose': 'Containerization of all microservices for consistent builds',
        'Rationale': 'Ensures identical environments across local dev, CI build, and cloud deployment - eliminating environment-specific bugs entirely.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Compute / Infrastructure',
        'Technology': 'Azure Kubernetes Service (AKS)',
        'Purpose': 'Container orchestration and autoscaling in production',
        'Rationale': 'Dynamically scales the Banking service during simulation peaks without scaling idle services. Supports rolling updates with zero downtime deployments.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Data Persistence',
        'Technology': 'Azure SQL Database',
        'Purpose': 'Core financial ledger, transactions, student accounts',
        'Rationale': 'ACID-compliant relational database ensuring no money is double-spent or lost. The right tool where data integrity is non-negotiable (banking, POS, payroll).',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Data Persistence',
        'Technology': 'Azure Cosmos DB',
        'Purpose': 'BizTown configuration, facility layouts, gamification data',
        'Rationale': 'Flexible JSON document model allows JA staff to define dynamic configurations without schema migrations. Low-latency reads serve 30+ tablets simultaneously.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Data Persistence',
        'Technology': 'Azure Cache for Redis',
        'Purpose': 'Idempotency key tracking, session caching',
        'Rationale': 'Sub-millisecond in-memory store used to deduplicate retried POS payment requests from tablets on unstable networks, preventing students from being double-charged.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Real-Time Communication',
        'Technology': 'Azure Web PubSub / SignalR',
        'Purpose': 'Live WebSocket push for simulation events to tablets & dashboards',
        'Rationale': 'Enables instant broadcasting of admin-triggered events (Tornado Alerts, Town Hall, Price Shocks) to all connected devices without polling.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Async Messaging',
        'Technology': 'Azure Service Bus',
        'Purpose': 'Event-driven choreography between microservices',
        'Rationale': 'Decouples banking from gamification and reporting. A crashed Gamification service never blocks a student checkout. Guarantees at-least-once message delivery.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Analytics & BI',
        'Technology': 'Microsoft Power BI',
        'Purpose': 'End-of-day simulation reporting and historical analytics',
        'Rationale': 'Azure-native BI tool requiring no additional licensing beyond existing Microsoft agreements. Pre-built Azure SQL connectors reduce integration effort significantly.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Observability',
        'Technology': 'Azure Monitor & Application Insights',
        'Purpose': 'Distributed tracing, telemetry, alerting across all microservices',
        'Rationale': 'Injects a Correlation ID at the edge that traces a single student transaction across APIM, Service Bus, and every backend service for rapid root-cause analysis.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'Resilience',
        'Technology': 'Polly (Circuit Breaker)',
        'Purpose': 'Retry policies and circuit-breaking at service mesh level',
        'Rationale': 'Prevents cascading failures: if the Gamification service is slow, Polly trips the circuit and returns a graceful degraded response to the tablet rather than hanging indefinitely.',
        'Phase': 'Phase 1'
    },
    {
        'Layer': 'AI / ML (Optional)',
        'Technology': 'Azure OpenAI',
        'Purpose': 'Business slogan generation, speech-to-text transcription',
        'Rationale': 'Microsoft-managed LLM endpoint keeps API keys server-side and off tablets. Adds generative AI capabilities as a Phase 2 enhancement without architectural restructuring.',
        'Phase': 'Phase 2 (Optional)'
    },
]

df = pd.DataFrame(data)
writer = pd.ExcelWriter('D:\\Venkata\\JA\\Technology Stack.xlsx', engine='openpyxl')
df.to_excel(writer, index=False, sheet_name='Technology Stack')
writer.close()
print('Done: Technology Stack.xlsx created')

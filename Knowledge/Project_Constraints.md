# JA BizTown 3.0: Project Constraints & Reference Guide

This document centralizes all budget, technical, and operational constraints derived from the RFP, Architecture documentation, and official Q&A responses.

## 1. Budget & Scope Constraints

| Constraint | Value / Detail | Source |
| :--- | :--- | :--- |
| **Total Budget Cap** | **$1,000,000** (Strict cap for initial release) | [QA Responses (Q25)](file:///d:/Venkata/JA/qa_responses.txt#L646) |
| **Simulation Timing** | **4.5 Hours** total simulation day | [RFP Summary](file:///d:/Venkata/JA/rfp_text.txt#L216) |
| **Device Model** | **One-device-per-user** (1:1 student-to-tablet) | [QA Responses (Q23)](file:///d:/Venkata/JA/qa_responses.txt#L615) |
| **Pilot Scale** | 10–15 Areas; 3–5 simulations/Area; 80–150 students/sim | [QA Responses (Q9)](file:///d:/Venkata/JA/qa_responses.txt#L243) |
| **Target Audience** | Grades 5-6 (Ages 9-12) | [RFP Summary](file:///d:/Venkata/JA/rfp_text.txt#L286) |

---

## 2. Technical Performance Targets (SLA)

> [!IMPORTANT]
> Failure to meet these latency and throughput targets will directly impact simulation "realism" and educational value.

*   **Transaction Throughput:** **50–100 transactions per second** during peak load.
*   **Latency Threshold:** Cross-system updates must occur within **1–2 seconds**.
*   **Availability SLA:** **100% Uptime** during peak simulation hours (Mon-Fri, 8 AM - 7 PM ET).
*   **Sync Logic:** "Local-first" operation required; transactions must queue when WiFi is spotty and sync seamlessly upon restoration.

**References:**
*   [Performance Benchmarks](file:///d:/Venkata/JA/qa_responses.txt#L182-187)
*   [Latency Thresholds](file:///d:/Venkata/JA/qa_responses.txt#L373)
*   [Availability SLA](file:///d:/Venkata/JA/qa_responses.txt#L119)
*   [Network Resilience](file:///d:/Venkata/JA/qa_responses.txt#L462)

---

## 3. Architecture & Security Policy

*   **Platform:** **Azure-Native Microservices** (AKS/API Management/Cosmos DB).
*   **Rate-Limiting:** Enforced at the **API Management (APIM)** layer to prevent flooding.
*   **Idempotency:** Required for all financial mutations to prevent duplicate charges during network retries.
*   **Privacy:** No collection of student email addresses or personally identifying information (PII) to simplify FERPA/COPPA compliance.

**References:**
*   [Architecture Structure](file:///d:/Venkata/JA/Architecture_Module_Structure.md#L23)
*   [Privacy Policy Clarification](file:///d:/Venkata/JA/qa_responses.txt#L684)

---

## 4. Content & AI Guardrails

*   **AI Character Scaffolding:** 
    *   Slogan generation must be "guided" (template-based).
    *   **Three-attempt limit** for retrying AI generations.
    *   *No general-purpose chatbots allowed.*
*   **CMS Field Limits:**
    *   Survey Prompts: **125 characters** max.
    *   Response Options: **25 characters** max.
*   **Customization:** Local Areas typically manage **100-150 job roles**.

**References:**
*   [AI Guardrails](file:///d:/Venkata/JA/qa_responses.txt#L85), [L577](file:///d:/Venkata/JA/qa_responses.txt#L577)
*   [CMS Character Limits](file:///d:/Venkata/JA/rfp_text.txt#L767-L770)
*   [Role Customization](file:///d:/Venkata/JA/qa_responses.txt#L139)

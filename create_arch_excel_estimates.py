import pandas as pd

def create_excel(filename, data, notes):
    columns = ["", "Phase", "Feature (Module Area)", "Hours", "Cost", "Team", "Comments"]
    df = pd.DataFrame(data, columns=columns)
    
    empty_row = ["", "", "", "", "", "", ""]
    notes_rows = [empty_row, ["", "Notes", "", "", "", "", ""]]
    for note in notes:
        notes_rows.append(["", note, "", "", "", "", ""])
    
    df = pd.concat([df, pd.DataFrame(notes_rows, columns=columns)], ignore_index=True)
    
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.close()

def main():
    rate = 65
    
    # ----------------------------------------------------
    # PHASE 1: CORE MVP EXACTLY MAPPED TO ARCHITECTURE
    # ----------------------------------------------------
    phase1_data = [
        ["", "Phase 1: Core MVP", "Foundation - Requirements Analysis & Technical Discovery", 40, 40*rate, "PM, SA", "Mapping RFP requirements to System logic"],
        ["", "", "Foundation - Architecture & Database Schema Design", 30, 30*rate, "SA", "Designing Microservices topography"],
        ["", "", "Foundation - Azure Cloud Environment Setup & CI/CD Pipelines", 70, 70*rate, "DevOps", "3 secure target environments (Dev, Staging, Prod)"],
        ["", "", "Foundation - Local Developer Testing Setup (Docker Compose)", 40, 40*rate, "DevOps, BE", "Containerized local-dev hooks for frictionless builds"],
        ["", "", "Layer 1: Edge & UI - UX Conceptualization, Visual Identity, WCAG 2.2 AA", 130, 130*rate, "Designer, FE", "Core flow designs"],
        ["", "", "Layer 1: Edge & UI - Student Tablet Mobile Application (PWA)", 260, 260*rate, "FE", "Core banking flows, Civic Voting Module, POS checkout UX, QR Scanning"],
        ["", "", "Layer 1: Edge & UI - Teacher & Volunteer Monitoring Dashboard", 80, 80*rate, "FE", "Real-time read-only oversight metrics"],
        ["", "", "Layer 1: Edge & UI - Admin Core: User Mgmt, Roles, Controls & Moderation Flows", 120, 120*rate, "FE, BE", "Secure CMS for Staff routing, localization, configuration moderation"],
        ["", "", "Layer 1: Edge & UI - Admin Automation: Real-time Event Controllers", 60, 60*rate, "FE, BE", "UI event creation dispatch (e.g. Town Hall, Tornado Alert triggers)"],
        ["", "", "Layer 2: API Gateway & Security - APIM (BFF) & Entra B2C Auth Setup", 120, 120*rate, "SA, BE", "Token auth, Rate Limiting, Zero Trust architecture"],
        ["", "", "Layer 3: Compute - Transaction & Ledger Service (Core Banking Engine)", 210, 210*rate, "BE", "SQL persistence, Idempotency tracking"],
        ["", "", "Layer 3: Compute - Configuration & Town Map Service", 60, 60*rate, "BE", "Cosmos DB configuration bindings"],
        ["", "", "Layer 3: Compute - Basic Gamification Progression Service (No AI)", 60, 60*rate, "BE", "Standard progression APIs (Integrates with Admin Controller triggers)"],
        ["", "", "Layer 3: Compute - Analytics & Reporting Service", 80, 80*rate, "BE, Data", "Read-replica historical reports"],
        ["", "", "Layer 4: Async Event-Bus - Azure Service Bus Provisioning", 50, 50*rate, "DevOps, BE", "Event choreography messaging infrastructure"],
        ["", "", "Layer 5: Observability & Validation - QA, Load Tests, App Insights, Store Deployment", 270, 270*rate, "QA, Sec, PM", "E2E bugs, Distributed Tracing integration"],
    ]

    # ----------------------------------------------------
    # PHASE 2: OPTIONAL EXACTLY MAPPED TO ARCHITECTURE
    # ----------------------------------------------------
    phase2_data = [
        ["", "Phase 2: Nice to Have", "Layer 1: Edge & UI - Extensive External Hardware SDK Integrations", 180, 180*rate, "FE, QA", "Physical NFC tags, ePOS Swipers, Radio Hook"],
        ["", "", "Layer 3: Compute - Cutting-Edge AI Integrations / Gateway Hook", 100, 100*rate, "BE, Designer", "Azure OpenAI business slogans, speech-to-text"],
        ["", "", "Layer 3: Compute - True Offline Synchronization Resolution Logic", 100, 100*rate, "BE, FE, SA", "Heavy conflict engine for extreme network outage"],
        ["", "", "Layer 3: Compute - Intricate Gamification & Supply Line Math", 130, 130*rate, "BE, QA", "Granular logistics depletion, real-time demand engines"],
        ["", "", "Layer 3: Compute - Automated Dynamic PDF Generation Engine", 70, 70*rate, "FE, BE", "Code-driven offline paper backups"],
        ["", "", "Layer 5: Observability & Scale - Expanded Enterprise Environments", 40, 40*rate, "DevOps", "Dedicated segregated QA cluster setup"],
    ]

    # --- OPTION A: Full RFP (Phase 1 + Phase 2) ---
    option_a_data = list(phase1_data) + list(phase2_data)
    
    dev_hours_a = sum([row[3] for row in option_a_data if type(row[3]) in (int, float)])
    pm_hours_a = int(dev_hours_a * 0.1)
    sub_total_a_hours = dev_hours_a + pm_hours_a
    total_a_cost = sub_total_a_hours * rate
    
    option_a_data.extend([
        ["", "", "", "", "", "", ""],
        ["", "", "Sub-Total", dev_hours_a, dev_hours_a*rate, "", ""],
        ["", "", "PM (10%)", pm_hours_a, pm_hours_a*rate, "", ""],
        ["", "", "Year 1 Support (Hyper-Care & Maintenance)", 1200, 1200*rate, "1 FTE", "Post-launch monitoring"],
        ["", "", "Total", sub_total_a_hours + 1200, (sub_total_a_hours + 1200)*rate, "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "Man Months", round(sub_total_a_hours / 160, 1), "", "", "Based on 160h/month"]
    ])
    
    option_a_notes = [
        "These estimates represent the FULL Scope (Option A), categorised by the Microservices Architecture SDLC.",
        "Total Core Dev Hours: 1680. Total Phase 2 / Optional Dev Hours: 620. Total: 2300 Dev Hours."
    ]

    create_excel("D:\\Venkata\\JA\\Estimates - Option A (Architecture Mapped) v4.xlsx", option_a_data, option_a_notes)
    
    
    # --- OPTION B: MVP Only (Phase 1) ---
    option_b_data = list(phase1_data)
    
    dev_hours_b = sum([row[3] for row in option_b_data if type(row[3]) in (int, float)])
    pm_hours_b = int(dev_hours_b * 0.1)
    sub_total_b_hours = dev_hours_b + pm_hours_b
    total_b_cost = sub_total_b_hours * rate
    
    option_b_data.extend([
        ["", "", "", "", "", "", ""],
        ["", "", "Sub-Total", dev_hours_b, dev_hours_b*rate, "", ""],
        ["", "", "PM (10%)", pm_hours_b, pm_hours_b*rate, "", ""],
        ["", "", "Year 1 Support (Hyper-Care & Maintenance)", 1200, 1200*rate, "1 FTE", "Post-launch monitoring"],
        ["", "", "Total", sub_total_b_hours + 1200, (sub_total_b_hours + 1200)*rate, "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "Man Months", round(sub_total_b_hours / 160, 1), "", "", "Based on 160h/month"]
    ])
    
    option_b_notes = [
        "These estimates represent the core MVP ONLY (Option B), strictly categorised by the essential Azure Microservices.",
        "Mobile App, Admin Staff Portals (Controls, Tornado Events, User Mgmt), and SDLC processes are distinctly itemized for transparency."
    ]

    create_excel("D:\\Venkata\\JA\\Estimates - Option B (Architecture Mapped) v4.xlsx", option_b_data, option_b_notes)

if __name__ == "__main__":
    main()

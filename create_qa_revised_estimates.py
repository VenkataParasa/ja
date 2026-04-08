import pandas as pd
import math

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

    # ============================================================
    # PHASE 1: CORE MVP  (Q&A-adjusted)
    # ============================================================
    # Key Q&A changes:
    # - Business Scenarios/Character Education = MUST be Phase 1 (Q16 - grant funded)
    # - Offline local-first = MUST be Phase 1 (Q7, Q15, Q133 - JA explicitly required it)
    # - Canva-like Digital Marketing Tool = MVP (Q13)
    # - Real-time Screen Sharing (CFO) = required (Q14, Q131)
    # - DJ Radio Dashboard = required feature (Q17)
    # - 10-15K concurrent users / 60-70 simulations = infra impact (Q125/Q126)
    # - Data anonymization (30 day) = needed (Q110)
    # - Physical debit card reader support = needed (Q137)
    # - Single app (tablet + laptop compatible) = required (Q139/Q140)
    # - Student = session-based (simplifies auth) (Q71)

    phase1_data = [
        # --- FOUNDATION ---
        ["", "Phase 1: Core MVP", "Foundation - Requirements Analysis & Technical Discovery", 40, 40*rate, "PM, SA", "Q2: Discovery substantially done by JA -- vendor refines execution"],
        ["", "", "Foundation - Architecture & Database Schema Design", 40, 40*rate, "SA", "Q125/Q126: Must support 10-15K concurrent users / 60-70 parallel simulations"],
        ["", "", "Foundation - Azure Cloud Env Setup & CI/CD Pipelines (3 Envs)", 80, 80*rate, "DevOps", "Q57: JA will work with vendor to deploy architecture into JA environment"],
        ["", "", "Foundation - Local Developer Testing Setup (Docker Compose)", 40, 40*rate, "DevOps, BE", "Containerized local-dev hooks for frictionless developer builds"],
        ["", "", "Foundation - Data Anonymization Engine (30-day COPPA rule)", 30, 30*rate, "BE, SA", "Q110: Anonymization process required after simulation reaches 30 days"],

        # --- LAYER 1: UI ---
        ["", "", "Layer 1: UI - UX Conceptualization, Style Tiles, WCAG 2.2 AA", 130, 130*rate, "Designer, FE", "Q18: 2.5D or isometric, TBD. Q40: 3rd grade reading level. Mood boards required"],
        ["", "", "Layer 1: UI - Core Tablet + Laptop App (Single Codebase PWA)", 280, 280*rate, "FE", "Q139: Single app, tablet primary; Q140: portrait AND landscape support"],
        ["", "", "Layer 1: UI - Student Role UIs (POS, Payroll, Banking, Billing, Voting)", 160, 160*rate, "FE", "Q22/Q38: Different UIs per role function (POS, CFO Payroll, etc.) not visual themes"],
        ["", "", "Layer 1: UI - Teacher & Volunteer Real-Time Monitoring Dashboard", 80, 80*rate, "FE", "Q24/Q48: Real-time business health visibility - No alert rules engine needed"],
        ["", "", "Layer 1: UI - Admin Core: User Mgmt, Roles, Moderation & Controls", 120, 120*rate, "FE, BE", "Q37: Simulation Managers, Volunteers, Educators as distinct roles"],
        ["", "", "Layer 1: UI - Admin Automation: Real-time Event Controllers (Town Hall, Tornado)", 60, 60*rate, "FE, BE", "Staff controls for live simulation event dispatch to all tablets"],
        ["", "", "Layer 1: UI - CMS National + Local Config (Inheritance Model)", 200, 200*rate, "FE, BE", "Q6/Q128: Local Area inherits national config. Local overrides take precedence"],
        ["", "", "Layer 1: UI - Canva-Like Digital Marketing Tool (Template-based)", 120, 120*rate, "FE, BE", "Q13/Q135: Step-by-step mission, templates, text edit, image library, publish/display"],
        ["", "", "Layer 1: UI - CFO Real-Time Screen Sharing (14-20 concurrent sessions)", 80, 80*rate, "FE, BE", "Q14/Q131: Mirror CFO device to teammates; no audio. Azure Web PubSub"],
        ["", "", "Layer 1: UI - DJ Radio Dashboard (Playlist, Mic Announcements)", 60, 60*rate, "FE", "Q17: Built-in DJ UI; plays to A/V system; wide variety of setups supported"],

        # --- LAYER 2: API GATEWAY ---
        ["", "", "Layer 2: API Gateway - APIM, Entra B2C Auth (Session-based Students)", 100, 100*rate, "SA, BE", "Q71/Q116: Students are session-based. Simpler auth. Q60: Vendor manages CI/CD perms"],

        # --- LAYER 3: BACKEND MICROSERVICES ---
        ["", "", "Layer 3: Compute - Transaction & Ledger Service (50-100 TPS capable)", 240, 240*rate, "BE", "Q7/Q59: 500 transactions per 10-min window; 50-100 TPS; Idempotency critical"],
        ["", "", "Layer 3: Compute - Offline Local-First Queue & Sync Engine", 150, 150*rate, "BE, FE, SA", "Q7/Q15/Q133: Explicitly required. Queue transactions locally, sync on reconnect"],
        ["", "", "Layer 3: Compute - Configuration & Town Map Service (Cosmos DB)", 70, 70*rate, "BE", "Q31/Q62: Businesses and job roles are unique per Area. Local Areas create new workflows"],
        ["", "", "Layer 3: Compute - Business Scenarios & Character Education Engine", 90, 90*rate, "BE", "Q16: MUST be MVP - grant-funded requirement. Ethical dilemmas, XP consequences"],
        ["", "", "Layer 3: Compute - Physical Debit Card Reader Integration", 70, 70*rate, "FE, BE", "Q137: Current system uses physical debit cards coded with 3-digit account numbers"],
        ["", "", "Layer 3: Compute - Gamification & XP Engine (with JA-defined rules)", 80, 80*rate, "BE", "Q51: JA provides actions, vendor designs formula collaboratively"],
        ["", "", "Layer 3: Compute - Reporting Service (In-app + PDF + CMS Export)", 100, 100*rate, "BE, Data", "Q72/Q122/Q123: In-app dashboards, PDF reports, export for Power BI"],
        ["", "", "Layer 3: Compute - Sponsor Tracking & Analytics Service", 40, 40*rate, "BE, Data", "Q127: Track students per business, sales prices, marketing assets per sponsor"],

        # --- LAYER 4: ASYNC EVENT BUS ---
        ["", "", "Layer 4: Async Event-Bus - Azure Service Bus (transactions, events)", 50, 50*rate, "DevOps, BE", "Decouples banking from gamification, notifications, and reporting"],

        # --- LAYER 5: OBSERVABILITY & DELIVERY ---
        ["", "", "Layer 5: Observability - App Insights, Distributed Tracing, DR State Recovery", 60, 60*rate, "DevOps, BE", "Q143: Full state recovery after failure; simulations resume from exact prior state"],
        ["", "", "Layer 5: Testing - QA, WCAG Audit (3rd party), Load to 10-15K users", 180, 180*rate, "QA, Sec", "Q8/Q46: JA has 3rd-party auditor. Load testing for 60-70 concurrent simulations"],
        ["", "", "Layer 5: Delivery - App Store (iOS/Android), MDM compat, JA User Training Manuals", 90, 90*rate, "PM, SA, DevOps", "Q74: App store + MDM dual distribution. Q42: Admin CMS + Simulation user guides"],
    ]

    # ============================================================
    # PHASE 2: OPTIONAL (confirmed nice-to-have via Q&A)
    # ============================================================
    # - AI features (slogan + speech-to-text) = flexible for pilot (Q136), keep Phase 2
    # - NFC = confirmed nice-to-have (Q19/Q138)
    # - Paper fallback = not needed if offline works (Q134)
    # - Dynamic PDF generator = not required
    # - 4th dedicated QA environment = optional

    phase2_data = [
        ["", "Phase 2: Nice to Have", "AI - Slogan Generation (Azure OpenAI, 3-strike guardrails)", 100, 100*rate, "BE, Designer", "Q20/Q136: Guided scaffolded generation. Age-appropriate. Flexible for pilot"],
        ["", "", "AI - CEO Speech-to-Text Transcription & Display", 60, 60*rate, "BE, FE", "Q20: Transcription only (not AI writing). Student expression support"],
        ["", "", "Layer 1: UI - NFC Tap-to-Pay Integration (iOS + Android cross-platform)", 130, 130*rate, "FE, QA", "Q19/Q138: Nice-to-have. Cross-platform NFC + graceful QR fallback"],
        ["", "", "Layer 3: Compute - Advanced Gamification & Supply Chain Depletion Math", 100, 100*rate, "BE, QA", "Complex depletion logistics beyond unlimited stock assumption"],
        ["", "", "Layer 5: Observability - Expanded Dedicated QA Environment", 40, 40*rate, "DevOps", "4th segregated environment beyond Dev/Staging/Prod"],
    ]

    # --- OPTION A: Full RFP ---
    option_a_data = list(phase1_data) + list(phase2_data)
    dev_hours_a = sum([row[3] for row in option_a_data if type(row[3]) in (int, float)])
    pm_hours_a = int(dev_hours_a * 0.1)
    sub_total_a = dev_hours_a + pm_hours_a
    option_a_data.extend([
        ["", "", "", "", "", "", ""],
        ["", "", "Sub-Total Dev", dev_hours_a, dev_hours_a*rate, "", ""],
        ["", "", "PM (10%)", pm_hours_a, pm_hours_a*rate, "", ""],
        ["", "", "Year 1 Support (Hyper-Care & Maintenance)", 1200, 1200*rate, "1 FTE", "Post-launch monitoring"],
        ["", "", "Total", sub_total_a + 1200, (sub_total_a + 1200)*rate, "", f"NOTE: $1M budget cap per Q&A #25"],
        ["", "", "Man Months", round(sub_total_a / 160, 1), "", "", "Based on 160h/month"],
    ])
    option_a_notes = [
        "UPDATED based on full Q&A review (143 questions).",
        "Key changes: Business Scenarios moved to Phase 1 (Q16 - grant requirement).",
        "Offline Local-First Sync moved to Phase 1 (Q7/Q133 - JA explicitly required).",
        "Added: Canva Digital Marketing Tool (Q13), CFO Screen Sharing (Q14), DJ Radio (Q17).",
        "Added: Physical Debit Card Reader (Q137), Data Anonymization 30-day (Q110).",
        "Added: Sponsor Tracking Service (Q127), 10-15K concurrent user load testing (Q125).",
        "BUDGET CONSTRAINT: JA confirmed $1M cap for initial release (Q25).",
    ]
    create_excel("D:\\Venkata\\JA\\Estimates - Option A (Q&A Revised).xlsx", option_a_data, option_a_notes)

    # --- OPTION B: MVP Only ---
    option_b_data = list(phase1_data)
    dev_hours_b = sum([row[3] for row in option_b_data if type(row[3]) in (int, float)])
    pm_hours_b = int(dev_hours_b * 0.1)
    sub_total_b = dev_hours_b + pm_hours_b
    option_b_data.extend([
        ["", "", "", "", "", "", ""],
        ["", "", "Sub-Total Dev", dev_hours_b, dev_hours_b*rate, "", ""],
        ["", "", "PM (10%)", pm_hours_b, pm_hours_b*rate, "", ""],
        ["", "", "Year 1 Support (Hyper-Care & Maintenance)", 1200, 1200*rate, "1 FTE", "Post-launch monitoring"],
        ["", "", "Total", sub_total_b + 1200, (sub_total_b + 1200)*rate, "", f"NOTE: $1M budget cap per Q&A #25"],
        ["", "", "Man Months", round(sub_total_b / 160, 1), "", "", "Based on 160h/month"],
    ])
    option_b_notes = [
        "UPDATED based on full Q&A review (143 questions).",
        "Phase 1 MVP now explicitly includes: Offline Sync, Business Scenarios, Canva Marketing Tool.",
        "Phase 1 MVP now explicitly includes: CFO Screen Sharing, DJ Radio Dashboard, Debit Card support.",
        "Phase 2 retains: AI Slogan/Speech (Q136 - flexible), NFC (Q19 - nice to have), Advanced Gamification.",
        "BUDGET CONSTRAINT: JA confirmed $1M cap for initial release (Q25).",
    ]
    create_excel("D:\\Venkata\\JA\\Estimates - Option B (Q&A Revised).xlsx", option_b_data, option_b_notes)

if __name__ == "__main__":
    main()

import pandas as pd
import math

def create_three_point_excel(filename):
    """
    Three-Point Estimation using PERT (Program Evaluation and Review Technique)
    
    Optimistic (O):  Best case - requirements clear, no blockers, experienced team
    Most Likely (M): Realistic - normal dev friction, minor unknowns
    Pessimistic (P): Worst case - scope creep, integration issues, hardware delays
    
    PERT Expected Value: E = (O + 4M + P) / 6
    PERT Std Deviation:  SD = (P - O) / 6
    """
    
    rate = 65
    
    line_items = [
        # (Label, Phase, O_hours, M_hours, P_hours, Team, Comments)
        ("Foundation - Requirements Analysis & Technical Discovery",         "Phase 1: Core MVP",        30,  40,  60,  "PM, SA",       "Scope clarity risk: RFP has ambiguous areas"),
        ("Foundation - Architecture & Database Schema Design",               "Phase 1: Core MVP",        25,  30,  45,  "SA",           "Schema complexity may increase with gamification data"),
        ("Foundation - Azure Cloud Environment Setup & CI/CD Pipelines",     "Phase 1: Core MVP",        50,  70,  100, "DevOps",       "Azure subscription + permissions can cause delays"),
        ("Foundation - Local Developer Testing Setup (Docker Compose)",      "Phase 1: Core MVP",        30,  40,  55,  "DevOps, BE",   "Service interdependencies can complicate local setup"),
        ("Layer 1: Edge & UI - UX Conceptualization, Visual Identity",       "Phase 1: Core MVP",        100, 130, 180, "Designer, FE", "Stakeholder feedback loops can stretch design cycles"),
        ("Layer 1: Edge & UI - Student Tablet Mobile Application (PWA)",     "Phase 1: Core MVP",        200, 260, 360, "FE",           "POS, QR, offline caching add mobile complexity"),
        ("Layer 1: Edge & UI - Teacher & Volunteer Monitoring Dashboard",    "Phase 1: Core MVP",        60,  80,  110, "FE",           "Real-time data binding and WebSocket integration risk"),
        ("Layer 1: Edge & UI - Admin Core: User Mgmt, Roles, Moderation",   "Phase 1: Core MVP",        90,  120, 170, "FE, BE",       "Complex RBAC flows often have edge case bugs"),
        ("Layer 1: Edge & UI - Admin Automation: Event Controllers",         "Phase 1: Core MVP",        45,  60,  90,  "FE, BE",       "Real-time event broadcasting integration risk"),
        ("Layer 2: API Gateway & Security - APIM & Entra B2C Auth",         "Phase 1: Core MVP",        90,  120, 170, "SA, BE",       "B2C custom flows and APIM policies can be finicky"),
        ("Layer 3: Compute - Transaction & Ledger Service (Core Banking)",   "Phase 1: Core MVP",        160, 210, 300, "BE",           "Idempotency logic and ledger integrity are high-risk areas"),
        ("Layer 3: Compute - Configuration & Town Map Service",              "Phase 1: Core MVP",        45,  60,  85,  "BE",           "Cosmos DB schema design relatively straightforward"),
        ("Layer 3: Compute - Basic Gamification Progression Service",        "Phase 1: Core MVP",        45,  60,  90,  "BE",           "Progression rules may expand based on JA feedback"),
        ("Layer 3: Compute - Analytics & Reporting Service",                 "Phase 1: Core MVP",        60,  80,  120, "BE, Data",     "Read-replica setup and BI formatting take iteration"),
        ("Layer 4: Async Event-Bus - Azure Service Bus Provisioning",        "Phase 1: Core MVP",        35,  50,  75,  "DevOps, BE",   "Message topic design needs careful upfront planning"),
        ("Layer 5: Observability & Validation - QA, AppInsights, Deployment","Phase 1: Core MVP",       210, 270, 390, "QA, Sec, PM",  "Bug count varies heavily with integration scope"),
        ("Layer 1: Edge & UI - External Hardware SDK Integrations",          "Phase 2: Nice to Have",   130, 180, 280, "FE, QA",       "NFC/ePOS SDK docs are often poorly maintained"),
        ("Layer 3: Compute - AI Integrations (Azure OpenAI)",                "Phase 2: Nice to Have",   70,  100, 160, "BE, Designer", "LLM prompt engineering requires many iterations"),
        ("Layer 3: Compute - True Offline Synchronization Logic",            "Phase 2: Nice to Have",   70,  100, 170, "BE, FE, SA",   "Conflict resolution edge cases are notoriously complex"),
        ("Layer 3: Compute - Intricate Gamification & Supply Line Math",     "Phase 2: Nice to Have",   90,  130, 200, "BE, QA",       "Logistics math requires extensive domain modeling"),
        ("Layer 3: Compute - Automated Dynamic PDF Generation Engine",       "Phase 2: Nice to Have",   50,  70,  110, "FE, BE",       "PDF layout precision across devices adds edge cases"),
        ("Layer 5: Observability - Expanded Enterprise Environments",        "Phase 2: Nice to Have",   30,  40,  65,  "DevOps",       "Additional env provisioning is well-understood work"),
    ]
    
    rows = []
    for label, phase, O, M, P, team, comments in line_items:
        E = round((O + 4*M + P) / 6)           # PERT Expected Value
        SD = round((P - O) / 6, 1)              # Standard Deviation
        
        rows.append({
            "Phase": phase,
            "Feature / Module": label,
            "Optimistic (O) hrs": O,
            "Most Likely (M) hrs": M,
            "Pessimistic (P) hrs": P,
            "PERT Expected hrs": E,
            "Std Deviation (±)": SD,
            "Optimistic Cost ($)": O * rate,
            "Most Likely Cost ($)": M * rate,
            "Pessimistic Cost ($)": P * rate,
            "PERT Expected Cost ($)": E * rate,
            "Team": team,
            "Risk / Comments": comments
        })
    
    df = pd.DataFrame(rows)
    
    # --- Phase 1 Totals ---
    p1 = df[df["Phase"] == "Phase 1: Core MVP"]
    p2 = df[df["Phase"] == "Phase 2: Nice to Have"]
    
    def total_row(label, subset):
        return {
            "Phase": "TOTAL",
            "Feature / Module": label,
            "Optimistic (O) hrs": subset["Optimistic (O) hrs"].sum(),
            "Most Likely (M) hrs": subset["Most Likely (M) hrs"].sum(),
            "Pessimistic (P) hrs": subset["Pessimistic (P) hrs"].sum(),
            "PERT Expected hrs": subset["PERT Expected hrs"].sum(),
            "Std Deviation (±)": round(math.sqrt(sum(subset["Std Deviation (±)"]**2)), 1),
            "Optimistic Cost ($)": subset["Optimistic Cost ($)"].sum(),
            "Most Likely Cost ($)": subset["Most Likely Cost ($)"].sum(),
            "Pessimistic Cost ($)": subset["Pessimistic Cost ($)"].sum(),
            "PERT Expected Cost ($)": subset["PERT Expected Cost ($)"].sum(),
            "Team": "",
            "Risk / Comments": "Combined PERT SD uses root-sum-of-squares"
        }
    
    spacer = {col: "" for col in df.columns}
    
    df = pd.concat([
        df[df["Phase"] == "Phase 1: Core MVP"],
        pd.DataFrame([spacer, total_row("Phase 1 Sub-Total (Dev)", p1), spacer]),
        df[df["Phase"] == "Phase 2: Nice to Have"],
        pd.DataFrame([spacer, total_row("Phase 2 Sub-Total (Dev)", p2), spacer]),
        pd.DataFrame([total_row("FULL SCOPE TOTAL (Dev Only)", df)])
    ], ignore_index=True)
    
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='3-Point Estimates')
    writer.close()
    print(f"Saved: {filename}")

if __name__ == "__main__":
    create_three_point_excel("D:\\Venkata\\JA\\Estimates - 3 Point (PERT).xlsx")

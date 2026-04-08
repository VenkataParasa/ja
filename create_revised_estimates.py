import pandas as pd

rate = 85   # Blended hourly rate

# ============================================================
# TARGET: $750,000 total budget @ $85/hr
# Dev hours:  ~6,300  × $85 = $535,500
# PM (11%):   ~693    × $85 =  $58,905
# Y1 Support: 1,200   × $85 = $102,000
# Y2 Support:   600   × $85 =  $51,000
# Total:      ~8,793  × $85 = $747,405 ≈ $750K
# ============================================================

rows = []

def add(phase, feature, hours, team, comments=""):
    rows.append(["", phase, feature, hours, hours * rate, team, comments])

# ------------------------------------------------------------
# FOUNDATION  (340 hrs)
# ------------------------------------------------------------
add("Phase 1: Core MVP", "Foundation - Requirements Analysis & Technical Discovery",        50,  "PM, SA",       "Q2: Discovery largely done by JA; vendor refines execution per Q&A")
add("",                  "Foundation - Architecture & DB Schema (scaled to 10-15K users)",  70,  "SA",           "Q125/Q126: 60-70 concurrent simulations; design for horizontal scaling")
add("",                  "Foundation - Azure Cloud Env Setup & CI/CD Pipelines (3 envs)",   100, "DevOps",       "Q57: JA provides Azure tenant; vendor owns pipeline config & permissions")
add("",                  "Foundation - Local Developer Testing Setup (Docker Compose)",       40,  "DevOps, BE",   "Full service mesh containerized locally for all developers")
add("",                  "Foundation - Security Policy, Key Vault & Zero Trust Setup",        40,  "SA, DevOps",   "Managed Identities, internal mTLS, secret scanning in CI")
add("",                  "Foundation - Data Anonymization Engine (COPPA 30-day rule)",        40,  "BE, SA",       "Q110: Anonymize student data after 30 days post-simulation")

# ------------------------------------------------------------
# LAYER 1: UX / UI  (1,870 hrs)
# ------------------------------------------------------------
add("",  "Layer 1: UI - UX Research, User Flows & Wireframes (all roles)",             160,  "Designer",     "Q79: B&W wireframes per JA review process; all functional roles covered")
add("",  "Layer 1: UI - Visual Design System, Style Guide, Mood Boards",               160,  "Designer, FE", "Q18: 2.5D/isometric TBD; Q40: 3rd grade reading level; age-appropriate")
add("",  "Layer 1: UI - Core Tablet & Laptop App (Single PWA codebase)",               320,  "FE",           "Q139: One app; Q140: portrait and landscape; tablets + laptops supported")
add("",  "Layer 1: UI - Student Role UIs (POS, Payroll, Banking, Loan, Billing, Voting)",240, "FE",           "Q22/Q38: Role UIs differ by function; custom business graphic per CMS")
add("",  "Layer 1: UI - Teacher & Volunteer Real-Time Monitoring Dashboard",            100,  "FE",           "Q24/Q48: Real-time business health; simple visual indicators; no rules engine")
add("",  "Layer 1: UI - Admin Core: User Mgmt, RBAC, Simulation Moderation",           150,  "FE, BE",       "Q37: Sim Managers, Volunteers, Educators, JA National as distinct roles")
add("",  "Layer 1: UI - Admin Live Event Controllers (Tornado Alert, Town Hall)",        70,  "FE, BE",       "Staff dispatches live simulation events to all connected tablets")
add("",  "Layer 1: UI - CMS Multi-Tenant National/Local Inheritance (clone/duplicate)", 280,  "FE, BE",       "Q6/Q128: Local overrides take precedence; clone Area configs; version control")
add("",  "Layer 1: UI - Canva-Like Digital Marketing Tool (template + publish)",        160,  "FE, BE",       "Q13/Q135: Step-by-step mission, templates, text, image library, display in town")
add("",  "Layer 1: UI - CFO Real-Time Screen Sharing (14-20 concurrent business sessions)",100,"FE, BE",      "Q14/Q131: Mirror CFO to teammates via Azure Web PubSub; no audio narration")
add("",  "Layer 1: UI - DJ Radio Dashboard (Playlist, Mic Announcements, A/V out)",      80,  "FE",           "Q17/Q45: Bluetooth to built-in speakers; wide A/V variety; microphone for DJ")
add("",  "Layer 1: UI - Contextual In-App Guided Flows (POS, Loan, Billing first use)",  60,  "FE",           "Q42/Q107: First-time guided step-by-step; no extensive system onboarding")
add("",  "Layer 1: UI - Sponsor Logo & Branding Upload via CMS",                         40,  "FE, BE",       "Q64: Logo, colors, business name text override; no custom sponsor code")

# ------------------------------------------------------------
# LAYER 2: API GATEWAY  (130 hrs)
# ------------------------------------------------------------
add("",  "Layer 2: API - APIM BFF (routing, rate-limiting, payload transforms)",         80,  "SA, BE",       "Single entry point; tablet vs desktop payload optimization; rate-limiting")
add("",  "Layer 2: API - Entra B2C Auth + JWT + Session Token (per-device auth)",        50,  "SA, BE",       "Q71/Q116: Session-based students; simpler auth; no individual student accounts")

# ------------------------------------------------------------
# LAYER 3: COMPUTE MICROSERVICES  (1,480 hrs)
# ------------------------------------------------------------
add("",  "Layer 3: Compute - Transaction & Ledger Service (50-100 TPS, Idempotency)",   320,  "BE",           "Q7/Q59: 500 events per 10-min window; Redis idempotency key; ACID SQL")
add("",  "Layer 3: Compute - Offline Local-First Queue & Reconciliation Engine",         220,  "BE, FE, SA",   "Q7/Q133: Core requirement; queue locally; sync + reconcile on reconnect")
add("",  "Layer 3: Compute - Configuration & Town Map Service (Cosmos DB)",               80,  "BE",           "Q31/Q62: Unique per Area; local Areas create new workflows and job roles")
add("",  "Layer 3: Compute - Business Scenarios & Character Education Engine",           110,  "BE",           "Q16: MANDATORY for grant funding. Ethical dilemmas, XP consequences")
add("",  "Layer 3: Compute - Physical Debit Card Reader SDK Integration",                 80,  "FE, BE",       "Q137: 3-digit account number swiped to populate POS; currently in production")
add("",  "Layer 3: Compute - Gamification + XP Engine (JA rules, collaborative formula)",100,  "BE",           "Q51: JA provides action list; vendor + JA co-design XP formula")
add("",  "Layer 3: Compute - Reporting Service (in-app + PDF export + Power BI ready)", 160,  "BE, Data",     "Q72/Q122/Q123: Student, business, simulation-level reports; PDF shareable")
add("",  "Layer 3: Compute - Sponsor Tracking & Yearly Analytics",                       60,  "BE, Data",     "Q127: Track students per business, popular options, sales prices, ad assets")
add("",  "Layer 3: Compute - Notification & WebSocket Service (town-scoped events)",      70,  "BE, DevOps",   "Azure Web PubSub: admin broadcasts, alerts, per-business live updates")
add("",  "Layer 3: Compute - Audit Log & Transaction Cancellation (Admin only)",          60,  "BE",           "Q111/Q121: Admin audit 30d; user actions 7d; admin can cancel sim transactions")
add("",  "Layer 3: Compute - Disaster Recovery & Full Simulation State Resume",          120,  "BE, DevOps",   "Q143: Full state recovery mandatory; simulation resumes exact prior state")
add("",  "Layer 3: Compute - Data Pipeline & CMS Asset Management",                      100,  "BE, DevOps",   "Q47/Q142: JA Area sponsor logo uploads; vendor defines size + format specs")

# ------------------------------------------------------------
# LAYER 4: ASYNC EVENT-BUS  (70 hrs)
# ------------------------------------------------------------
add("",  "Layer 4: Event Bus - Azure Service Bus Topics & Dead-Letter Handling",          70,  "DevOps, BE",   "Decouples banking from gamification, reporting, and notification pipelines")

# ------------------------------------------------------------
# TESTING & SECURITY  (1,080 hrs)
# ------------------------------------------------------------
add("",  "Layer 5: QA - Automated Test Suite (unit, integration, regression, CI-gated)", 280,  "QA",           "CI-gated; every PR triggers regression; full coverage on banking + sync")
add("",  "Layer 5: QA - WCAG 2.2 AA + 3rd-Party Audit Coordination",                    100,  "QA, Designer", "Q8/Q46: JA has external auditor; vendor supports VPAT and remediation cycles")
add("",  "Layer 5: QA - Security Hardening & Penetration Testing (OWASP Top 10)",        160,  "Sec, SA",      "Threat modelling, zero-trust validation, API fuzzing, secrets audit")
add("",  "Layer 5: QA - Performance Engineering & 60-70 Concurrent Simulation Load Test", 200,  "QA, DevOps",  "Q125/Q126: 10-15K users; shopping period spike testing (50-100 TPS)")
add("",  "Layer 5: QA - User Acceptance Testing + Bug Fix Cycles",                        180,  "QA, FE, BE",   "Structured UAT with JA advisory group + pilot participants")
add("",  "Layer 5: QA - Cross-Device & Offline Degradation Testing",                     100,  "QA, BE",       "Q112/Q114/Q115: iPad, Android tablet, Chromebook, laptop; degraded-mode check")
add("",  "Layer 5: QA - Real-Time Sync & Transaction Conflict Stress Tests",               60,  "QA, BE",       "Q12: Frozen accounts, payroll + purchase contention, mid-tx network drop")

# ------------------------------------------------------------
# DELIVERY  (310 hrs)
# ------------------------------------------------------------
add("",  "Layer 5: Delivery - App Store (iOS + Android) & MDM Distribution",              80,  "PM, DevOps",   "Q74: Both App Store + MDM; Q83: JA provides Apple + Google dev accounts")
add("",  "Layer 5: Delivery - CMS User Guide + Simulation User Guide (non-technical JA staff)", 100, "PM, SA", "Q42/Q66: In-depth manuals; JA staff are education-focused not technical")
add("",  "Layer 5: Delivery - Spanish Localization (vendor provided per Q68)",            130,  "FE, Designer", "Q68: JA expects vendor to provide translated content")

# ------------------------------------------------------------
# PILOT & POST-LAUNCH (included as Phase 1 line items)
# ------------------------------------------------------------
add("",  "Pilot - On-Site Support (select JA Area live simulation sessions)",             160,  "PM, QA, SA",   "Q77: Vendor expected in-person for select pilots; instant availability for rest")
add("",  "Pilot - Post-Pilot Remediation Sprint (10-15 JA Area feedback resolution)",    280,  "FE, BE, QA",   "Q9/Q81: Structured sprint; defects vs enhancements triaged per governance")

# ------------------------------------------------------------
# PHASE 2: NICE TO HAVE  (540 hrs)
# ------------------------------------------------------------
add("Phase 2: Nice to Have", "AI - Slogan Generation (Azure OpenAI, scaffolded, 3-strike guardrails)", 120, "BE, Designer", "Q20/Q136: Flexible for pilot; guided; constrained outputs; age-appropriate")
add("",  "AI - CEO Speech-to-Text Transcription & In-Simulation Display",                  80,  "BE, FE",       "Q20: Transcription only; student writes own speech; system records/displays")
add("",  "NFC Tap-to-Pay (iOS + Android + graceful QR code fallback)",                   160,  "FE, QA",       "Q19/Q138: Confirmed nice-to-have; cross-platform NFC hardware variability")
add("",  "Advanced Gamification - Inventory Depletion & Supply Chain Math",               140,  "BE, QA",       "Replaces unlimited stock assumption with real depletion logistics engine")
add("",  "Expanded QA Environment (4th dedicated regression cluster)",                     40,  "DevOps",       "Dedicated cluster separate from Dev/Staging/Prod for isolated load testing")

# ============================================================
# TOTALS
# ============================================================
dev_hours = sum(r[3] for r in rows if isinstance(r[3], (int, float)))
pm_hours  = round(dev_hours * 0.11)
sub_total = dev_hours + pm_hours

y1_support = 1200
y2_support = 600
grand_total_hrs  = sub_total + y1_support + y2_support
grand_total_cost = grand_total_hrs * rate

rows.extend([
    ["", "", "", "", "", "", ""],
    ["", "", "Sub-Total Dev Hours", dev_hours, dev_hours * rate, "", ""],
    ["", "", "PM / Delivery Management (11%)", pm_hours, pm_hours * rate, "",
     "Weekly working sessions, milestone reviews, pre-reads, stakeholder sign-offs per Q10/Q89"],
    ["", "", "Year 1 Support - Hyper-Care & Maintenance", y1_support, y1_support * rate, "1 FTE",
     "Q5: 100% uptime M-F 8AM-7PM ET; alerts + monitors enable JA to handle incidents with vendor escalation"],
    ["", "", "Year 2 Support - Maintenance & Annual Enhancements", y2_support, y2_support * rate, "0.5 FTE",
     "Annual upgrade cycle per RFP; infrastructure health; minor feature additions"],
    ["", "", "Total", grand_total_hrs, grand_total_cost, "",
     f"Budget Target: $750,000  |  Actual: ${grand_total_cost:,.0f}"],
    ["", "", "", "", "", "", ""],
    ["", "", "Man Months (Dev Only)", round(dev_hours / 160, 1), "", "", "Based on 160h/month"],
    ["", "", "Man Months (Full Engagement)", round(grand_total_hrs / 160, 1), "", "", "Including PM and support years"],
])

# ============================================================
# EXPORT
# ============================================================
columns = ["", "Phase", "Feature (Module Area)", "Hours", f"Cost (@ ${rate}/hr)", "Team", "Comments / Q&A Reference"]
df = pd.DataFrame(rows, columns=columns)

notes = [
    f"REVISED ESTIMATES  |  Rate: ${rate}/hr  |  Dev: {dev_hours} hrs  |  PM: {pm_hours} hrs  |  Support: {y1_support+y2_support} hrs  |  TOTAL: {grand_total_hrs} hrs  |  COST: ${grand_total_cost:,.0f}",
    "Built from comprehensive review of all 143 Q&A responses from JA BizTown RFP.",
    "",
    "ITEMS MOVED INTO PHASE 1 BASED ON Q&A::",
    "  [Q16]  Business Scenarios / Character Education = MANDATORY (grant-funded requirement)",
    "  [Q7/Q15/Q133]  Offline Local-First Queue + Sync Engine = REQUIRED by JA",
    "  [Q13/Q135]  Canva-Like Digital Marketing Tool = confirmed MVP scope",
    "  [Q14/Q131]  CFO Real-Time Screen Sharing = required feature (14-20 concurrent)",
    "  [Q17/Q45]  DJ Radio Dashboard = required (replaces fragmented A/V approach)",
    "  [Q137]  Physical Debit Card Reader = current production integration",
    "  [Q110]  Data Anonymization 30-day = COPPA compliance",
    "  [Q68]  Spanish Localization = vendor to provide",
    "  [Q77/Q9]  Pilot On-Site Support + Post-Pilot Sprint = vendor commitment",
    "",
    "CONFIRMED PHASE 2 / OPTIONAL:",
    "  [Q136]  AI features (slogan + speech-to-text) = flexible, can slip past pilot",
    "  [Q19/Q138]  NFC = nice-to-have, graceful QR fallback required",
    "  [Q134]  Paper fallback = not required if offline mode works",
    "  [Q25]  Budget confirmed: $1M cap for initial release",
]

notes_rows = [["", "", "", "", "", "", ""], ["", "Notes", "", "", "", "", ""]]
notes_rows += [["", n, "", "", "", "", ""] for n in notes]
df = pd.concat([df, pd.DataFrame(notes_rows, columns=columns)], ignore_index=True)

output_path = "D:\\Venkata\\JA\\Revised Estimates.xlsx"
writer = pd.ExcelWriter(output_path, engine='openpyxl')
df.to_excel(writer, index=False, sheet_name="Revised Estimates")
writer.close()

print(f"Saved: {output_path}")
print(f"Dev Hours : {dev_hours}")
print(f"PM Hours  : {pm_hours} (11%)")
print(f"Y1+Y2 Sup : {y1_support + y2_support}")
print(f"Total Hrs : {grand_total_hrs}")
print(f"Total Cost: ${grand_total_cost:,.0f}")

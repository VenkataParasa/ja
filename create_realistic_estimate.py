import pandas as pd

rate = 85  # Blended hourly rate

rows = []

def add(phase, feature, hours, team, comments=""):
    rows.append(["", phase, feature, hours, hours * rate, team, comments])

# ====================================================================
# PHASE 1: CORE MVP  — Realistic, accuracy-focused estimates
# ====================================================================

# --- FOUNDATION (420 hrs) ---
add("Phase 1: Core MVP", "Foundation - Requirements Analysis & Technical Discovery",          60, "PM, SA",        "RFP + Q&A review; user story mapping; acceptance criteria definition")
add("",                  "Foundation - Architecture & DB Schema (10-15K user scale)",         90, "SA",             "Microservices topography; schema design for 60-70 concurrent simulations")
add("",                  "Foundation - Azure Cloud Env Setup & CI/CD Pipelines (3 envs)",    110, "DevOps",         "Dev, Staging, Prod + branch preview envs; automated build, test, deploy")
add("",                  "Foundation - Local Developer Testing (Docker Compose service mesh)", 50,  "DevOps, BE",    "All services containerized; local seed data; dev onboarding < 1 day")
add("",                  "Foundation - Security Policy, Zero Trust & Key Vault Setup",         60,  "SA, DevOps",    "Managed Identities, internal mTLS, secret scanning, APIM threat policies")
add("",                  "Foundation - COPPA Data Anonymization Engine (30-day rule)",         50,  "BE, SA",        "Q110: Scheduled job anonymizes student data post-simulation")

# --- LAYER 1: UI (2,280 hrs) ---
add("",  "Layer 1: UI - UX Research, User Flows & B&W Wireframes (all roles)",              180,  "Designer",      "Q79: B&W wireframe review before visual design; all 6+ student roles covered")
add("",  "Layer 1: UI - Visual Design System, Style Guide, 2.5D Mood Boards",              200,  "Designer, FE",  "Q18/Q40: 2.5D/isometric; 3rd grade reading level; state-of-art for age 9-12")
add("",  "Layer 1: UI - Core Tablet + Laptop App (Single PWA codebase, all states)",       380,  "FE",             "Q139/Q140: Portrait + landscape; tablet primary; laptop fallback; smooth UX")
add("",  "Layer 1: UI - Student Role UIs: POS, Payroll, Banking, Loan, Billing, Voting",   290,  "FE",             "Q22/Q38: Distinct functional UIs per role; custom business graphic from CMS")
add("",  "Layer 1: UI - Teacher & Volunteer Real-Time Monitoring Dashboard",                120,  "FE",             "Q24/Q48: Real-time business health; financial indicators; no forced-alert engine")
add("",  "Layer 1: UI - Admin Core: User Mgmt, Roles, Permissions, Moderation",            170,  "FE, BE",         "Q37: Sim Managers, Volunteers, Educators, JA National with distinct permissions")
add("",  "Layer 1: UI - Admin Live Event Controllers (Tornado Alert, Town Hall, Pause)",     90,  "FE, BE",         "Dispatch real-time simulation triggers to all connected tablets simultaneously")
add("",  "Layer 1: UI - CMS Multi-Tenant: National Inheritance + Local Override + Clone",   320,  "FE, BE",         "Q6/Q128: Local precedence; clone/duplicate Areas; version history; rollback")
add("",  "Layer 1: UI - Canva-Like Digital Marketing Tool (template + library + publish)",  200,  "FE, BE",         "Q13: Structured step-by-step; templates; text edit; image library; town display")
add("",  "Layer 1: UI - CFO Real-Time Screen Sharing (14-20 concurrent biz sessions)",     130,  "FE, BE",         "Q14/Q131: Mirror CFO device via Azure Web PubSub; no audio; resilient on WiFi")
add("",  "Layer 1: UI - DJ Radio Dashboard (Playlist control, Mic, A/V output)",            90,  "FE",              "Q17/Q45: Built-in DJ UI; wide A/V adaptability; live microphone announcements")
add("",  "Layer 1: UI - Voting Module UI (Civic engagement per simulation schedule)",        60,  "FE",             "Students vote during simulation; real-time results; admin-triggered")
add("",  "Layer 1: UI - Team Building & Onboarding Guided Flows",                           60,  "FE",              "Q36/Q42: Business intro; first-time guided walkthroughs for POS/Loan/Billing")
add("",  "Layer 1: UI - Sponsor Logo + Color + Branding Upload (per business via CMS)",     50,  "FE, BE",          "Q64: Logo, color, text override per business; no custom sponsor code")
add("",  "Layer 1: UI - Business Scenarios: Ethical Dilemma UX & Donation Decision Flows", 80,  "FE",              "Q16: Character education UI; XP consequences displayed; CMS-configurable amounts")
add("",  "Layer 1: UI - Post-Simulation Student & Teacher Reflection Report UI",             60,  "FE",              "Q48: Post-sim view for student self-reflection; educator review dashboard")

# --- LAYER 2: API GATEWAY (150 hrs) ---
add("",  "Layer 2: API - APIM BFF (routing, rate-limiting, tablet vs desktop payloads)",    90,  "SA, BE",          "Single entry; rate-limiting during peak shopping windows; payload transforms")
add("",  "Layer 2: API - Entra B2C + Session-Based JWT Auth (per-device, no student PII)",  60,  "SA, BE",          "Q71/Q116: Session-auth per device; no individual student accounts or emails")

# --- LAYER 3: COMPUTE MICROSERVICES (1,980 hrs) ---
add("",  "Layer 3: Compute - Transaction & Ledger Service (50-100 TPS, Idempotency, ACID)", 360,  "BE",             "Q7/Q59: 500 txn/10-min; Redis idempotency; SQL ACID; debit + payroll + billing")
add("",  "Layer 3: Compute - Offline Local-First Queue + Sync + Conflict Resolution",        260,  "BE, FE, SA",     "Q7/Q15/Q133: Core requirement; queue locally; reconcile on reconnect; no-PII keys")
add("",  "Layer 3: Compute - Configuration & Town Map Service (Cosmos DB flexible schema)",  100,  "BE",             "Q31/Q62: Dynamic per-Area layouts; local Areas define businesses, roles, tasks")
add("",  "Layer 3: Compute - Business Scenarios & Character Education Engine",               140,  "BE",              "Q16: MANDATORY. Ethical dilemmas; XP consequences; donation CMS config amounts")
add("",  "Layer 3: Compute - Physical Debit Card Reader SDK Integration",                     90,  "FE, BE",         "Q137: 3-digit account swipe → POS; existing production model; iOS + Android")
add("",  "Layer 3: Compute - Gamification + XP Engine (JA co-designed formula)",            130,  "BE",              "Q51: JA provides action list; formula built collaboratively with JA team")
add("",  "Layer 3: Compute - Reporting Service (in-app + PDF + Power BI export)",           190,  "BE, Data",        "Q72/Q122/Q123: Student, business, simulation reports; PDF shareable; BI-ready")
add("",  "Layer 3: Compute - Sponsor Tracking & Yearly Analytics Service",                    80,  "BE, Data",        "Q127: Students per business; popular choices; sales prices; ad assets per Area")
add("",  "Layer 3: Compute - Notification & WebSocket Service (room-scoped events)",          80,  "BE, DevOps",      "Azure Web PubSub: town alerts; per-business updates; admin broadcast channel")
add("",  "Layer 3: Compute - Audit Log, Transaction Cancellation & Admin Override",           80,  "BE",              "Q111/Q121: Admin audit 30d; user actions 7d; admin-only txn cancel; log export")
add("",  "Layer 3: Compute - Disaster Recovery, Full Simulation State Save & Resume",        130,  "BE, DevOps",      "Q143: Full state resume mandatory; simulations CANNOT restart; RTO: 1-2 seconds")
add("",  "Layer 3: Compute - Voting Service (civic simulation ballot + results engine)",       80,  "BE",              "Real-time ballot processing; business-level and town-wide vote types")
add("",  "Layer 3: Compute - CMS Asset Pipeline (logo uploads, image library, CDN delivery)", 80,  "BE, DevOps",     "Q47/Q142: Sponsor logos; marketing image library; vendor dictates size/format")
add("",  "Layer 3: Compute - Payroll Engine (CFO submission, student salary credit)",         70,  "BE",              "Q101: Payroll = most software-intensive phase; CFO submits; distributes salaries")

# --- LAYER 4: EVENT BUS (80 hrs) ---
add("",  "Layer 4: Event Bus - Azure Service Bus Topics, Subscriptions & DLQ Handling",      80,  "DevOps, BE",      "Decouples banking from gamification, notifications, and reporting asynchronously")

# --- TESTING & SECURITY (1,490 hrs) ---
add("",  "Layer 5: QA - Automated Test Suite (unit, integration, regression, CI-gated)",    280,  "QA",              "All PRs trigger regression; banking + offline sync tests mandatory before merge")
add("",  "Layer 5: QA - WCAG 2.2 AA (all interfaces) + 3rd-Party Audit Coordination",      130,  "QA, Designer",    "Q8/Q46: JA has external auditor; vendor remediates and supports VPAT completion")
add("",  "Layer 5: QA - Security Hardening & Penetration Testing (OWASP Top 10)",           200,  "Sec, SA",         "Threat modelling, API fuzzing, zero-trust validation, student PII protection")
add("",  "Layer 5: QA - Performance Engineering & 60-70 Concurrent Simulation Load Test",   220,  "QA, DevOps",      "Q125/Q126: 10-15K concurrent users; 50-100 TPS spikes; shopping period simulation")
add("",  "Layer 5: QA - Cross-Device Testing (iPad, Android tablet, Chromebook, laptop)",   130,  "QA",              "Q112/Q114: Area-owned devices; no standardized hardware; wide OS + browser range")
add("",  "Layer 5: QA - Offline & Network Degradation Testing",                             130,  "QA, BE",          "Q115: 100 Mbps typical; validate local queue behavior under network interruption")
add("",  "Layer 5: QA - User Acceptance Testing + Iterative Bug Fix Cycles",                180,  "QA, FE, BE",      "Structured UAT with JA advisory group + end users; 2 full UAT cycles minimum")
add("",  "Layer 5: QA - Real-Time Sync & Transaction Conflict Stress Testing",               100,  "QA, BE",          "Q12: Frozen accounts; payroll + purchase contention; mid-transaction drops tested")

# --- DELIVERY (590 hrs) ---
add("",  "Layer 5: Delivery - App Store (iOS + Android) & MDM Distribution Setup",           90,  "PM, DevOps",      "Q74: App Store + MDM dual paths; Q83: JA provides Apple + Google Dev accounts")
add("",  "Layer 5: Delivery - Admin CMS Guide + Simulation User Guide (non-tech JA staff)", 130,  "PM, SA",          "Q42/Q66: In-depth manuals; education-focused non-technical staff audience")
add("",  "Layer 5: Delivery - Spanish Localization (vendor-provided per Q68)",              150,  "FE, Designer",    "Q68: JA expects vendor to provide all translated simulation content")
add("",  "Layer 5: Delivery - Pilot On-Site Support (select JA Area live sessions)",        200,  "PM, QA, SA",      "Q77/Q78: Vendor on-site for select pilots; instant availability for remainder")
add("",  "Layer 5: Delivery - Post-Pilot Remediation Sprint (10-15 JA Areas feedback)",     280,  "FE, BE, QA",      "Q9/Q81: Defects triaged vs enhancements; critical issues resolved pre-launch")
add("",  "Layer 5: Delivery - DR Testing, Simulation State Recovery Validation",             80,  "QA, DevOps",      "Q143: Full walkthrough of failure + resume; verify no data loss or txn gaps")
add("",  "Layer 5: Delivery - Go-Live Readiness & Stakeholder Sign-Off Coordination",        80,  "PM",              "Q9: JA USA product + program leadership + functional stakeholders sign-off")
add("",  "Layer 5: Delivery - First-Week Post-Launch Hypercare (instant availability)",        60,  "PM, BE, QA",      "Q78: Vendor on-standby during first weeks of initial release")

# ====================================================================
# PHASE 2: NICE TO HAVE — All optional features, realistic estimates
# ====================================================================
add("Phase 2: Nice to Have", "AI - Slogan Generation (Azure OpenAI, scaffolded, 3-strike guardrails)", 150, "BE, Designer", "Q20/Q136: Guided structured generation; limited options; content moderation filter")
add("",  "AI - CEO Speech-to-Text Transcription & In-Simulation Display",                   100,  "BE, FE",          "Q20: Transcription only; student writes speech; system transcribes + displays")
add("",  "NFC Tap-to-Pay (iOS + Android cross-platform + graceful QR code fallback)",       200,  "FE, QA",          "Q19/Q138: Nice-to-have; cross-platform NFC variability; graceful degradation")
add("",  "Advanced Gamification - Inventory Depletion & Supply Chain Logistics",            180,  "BE, QA",           "Replaces unlimited stock assumption; real depletion math; demand-driven pricing")
add("",  "Expanded Dedicated QA Environment (4th standalone regression cluster)",             50,  "DevOps",           "Isolated env for automated regression and load test pipelines")

# ====================================================================
# CALCULATE TOTALS
# ====================================================================
dev_hours  = sum(r[3] for r in rows if isinstance(r[3], (int, float)))
contingency = round(dev_hours * 0.10)
pm_hours   = round((dev_hours + contingency) * 0.11)
sub_total  = dev_hours + contingency + pm_hours

y1_support = 1200
y2_support = 600
grand_total_hrs  = sub_total + y1_support + y2_support
grand_total_cost = grand_total_hrs * rate

rows.extend([
    ["", "", "", "", "", "", ""],
    ["", "", "Sub-Total Dev Hours (Phase 1 + Phase 2)", dev_hours, dev_hours * rate, "", ""],
    ["", "", "Contingency Buffer (10%)", contingency, contingency * rate, "", "Planned risk buffer for scope creep, integration surprises, and unknowns"],
    ["", "", "PM / Delivery Management (11% of Dev+Contingency)", pm_hours, pm_hours * rate, "", "Weekly sessions, milestone reviews, stakeholder sign-offs, pre-reads per Q10"],
    ["", "", "Year 1 Support - Hyper-Care & Maintenance", y1_support, y1_support * rate, "1 FTE", "Q5: 100% uptime M-F 8AM-7PM ET; alerts allow JA to manage with vendor escalation"],
    ["", "", "Year 2 Support - Maintenance & Annual Upgrade Cycle", y2_support, y2_support * rate, "0.5 FTE", "Annual enhancements per RFP; model refresh; infrastructure health"],
    ["", "", "GRAND TOTAL", grand_total_hrs, grand_total_cost, "", f"Rate: ${rate}/hr  |  Budget Reference: $1M cap per Q25"],
    ["", "", "", "", "", "", ""],
    ["", "", "Man Months (Dev Only)", round(dev_hours / 160, 1), "", "", "Based on 160h/month"],
    ["", "", "Man Months (Full Engagement)", round(grand_total_hrs / 160, 1), "", "", "Including contingency, PM, and support"],
])

# ====================================================================
# EXPORT
# ====================================================================
columns = ["", "Phase", "Feature (Module Area)", "Hours", f"Cost (@ ${rate}/hr)", "Team", "Comments / Q&A Reference"]
df = pd.DataFrame(rows, columns=columns)

notes = [
    f"REALISTIC ESTIMATE  |  Rate: ${rate}/hr (blended)  |  Dev: {dev_hours} hrs  |  Contingency (10%): {contingency} hrs  |  PM: {pm_hours} hrs",
    f"Y1+Y2 Support: {y1_support + y2_support} hrs  |  TOTAL: {grand_total_hrs} hrs  |  TOTAL COST: ${grand_total_cost:,.0f}",
    f"JA Confirmed Budget Cap: $1,000,000 (Q25)  |  This estimate is within that cap.",
    "",
    "SCOPE NOTES:",
    "  - Includes ALL Phase 1 (Core MVP) + ALL Phase 2 (Optional) features",
    "  - 10% contingency explicitly added as a line item for risk management",
    "  - Phase 1 mandatory items confirmed by Q&A: Business Scenarios (Q16), Offline Sync (Q7/Q133),",
    "    Canva Marketing Tool (Q13), CFO Screen Sharing (Q14), DJ Radio (Q17), Debit Card (Q137),",
    "    Data Anonymization (Q110), Spanish Localization (Q68), Voting Engine, Pilot Support (Q77)",
    "  - Phase 2 optional: AI Slogan/Speech (Q136), NFC (Q19), Advanced Supply Chain Math",
    "  - Paper fallback NOT included - not required if offline mode works (Q134)",
    "  - Budget cap confirmed at $1M for initial release (Q25)",
    "  - Hourly rate: $85/hr blended across all roles",
]

notes_rows = [["", "", "", "", "", "", ""], ["", "Notes", "", "", "", "", ""]]
notes_rows += [["", n, "", "", "", "", ""] for n in notes]
df = pd.concat([df, pd.DataFrame(notes_rows, columns=columns)], ignore_index=True)

output_path = "D:\\Venkata\\JA\\Realistic Estimate.xlsx"
writer = pd.ExcelWriter(output_path, engine='openpyxl')
df.to_excel(writer, index=False, sheet_name="Realistic Estimate")
writer.close()

print(f"Saved: {output_path}")
print(f"Dev (P1+P2)  : {dev_hours} hrs  = ${dev_hours * rate:,.0f}")
print(f"Contingency  : {contingency} hrs  = ${contingency * rate:,.0f}  (10%)")
print(f"PM           : {pm_hours} hrs  = ${pm_hours * rate:,.0f}  (11%)")
print(f"Y1+Y2 Support: {y1_support + y2_support} hrs  = ${(y1_support + y2_support) * rate:,.0f}")
print(f"TOTAL        : {grand_total_hrs} hrs  = ${grand_total_cost:,.0f}")

import pandas as pd

def create_excel(filename, data, notes):
    columns = ["", "Phase", "Feature", "Hours", "Cost", "Team", "Comments"]
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
    
    initial_data = [
        ["", "Discovery and Design", "Requirements Analysis & Technical Discovery", 60, 60*rate, "PM, SA", ""],
        ["", "", "UX/UI Conceptualization & Mood Boards, Wireframes & Clickable Prototyping, Visual Identity", 170, 170*rate, "Designer, FE", "Designer Full Time"],
        ["", "", "System Architecture & Database Schema Design", 40, 40*rate, "SA", ""],
        ["", "Development", "Azure Subscriptions, Network & Governance Setup, CI/CD Pipelines, 4 Environments (Dev, QA, Staging, Prod)", 110, 110*rate, "DevOps, SA", "Terraform/ARM Infrastructure"],
        ["", "", "Backend Core Simulation Engine, Financial Engine, Auth Entra B2C", 240, 240*rate, "BE", ""],
        ["", "", "Backend Gamification API Engine & Azure OpenAI Integration", 120, 120*rate, "BE", ""],
        ["", "", "CMS: Multi-Tenant Admin, Templates, Localization, React UI, Offline PDF Gen", 350, 350*rate, "FE, BE", ""],
        ["", "", "Mobile Apps: Student App SPA, Onboarding, Financial App UI, AI Tools, POS Hardware (NFC/ePOS/Swipers)", 490, 490*rate, "FE", "React Native / Expo"],
        ["", "", "Web/Tablet Dashboards: Staff, Teacher & Volunteer", 230, 230*rate, "FE, BE", ""],
        ["", "", "Reporting & Power BI Analytics Data", 160, 160*rate, "Data, BE", ""],
        ["", "Testing & Delivery", "Accessibility Validation (WCAG 2.2 AA), Load Testing, Security Assessments", 160, 160*rate, "QA, Sec", ""],
        ["", "", "End-to-End User Acceptance Iterative Bug Fixes", 80, 80*rate, "QA, FE, BE", ""],
        ["", "", "App Store Processing, Final Code Reviews, Data Schema Manuals, Admin Training", 90, 90*rate, "PM, SA, DevOps", ""],
    ]
    
    dev_hours_initial = sum([row[3] for row in initial_data if type(row[3]) in (int, float)])
    pm_hours_initial = int(dev_hours_initial * 0.1)
    
    initial_data.extend([
        ["", "", "", "", "", "", ""],
        ["", "", "Sub-Total", dev_hours_initial, dev_hours_initial*rate, "", ""],
        ["", "", "PM (10%)", pm_hours_initial, pm_hours_initial*rate, "", ""],
        ["", "", "Year 1 Support (Hyper-Care & Maintenance)", 1200, 1200*rate, "1 - FTE", ""],
        ["", "", "Total", dev_hours_initial + pm_hours_initial + 1200, (dev_hours_initial + pm_hours_initial + 1200)*rate, "", ""]
    ])
    
    initial_notes = [
        "These estimates account for the complete set of RFP requirements.",
        "Includes complex AI integrations, Gamification engine APIs, and 4 environment setups.",
        "Assumes fully offline dynamic configurable PDFs generator.",
        "Explicitly includes SDK connections for physical NFC usage and external ePOS debit card swipers."
    ]

    create_excel("D:\\Venkata\\JA\\Estimates - Initial.xlsx", initial_data, initial_notes)
    
    optimized_data = [
        ["", "Discovery and Design", "Requirements Analysis & Technical Discovery", 40, 40*rate, "PM, SA", "Skipped Discovery for Luxury Items"],
        ["", "", "UX/UI Conceptualization, Wireframes & Visual Identity (Core Only)", 130, 130*rate, "Designer, FE", "No AI Interfaces, No Advanced Gamification Visuals"],
        ["", "", "System Architecture & Database Schema Design", 30, 30*rate, "SA", ""],
        ["", "Development", "Azure Setups, CI/CD, 3 Environments (Dev, Staging, Prod)", 90, 90*rate, "DevOps, SA", "Removed QA Env"],
        ["", "", "Backend Core Simulation Engine, Financial Engine, Auth", 210, 210*rate, "BE", "Unlimited Inventory Assumption"],
        ["", "", "Backend Gamification API Engine (Simpler XP)", 60, 60*rate, "BE", "No AI Scenario Generation"],
        ["", "", "CMS: Admin, Templates, Localization, React UI", 280, 280*rate, "FE, BE", "Removed code-generated PDF engine"],
        ["", "", "Mobile Apps: Student App SPA, Core Financial App UI", 280, 280*rate, "FE", "No Deep Offline resolution, No A/V Integration, No Hardware APIs"],
        ["", "", "Web/Tablet Dashboards: Staff, Teacher & Volunteer", 190, 190*rate, "FE, BE", ""],
        ["", "", "Reporting & Power BI Analytics Data", 110, 110*rate, "Data, BE", "Less Complex Historic Views"],
        ["", "Testing & Delivery", "Accessibility Validation (WCAG 2.2 AA), Load Testing, Security Assessments", 120, 120*rate, "QA, Sec", "Lighter load with fewer modules"],
        ["", "", "End-to-End User Acceptance Iterative Bug Fixes", 60, 60*rate, "QA, FE, BE", ""],
        ["", "", "App Store Processing, Final Code Reviews, Training", 80, 80*rate, "PM, SA, DevOps", ""],
    ]
    
    dev_hours_opt = sum([row[3] for row in optimized_data if type(row[3]) in (int, float)])
    pm_hours_opt = int(dev_hours_opt * 0.1)
    
    optimized_data.extend([
        ["", "", "", "", "", "", ""],
        ["", "", "Sub-Total", dev_hours_opt, dev_hours_opt*rate, "", ""],
        ["", "", "PM (10%)", pm_hours_opt, pm_hours_opt*rate, "", ""],
        ["", "", "Year 1 Support (Hyper-Care & Maintenance)", 1200, 1200*rate, "1 - FTE", ""],
        ["", "", "Total", dev_hours_opt + pm_hours_opt + 1200, (dev_hours_opt + pm_hours_opt + 1200)*rate, "", ""]
    ])
    
    optimized_notes = [
        "These optimized estimates defer 'nice-to-have' luxury items.",
        "Reductions applied: Omitting AI generation (Slogans/Speech-to-text), removing deep offline conflict sync.",
        "Reductions applied: Removing A/V hardware integrations, physical radio stations, replacing dynamic PDF engine with static downloads.",
        "Reductions applied: Assuming unlimited stock, avoiding complex supply-chain inventory backend logic.",
        "Reductions applied: Defers physical external ePOS (debit card swipers/NFC readers) to Phase 2. Payment natively utilizes tablet camera QR scanning instead."
    ]

    create_excel("D:\\Venkata\\JA\\Estimates - Optimized.xlsx", optimized_data, optimized_notes)

if __name__ == "__main__":
    main()

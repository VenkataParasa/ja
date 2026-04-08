import pandas as pd
import math

def create_excel(filename, data, notes):
    # The format exactly demands these columns
    columns = ["", "Phase", "Feature", "Hours", "Cost", "Team", "Comments"]
    df = pd.DataFrame(data, columns=columns)
    
    # Appending notes at the bottom like the format
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
    
    # --- OPTION A: Full RFP (Phase 1 + Phase 2) ---
    option_a_data = [
        ["", "Phase 1: Core MVP", "System Architecture & Setup: 3 environments, Core Cloud Setup", 120, 120*rate, "SA, DevOps", "Infrastructure Design + CI/CD"],
        ["", "", "UX/UI Conceptualization & Prototyping: Core flows, WCAG 2.2 AA", 130, 130*rate, "Designer, FE", "No Generative AI visuals"],
        ["", "", "Backend Core Simulation & Financial Engine: Basic Banking, Ledgers, APIs", 210, 210*rate, "BE", "Entra B2C Auth, Unlimited Inventory Assumption"],
        ["", "", "CMS & Multi-Tenant Administration: React UI for Staff, Static Template downloads", 280, 280*rate, "FE, BE", ""],
        ["", "", "Mobile Apps & Web Dashboards: Student React Native SPA, Teacher Dashboard", 470, 470*rate, "FE, BE", "Tablet Camera QR usage"],
        ["", "", "Gamification Core & Basic Reporting: Simple Progression API, Historical BI Views", 170, 170*rate, "BE, Data", ""],
        ["", "", "Testing, Delivery, & App Store: E2E, Bug Fixes, Accessibility Auditing", 300, 300*rate, "QA, Sec, PM", ""],
        ["", "Phase 2: Nice to Have / Optional", "Extensive External Hardware SDK Integrations", 180, 180*rate, "FE, QA", "Physical NFC tags, ePOS Swipers, Radio Hook"],
        ["", "", "Intricate Gamification & Supply Line Math", 130, 130*rate, "BE, QA", "Granular logistics depletion, real-time demand engines"],
        ["", "", "Cutting-Edge AI Integrations", 100, 100*rate, "BE, Designer", "Azure OpenAI business slogans, speech-to-text"],
        ["", "", "Deep Offline Synchronization Logic", 100, 100*rate, "BE, FE, SA", "Conflict Resolution over unstable facility LAN"],
        ["", "", "Automated Dynamic PDF Generation", 70, 70*rate, "FE, BE", "Code-driven offline paper backups"],
        ["", "", "Expanded Enterprise Environments", 40, 40*rate, "DevOps", "Dedicated QA testing stacks"],
    ]
    
    dev_hours_a = sum([row[3] for row in option_a_data if type(row[3]) in (int, float)])
    pm_hours_a = int(dev_hours_a * 0.1)
    sub_total_a_hours = dev_hours_a + pm_hours_a
    total_a_cost = sub_total_a_hours * rate
    
    # Adding summary section as seen in the format
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
        "These estimates account for ALL requirements strictly as outlined in the RFP.",
        "Both Phase 1 (MVP) and Phase 2 (Optional) items are delivered.",
        "Includes AI, Gamification depth, true offline sync, hardware SDKs, and dynamic PDFs."
    ]

    create_excel("D:\\Venkata\\JA\\Estimates - Option A (Full RFP).xlsx", option_a_data, option_a_notes)
    
    
    # --- OPTION B: MVP Only (Phase 1) ---
    option_b_data = [
        ["", "Phase 1: Core MVP", "System Architecture & Setup: 3 environments, Core Cloud Setup", 120, 120*rate, "SA, DevOps", "Infrastructure Design + CI/CD"],
        ["", "", "UX/UI Conceptualization & Prototyping: Core flows, WCAG 2.2 AA", 130, 130*rate, "Designer, FE", "No Generative AI visuals"],
        ["", "", "Backend Core Simulation & Financial Engine: Basic Banking, Ledgers, APIs", 210, 210*rate, "BE", "Entra B2C Auth, Unlimited Inventory Assumption"],
        ["", "", "CMS & Multi-Tenant Administration: React UI for Staff, Static Template downloads", 280, 280*rate, "FE, BE", ""],
        ["", "", "Mobile Apps & Web Dashboards: Student React Native SPA, Teacher Dashboard", 470, 470*rate, "FE, BE", "Tablet Camera QR usage"],
        ["", "", "Gamification Core & Basic Reporting: Simple Progression API, Historical BI Views", 170, 170*rate, "BE, Data", ""],
        ["", "", "Testing, Delivery, & App Store: E2E, Bug Fixes, Accessibility Auditing", 300, 300*rate, "QA, Sec, PM", ""],
    ]
    
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
        "These optimized estimates deliver Phase 1 ONLY (The Core MVP).",
        "Phase 2 features (Luxury AI, External Hardware, True Offline Sync, Dynamic PDFs) are completely deferred.",
        "Creates a highly stable, affordable launch platform strictly focused on the core simulation."
    ]

    create_excel("D:\\Venkata\\JA\\Estimates - Option B (MVP).xlsx", option_b_data, option_b_notes)

if __name__ == "__main__":
    main()

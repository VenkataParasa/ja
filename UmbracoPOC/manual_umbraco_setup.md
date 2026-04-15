# JA BizTown 3.0: Manual Umbraco Setup Guide (Refined Model)

This guide walks you through the **Relational Library Model** for the JA BizTown POC. This is the recommended "best-practice" for Headless Umbraco deployments where regional simulations inherit global rules from a National Master.

---

## Prerequisites
1.  Navigate to: `http://localhost:8080/umbraco`.
2.  Login with:
    -   **Email**: `admin@example.com`
    -   **Password**: `Password123!`

---

## Step 1: Create the "National Master" (The Source of Truth)
1.  Go to the **Settings** icon -> Right-click **Document Types** -> **Create** -> **Document Type**.
2.  **Name**: `Simulation Master`
3.  Add Group: `General Settings`
4.  Add Properties:
    -   `Master Simulation ID` (Alias: `masterSimulationId`, Editor: **Textstring**)
    -   `Global Ruleset` (Alias: `globalRuleset`, Editor: **Textarea**)
5.  Go to **Structure** tab -> Enable **Allow as root**.
6.  Click **Save**.

---

## Step 2: Create the "Local Simulation" (The Unique Overrides)
*Note: We are NOT using Compositions here. This keeps our JSON clean and non-redundant.*

1.  Go to **Settings** -> Right-click **Document Types** -> **Create** -> **Document Type**.
2.  **Name**: `Simulation Local`
3.  Add Group: `Relational Heritage`
4.  Add Property:
    -   **Name**: `Master Source`
    -   **Alias**: `masterSource`
    -   **Type**: **Content Picker** (and Save).
5.  Add Group: `Local Settings`
6.  Add Property:
    -   **Name**: `Local Office Name`
    -   **Alias**: `localOfficeName`
    -   **Type**: **Textstring**.
7.  Click **Save**.

---

## Step 3: Create the Inheritance Tree

1.  Go to the **Content** icon top-menu.
2.  Create **Simulation Master**:
    -   **Node Name**: `National Master Library`
    -   **Master Simulation ID**: `NAT-2026-v1`
    -   **Global Ruleset**: `Default Ruleset for JA USA.`
    -   **Save and Publish**.
3.  Create **Simulation Local**:
    -   **Node Name**: `JA San Diego Simulation`
    -   **Master Source**: Click **+** and select `National Master Library`.
    -   **Local Office Name**: `San Diego Office`
    -   **Save and Publish**.

---

## Step 4: Verify the Hydrated JSON Result

1.  Visit the Delivery API with the **Expansion Parameter**:
    `http://localhost:8080/umbraco/delivery/api/v1/content?expand=properties[masterSource[properties[$all]]]`

### Why this is better:
-   **No Redundant Nulls**: Since `Simulation Local` doesn't have the Master fields directly on it, the JSON is clean and lightweight.
-   **Single Source of Truth**: Updating the `National Master Library` node instantly updates every regional office that points to it.
-   **Deep Inheritance**: Your front-end apps can access all "National" data through the `masterSource` object in a single API call.

---

> [!IMPORTANT]
> **Resolving 401 Errors**: If you encounter an "Unauthorized" error, go to **Settings > Examine Management** and click **Rebuild index** on the `DeliveryApiContentIndex`.

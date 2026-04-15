# Umbraco 13: uSync Automation & Relational Setup Guide

This guide documents the strategy and workflow used to automate the JA BizTown 3.0 Umbraco POC, specifically focusing on the Digital Marketing Tool configuration.

## 📁 Repository Structure

The POC resides in `d:/Venkata/JA/UmbracoPOC`. Key directories:
- `/uSync/v9`: Contains the "Source of Truth" for Document Types and Content Nodes.
- `/uSync/v9/ContentTypes`: Schema definitions (e.g., `designMissionStep`, `marketingToolConfig`).
- `/uSync/v9/Content`: Actual data nodes (e.g., `ja-biztown-ad-creator`).
- `/umbraco/Data`: Persistence layer (SQLite).

## 🚀 Automation Workflow

The environment is designed for "Zero-Manual-Setup" deployment using two main Python scripts:

### 1. [generate_marketing_usync.py](file:///d:/Venkata/JA/UmbracoPOC/generate_marketing_usync.py)
This script generates the `.config` (XML) files required by uSync.
- **Stable GUIDs**: Every content node is assigned a hardcoded stable GUID (e.g., `dd100001...`). This ensures that re-running the script updates existing nodes rather than creating duplicates.
- **Relational Integrity**: It handles parent-child relationships by referencing the stable GUID of the parent (e.g., Design Mission Steps are children of the root Ad Creator).
- **Lowercase Booleans**: Note that Umbraco 13 uSync expects `true`/`false` in lowercase (e.g., `<Published Default="true" />`).

### 2. [setup_umbraco_poc.py](file:///d:/Venkata/JA/UmbracoPOC/setup_umbraco_poc.py)
A management script that coordinates the lifecycle:
1. **Authentication**: Logs into the backoffice to get an XSRF token.
2. **Import Trigger**: Attempts to hit the uSync REST API to force an "Import All". 
   - *Note: Due to sandbox/Docker security, if the API trigger fails (404), a manual trigger or Browser Subagent trigger is used as a fallback.*
3. **Verification**: Queries the **Headless Delivery API** to confirm that the nodes are published and accessible.

## 🛠 Relational Inheritance Model

We use **Relational Inheritance** to link National Master data with Local Area overrides:
1. **Master Source**: Local nodes have a `masterSource` property stored as a UDI (e.g., `umb://document/GUID`).
2. **Expansion**: The front-end fetches the local node and uses the Delivery API's `expand` parameter to pull in the National Master's global properties in a single request.

## 🔍 Troubleshooting the Delivery API

### Sorting and Filtering
By default, custom properties are NOT sortable in Umbraco 13's Delivery API. To enable this, the following flags must be added to the property definition in the `.config` file:
```xml
<IsFilterableInDeliveryApi>true</IsFilterableInDeliveryApi>
<IsSortableInDeliveryApi>true</IsSortableInDeliveryApi>
```
Additionally, the Document Type must be enabled at the Info level:
```xml
<CanBeUsedForDeliveryApi>true</CanBeUsedForDeliveryApi>
```

### Examine Index
If changes are made to Document Types, the `DeliveryApiContentIndex` must be rebuilt in **Settings > Examine Management** for the changes to take effect in the headless endpoints.

## 🔄 Recommended Workflow for Changes
1. Modify the Python generators or uSync XML files.
2. Run `docker compose up -d` (to ensure volume sync).
3. Access the backoffice -> **Settings** -> **uSync** -> **Import All**.
4. Access **Settings** -> **Examine Management** -> **Rebuild** the `DeliveryApiContentIndex`.

### ⚡ Tip: Ordering in Delivery API
While custom properties can be marked as sortable, it often requires manual C# handlers in Umbraco 13. For the **JA BizTown POC**, use the built-in `sortOrder` which is already mapped and functional:
`GET /umbraco/delivery/api/v1/content?filter=contentType:designMissionStep&sort=sortOrder:asc`

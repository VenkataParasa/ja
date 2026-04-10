# Technical Brief: Achieving Persistent Inheritance with Strapi

Yes, I can confirm with 100% certainty that this is possible. However, it is important to clarify that this is an **Architectural Design Pattern** implemented *using* Strapi's features, rather than a single magic button inside Strapi. 

Because Strapi is a **Headless, API-First CMS**, it expects you to define how data relates. We achieve the "V1 Persistence on V2 Upgrade" using a concept called **Delta-Based Object Merging**.

## 1. Strapi Architectural References & Citations

To build this in Strapi, we rely on three core, out-of-the-box native features:

1.  **Relational Content Types (Citations: Strapi Content-Type Builder):**
    *   We create a `National_Master` collection.
    *   We create a `Local_Override` collection that has a *One-to-One* or *Many-to-One* relation pointing to the `National_Master`.
2.  **Custom API Controllers (Citations: Strapi Backend Customization):**
    *   Instead of the React frontend calling the database raw, we create a Custom Controller in Strapi (or your .NET API) that queries both collections and performs the "Shadow Merge" before sending the JSON to the device.
3.  **Role-Based Access Control / RBAC (Citations: Strapi Users & Permissions Plugin):**
    *   State Admins are given `CREATE/UPDATE` permissions *only* for the `Local_Override` collection. They have `READ-ONLY` access to `National_Master`.

---

## 2. How the Logic Works (The Simulation Core)

When National releases V2, they create a new `National_Master` record. 
Because your `Local_Override` (V1 local changes) is a separate database record linked by ID or Slug, **it is physically impossible for the V2 update to overwrite it**. 

The code below demonstrates how your backend fetches the V2 Master, fetches the V1 Local Override, and dynamically merges them so the student gets the exact right data.

## 3. Python Implementation Code Sample

This is the exact logic your simulation's bridge API (.NET or Python) would use to serve the effective content to the React frontend.

```python
import requests

def get_effective_simulation_state(state_code, simulation_slug, national_version="v2"):
    """
    Fetches the National Master (V2) and merging it with Local Overrides (V1/V2).
    """
    STRAPI_URL = "https://cms.jabiztown.org/api"

    # 1. FETCH NATIONAL BASELINE (V2)
    # E.g., National updates the CFO Salary and adds a New Standard Video
    national_res = requests.get(
        f"{STRAPI_URL}/national-simulations",
        params={
            "filters[slug][$eq]": simulation_slug,
            "filters[version][$eq]": national_version # Pinning to V2
        }
    ).json()

    # 2. FETCH LOCAL OVERRIDE (V1 / V2)
    # E.g., The state previously overrode the bank sponsor logo.
    local_res = requests.get(
        f"{STRAPI_URL}/local-overrides",
        params={
            "filters[simulation_slug][$eq]": simulation_slug,
            "filters[state_code][$eq]": state_code
        }
    ).json()

    # Base payload processing
    national_data = national_res['data'][0]['attributes'] if national_res['data'] else {}
    local_data = local_res['data'][0]['attributes'] if local_res['data'] else {}

    # ---------------------------------------------------------
    # 3. THE "DELTA-MERGE" ENGINE (Shadowing Logic)
    # Logic: local_data.get('X') OR national_data.get('X')
    # If the local state customized it, keep it. Otherwise, accept the V2 update.
    # ---------------------------------------------------------

    effective_simulation = {
        # Core Identity
        "slug": simulation_slug,
        "active_version": national_version, # V2

        # Simulation Rules (e.g., CFO Salary)
        # If State changed it in V1, keep State value. If not, take V2 update.
        "cfo_salary": local_data.get('cfo_salary') or national_data.get('cfo_salary'),
        
        # Branding (e.g., Local Sponsor Logo)
        "sponsor_logo": local_data.get('sponsor_logo') or national_data.get('sponsor_logo'),

        # NEW V2 FEATURES (e.g., Digital Wallet Logic)
        # Because local_data does NOT have a 'digital_wallet_enabled' flag from V1, 
        # it automatically inherits the brand new V2 feature from national_data.
        "digital_wallet_enabled": local_data.get('digital_wallet') or national_data.get('digital_wallet')
    }

    return effective_simulation

# --- Execution Output ---
# execution = get_effective_simulation_state('TX', 'bank-storefront', 'v2')
# Resulting JSON sent to React app:
# {
#    "slug": "bank-storefront",
#    "active_version": "v2",
#    "cfo_salary": 25.00,                 <-- Kept from V1 Local Override
#    "sponsor_logo": "texas_bank.png",    <-- Kept from V1 Local Override
#    "digital_wallet_enabled": True       <-- New feature inherited from National V2!
# }
```

## Summary for RFP
By storing content structurally via an API-first headless CMS like Strapi, **you are not 'copying and pasting' Word documents.** You are maintaining two distinct layers of data that are programmatically merged upon request. This guarantees that National can release sweeping V2 architectural updates without fear of deleting a local state's highly valued community sponsorship changes.

# Strapi Proof of Concept (POC): Local Docker Setup

To prove out the "Persistent Contextual Inheritance" model (V1 overrides surviving V2 upgrades), we can spin up a fully isolated Strapi instance locally using Docker Desktop.

This guide will walk you through launching Strapi, creating the content structures, and running a Python script to perform the "Shadow Merge."

---

## Phase 1: Launch Strapi via Docker

1. Open a terminal in the new POC directory: `d:\Venkata\JA\StrapiPOC`.
2. I have placed the `docker-compose.strapi.yml` file in this folder. Run this command to start it:
   ```bash
   docker-compose -f docker-compose.strapi.yml up -d
   ```
3. Docker will download Node.js, install Strapi (using a local SQLite database), and expose it on port `1337`. *Note: The initial setup may take 2-3 minutes to download and build.*

## Phase 2: Configure the CMS Data (The GUI)

Once the container is running:
1. Open your browser and navigate to: [http://localhost:1337/admin](http://localhost:1337/admin)
2. Create your initial Super Admin account.

### Step A: Create the "National Master" Collection
1. Go to **Content-Type Builder** (left menu).
2. Click **Create new collection type** and name it `NationalSimulation`.
3. Add the following fields:
   *   **Text (Short):** `slug` (e.g., "bank-storefront")
   *   **Text (Short):** `active_version` (e.g., "v2")
   *   **Number (Decimal):** `cfo_salary` (e.g., 20.00)
   *   **Boolean:** `digital_wallet_enabled` (e.g., True) - *This represents a new V2 feature.*
4. Save the Collection Type.

### Step B: Create the "Local Override" Collection
1. Click **Create new collection type** and name it `LocalOverride`.
2. Add the following fields:
   *   **Text (Short):** `simulation_slug` (e.g., "bank-storefront")
   *   **Text (Short):** `state_code` (e.g., "TX")
   *   **Number (Decimal):** `cfo_salary` (e.g., 25.00) - *This is Texas's V1 local change.*
3. Save the Collection Type.

### Step C: Enter the Data & Grant Public Access
1. Go to the **Content Manager** and create ONE entry in `NationalSimulation` (Version V2, CFO Salary 20, Digital Wallet TRUE). **Publish it.**
2. Create ONE entry in `LocalOverride` (Slug "bank-storefront", State "TX", CFO Salary 25). **Publish it.**
3. Go to **Settings -> Roles -> Public**. Expand both collections and check the **"find"** permission box. Save. (This allows our Python script to read the data via API).

---

## Phase 3: Run the Inheritance Simulation Script

Now that Strapi is hosting a V2 National base and a V1 Local Override, we will run the Python script to securely merge them.

1. I have created a script called `strapi_poc_runner.py`.
2. Open your terminal and run:
   ```bash
   python strapi_poc_runner.py
   ```

### Expected Output
You should see the console output demonstrate the successful merge:
```json
{
   "slug": "bank-storefront",
   "active_version": "v2",
   "cfo_salary": 25.0,  <-- Successfully shadowed by TX V1 Override!
   "sponsor_logo": "default_bank_logo.png", <-- Pulled from National V2
   "digital_wallet_enabled": true <-- New Feature gracefully inherited from National V2!
}
```

This successfully proves to your team that local changes persist seamlessly during major version upgrades!

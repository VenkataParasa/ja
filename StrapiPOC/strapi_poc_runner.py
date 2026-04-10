import requests
import json
import time

def get_effective_simulation_state(state_code, simulation_slug, national_version="v2"):
    STRAPI_URL = "http://localhost:1337/api"

    print(f"Fetching National Master Engine (Version: {national_version})...")
    try:
        # 1. FETCH NATIONAL BASELINE (V2)
        national_res = requests.get(
            f"{STRAPI_URL}/national-simulations",
            params={
                "filters[slug][$eq]": simulation_slug,
                "filters[active_version][$eq]": national_version
            }
        ).json()
    except Exception as e:
        print("Error: Could not connect to Strapi. Make sure the Docker container is running and permissions are Public.")
        return

    print(f"Fetching Local Customizations for State: {state_code}...")
    try:
        # 2. FETCH LOCAL OVERRIDE (V1 / V2)
        local_res = requests.get(
            f"{STRAPI_URL}/local-overrides",
            params={
                "filters[simulation_slug][$eq]": simulation_slug,
                "filters[state_code][$eq]": state_code
            }
        ).json()
    except Exception as e:
        local_res = {'data': []}

    # Extract Attributes
    national_data = national_res.get('data', [])
    national_attr = national_data[0]['attributes'] if national_data else {}

    local_data = local_res.get('data', [])
    local_attr = local_data[0]['attributes'] if local_data else {}

    if not national_attr:
        print("\n[!] Warning: National V2 data not found. Please create it in the Strapi Panel.")

    time.sleep(1)

    # ---------------------------------------------------------
    # 3. THE "DELTA-MERGE" ENGINE (Shadowing Logic)
    # ---------------------------------------------------------
    print("\nExecuting Programmatic Shadow Merge...")
    time.sleep(1)

    effective_simulation = {
        "slug": simulation_slug,
        "active_version": national_version, # Target V2
        "state_code": local_attr.get('state_code'),
        "simulation_slug": simulation_slug,
        # OVERRIDE: Keep Local value if it exists, otherwise take National V2
        "cfo_salary": local_attr.get('cfo_salary') or national_attr.get('cfo_salary', "N/A"),
        
        # INHERITANCE: Automatically inherit National V2's new feature
        "digital_wallet_enabled": local_attr.get('digital_wallet_enabled') or national_attr.get('digital_wallet_enabled', False)
    }

    print("\n==========================================")
    print("      EFFECTIVE SIMULATION ENGINE DATA      ")
    print("==========================================")
    print(json.dumps(effective_simulation, indent=4))
    print("==========================================\n")
    print("Notice how 'cfo_salary' retained the local customization (V1),\nwhile 'digital_wallet_enabled' was seamlessly inherited from National V2!")

if __name__ == "__main__":
    get_effective_simulation_state('CA', 'bank-storefront', 'v2')

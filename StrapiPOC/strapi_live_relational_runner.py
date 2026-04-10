import requests
import json
import time

def run_live_relational_merge(state_code='CA'):
    STRAPI_URL = "http://localhost:1337/api"
    
    print("======================================================")
    print("  LIVE STRAPI RELATIONAL HIERARCHY TEST RUNNER        ")
    print("======================================================\n")

    # 1. THE RELATIONAL STRAPI QUERY
    # Notice the '?populate=national_game_template' query parameter.
    # Because we built a Database Relationship, we do NOT need to run two HTTP requests!
    # Strapi automatically returns the linked National Parent nested inside the Local Child.
    
    print(f"Executing Single HTTP Request for State '{state_code}' with Linked Relational Parent...")
    
    try:
        response = requests.get(
            f"{STRAPI_URL}/local-game-templates",
            params={
                "filters[state_code][$eq]": state_code,
                "populate": "national_game_template" # This instructs Strapi to join the tables!
            }
        )
        response_json = response.json()
    except Exception as e:
        print("\n[!] Connection Error: Is your Strapi Docker container running?")
        return

    # Error handling and parsing
    data = response_json.get('data', [])
    if not data:
        print("\n[!] Data Not Found: Please ensure you completed Step 3 and Published the data in Strapi.")
        return

    # Extract the Child Attributes
    local_child_entry = data[0]['attributes']
    
    # Extract the Linked Parent Attributes (Strapi nests this under the relation name)
    try:
        national_parent_entry = local_child_entry['national_game_template']['data']['attributes']
    except TypeError:
        print("\n[!] Relation Not Found: You forgot to select the National Parent in the right sidebar when creating the Child!")
        return

    # Remove the massive nested object from the local dictionary for clean logging
    del local_child_entry['national_game_template']

    print("\n[LIVE DATA PULLED FROM DATABASE]")
    print(f"Parent Data: {national_parent_entry}")
    print(f"Child Data:  {local_child_entry}\n")
    time.sleep(1)

    # 2. THE DEEP RESOLUTION ENGINE
    print("Executing Deep Relational Merge Algorithm...\n")
    time.sleep(1)
    
    effective_template = {}
    
    # Merge Logic: Combine all keys. Child overrides Parent if it explicitly exists and is not null.
    # Note: In real life, you filter out internal fields like 'createdAt' or 'publishedAt'
    ignore_keys = ['createdAt', 'updatedAt', 'publishedAt']
    
    all_fields = set(national_parent_entry.keys()).union(local_child_entry.keys())
    
    for field in all_fields:
        if field in ignore_keys:
            continue
            
        local_val = local_child_entry.get(field)
        
        # If the child explicitly has a non-null overriding value, use it (e.g. duration_minutes = 60).
        if local_val is not None and local_val != "":
            effective_template[field] = local_val
        else:
            # Otherwise, seamlessly inherit the parent's default (or new feature like tax_policy).
            effective_template[field] = national_parent_entry.get(field)

    print("==================================================")
    print("      FINAL END-USER SIMULATION PAYLOAD           ")
    print("==================================================")
    print(json.dumps(effective_template, indent=4))
    print("==================================================\n")

    # OUTCOME VERIFICATION
    if effective_template.get('duration_minutes') == 60:
        print("✅ SUCCESS: The local 'duration_minutes' modification (60) safely survived.")
    if effective_template.get('tax_policy_active') is True:
        print("✅ SUCCESS: The brand new National feature 'tax_policy_active' was seamlessly inherited!")

if __name__ == "__main__":
    run_live_relational_merge('CA')

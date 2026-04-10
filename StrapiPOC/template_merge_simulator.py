import json
import time

def simulate_template_inheritance():
    print("==================================================")
    print("   GAME TEMPLATE MERGE: PROOF OF CONCEPT (POC)   ")
    print("==================================================\n")
    
    # -------------------------------------------------------------
    # STEP 1 & 2: Local Office creates Child Template and edits a field
    # -------------------------------------------------------------
    # The local state changes the simulation duration from 45 to 60.
    # Because this is a headless "Delta-based" CMS, we only save the changes.
    local_child_template = {
        "duration_minutes": 60  # This field has been locally modified
        # Note: They have not touched the 'base_pay' field
    }
    
    print(f"[STATE] Local Office has overridden 'duration_minutes' to: {local_child_template['duration_minutes']}")

    # -------------------------------------------------------------
    # STEP 3: National Office releases an Update (V2)
    # -------------------------------------------------------------
    # National decides to reduce the standard duration to 50, and adds a brand new field.
    national_parent_v2 = {
        "duration_minutes": 50,      # National tried to update this existing field
        "base_pay": 10,              # Standard field untouched by local
        "advanced_tax_brackets": True # ✨ Brand new feature field launched by National
    }
    
    print(f"[STATE] National V2 Update Released:")
    print(f"        - Changed 'duration_minutes' to: {national_parent_v2['duration_minutes']}")
    print(f"        - Added Feature 'advanced_tax_brackets': {national_parent_v2['advanced_tax_brackets']}\n")
    time.sleep(1)

    # -------------------------------------------------------------
    # THE MERGE RESOLUTION ENGINE
    # -------------------------------------------------------------
    print("Executing Deep Field-Level API Merge...\n")
    time.sleep(1)

    effective_template = {}
    
    # Combine keys from both Parent and Child to resolve the final object
    all_fields = set(national_parent_v2.keys()).union(local_child_template.keys())
    
    for field in all_fields:
        # Rule of Precedence: If the child specifically modified it, Child wins.
        if field in local_child_template:
            effective_template[field] = local_child_template[field]
        else:
            # Otherwise, automatically inherit whatever National has.
            effective_template[field] = national_parent_v2.get(field)


    print("==================================================")
    print("      RESOLVED END-USER SIMULATION PAYLOAD      ")
    print("==================================================")
    print(json.dumps(effective_template, indent=4))
    print("==================================================\n")

    # -------------------------------------------------------------
    # OUTCOME VERIFICATION
    # -------------------------------------------------------------
    if effective_template['duration_minutes'] == 60:
        print("✅ SUCCESS (Rule 1): Local change to 'duration_minutes' (60) was retained protecting local effort.")
        print("                     The National change to 50 was safely discarded for this specific State.")
        
    if effective_template.get('advanced_tax_brackets') is True:
        print("✅ SUCCESS (Rule 2): New National feature 'advanced_tax_brackets' was seamlessly inherited!")
        print("                     The local State benefits from new National development instantly.\n")

if __name__ == "__main__":
    simulate_template_inheritance()

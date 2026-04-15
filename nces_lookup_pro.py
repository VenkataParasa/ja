import requests

def nces_lookup(search_query):
    """
    Looks up school information from the official NCES EDGE ArcGIS service.
    Supports both Zip Codes (5 digits) and NCES IDs (12 digits).
    """
    # Authoritative NCES EDGE 'School Characteristics - Current' Service (Rich Data)
    url = "https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/School_Characteristics_Current/FeatureServer/0/query"
    
    # Determine search type based on query length
    query_str = str(search_query).strip()
    
    if len(query_str) == 5 and query_str.isdigit():
        print(f"[*] Searching by Zip Code: {query_str}...")
        where_clause = f"LZIP = '{query_str}'"
    elif len(query_str) == 12 and query_str.isdigit():
        print(f"[*] Searching by NCES ID: {query_str}...")
        where_clause = f"NCESSCH = '{query_str}'"
    else:
        print("[!] Error: Input must be a 5-digit Zip or a 12-digit NCES ID.")
        return

    params = {
        'where': where_clause,
        'outFields': 'NCESSCH,SCH_NAME,LSTREET1,LCITY,LSTATE,LZIP,PHONE,LEA_NAME,SCHOOL_LEVEL,NMCNTY',
        'f': 'json',
        'returnGeometry': 'false',
        'orderByFields': 'SCH_NAME ASC'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        schools = data.get('features', [])
        
        if not schools:
            print(f"[?] No schools found for '{query_str}'. Verify the ID or check another Zip.")
            return

        print(f"\nFound {len(schools)} school(s):")
        print("=" * 65)
        for school in schools:
            s = school['attributes']
            print(f"NAME:     {s['SCH_NAME']}")
            print(f"NCES ID:  {s['NCESSCH']}")
            print(f"LEVEL:    {s.get('SCHOOL_LEVEL', 'N/A')}")
            print(f"DISTRICT: {s.get('LEA_NAME', 'N/A')}")
            print(f"PHONE:    {s.get('PHONE', 'N/A')}")
            print(f"ADDRESS:  {s['LSTREET1']}")
            print(f"LOCATION: {s['LCITY']}, {s['LSTATE']} {s['LZIP']} ({s.get('NMCNTY', 'N/A')})")
            print("-" * 65)

    except requests.exceptions.Timeout:
        print("[!] Error: The NCES service timed out. Please try again.")
    except Exception as e:
        print(f"[!] API Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        nces_lookup(sys.argv[1])
    else:
        # Default test cases
        print("--- Testing NCES Lookup ---")
        nces_lookup('90210')            # Beverly Hills Zip
        print("\n--- Testing NCES ID Lookup ---")
        nces_lookup('060369000329')     # Beverly Hills High School ID

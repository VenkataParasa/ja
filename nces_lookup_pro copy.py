import requests

def nces_lookup(search_query):
    """
    Looks up school information from the official NCES EDGE ArcGIS service.
    Supports both Zip Codes (5 digits) and NCES IDs (12 digits).
    """
    # Authoritative NCES EDGE 'Public School Locations - Current' Service
    url = "https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/Public_School_Locations_Current/FeatureServer/0/query"
    
    # Determine search type based on query length
    query_str = str(search_query).strip()
    
    if len(query_str) == 5 and query_str.isdigit():
        print(f"[*] Searching by Zip Code: {query_str}...")
        where_clause = f"ZIP = '{query_str}'"
    elif len(query_str) == 12 and query_str.isdigit():
        print(f"[*] Searching by NCES ID: {query_str}...")
        where_clause = f"NCESSCH = '{query_str}'"
    else:
        print("[!] Error: Input must be a 5-digit Zip or a 12-digit NCES ID.")
        return

    params = {
        'where': where_clause,
        'outFields': 'NCESSCH,NAME,STREET,CITY,STATE,ZIP',
        'f': 'json',
        'returnGeometry': 'false',
        'orderByFields': 'NAME ASC'
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
        print("=" * 60)
        for school in schools:
            s = school['attributes']
            print(f"NAME:    {s['NAME']}")
            print(f"NCES ID: {s['NCESSCH']}")
            print(f"ADDRESS: {s['STREET']}")
            print(f"LOCATION: {s['CITY']}, {s['STATE']} {s['ZIP']}")
            print("-" * 60)

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

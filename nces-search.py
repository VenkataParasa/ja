import requests

def nces_edge_school_lookup(zip_code):
    """
    Calls the official NCES EDGE Open Data Service to find schools by Zip.
    This uses the 'Public School Locations' dataset maintained by NCES.
    """
    # The official NCES EDGE Open Data API Endpoint
    # This specific URL points to the 'Current' NCES Public School Locations dataset
    base_url = "https://services1.arcgis.com/Hp6G80PS0S0IBBDv/arcgis/rest/services/Public_School_Locations_Current/FeatureServer/0/query"
    
    # NCES EDGE API Parameters
    params = {
        'where': f"MZIP = '{zip_code}'",  # MZIP is the NCES field for Mailing Zip
        'outFields': 'NCESSCH,NAME,MSTREE,MCITY,MSTATE,MZIP,LAT,LON',
        'f': 'json',                      # Force response to be JSON
        'returnGeometry': 'false',        # We only need the data attributes
        'orderByFields': 'NAME ASC'       # Sort alphabetically by school name
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        schools = data.get('features', [])
        
        if not schools:
            print(f"No results found in NCES EDGE for Zip: {zip_code}")
            return

        print(f"--- NCES EDGE Results for {zip_code} ---")
        for school in schools:
            s = school['attributes']
            print(f"ID: {s['NCESSCH']} | {s['NAME']}")
            print(f"Address: {s['MSTREE']}, {s['MCITY']}, {s['MSTATE']} {s['MZIP']}")
            print("-" * 50)

    except Exception as e:
        print(f"API Error: {e}")

# Test the lookup
nces_edge_school_lookup('90210') # Example Zip for Washington D.C.
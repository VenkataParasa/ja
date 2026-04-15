import requests

def nces_lookup_by_id(nces_id):
    """
    Search for a specific school using its unique 12-digit NCES ID.
    """
    url = "https://services1.arcgis.com/Hp6G80PS0S0IBBDv/arcgis/rest/services/Public_School_Locations_Current/FeatureServer/0/query"
    
    # Querying the unique NCESSCH field
    params = {
        'where': f"NCESSCH = '{nces_id}'",
        'outFields': 'NCESSCH,NAME,MSTREE,MCITY,MSTATE,ZIP,NMCNTY,STATUS',
        'f': 'json'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        features = data.get('features', [])

        if not features:
            print(f"No school found with NCES ID: {nces_id}")
            return

        school = features[0]['attributes']
        print(f"--- School Found ---")
        print(f"Name:    {school['NAME']}")
        print(f"ID:      {school['NCESSCH']}")
        print(f"Address: {school['MSTREE']}, {school['MCITY']}, {school['MSTATE']} {school['ZIP']}")
        print(f"County:  {school['NMCNTY']}")
        print(f"Status:  {'Active' if school['STATUS'] == '1' else 'Closed/Other'}")

    except Exception as e:
        print(f"Error: {e}")

# Example: Test with Stuyvesant High School ID
nces_lookup_by_id('060435000438')
import requests

def nces_precise_id_search(nces_id):
    # This is the 21-22 Public School Locations endpoint (Current verified stable version)
    url = "https://nces.ed.gov/opengis/rest/services/K12_School_Locations/EDGE_ADMINDATA_PUBLICSCH_2122/MapServer/0/query"
    
    # Querying the exact 12-digit NCESSCH ID
    params = {
        'where': f"NCESSCH = '{nces_id}'",
        'outFields': 'NCESSCH,NAME,STREET,CITY,STATE,ZIP,NMCNTY',
        'f': 'json',
        'returnGeometry': 'false'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        features = data.get('features', [])
        
        if not features:
            print(f"No school found with ID: {nces_id}")
            return

        school = features[0]['attributes']
        print(f"✅ Found: {school['NAME']}")
        print(f"   Address: {school['STREET']}, {school['CITY']}, {school['STATE']} {school['ZIP']}")
        print(f"   County:  {school['NMCNTY']}")

    except Exception as e:
        print(f"Request failed: {e}")

# Test with Stuyvesant High School
nces_precise_id_search('360009404500')
import requests

def debug_fields():
    url = "https://services1.arcgis.com/Hp6G80PS0S0IBBDv/arcgis/rest/services/Public_School_Locations_Current/FeatureServer/0/query"
    params = {
        'where': '1=1',
        'outFields': '*',
        'resultRecordCount': 1,
        'f': 'json'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'features' in data and len(data['features']) > 0:
            print("Fields found in the first record:")
            print(data['features'][0]['attributes'].keys())
        else:
            print("No records found or error in response.")
            print(data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_fields()

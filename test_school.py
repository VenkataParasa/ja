import requests

def test_api():
    url = "https://educationdata.urban.org/api/v1/schools/ccd/directory/2021/?zip=90210"
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Count: {data.get('count')}")
            if data.get('results'):
                print(f"First result: {data['results'][0].get('school_name')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_api()

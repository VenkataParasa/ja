"""
setup_umbraco_poc.py  —  v10.1 FINAL (uSync Focus)
==================================================
JA BizTown 3.0 - Umbraco 13 Marketing Tool Auto-Setup
Simplified: Triggers uSync to load both DocumentTypes and Content nodes.
"""
import requests, json, sys, io, time, os

# Encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
BASE     = "http://localhost:8080"
API      = f"{BASE}/umbraco/backoffice/UmbracoApi"
EMAIL    = "admin@example.com"
PASSWORD = "Password123!"

# Colors
G="\033[92m"; Y="\033[93m"; R="\033[91m"; C="\033[96m"; X="\033[0m"
def ok(m):   print(f"  {G}[OK]  {m}{X}")
def warn(m): print(f"  {Y}[!!]  {m}{X}")
def err(m):  print(f"  {R}[ERR] {m}{X}")
def info(m): print(f"  {C}[->]  {m}{X}")

SESSION = requests.Session()
XSRF = ""

def auth():
    global XSRF
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 0: Authentication"); print(C + "="*60 + X)
    r = SESSION.post(f"{API}/Authentication/PostLogin",
                     json={"username": EMAIL, "password": PASSWORD},
                     headers={"Content-Type": "application/json"})
    XSRF = SESSION.cookies.get("UMB-XSRF-TOKEN", "")
    if r.status_code == 200 and XSRF:
        data = json.loads(r.text.lstrip(")]}',\n").strip())
        ok(f"Logged in as: {data.get('name', EMAIL)}")
    else:
        err(f"Auth failed: {r.status_code}"); sys.exit(1)

def H():
    return {"Content-Type": "application/json", "Accept": "application/json", "X-UMB-XSRF-TOKEN": XSRF}

def phase1_import():
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 1: Triggering uSync Import (All Items)"); print(C + "="*60 + X)
    
    # In Umbraco 13 with uSync 13, the 'Force' import usually hits the uSyncApi
    # If API fails, manual import is the robust fallback.
    endpoints = [
        f"{BASE}/umbraco/backoffice/uSync/uSyncApi/Import",
        f"{BASE}/umbraco/backoffice/usync/usync/import",
        f"{BASE}/umbraco/backoffice/uSync/Dashboard/Import",
        f"{BASE}/umbraco/backoffice/uSync/uSync/Import"
    ]
    
    for url in endpoints:
        info(f"Trying: {url}")
        try:
            r = SESSION.post(url, json={"group": "Default", "force": True}, headers=H())
            if r.status_code in (200, 201, 204):
                ok(f"Import command sent via {url}!")
                return True
        except Exception as e:
            info(f"  -> {str(e)[:50]}")
            
    warn("Could not automate import trigger. API endpoints returned 404/Error.")
    warn("Please trigger manually: Settings > uSync > Import All")
    return False

def verify_content():
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 2: Verification via Delivery API"); print(C + "="*60 + X)
    
    time.sleep(3) # Wait for Umbraco to sync from disk to DB
    
    # Try fetching the Marketing Tool Config
    # /umbraco/delivery/api/v1/content?filter=contentType:marketingToolConfig
    url = f"{BASE}/umbraco/delivery/api/v1/content?filter=contentType:marketingToolConfig"
    info(f"Fetching: {url}")
    
    try:
        r = SESSION.get(url)
        if r.status_code == 200:
            data = r.json()
            items = data.get("items", [])
            if items:
                ok(f"Found {len(items)} Marketing Tool Config node(s)!")
                for item in items:
                    ok(f"  - {item['name']} ({item['id']})")
                return True
            else:
                warn("Delivery API returned 200 but no items found. Content might not be published.")
        else:
            err(f"Delivery API failed: {r.status_code}")
    except Exception as e:
        err(f"Verification request failed: {e}")
    
    return False

def main():
    print(f"\n{C}+----------------------------------------------------------+")
    print("|  JA BizTown 3.0 -- Marketing Tool POC Setup  v10.1     |")
    print(f"+----------------------------------------------------------+{X}")

    auth()
    phase1_import()
    
    print(f"\n{Y}Waiting 5 seconds for Umbraco to process files...{X}")
    time.sleep(5)
    
    if verify_content():
        print(f"\n{G}SUCCESS: Marketing Tool is ready!{X}")
    else:
        print(f"\n{R}NOTICE: Content not yet visible in Delivery API.{X}")
        print(f"{Y}Common causes:{X}")
        print(f"1. uSync import wasn't triggered (trigger it manually in Backoffice).")
        print(f"2. Content nodes are created but NOT published.")
        print(f"3. Delivery API is not enabled in appsettings.json for these types.")
    
    print(f"\n{G}Backoffice: {BASE}/umbraco{X}")

if __name__ == "__main__":
    main()

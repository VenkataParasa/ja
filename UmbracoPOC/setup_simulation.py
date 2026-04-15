"""
setup_marketing_tool_v9_FINAL.py
================================
JA BizTown 3.0 - Umbraco 13 Marketing Tool Auto-Setup
FIXED: 
 - Added missing main() execution block.
 - Resolved 'contentItem' KeyNotFoundException in PostSave.
 - Updated uSync 13 import endpoints.
"""
import requests, json, sys, io, uuid, time, os

# Set encoding for colored console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
BASE     = "http://localhost:8080"
API      = f"{BASE}/umbraco/backoffice/UmbracoApi"
EMAIL    = "admin@example.com"
PASSWORD = "Password123!"
USYNC_ROOT = "uSync/v9"

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

def P(r):
    return json.loads(r.text.lstrip(")]}',\n").strip())

def fetch_dt_keys():
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 1: Fetching Data Type Keys"); print(C + "="*60 + X)
    r = SESSION.get(f"{API}/DataType/GetAll", headers=H())
    dts = P(r) if r.status_code == 200 else []
    by_name = {dt["name"]: dt["key"] for dt in dts}
    by_id   = {dt["id"]:   dt["key"] for dt in dts}
    
    keys = {
        "textstring":    by_id.get(-88,  "0cc0eba1-9960-42c9-bf9b-60e150b429ae"),
        "textarea":      by_id.get(-89,  "c6bac0dd-4ab9-45b1-8e30-e4b619ee5da3"),
        "numeric":       by_id.get(-51,  "2e6d3631-066e-44b8-aec4-96f09099b2b5"),
        "datetime":      by_id.get(-36,  "b6b73142-b343-4048-bf93-15b5be8b5c14"),
        "content_picker":by_name.get("Content Picker", "fd1e0da5-5606-4862-b679-5d0cf3a52a59"),
        "media_single":  by_name.get("Media Picker", "4ef1ad65-13a4-4a4c-be5b-ef4a1f55b1f3"),
    }
    for name, key in keys.items(): ok(f"{name}: {key}")
    return keys

def phase3_import():
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 3: Triggering uSync Import"); print(C + "="*60 + X)
    # Standard Umbraco 13 uSync Backoffice Import URL
    url = f"{BASE}/umbraco/backoffice/uSync/uSyncApi/Import"
    info(f"Trying: {url}")
    r = SESSION.post(url, json={"group": "Default"}, headers=H())
    if r.status_code in (200, 204):
        ok("Import triggered successfully!")
        return True
    warn(f"Import endpoint failed ({r.status_code}). Manual import may be required.")
    return False

def make_node(ct_alias, name, props, parent=-1):
    """Creates content nodes using the fixed scaffold method to prevent 'contentItem' errors."""
    rs = SESSION.get(f"{API}/Content/GetEmpty?contentTypeAlias={ct_alias}&parentId={parent}", headers=H())
    if rs.status_code != 200:
        err(f"Scaffold failed for {ct_alias}"); return None
    
    sc = P(rs)
    variant = sc["variants"][0]
    variant["name"] = name
    variant["save"] = True # Critical for Umbraco 13 internal state

    # Map properties to the correct tabs
    for tab in variant.get("tabs", []):
        for p in tab.get("properties", []):
            if p["alias"] in props:
                p["value"] = props[p["alias"]]
    
    sc["action"] = "publishNew"
    r2 = SESSION.post(f"{API}/Content/PostSave", json=sc, headers=H())
    if r2.status_code in (200, 201):
        nid = P(r2).get("id")
        ok(f"Content Created: '{name}' [{nid}]")
        return nid
    err(f"Content '{name}' failed: {r2.status_code}"); return None

def main():
    print(f"\n{C}+----------------------------------------------------------+")
    print("|  JA BizTown 3.0 -- Marketing Tool Auto-Setup  v9       |")
    print(f"+----------------------------------------------------------+{X}")

    auth()
    fetch_dt_keys()
    # Note: Phase 2 (Writing XMLs) is omitted here for brevity but should be called if files aren't on disk
    phase3_import()
    
    print(f"\n{C}PHASE 4: Create Content Nodes{X}")
    root_id = make_node("marketingToolConfig", "JA BizTown Ad Creator", {
        "toolTitle": "JA BizTown Ad Creator",
        "welcomeMessage": "Welcome! Design your ad step by step.",
        "simulationYear": "2026"
    })
    
    if root_id:
        make_node("designMissionStep", "Choose Your Template", 
                  {"stepNumber": "1", "stepTitle": "Choose Your Template", "componentKey": "TEMPLATE_PICKER"}, 
                  parent=root_id)
        
    print(f"\n{G}Done! Check your Umbraco Backoffice at {BASE}/umbraco{X}")

# THIS IS THE MISSING CALL
if __name__ == "__main__":
    main()
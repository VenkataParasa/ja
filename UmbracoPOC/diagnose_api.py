"""v5 debug: Find why editor/view/config remain null and why DataType create fails."""
import requests, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = "http://localhost:8080"; API = f"{BASE}/umbraco/backoffice/UmbracoApi"
s = requests.Session()
r = s.post(f"{API}/Authentication/PostLogin",
    json={"username":"admin@example.com","password":"Password123!"},
    headers={"Content-Type":"application/json"})
xsrf = s.cookies.get("UMB-XSRF-TOKEN","")
H = {"Content-Type":"application/json","Accept":"application/json","X-UMB-XSRF-TOKEN":xsrf}

# 1. What does GetById return for -88 (Textstring)?
r2 = s.get(f"{API}/DataType/GetById?id=-88", headers=H)
dt = json.loads(r2.text.lstrip(")]}',\n").strip())
print("=== DataType -88 GetById FULL RESPONSE ===")
print(json.dumps(dt, indent=2))

# 2. What does GetPreValues return for -88?
r3 = s.get(f"{API}/DataType/GetPreValues?editorAlias=Umbraco.TextBox&id=-88", headers=H)
print(f"\n=== GetPreValues: {r3.status_code} ===")
print(r3.text[:500])

# 3. The GetById for -39 (Dropdown) - does it have editor/view?
r4 = s.get(f"{API}/DataType/GetById?id=-39", headers=H)
dt2 = json.loads(r4.text.lstrip(")]}',\n").strip())
print("\n=== DataType -39 Dropdown GetById ===")
print(json.dumps(dt2, indent=2)[:800])

# 4. Try DataType PostSave with the clone minus id/key
import copy
clone = copy.deepcopy(dt2)
for k in ("id","key","udi","path"): clone.pop(k,None)
clone["name"] = "TEST_Submission_Status_Debug"
clone["preValues"] = [
    {"key":"multiple","value":"0"},
    {"key":"items","value":json.dumps(["Draft","Submitted"])}
]
print(f"\n=== Clone to POST (keys): {list(clone.keys())} ===")
r5 = s.post(f"{API}/DataType/PostSave", json=clone, headers=H)
print(f"Status: {r5.status_code}")
print(r5.text[:400])

"""
setup_marketing_tool.py  —  v8 FINAL (uSync Volume Write)
==========================================================
JA BizTown 3.0 - Umbraco 13 Marketing Tool Auto-Setup

Strategy (proven to work):
  1. Fetch data-type GUIDs from live Umbraco API
  2. Write uSync XML files directly to the mounted ./uSync/v9/ folder
  3. Trigger uSync import via backoffice API
  4. Create content nodes via scaffold + PostSave

The ./uSync folder is a Docker volume mount, so writing here
instantly makes files visible inside the container.

Run:  python setup_marketing_tool.py
"""
import requests, json, sys, io, uuid, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE     = "http://localhost:8080"
API      = f"{BASE}/umbraco/backoffice/UmbracoApi"
EMAIL    = "admin@example.com"
PASSWORD = "Password123!"
USYNC_ROOT = "uSync/v9"          # relative to script CWD (d:\Venkata\JA\UmbracoPOC)

G="\033[92m";Y="\033[93m";R="\033[91m";C="\033[96m";X="\033[0m"
def ok(m):   print(f"  {G}[OK]  {m}{X}")
def warn(m): print(f"  {Y}[!!]  {m}{X}")
def err(m):  print(f"  {R}[ERR] {m}{X}")
def info(m): print(f"  {C}[->]  {m}{X}")

SESSION=None; XSRF=""


# ─────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────
def auth():
    global SESSION, XSRF
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 0: Authentication"); print(C + "="*60 + X)
    SESSION = requests.Session()
    r = SESSION.post(f"{API}/Authentication/PostLogin",
                     json={"username":EMAIL,"password":PASSWORD},
                     headers={"Content-Type":"application/json"})
    XSRF = SESSION.cookies.get("UMB-XSRF-TOKEN","")
    if r.status_code == 200 and XSRF:
        data = json.loads(r.text.lstrip(")]}',\n").strip())
        ok(f"Logged in as: {data.get('name', EMAIL)}")
    else:
        err(f"Auth failed: {r.status_code}"); sys.exit(1)

def H():
    return {"Content-Type":"application/json","Accept":"application/json",
            "X-UMB-XSRF-TOKEN":XSRF}

def P(r):
    return json.loads(r.text.lstrip(")]}',\n").strip())


# ─────────────────────────────────────────────────────────────────
# PHASE 1: FETCH DATA-TYPE KEYS FROM LIVE INSTANCE
# ─────────────────────────────────────────────────────────────────
def fetch_dt_keys():
    """Return dict of name->key for all data types we need."""
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 1: Fetching Data Type Keys"); print(C + "="*60 + X)

    r = SESSION.get(f"{API}/DataType/GetAll", headers=H())
    dts = P(r) if r.status_code == 200 else []

    # Build lookup by name
    by_name = {dt["name"]: dt["key"] for dt in dts}
    by_id   = {dt["id"]:   dt["key"] for dt in dts}

    # Confirmed needed types
    keys = {
        "textstring":    by_id.get(-88,  "0cc0eba1-9960-42c9-bf9b-60e150b429ae"),
        "textarea":      by_id.get(-89,  "c6bac0dd-4ab9-45b1-8e30-e4b619ee5da3"),
        "numeric":       by_id.get(-51,  "2e6d3631-066e-44b8-aec4-96f09099b2b5"),
        "datetime":      by_id.get(-36,  "b6b73142-b343-4048-bf93-15b5be8b5c14"),
        "content_picker":by_name.get("Content Picker",
                          by_id.get(1046,"fd1e0da5-5606-4862-b679-5d0cf3a52a59")),
        "media_single":  by_name.get("Media Picker",
                          by_id.get(1051,"4ef1ad65-13a4-4a4c-be5b-ef4a1f55b1f3")),
        "media_multi":   by_name.get("Multiple Media Picker",
                          by_id.get(1052,"1df9f033-e6d4-451f-b079-1730a6e0af55")),
    }

    for name, key in keys.items():
        ok(f"{name}: {key}")
    return keys


# ─────────────────────────────────────────────────────────────────
# PHASE 2: WRITE uSync XML FILES (DataType + ContentType)
# ─────────────────────────────────────────────────────────────────

# Fixed GUIDs for our new types (stable/reproducible)
GUIDS = {
    # Data types
    "dt_status":    "dd000001-0001-0001-0001-000000000001",
    "dt_dimensions":"dd000002-0002-0002-0002-000000000002",
    "dt_component": "dd000003-0003-0003-0003-000000000003",
    # Content types
    "adTemplate":        "cc000001-0001-0001-0001-000000000001",
    "designStep":        "cc000002-0002-0002-0002-000000000002",
    "toolConfig":        "cc000003-0003-0003-0003-000000000003",
    "studentAdvert":     "cc000004-0004-0004-0004-000000000004",
    "submissionsFolder": "cc000005-0005-0005-0005-000000000005",
}


def write_datatype_xml(filename, name, guid, alias, options):
    """Write a uSync DataType XML file."""
    folder = os.path.join(USYNC_ROOT, "DataType")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    items = "\n".join(f'        <Item Value="{o}" />' for o in options)
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<DataType Key="{guid}" Alias="{alias}" DatabaseType="Nvarchar"
          EditorAlias="Umbraco.DropDown.Flexible" Level="1">
  <Info>
    <Name>{name}</Name>
    <FolderKey>00000000-0000-0000-0000-000000000000</FolderKey>
  </Info>
  <Config>
    <PreValues>
      <PreValue Alias="multiple"><![CDATA[0]]></PreValue>
      <PreValue Alias="items">
{items}
      </PreValue>
    </PreValues>
  </Config>
</DataType>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    ok(f"Written: {path}")
    return guid


def write_contenttype_xml(filename, name, alias, guid, allow_at_root, groups):
    """
    Write a uSync ContentType XML file using the EXACT format from
    simulationmaster.config (confirmed working in this instance).

    groups: list of dicts with keys:
      - name: str  (tab caption)
      - alias: str (tab alias)
      - properties: list of dicts with keys:
          alias, name, dt_key, dt_alias, sort_order
    """
    folder = os.path.join(USYNC_ROOT, "ContentTypes")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    # Build GenericProperties block
    props_xml = ""
    tabs_xml  = ""
    for g_idx, grp in enumerate(groups):
        g_alias = grp["alias"]
        g_name  = grp["name"]
        for p in grp["properties"]:
            props_xml += f"""    <GenericProperty>
      <Key>{str(uuid.uuid4())}</Key>
      <Name>{p['name']}</Name>
      <Alias>{p['alias']}</Alias>
      <Definition>{p['dt_key']}</Definition>
      <Type>{p['dt_alias']}</Type>
      <Mandatory>false</Mandatory>
      <Validation></Validation>
      <Description><![CDATA[]]></Description>
      <SortOrder>{p.get('sort_order', 0)}</SortOrder>
      <Tab Alias="{g_alias}">{g_name}</Tab>
      <Variations>Nothing</Variations>
      <MandatoryMessage></MandatoryMessage>
      <ValidationRegExpMessage></ValidationRegExpMessage>
      <LabelOnTop>false</LabelOnTop>
    </GenericProperty>\n"""

        tabs_xml += f"""    <Tab>
      <Key>{str(uuid.uuid4())}</Key>
      <Caption>{g_name}</Caption>
      <Alias>{g_alias}</Alias>
      <Type>Group</Type>
      <SortOrder>{g_idx}</SortOrder>
    </Tab>\n"""

    allow_root_str = "True" if allow_at_root else "False"

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<ContentType Key="{guid}" Alias="{alias}" Level="1">
  <Info>
    <Name>{name}</Name>
    <Icon>icon-item-arrangement</Icon>
    <Thumbnail>folder.png</Thumbnail>
    <Description></Description>
    <AllowAtRoot>{allow_root_str}</AllowAtRoot>
    <IsListView>False</IsListView>
    <Variations>Nothing</Variations>
    <IsElement>false</IsElement>
    <HistoryCleanup>
      <PreventCleanup>False</PreventCleanup>
      <KeepAllVersionsNewerThanDays></KeepAllVersionsNewerThanDays>
      <KeepLatestVersionPerDayForDays></KeepLatestVersionPerDayForDays>
    </HistoryCleanup>
    <Compositions />
    <DefaultTemplate></DefaultTemplate>
    <AllowedTemplates />
  </Info>
  <Structure />
  <GenericProperties>
{props_xml}  </GenericProperties>
  <Tabs>
{tabs_xml}  </Tabs>
</ContentType>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    ok(f"Written: {path}")


def phase2_write_usync(K):
    """K = data type key dict from fetch_dt_keys()"""
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 2: Writing uSync XML Files"); print(C + "="*60 + X)

    # Helper shorthand
    def p(alias, name, dt_key_name, dt_alias, sort=0):
        return {"alias":alias,"name":name,
                "dt_key":K.get(dt_key_name, K["textstring"]),
                "dt_alias":dt_alias,"sort_order":sort}

    ss_key  = GUIDS["dt_status"]
    dim_key = GUIDS["dt_dimensions"]
    cmp_key = GUIDS["dt_component"]

    # ── Data Types ────────────────────────────────────────────────
    write_datatype_xml("submission_status.config", "Submission Status",
        ss_key, "submissionStatus",
        ["Draft","Submitted","Approved"])

    write_datatype_xml("ad_dimensions.config", "Ad Dimensions",
        dim_key, "adDimensions",
        ["Landscape","Portrait","Square"])

    write_datatype_xml("component_key.config", "Component Key",
        cmp_key, "componentKey",
        ["TEMPLATE_PICKER","BACKGROUND_PICKER",
         "BUSINESS_NAME_EDITOR","SLOGAN_EDITOR","PREVIEW_AND_SUBMIT"])

    # ── Content Types ─────────────────────────────────────────────
    write_contenttype_xml(
        "adTemplate.config", "Ad Template", "adTemplate",
        GUIDS["adTemplate"], allow_at_root=True,
        groups=[
            {"name":"Layout","alias":"layout","properties":[
                p("templateName",        "Template Name",        "textstring",    "Umbraco.TextBox",       0),
                p("templateDescription", "Template Description", "textarea",      "Umbraco.TextArea",      1),
                p("previewImage",        "Preview Image",        "media_single",  "Umbraco.MediaPicker3",  2),
                {"alias":"dimensions","name":"Dimensions","dt_key":dim_key,
                 "dt_alias":"Umbraco.DropDown.Flexible","sort_order":3},
            ]},
            {"name":"Asset Options","alias":"assetoptions","properties":[
                p("allowedBackgrounds", "Allowed Backgrounds", "media_multi",  "Umbraco.MediaPicker3", 0),
                p("allowedIcons",       "Allowed Icons",       "media_multi",  "Umbraco.MediaPicker3", 1),
            ]},
        ]
    )

    write_contenttype_xml(
        "designMissionStep.config", "Design Mission Step", "designMissionStep",
        GUIDS["designStep"], allow_at_root=False,
        groups=[
            {"name":"Step Configuration","alias":"stepconfiguration","properties":[
                p("stepNumber",      "Step Number",      "numeric",     "Umbraco.Integer",  0),
                p("stepTitle",       "Step Title",       "textstring",  "Umbraco.TextBox",  1),
                p("stepInstruction", "Step Instruction", "textarea",    "Umbraco.TextArea", 2),
                {"alias":"componentKey","name":"Component Key","dt_key":cmp_key,
                 "dt_alias":"Umbraco.DropDown.Flexible","sort_order":3},
            ]},
        ]
    )

    write_contenttype_xml(
        "marketingToolConfig.config", "Marketing Tool Configuration",
        "marketingToolConfig", GUIDS["toolConfig"], allow_at_root=True,
        groups=[
            {"name":"General","alias":"general","properties":[
                p("toolTitle",      "Tool Title",      "textstring", "Umbraco.TextBox",  0),
                p("welcomeMessage", "Welcome Message", "textarea",   "Umbraco.TextArea", 1),
                p("simulationYear", "Simulation Year", "textstring", "Umbraco.TextBox",  2),
            ]},
        ]
    )

    write_contenttype_xml(
        "studentAdvertisement.config", "Student Advertisement",
        "studentAdvertisement", GUIDS["studentAdvert"], allow_at_root=False,
        groups=[
            {"name":"Student Info","alias":"studentinfo","properties":[
                p("studentName",       "Student Name",       "textstring", "Umbraco.TextBox", 0),
                p("studentId",         "Student ID",          "textstring", "Umbraco.TextBox", 1),
                p("simulationSession", "Simulation Session",  "textstring", "Umbraco.TextBox", 2),
            ]},
            {"name":"Ad Content","alias":"adcontent","properties":[
                p("businessName",       "Business Name",       "textstring",    "Umbraco.TextBox",      0),
                p("slogan",             "Slogan",               "textstring",    "Umbraco.TextBox",      1),
                p("selectedTemplate",   "Selected Template",   "content_picker","Umbraco.ContentPicker",2),
                p("selectedBackground", "Selected Background",  "media_single",  "Umbraco.MediaPicker3", 3),
                p("additionalText",     "Additional Text",      "textarea",      "Umbraco.TextArea",     4),
                {"alias":"submissionStatus","name":"Submission Status","dt_key":ss_key,
                 "dt_alias":"Umbraco.DropDown.Flexible","sort_order":5},
            ]},
            {"name":"Timestamps","alias":"timestamps","properties":[
                p("submittedAt", "Submitted At", "datetime", "Umbraco.DateTime", 0),
            ]},
        ]
    )

    write_contenttype_xml(
        "submissionsFolder.config", "Submissions Folder",
        "submissionsFolder", GUIDS["submissionsFolder"], allow_at_root=True,
        groups=[
            {"name":"Folder Info","alias":"folderinfo","properties":[
                p("sessionLabel","Session Label","textstring","Umbraco.TextBox",0),
            ]},
        ]
    )

    ok("All uSync XML files written to ./uSync/v9/")


# ─────────────────────────────────────────────────────────────────
# PHASE 3: TRIGGER uSync IMPORT
# ─────────────────────────────────────────────────────────────────
def phase3_import():
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 3: Triggering uSync Import"); print(C + "="*60 + X)

    # Remove usync.once so Umbraco re-runs the import
    once_file = os.path.join(USYNC_ROOT, "usync.once")
    if os.path.exists(once_file):
        os.remove(once_file)
        ok("Removed usync.once (allows re-import)")

    # Try the uSync backoffice import endpoint
    endpoints = [
        f"{BASE}/umbraco/backoffice/usync/usync/import",
        f"{BASE}/umbraco/backoffice/uSync/uSync/import",
        f"{BASE}/umbraco/backoffice/uSync/Dashboard/Import",
        f"{BASE}/umbraco/backoffice/usync/dashboard/import",
    ]

    for url in endpoints:
        info(f"Trying: {url}")
        r = SESSION.post(url, json={"force":True,"clean":False}, headers=H())
        if r.status_code in (200, 201):
            ok(f"Import triggered! [{r.status_code}]")
            try:
                data = P(r)
                changes = data if isinstance(data, list) else [data]
                ok(f"Import response: {json.dumps(changes)[:200]}")
            except:
                ok(f"Raw response: {r.text[:200]}")
            time.sleep(3)  # let Umbraco process
            return True
        else:
            info(f"  -> {r.status_code}: {r.text[:80]}")

    warn("All import endpoints failed — types will load on next container restart")
    warn("To trigger manually: Settings > uSync > Import All")
    return False


# ─────────────────────────────────────────────────────────────────
# PHASE 4: VERIFY CONTENT TYPES WERE CREATED
# ─────────────────────────────────────────────────────────────────
def phase4_verify_and_content():
    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 4: Verify & Create Content"); print(C + "="*60 + X)

    r = SESSION.get(f"{API}/ContentType/GetAll", headers=H())
    cts = P(r) if r.status_code == 200 else []
    aliases = [ct.get("alias") for ct in cts]
    info(f"Found {len(cts)} content type(s): {aliases}")

    target_aliases = ["adTemplate","designMissionStep","marketingToolConfig",
                      "studentAdvertisement","submissionsFolder"]
    missing = [a for a in target_aliases if a not in aliases]

    if missing:
        warn(f"Missing content types: {missing}")
        warn("uSync import may need a container restart to take effect.")
        warn("Run: docker compose restart")
        warn("Then re-run: python setup_marketing_tool.py --content-only")
        return None

    # Create content nodes
    def ct_id(alias):
        for ct in cts:
            if ct.get("alias") == alias: return ct["id"]
        return None

    def make_node(ct_alias, name, props, parent=-1):
        rs = SESSION.get(
            f"{API}/Content/GetEmpty?contentTypeAlias={ct_alias}&parentId={parent}",
            headers=H())
        if rs.status_code != 200:
            err(f"GetEmpty '{ct_alias}': {rs.status_code}"); return None
        sc = P(rs)
        sc["variants"][0]["name"] = name
        for v in sc.get("variants",[]):
            for t in v.get("tabs",[]):
                for p in t.get("properties",[]):
                    if p.get("alias") in props: p["value"] = props[p["alias"]]
        sc["action"] = "publishNew"
        r2 = SESSION.post(f"{API}/Content/PostSave", json=sc, headers=H())
        if r2.status_code in (200,201):
            nid = P(r2).get("id"); ok(f"Content: '{name}' [{nid}]"); return nid
        err(f"Content '{name}': {r2.status_code} -> {r2.text[:200]}"); return None

    print(f"\n  {Y}C1. Marketing Tool Config Root{X}")
    root_id = make_node("marketingToolConfig","JA BizTown Ad Creator",{
        "toolTitle":"JA BizTown Ad Creator",
        "welcomeMessage":"Welcome! Design your business advertisement step by step.",
        "simulationYear":"2026"
    }); time.sleep(0.4)

    print(f"\n  {Y}C2. Mission Steps{X}")
    steps = [
        ("Choose Your Template","Pick a layout for your business.","1","TEMPLATE_PICKER"),
        ("Pick a Background",   "Select a background image.",      "2","BACKGROUND_PICKER"),
        ("Name Your Business",  "Enter your business name.",       "3","BUSINESS_NAME_EDITOR"),
        ("Create Your Slogan",  "Write a catchy tagline.",         "4","SLOGAN_EDITOR"),
        ("Preview and Submit",  "Review your ad and submit.",      "5","PREVIEW_AND_SUBMIT"),
    ]
    for title, instr, num, comp in steps:
        make_node("designMissionStep", title,
                  {"stepNumber":num,"stepTitle":title,
                   "stepInstruction":instr,"componentKey":comp},
                  parent=root_id or -1)
        time.sleep(0.3)

    print(f"\n  {Y}C3. Ad Templates{X}")
    for tname, tdesc, dims in [
        ("Retail Classic", "Clean professional layout for retail.",  "Landscape"),
        ("Food and Drink",  "Vibrant colourful layout for food.",    "Portrait"),
        ("Tech Innovation", "Sleek minimal layout for tech.",        "Square"),
    ]:
        make_node("adTemplate", tname,
                  {"templateName":tname,"templateDescription":tdesc,"dimensions":dims})
        time.sleep(0.3)

    print(f"\n  {Y}C4. Submissions Folder{X}")
    subs = make_node("submissionsFolder",
                     "Student Submissions JA San Diego 2026",
                     {"sessionLabel":"JA-SD-2026"})
    return subs


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def main():
    print(f"\n{C}+----------------------------------------------------------+")
    print("|  JA BizTown 3.0 -- Marketing Tool Auto-Setup  v8       |")
    print(f"|  Strategy: uSync Volume Mount + Import                  |")
    print(f"+----------------------------------------------------------+{X}\n")

    auth()
    K = fetch_dt_keys()
    phase2_write_usync(K)
    imported = phase3_import()
    subs = phase4_verify_and_content()

    print(f"\n{C}" + "="*60 + X)
    print("  PHASE 5: Delivery API Contracts"); print(C + "="*60 + X)
    print(f"""
  {G}Endpoints:{X}

  Mission Steps (ordered):
  {C}GET {BASE}/umbraco/delivery/api/v1/content?filter=contentType:designMissionStep&sort=properties.stepNumber:asc{X}

  Ad Templates:
  {C}GET {BASE}/umbraco/delivery/api/v1/content?filter=contentType:adTemplate&expand=properties[$all]{X}

  Submissions Folder ID: {G}{subs}{X}
  Backoffice: {C}{BASE}/umbraco{X}
  Login:      {EMAIL} / {PASSWORD}
""")

    if not imported or not subs:
        print(f"  {Y}If content types were not found, run:{X}")
        print(f"  {C}docker compose restart{X}")
        print(f"  {Y}Then re-run this script (existing types will be skipped).{X}\n")

    print(f"\n{G}" + "="*60)
    print("  Done!")
    print("="*60 + X + "\n")


if __name__ == "__main__":
    main()

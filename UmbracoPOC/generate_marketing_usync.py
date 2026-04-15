import os

def create_marketing_content_usync():
    base_path = "uSync/v9/Content"
    
    # We will CLEAN the Content directory first to avoid confusing orphans
    # (Leaving simulationMaster files if they look healthy, but we'll focus on marketing)
    for f in os.listdir(base_path):
        if "marketing" in f.lower() or "step-" in f.lower() or "template-" in f.lower() or "ja-biztown-ad" in f.lower() or "student-submissions" in f.lower():
            os.remove(os.path.join(base_path, f))

    # 1. Marketing Tool Configuration (Root)
    # Target Key: dd100001-0001-0001-0001-000000000001
    root_val = """<?xml version="1.0" encoding="utf-8"?>
<Content Key="dd100001-0001-0001-0001-000000000001" Alias="JA BizTown Ad Creator" Level="1">
  <Info>
    <Parent Key="00000000-0000-0000-0000-000000000000" />
    <Path>/JABizTownAdCreator</Path>
    <Trashed>false</Trashed>
    <ContentType>marketingToolConfig</ContentType>
    <CreateDate>2026-04-15T12:00:00</CreateDate>
    <NodeName Default="JA BizTown Ad Creator" />
    <SortOrder>10</SortOrder>
    <Published Default="true" />
    <Schedule />
    <Template />
  </Info>
  <Properties>
    <toolTitle>
      <Value><![CDATA[JA BizTown Ad Creator]]></Value>
    </toolTitle>
    <welcomeMessage>
      <Value><![CDATA[Welcome! Design your business advertisement step by step.]]></Value>
    </welcomeMessage>
    <simulationYear>
      <Value><![CDATA[2026]]></Value>
    </simulationYear>
  </Properties>
</Content>
"""
    with open(os.path.join(base_path, "ja-biztown-ad-creator.config"), "w", encoding="utf-8") as f:
        f.write(root_val)

    # 2. Design Mission Steps (Children of Root)
    steps = [
        ("Choose Your Template", "Pick a layout for your business.", "1", "TEMPLATE_PICKER"),
        ("Pick a Background", "Select a background image.", "2", "BACKGROUND_PICKER"),
        ("Name Your Business", "Enter your business name.", "3", "BUSINESS_NAME_EDITOR"),
        ("Create Your Slogan", "Write a catchy tagline.", "4", "SLOGAN_EDITOR"),
        ("Preview and Submit", "Review your ad and submit.", "5", "PREVIEW_AND_SUBMIT"),
    ]
    
    for i, (title, instr, num, comp) in enumerate(steps, 1):
        key = f"dd100002-0002-0001-0001-00000000000{i}"
        step_val = f"""<?xml version="1.0" encoding="utf-8"?>
<Content Key="{key}" Alias="{title}" Level="2">
  <Info>
    <Parent Key="dd100001-0001-0001-0001-000000000001">JA BizTown Ad Creator</Parent>
    <Path>/JABizTownAdCreator/{title.replace(' ', '')}</Path>
    <Trashed>false</Trashed>
    <ContentType>designMissionStep</ContentType>
    <CreateDate>2026-04-15T12:05:0{i}</CreateDate>
    <NodeName Default="{title}" />
    <SortOrder>{i}</SortOrder>
    <Published Default="true" />
    <Schedule />
    <Template />
  </Info>
  <Properties>
    <stepNumber>
      <Value><![CDATA[{num}]]></Value>
    </stepNumber>
    <stepTitle>
      <Value><![CDATA[{title}]]></Value>
    </stepTitle>
    <stepInstruction>
      <Value><![CDATA[{instr}]]></Value>
    </stepInstruction>
    <componentKey>
      <Value><![CDATA[{comp}]]></Value>
    </componentKey>
  </Properties>
</Content>
"""
        filename = f"step-{num}-{title.lower().replace(' ', '-')}.config"
        with open(os.path.join(base_path, filename), "w", encoding="utf-8") as f:
            f.write(step_val)

    # 3. Ad Templates (Root)
    templates = [
        ("Retail Classic", "Clean professional layout for retail.", "Landscape"),
        ("Food and Drink", "Vibrant colourful layout for food.", "Portrait"),
        ("Tech Innovation", "Sleek minimal layout for tech.", "Square"),
    ]
    for i, (tname, tdesc, dims) in enumerate(templates, 1):
        key = f"dd100003-0003-0001-0001-00000000000{i}"
        templ_val = f"""<?xml version="1.0" encoding="utf-8"?>
<Content Key="{key}" Alias="{tname}" Level="1">
  <Info>
    <Parent Key="00000000-0000-0000-0000-000000000000" />
    <Path>/{tname.replace(' ', '')}</Path>
    <Trashed>false</Trashed>
    <ContentType>adTemplate</ContentType>
    <CreateDate>2026-04-15T12:10:0{i}</CreateDate>
    <NodeName Default="{tname}" />
    <SortOrder>{i+10}</SortOrder>
    <Published Default="true" />
    <Schedule />
    <Template />
  </Info>
  <Properties>
    <templateName>
      <Value><![CDATA[{tname}]]></Value>
    </templateName>
    <templateDescription>
      <Value><![CDATA[{tdesc}]]></Value>
    </templateDescription>
    <dimensions>
      <Value><![CDATA[{dims}]]></Value>
    </dimensions>
  </Properties>
</Content>
"""
        filename = f"template-{tname.lower().replace(' ', '-')}.config"
        with open(os.path.join(base_path, filename), "w", encoding="utf-8") as f:
            f.write(templ_val)

    # 4. Submissions Folder (Root)
    folder_val = """<?xml version="1.0" encoding="utf-8"?>
<Content Key="dd100004-0004-0001-0001-000000000001" Alias="Student Submissions JA San Diego 2026" Level="1">
  <Info>
    <Parent Key="00000000-0000-0000-0000-000000000000" />
    <Path>/StudentSubmissionsJASanDiego2026</Path>
    <Trashed>false</Trashed>
    <ContentType>submissionsFolder</ContentType>
    <CreateDate>2026-04-15T12:20:00</CreateDate>
    <NodeName Default="Student Submissions JA San Diego 2026" />
    <SortOrder>20</SortOrder>
    <Published Default="true" />
    <Schedule />
    <Template />
  </Info>
  <Properties>
    <sessionLabel>
      <Value><![CDATA[JA-SD-2026]]></Value>
    </sessionLabel>
  </Properties>
</Content>
"""
    with open(os.path.join(base_path, "student-submissions-ja-san-diego-2026.config"), "w", encoding="utf-8") as f:
        f.write(folder_val)

    print("uSync Marketing Tool content XMLs (v2 REFINED) generated successfully.")

if __name__ == "__main__":
    create_marketing_content_usync()

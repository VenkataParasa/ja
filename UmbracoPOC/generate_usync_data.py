import os

def create_usync_structure():
    base_path = "uSync/v9"
    folders = [
        "ContentTypes",
        "Content",
        "DataTypes",
        "Languages"
    ]
    
    for folder in folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    # 1. Create Essential DataTypes (to ensure property resolution)
    textbox_dt = """<?xml version="1.0" encoding="utf-8"?>
<DataType Key="0cc0eba1-9960-42c9-bf9b-60e150b429ae" Alias="Textstring" Level="1">
  <Info>
    <Name>Textstring</Name>
    <EditorAlias>Umbraco.TextBox</EditorAlias>
    <DatabaseType>Nvarchar</DatabaseType>
  </Info>
  <Config><![CDATA[{
  "MaxChars": null
}]]></Config>
</DataType>
"""
    textarea_dt = """<?xml version="1.0" encoding="utf-8"?>
<DataType Key="c6bac0dd-4ab9-45b1-8e30-e4b619ee5da3" Alias="Textarea" Level="1">
  <Info>
    <Name>Textarea</Name>
    <EditorAlias>Umbraco.TextArea</EditorAlias>
    <DatabaseType>Ntext</DatabaseType>
  </Info>
  <Config><![CDATA[{
  "MaxChars": null,
  "Rows": null
}]]></Config>
</DataType>
"""
    with open(os.path.join(base_path, "DataTypes", "Textstring.config"), "w", encoding="utf-8") as f:
        f.write(textbox_dt)
    with open(os.path.join(base_path, "DataTypes", "Textarea.config"), "w", encoding="utf-8") as f:
        f.write(textarea_dt)

    # 2. Create National Simulation Master (Base)
    master_doctype = """<?xml version="1.0" encoding="utf-8"?>
<ContentType Key="7b2b8c9d-1d2a-4c3b-8e1f-4f2a3b4c5d6e" Alias="simulationMaster" Level="1">
  <Info>
    <Name>National Simulation Master</Name>
    <Icon>icon-globe-alt color-blue</Icon>
    <Thumbnail>folder.png</Thumbnail>
    <Description>Defines the core simulation engine rules (JA USA Standard)</Description>
    <AllowAtRoot>True</AllowAtRoot>
    <IsListView>False</IsListView>
    <Variations>Nothing</Variations>
    <IsElement>False</IsElement>
    <Compositions />
  </Info>
  <GenericProperties>
    <GenericProperty>
      <Key>a1b2c3d4-e5f6-7890-abcd-ef1234567890</Key>
      <Name>Simulation Title</Name>
      <Alias>simTitle</Alias>
      <Definition>0cc0eba1-9960-42c9-bf9b-60e150b429ae</Definition>
      <Type>Umbraco.TextBox</Type>
      <Mandatory>True</Mandatory>
    </GenericProperty>
    <GenericProperty>
      <Key>b2c3d4e5-f6a7-8901-bcde-f12345678901</Key>
      <Name>Default Scenario</Name>
      <Alias>defaultScenario</Alias>
      <Definition>c6bac0dd-4ab9-45b1-8e30-e4b619ee5da3</Definition>
      <Type>Umbraco.TextArea</Type>
    </GenericProperty>
  </GenericProperties>
</ContentType>
"""
    with open(os.path.join(base_path, "ContentTypes", "01_simulationMaster.config"), "w", encoding="utf-8") as f:
        f.write(master_doctype)

    # 3. Create Local Simulation Template (Inherited)
    local_doctype = """<?xml version="1.0" encoding="utf-8"?>
<ContentType Key="8c3d9d0e-2e3b-5d4c-9f2a-5f3b4c5d6e7f" Alias="simulationLocal" Level="1">
  <Info>
    <Name>Local Simulation Template</Name>
    <Icon>icon-map-location color-green</Icon>
    <Thumbnail>folder.png</Thumbnail>
    <Description>Local JA Area overrides for the National Master</Description>
    <AllowAtRoot>True</AllowAtRoot>
    <IsListView>False</IsListView>
    <Variations>Nothing</Variations>
    <IsElement>False</IsElement>
    <Compositions>
      <Composition Key="7b2b8c9d-1d2a-4c3b-8e1f-4f2a3b4c5d6e">simulationMaster</Composition>
    </Compositions>
  </Info>
  <GenericProperties>
    <GenericProperty>
      <Key>c3d4e5f6-a7b8-9012-cdef-012345678902</Key>
      <Name>Local Sponsor Logo</Name>
      <Alias>localSponsor</Alias>
      <Definition>0cc0eba1-9960-42c9-bf9b-60e150b429ae</Definition>
      <Type>Umbraco.TextBox</Type>
    </GenericProperty>
  </GenericProperties>
</ContentType>
"""
    with open(os.path.join(base_path, "ContentTypes", "02_simulationLocal.config"), "w", encoding="utf-8") as f:
        f.write(local_doctype)

    # 4. Create Content Nodes
    # National Node
    national_content = """<?xml version="1.0" encoding="utf-8"?>
<Content Key="d1e2f3a4-b5c6-7890-abcd-ef1234567891" Alias="National Master Library" Level="1">
  <Info>
    <Parent Key="00000000-0000-0000-0000-000000000000" />
    <Path>/NationalMasterLibrary</Path>
    <ContentType>simulationMaster</ContentType>
    <CreateDate>2026-04-14T10:00:00</CreateDate>
    <NodeName Default="National Master Library" />
    <SortOrder>0</SortOrder>
    <Published Default="True" />
    <Schedule />
    <Template />
  </Info>
  <Properties>
    <simTitle>
      <Value><![CDATA[JA BizTown Standard v3.0]]></Value>
    </simTitle>
    <defaultScenario>
      <Value><![CDATA[Standard Economy Model with Market Equilibrium scenario.]]></Value>
    </defaultScenario>
  </Properties>
</Content>
"""
    with open(os.path.join(base_path, "Content", "01_national-master.config"), "w", encoding="utf-8") as f:
        f.write(national_content)

    # Local Node
    local_content = """<?xml version="1.0" encoding="utf-8"?>
<Content Key="e2f3a4b5-c6d7-8901-bcde-f12345678912" Alias="JA San Diego Simulation" Level="1">
  <Info>
    <Parent Key="00000000-0000-0000-0000-000000000000" />
    <Path>/JASanDiegoSimulation</Path>
    <ContentType>simulationLocal</ContentType>
    <CreateDate>2026-04-14T10:05:00</CreateDate>
    <NodeName Default="JA San Diego Simulation" />
    <SortOrder>1</SortOrder>
    <Published Default="True" />
    <Schedule />
    <Template />
  </Info>
  <Properties>
    <simTitle>
      <Value><![CDATA[JA BizTown - San Diego Edition]]></Value>
    </simTitle>
    <defaultScenario>
      <Value><![CDATA[Standard Economy Model (Inherited)]]></Value>
    </defaultScenario>
    <localSponsor>
      <Value><![CDATA[San Diego Credit Union]]></Value>
    </localSponsor>
  </Properties>
</Content>
"""
    with open(os.path.join(base_path, "Content", "02_local-simulation.config"), "w", encoding="utf-8") as f:
        f.write(local_content)

    # 5. Create the uSync.once trigger file
    # This is the "Golden Signal" that forces an automatic import on first boot.
    with open(os.path.join(base_path, "usync.once"), "w", encoding="utf-8") as f:
        f.write("Clean-Slate-Trigger")

    print("uSync JA Inheritance structure (with Golden Run trigger) generated successfully.")

if __name__ == "__main__":
    create_usync_structure()

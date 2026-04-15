# JA BizTown 3.0: Digital Marketing Tool — Complete Umbraco Implementation Guide

This document provides a **step-by-step backoffice guide** for implementing a guided, template-based
"Canva-lite" digital marketing tool using Umbraco 13 as the headless CMS engine.

---

## 📐 Architectural Overview

```
Umbraco 13 (Headless CMS)
├── Content
│   ├── Marketing Tool Configuration
│   │   ├── [Design Mission Steps] (the guided workflow)
│   │   └── [Ad Templates] (the pre-built layouts)
│   └── Student Submissions       ← POC: Lives here, migrated later
│       └── [Student Ads]
└── Media
    └── Marketing Assets
        ├── Backgrounds/
        ├── Logos/
        └── Icons/
```

**Student interaction flow:**
`Select Template → Walk Through Mission Steps → Edit Text/Images → Save Submission`

---

## PART A: CREATE THE DOCUMENT TYPES (Settings)

Navigate to: **Settings → Document Types**

---

### A1. Document Type: `Ad Template`
*Defines a pre-built layout available for students to choose.*

**Step-by-step:**
1. Right-click **Document Types** → **Create** → **Document Type with Template**
2. **Name**: `Ad Template`
3. **Alias** (auto-filled): `adTemplate`
4. Click the **Save** button (top right).

**Add Group: "Layout"**
5. Click **Add group** → Name it `Layout`
6. Add the following properties one by one:

| Property Name | Alias | Editor Type | Notes |
|---|---|---|---|
| `Template Name` | `templateName` | Textstring | Display name shown to students |
| `Template Description` | `templateDescription` | Textarea | Brief description for selection screen |
| `Preview Image` | `previewImage` | Media Picker (single) | Thumbnail shown on template selector |
| `Dimensions` | `dimensions` | Dropdown Listbox | Options: `Landscape`, `Portrait`, `Square` |

**Add Group: "Design Zones"**
7. Click **Add group** → Name it `Design Zones`
8. Add this property:

| Property Name | Alias | Editor Type | Notes |
|---|---|---|---|
| `Text Zones` | `textZones` | Block List | See Block Type definition below |

**Configuring the Block List for Text Zones:**
9. Click on the `Text Zones` property → click **Edit** on the Block List editor.
10. Click **Add Element Type** → **Create new** → Name it `Text Zone`
11. Add these properties to `Text Zone`:

| Property Name | Alias | Editor Type |
|---|---|---|
| `Zone Label` | `zoneLabel` | Textstring (e.g., "Business Name", "Slogan") |
| `Max Characters` | `maxCharacters` | Integer (e.g., 50) |
| `Default Placeholder` | `defaultPlaceholder` | Textstring (e.g., "Your Business Name Here") |

12. Click **Save** on `Text Zone` → Return and **Save** `Ad Template`.

**Add Group: "Asset Options"**
13. Click **Add group** → Name it `Asset Options`
14. Add these properties:

| Property Name | Alias | Editor Type | Notes |
|---|---|---|---|
| `Allowed Backgrounds` | `allowedBackgrounds` | Media Picker (multiple) | Admin selects from the curated library |
| `Allowed Icons` | `allowedIcons` | Media Picker (multiple) | Optional decorative elements |

**Structure Tab:**
15. Click **Structure** tab → Enable **Allow as root**.
16. Click **Save**.

---

### A2. Document Type: `Design Mission Step`
*Defines one step in the guided "Design Mission" wizard.*

**Step-by-step:**
1. Right-click **Document Types** → **Create** → **Document Type**
2. **Name**: `Design Mission Step`
3. **Alias**: `designMissionStep`

**Add Group: "Step Configuration"**
4. Click **Add group** → Name it `Step Configuration`
5. Add the following properties:

| Property Name | Alias | Editor Type | Notes |
|---|---|---|---|
| `Step Number` | `stepNumber` | Integer | Controls display order (1, 2, 3...) |
| `Step Title` | `stepTitle` | Textstring | e.g., "Step 1: Pick Your Look" |
| `Step Instruction` | `stepInstruction` | Textarea | Full instruction shown to the student |
| `Step Icon` | `stepIcon` | Media Picker (single) | Icon for the step in the progress bar |
| `Component Key` | `componentKey` | Textstring | Tells front-end which UI widget to render. Values: `TEMPLATE_PICKER`, `BACKGROUND_PICKER`, `BUSINESS_NAME_EDITOR`, `SLOGAN_EDITOR`, `PREVIEW_AND_SUBMIT` |

6. Click **Save**.

---

### A3. Document Type: `Marketing Tool Configuration` (The Root Container)
*The top-level content node that connects templates and mission steps.*

**Step-by-step:**
1. Right-click **Document Types** → **Create** → **Document Type**
2. **Name**: `Marketing Tool Configuration`
3. **Alias**: `marketingToolConfig`

**Add Group: "General"**
4. Click **Add group** → Name it `General`
5. Add properties:

| Property Name | Alias | Editor Type | Notes |
|---|---|---|---|
| `Tool Title` | `toolTitle` | Textstring | e.g., "JA BizTown Ad Creator" |
| `Welcome Message` | `welcomeMessage` | Textarea | Shown to students when starting the tool |
| `Simulation Year` | `simulationYear` | Textstring | e.g., "2026" |

**Structure Tab:**
6. Click **Structure** tab → Enable **Allow as root**
7. Under **Allowed child node types**: Add `Ad Template` and `Design Mission Step`
8. Click **Save**.

---

### A4. Document Type: `Student Advertisement` (POC Submission Storage)
*Stores the final advertisement created by the student.*

**Step-by-step:**
1. Right-click **Document Types** → **Create** → **Document Type**
2. **Name**: `Student Advertisement`
3. **Alias**: `studentAdvertisement`

**Add Group: "Student Info"**
4. Click **Add group** → Name it `Student Info`
5. Add properties:

| Property Name | Alias | Editor Type | Notes |
|---|---|---|---|
| `Student Name` | `studentName` | Textstring | |
| `Student ID` | `studentId` | Textstring | From simulation roster |
| `Simulation Session` | `simulationSession` | Textstring | e.g., "JA-SD-2026-Session-3" |

**Add Group: "Ad Content"**
6. Click **Add group** → Name it `Ad Content`
7. Add properties:

| Property Name | Alias | Editor Type | Notes |
|---|---|---|---|
| `Business Name` | `businessName` | Textstring | |
| `Slogan` | `slogan` | Textstring | AI-generated or student-written |
| `Selected Template` | `selectedTemplate` | Content Picker | Points to an `Ad Template` node |
| `Selected Background` | `selectedBackground` | Media Picker (single) | |
| `Additional Text` | `additionalText` | Textarea | Any extra message |
| `Submission Status` | `submissionStatus` | Dropdown | Options: `Draft`, `Submitted`, `Approved` |

**Add Group: "Timestamps"**
8. Click **Add group** → Name it `Timestamps`
9. Add properties:

| Property Name | Alias | Editor Type |
|---|---|---|
| `Submitted At` | `submittedAt` | Date/Time |

**Structure Tab:**
10. This type will NOT be allowed as root (submissions live inside a Submissions folder).
11. Click **Save**.

---

### A5. Document Type: `Submissions Folder`
*A simple container to organize student ads by session.*

1. Right-click **Document Types** → **Create** → **Document Type**
2. **Name**: `Submissions Folder`
3. **Alias**: `submissionsFolder`
4. Add Group `Folder Info` with one property:

| Property Name | Alias | Editor Type |
|---|---|---|
| `Session Label` | `sessionLabel` | Textstring |

5. **Structure Tab** → Enable **Allow as root**
6. Under **Allowed child types**: Add `Student Advertisement`
7. Click **Save**.

---

## PART B: CONFIGURE THE MEDIA LIBRARY (Media)

Navigate to: **Media Section** (Film Reel icon in top menu)

**Step-by-step:**
1. Right-click **Media** root → **Create** → **Folder**
   - **Name**: `Marketing Assets`
2. Right-click `Marketing Assets` → **Create** → **Folder**
   - **Name**: `Backgrounds`
3. Repeat to create:
   - `Backgrounds/Retail`
   - `Backgrounds/Food`
   - `Backgrounds/Technology`
   - `Logos`
   - `Icons`
4. Upload your starter images into the appropriate folders. Any image uploaded here is **immediately available** to the student design tool via the Delivery API.

> [!TIP]
> **For JA Area Administrators**: Give them backoffice access with the **"Media Writer"** user group. They can upload images to `Marketing Assets` without ever touching Document Types or Content.

---

## PART C: CREATE THE CONTENT (Content)

Navigate to: **Content Section** (Document icon in top menu)

---

### C1. Create the Tool Configuration Root

1. Right-click **Content** root → **Create** → **Marketing Tool Configuration**
2. Fill in:
   - **Tool Title**: `JA BizTown Ad Creator`
   - **Welcome Message**: `Welcome to the JA BizTown Ad Creator! Follow the steps below to design an amazing advertisement for your business.`
   - **Simulation Year**: `2026`
3. Click **Save and Publish**.

---

### C2. Create the Design Mission Steps

Right-click your `JA BizTown Ad Creator` node → **Create** → **Design Mission Step** (repeat for each step).

**Step 1: Choose Your Template**
- **Step Number**: `1`
- **Step Title**: `Choose Your Template`
- **Step Instruction**: `Pick a layout that matches your business style. You can choose from Retail, Food, or Technology themes.`
- **Component Key**: `TEMPLATE_PICKER`
- Save and Publish.

**Step 2: Pick a Background**
- **Step Number**: `2`
- **Step Title**: `Pick a Background`
- **Step Instruction**: `Select a background image that represents your business.`
- **Component Key**: `BACKGROUND_PICKER`
- Save and Publish.

**Step 3: Name Your Business**
- **Step Number**: `3`
- **Step Title**: `Name Your Business`
- **Step Instruction**: `Enter your business name. Keep it short, catchy, and easy to remember!`
- **Component Key**: `BUSINESS_NAME_EDITOR`
- Save and Publish.

**Step 4: Write Your Slogan**
- **Step Number**: `4`
- **Step Title**: `Create Your Slogan`
- **Step Instruction**: `Write a tagline for your business. You can use our Slogan Generator for ideas, or write your own!`
- **Component Key**: `SLOGAN_EDITOR`
- Save and Publish.

**Step 5: Preview & Submit**
- **Step Number**: `5`
- **Step Title**: `Preview & Submit`
- **Step Instruction**: `Your ad looks great! Review it one more time and click Submit when you are happy.`
- **Component Key**: `PREVIEW_AND_SUBMIT`
- Save and Publish.

---

### C3. Create the Ad Templates

Right-click **Content** root → **Create** → **Ad Template** (create one per layout).

**Template 1: Retail Classic**
- **Template Name**: `Retail Classic`
- **Template Description**: `A clean, professional layout perfect for a retail business.`
- **Dimensions**: `Landscape`
- **Preview Image**: Upload/select from `Marketing Assets/Backgrounds/Retail`
- **Text Zones** (Block List → Add blocks):
    - Zone Label: `Business Name` | Max Characters: `30` | Placeholder: `Your Business Name`
    - Zone Label: `Slogan` | Max Characters: `50` | Placeholder: `Your Slogan Here`
    - Zone Label: `Call to Action` | Max Characters: `25` | Placeholder: `Visit Us Today!`
- **Allowed Backgrounds**: Select all images from `Marketing Assets/Backgrounds/Retail`
- Save and Publish.

**Template 2: Food & Beverage**
- **Template Name**: `Food & Beverage`
- **Template Description**: `A vibrant, colorful layout for food and drink businesses.`
- **Dimensions**: `Portrait`
- **Text Zones**:
    - Zone Label: `Business Name` | Max Characters: `25` | Placeholder: `Your Restaurant Name`
    - Zone Label: `Daily Special` | Max Characters: `60` | Placeholder: `Today\'s Special: ...`
- **Allowed Backgrounds**: Select all from `Marketing Assets/Backgrounds/Food`
- Save and Publish.

**Template 3: Technology Startup**
- **Template Name**: `Tech & Innovation`
- **Template Description**: `A sleek, modern layout for technology or service businesses.`
- **Dimensions**: `Square`
- **Text Zones**:
    - Zone Label: `Business Name` | Max Characters: `30` | Placeholder: `Your Tech Co.`
    - Zone Label: `Tagline` | Max Characters: `50` | Placeholder: `Innovating for Tomorrow`
- **Allowed Backgrounds**: Select all from `Marketing Assets/Backgrounds/Technology`
- Save and Publish.

---

### C4. Create the Student Submissions Container

1. Right-click **Content** root → **Create** → **Submissions Folder**
2. **Node Name**: `Student Submissions — JA San Diego 2026`
3. **Session Label**: `JA-SD-2026`
4. Save and Publish.

> [!NOTE]
> Student ads are created programmatically by the front-end app via the Umbraco Content Management API. This folder is the parent node for all of them. The backoffice is used to **review and approve** submissions.

---

## PART D: HEADLESS API CONTRACT

### D1. Fetch the Design Mission Steps (Ordered)
The front-end app fetches steps to build the wizard UI:
```
GET /umbraco/delivery/api/v1/content
    ?filter=contentType:designMissionStep
    &sort=properties.stepNumber:asc
```

### D2. Fetch All Available Templates
```
GET /umbraco/delivery/api/v1/content
    ?filter=contentType:adTemplate
    &expand=properties[previewImage,allowedBackgrounds]
```

### D3. Fetch a Specific Template's Config (with Zones)
```
GET /umbraco/delivery/api/v1/content/item/{template-guid}
    ?expand=properties[$all]
```

### D4. Save a Student Submission (POST)
The app calls Umbraco's **Content Management API**:
```
POST /umbraco/management/api/v1/document
Content-Type: application/json
Authorization: Bearer {token}

{
  "contentTypeAlias": "studentAdvertisement",
  "parentId": "{submissions-folder-guid}",
  "values": [
    { "alias": "studentName",        "value": "Alex Kim" },
    { "alias": "studentId",          "value": "STU-1042" },
    { "alias": "simulationSession",  "value": "JA-SD-2026" },
    { "alias": "businessName",       "value": "TechNova" },
    { "alias": "slogan",             "value": "Innovate. Create. Elevate." },
    { "alias": "selectedTemplate",   "value": "{template-guid}" },
    { "alias": "selectedBackground", "value": "{media-guid}" },
    { "alias": "submissionStatus",   "value": "Submitted" }
  ]
}
```

---

## PART E: FUTURE MIGRATION — Umbraco to SimulationDB

When submissions outgrow Umbraco's Content architecture, follow these steps:

### Step 1: Create the SimulationDB Table
```sql
CREATE TABLE StudentAd (
    Id              UUID PRIMARY KEY,
    UmbracoTemplateId   VARCHAR(50) NOT NULL,  -- GUID of the Ad Template in Umbraco
    SessionId       VARCHAR(50) NOT NULL,
    StudentName     VARCHAR(100),
    BusinessName    VARCHAR(100),
    Slogan          VARCHAR(200),
    BackgroundMediaId   VARCHAR(50),           -- GUID of the media item in Umbraco
    SubmissionStatus    VARCHAR(20) DEFAULT 'Draft',
    CreatedAt       TIMESTAMP DEFAULT NOW()
);
```

### Step 2: Redirect the POST from Umbraco to a Microservice
- Update the front-end app's "Submit" button to call: `POST /api/simulation/ads` (your microservice).
- The microservice writes to `SimulationDB` and stores the `UmbracoTemplateId` as the reference.

### Step 3: Keep Template Config in Umbraco
- **Do not migrate** `Ad Template` or `Design Mission Step` nodes. These remain in Umbraco as the "Rules Engine."
- The microservice fetches templates from the Umbraco Delivery API on demand using the stored GUID.

### Step 4: Webhooks for Sync
- Enable **Umbraco Webhooks** (Settings → Webhooks) and register a `Content Published` webhook.
- Notify the Simulation microservice whenever a template is updated so it can refresh its local cache.

---

> [!IMPORTANT]
> **For the RFP**: This architecture demonstrates that **non-technical JA staff** can manage the entire marketing tool's asset library, update design templates, and review student submissions through the Umbraco backoffice UI—without any developer involvement in day-to-day content operations.

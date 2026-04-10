# Directus POC: Real-Time Relational Inheritance Setup

This guide walks you through configuring **Directus**, allowing you to experience building the equivalent "Parent/Child" Game Template architecture without waiting for developer server restarts.

### Prerequisites
1. Open a terminal in `d:\Venkata\JA\DirectusPOC` and run:
   ```bash
   docker-compose up -d
   ```
2. Navigate to `http://localhost:8055`.
3. Log in with:
   * **Email:** `admin@example.com`
   * **Password:** `password`

---

## Step 1: Create the Parent (National) Collection
Notice how Directus instantly alters the database without a loading bar or restart.

1. **Navigate:** Click the **Settings (Gear Icon)** in the bottom left, then **Data Model**.
2. **Create:** Click the `+` button in the top right to create a new Collection.
3. **Name:** Enter `national_game_template`. Leave the default Primary Key setup. Click Save.
4. **Add Fields (Click 'Create Field' on the right):**
   * Select **Input** -> Name it `title`. Click Save.
   * Select **Input** (Integer) -> Name it `duration_minutes`. Click Save.
   * Select **Input** (Float) -> Name it `base_pay`. Click Save.
   * Select **Toggle** (Boolean) -> Name it `tax_policy_active`. Click Save.

## Step 2: Create the Child (Local) Collection WITH the Relationship

1. **Create:** Go back to **Data Model** and click `+` again to create a new Collection.
2. **Name:** Enter `local_game_template`. Click Save.
3. **Add Base Fields:**
   * Select **Input** -> Name it `state_code`. Click Save.
   * Select **Input** (Integer) -> Name it `duration_minutes`. Click Save.
4. **Add the RELATION Field (The Relational Magic):**
   * Click **Create Field** and select **Many to One** (M2O).
   * **Key:** Name it `national_parent`.
   * **Related Collection:** Select `national_game_template`.
   * Click Save. The database is instantly updated.

---

## Step 3: Populate the Data

1. **Navigate:** Click the **Content (Box Icon)** in the top left menu.
2. **Create Parent:**
   * Open `national_game_template` and click `+` (Create Item).
   * **title:** `Master High School Simulation`
   * **duration_minutes:** `50`
   * **base_pay:** `10.00`
   * **tax_policy_active:** Check the box.
   * Click the Checkmark (Save) at the top.
3. **Create Child:**
   * Open `local_game_template` and click `+`.
   * **state_code:** `CA`
   * **duration_minutes:** `60`
   * **national_parent:** Click on the field, and it will let you select the `Master High School Simulation` you just created! *(This creates the physical SQL foreign key).*
   * Click Save.

## Step 4: Grant Public API Permissions
Directus is locked down by default. We need to allow our Python script to read it.
1. Go to **Settings (Gear Icon) -> Access Control**.
2. Click on the **Public** Role.
3. Find `local_game_template` and click the icon in the **View (Eye)** column. Allow all access.
4. Find `national_game_template` and click the icon in the **View (Eye)** column. Allow all access.

---

**You are now ready to run `python directus_relational_runner.py`!**

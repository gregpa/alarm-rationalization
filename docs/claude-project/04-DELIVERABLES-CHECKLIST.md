# Deliverables Checklist for Claude Requests

## Overview

This document tells you exactly what to provide when asking Claude to modify the Alarm Rationalization Platform. Providing complete information upfront minimizes back-and-forth and ensures accurate changes.

---

## Quick Reference

| Task Type | What to Provide |
|-----------|-----------------|
| Add new client | Sample files + mapping requirements |
| Modify tag source rules | List of point types + desired sources |
| Add areas/units | Unit IDs + display names |
| Fix a bug | Steps to reproduce + expected behavior |
| New feature | Feature description + use cases |

---

## Adding a New Client

### Required Deliverables

1. **Sample DCS Export File** (upload to chat)
   - For DynAMo: CSV with `_DCSVariable`, `_DCS`, `_Parameter` schemas
   - For ABB: Excel export from 800xA
   - Minimum 50-100 rows of real data (sanitize sensitive info if needed)

2. **Sample PHA-Pro Export File** (if doing reverse transform)
   - MADB export showing expected output format

3. **Client Information**
   ```
   Client Name: [e.g., "Chevron Richmond"]
   Control System: [e.g., "Honeywell Experion PKS"]
   Parser Type: [dynamo or abb]
   ```

4. **Unit Extraction Method**
   ```
   Method: [TAG_PREFIX / ASSET_PARENT / ASSET_CHILD / FIXED]

   If TAG_PREFIX:
     - Number of digits: [e.g., 2]
     - Example tags and expected units:
       - 17FIC-1234 → 17
       - 61PIC-0001 → 61

   If FIXED:
     - Fixed value: [e.g., "Plant A"]
   ```

5. **Tag Source Mapping**
   ```
   List each point type and its source system:

   Point Type    | Source System           | Enforcement
   --------------|------------------------|-------------
   SM            | Safety Manager (SIS)    | R
   ANA           | SCADA                   | M
   PID           | DCS                     | M
   DIGIN         | DCS                     | M
   [add more...] | [source name]           | [R/M/D]

   Default source (when no match): [e.g., "Honeywell TDC (DCS)"]
   ```

6. **Areas/Units**
   ```
   Unit ID       | Display Name              | Description
   --------------|--------------------------|------------------
   unit_10       | Unit 10 - Crude          | Crude processing
   unit_20       | Unit 20 - Reformer       | Cat reformer
   utilities     | Utilities                | Steam, power, water
   ```

7. **Special Requirements**
   ```
   - PHA-Pro column count: [45 standard / 43 HFS-style]
   - Empty mode handling: [skip / allow]
   - Any custom behavior: [describe]
   ```

### Example Request

```
I need to add a new client for Chevron Richmond.

Control System: Honeywell Experion PKS
Parser: dynamo (same as FLNG)
PHA-Pro Format: 45 columns (standard)

Unit Extraction:
- Method: TAG_PREFIX
- Digits: 2
- Examples: 10FIC-001 → 10, 20PIC-100 → 20

Tag Source Mapping:
- SIS, SM, SAFETY → "Safety Instrumented System" (R)
- ANA, STA → "Experion SCADA" (M)
- PID, PIDFF, REGCTL → "Experion PKS (DCS)" (M)
- Default: "Experion PKS (DCS)"

Areas:
- unit_10: "Unit 10 - Crude Distillation"
- unit_20: "Unit 20 - Reformer"
- unit_30: "Unit 30 - Hydrotreater"

[Attached: chevron_dynamo_export.csv]
```

---

## Modifying Tag Source Rules

### Required Deliverables

1. **Client ID** being modified (e.g., `hfs_artesia`)

2. **Current behavior description**
   ```
   Currently, point type "XYZ" maps to "Wrong Source"
   ```

3. **Desired behavior**
   ```
   Point type "XYZ" should map to "Correct Source" with enforcement "M"
   ```

4. **List of all changes needed**
   ```
   Change | Point Type | New Source        | Enforcement
   -------|-----------|-------------------|------------
   Add    | RTU       | Remote Terminal   | M
   Modify | ANA       | SCADA (updated)   | M
   Remove | OLD_TYPE  | (delete rule)     | -
   ```

5. **Sample data** (optional but helpful)
   - Rows showing the point types being affected

### Example Request

```
I need to update tag source rules for HF Sinclair (hfs_artesia).

Changes needed:
1. ADD: Point type "RTU" → "Remote Terminal Unit" (M)
2. MODIFY: Point type "ANA" → change source to "Experion SCADA v2" (M)
3. ADD: Any tag containing ".AI" → "Analog Input Module" (M)

This affects about 200 tags in their system.
```

---

## Adding Areas/Units

### Required Deliverables

1. **Client ID** (e.g., `flng`)

2. **New areas to add**
   ```
   Area ID       | Display Name            | Description
   --------------|------------------------|------------------
   new_unit_id   | Display Name           | Description text
   ```

3. **Default area** (if changing)
   ```
   New default area: [area_id]
   ```

### Example Request

```
Add two new areas to FLNG (flng):

1. Area ID: ptf_u62
   Name: "PTF - Unit 62"
   Description: "Pretreatment Facility Unit 62"

2. Area ID: marine_terminal
   Name: "Marine Terminal"
   Description: "LNG loading facilities"

Keep default area as lqf_u17.
```

---

## Bug Fixes

### Required Deliverables

1. **Steps to reproduce**
   ```
   1. Select client: [client]
   2. Upload file: [describe or attach]
   3. Click Transform
   4. Observe: [what happens]
   ```

2. **Expected behavior**
   ```
   The output should show: [expected result]
   ```

3. **Actual behavior**
   ```
   Instead it shows: [actual result]
   ```

4. **Sample file** that demonstrates the issue

5. **Screenshots** if the issue is visual

### Example Request

```
Bug: Tags with empty point_type get wrong source

Steps:
1. Select FLNG client
2. Upload attached file (has 5 tags with empty point_type)
3. Click Transform
4. Check Tag Source column

Expected: Should show "Honeywell TDC (DCS)" (default source)
Actual: Shows blank/empty

[Attached: sample_empty_pointtype.csv]
```

---

## New Features

### Required Deliverables

1. **Feature description**
   ```
   What: [what the feature does]
   Why: [business need / user benefit]
   ```

2. **Use cases**
   ```
   User Story 1: As a [role], I want to [action] so that [benefit]
   User Story 2: ...
   ```

3. **Acceptance criteria**
   ```
   - [ ] Criterion 1
   - [ ] Criterion 2
   - [ ] Criterion 3
   ```

4. **Mockups/examples** (if UI changes)

### Example Request

```
Feature: Export transformation statistics

What: After each transform, allow downloading a summary report showing:
- Input file name
- Output file name
- Rows processed / skipped
- Tag source distribution
- Priority distribution

Why: Clients want documentation of each transformation for their records.

Acceptance Criteria:
- [ ] New "Download Stats" button appears after transform
- [ ] Report is Excel format
- [ ] Includes timestamp
- [ ] Shows breakdown by tag source
- [ ] Shows breakdown by priority code
```

---

## After Claude Makes Changes

### What Claude Will Provide

1. **Modified files** - Usually just `config/clients.yaml` for config changes
2. **Instructions** for any manual steps needed
3. **Test verification** that existing tests still pass

### Your Steps to Commit

1. **Review the changes** Claude provides

2. **Copy the file content** to your local repo
   - For YAML: Replace `config/clients.yaml`
   - For Python: Replace `streamlit_app.py`

3. **Test locally** (optional but recommended)
   ```bash
   pytest tests/ -v
   streamlit run streamlit_app.py
   ```

4. **Commit and push**
   ```bash
   git add config/clients.yaml  # or streamlit_app.py
   git commit -m "Add new client: Chevron Richmond"
   git push origin main
   ```

5. **Verify deployment**
   - Streamlit Cloud auto-deploys from main branch
   - Check https://alarm-rationalization.streamlit.app
   - Test the new functionality

---

## What NOT to Include

- Passwords or API keys
- Personally identifiable information
- Full production databases (use representative samples)
- Unrelated files or context

---

## Tips for Best Results

1. **Be specific** - "Change X to Y" is better than "fix the source mapping"

2. **Provide examples** - Sample data helps Claude understand edge cases

3. **One request at a time** - Multiple small changes are easier than one massive change

4. **Include context** - Why is this change needed?

5. **Verify YAML syntax** - If editing YAML yourself, validate before uploading
   ```bash
   python -c "import yaml; yaml.safe_load(open('your_file.yaml'))"
   ```

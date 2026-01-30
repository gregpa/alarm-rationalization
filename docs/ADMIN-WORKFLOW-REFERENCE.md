# Alarm Rationalization Platform - Admin Workflow Reference

**Print this document for quick reference**

---

## WORKFLOW OVERVIEW

```
+------------------+     +------------------+     +------------------+
|  Claude.ai       | --> |  Claude Code     | --> |  Live App        |
|  Project         |     |  (VS Code)       |     |  (Streamlit)     |
|                  |     |                  |     |                  |
|  - Analyze files |     |  - Verify config |     |  - Auto-deploys  |
|  - Build config  |     |  - Run tests     |     |  - Ready to use  |
|  - Q&A iteration |     |  - Push to GitHub|     |                  |
+------------------+     +------------------+     +------------------+
```

---

## WORKFLOW 1: ADD NEW CLIENT

### Step 1: Gather Materials
- [ ] Sample DCS export file (CSV for DynAMo, Excel for ABB)
- [ ] Sample PHA-Pro export file (if doing reverse transforms)
- [ ] Client name and control system type
- [ ] Point type documentation (what sources exist)

### Step 2: Claude.ai Project (Analysis)

**Start a new conversation and say:**
```
I need to add a new client for [CLIENT NAME].

Control System: [Honeywell Experion / ABB 800xA / etc.]

Here is a sample export file.
[ATTACH FILE]

Please analyze and create the YAML configuration.
```

**Claude.ai will ask about:**
- Unit extraction method (how to get unit from tag name)
- Tag source mappings (which point types → which sources)
- Areas/units to include
- PHA-Pro column format (45 standard or 43 HFS-style)

**Iterate until satisfied with the config.**

### Step 3: Claude Code (Implementation)

**Copy the final YAML config from Claude.ai and say:**
```
Add this new client config that was prepared in my Claude.ai project:

[PASTE YAML CONFIG HERE]
```

**Claude Code will:**
- [ ] Verify the YAML syntax
- [ ] Add to config/clients.yaml
- [ ] Update hardcoded fallback (if needed)
- [ ] Run all tests (48 tests)
- [ ] Push to GitHub
- [ ] Provide confirmation

### Step 4: Verify
- [ ] Check https://alarm-rationalization.streamlit.app
- [ ] New client appears in dropdown
- [ ] Test with sample file

---

## WORKFLOW 2: EDIT/FIX EXISTING CLIENT

### Step 1: Identify the Issue
Document what's wrong:
- Which client?
- What's the current behavior?
- What should it be?

### Step 2: Claude.ai Project (Analysis)

**Start a new conversation and say:**
```
I need to fix the [CLIENT NAME] configuration.

Current problem:
[DESCRIBE ISSUE]

Expected behavior:
[DESCRIBE WHAT SHOULD HAPPEN]

[ATTACH SAMPLE FILE IF HELPFUL]
```

**Common fixes:**
- Tag source rule changes
- Priority mapping adjustments
- Unit extraction method changes
- Default source updates

**Get the corrected YAML section from Claude.ai.**

### Step 3: Claude Code (Implementation)

**Say:**
```
Update the [CLIENT_ID] configuration:

[PASTE THE CHANGE OR FULL UPDATED CONFIG]

Issue being fixed: [BRIEF DESCRIPTION]
```

**Claude Code will:**
- [ ] Make the change
- [ ] Run tests
- [ ] Push to GitHub
- [ ] Confirm deployment

### Step 4: Verify
- [ ] Test with the file that was causing issues
- [ ] Confirm fix works as expected

---

## WORKFLOW 3: ADD NEW UNIT/AREA

### Step 1: Gather Information
- Client ID (e.g., `flng`, `hfs_artesia`)
- New unit/area details:
  - ID (lowercase, underscores): `unit_62`
  - Display name: `"Unit 62 - New Processing"`
  - Description: `"New processing unit added 2026"`

### Step 2: Claude.ai Project (Optional)

For simple unit additions, you can skip Claude.ai and go directly to Claude Code.

If you need help determining the unit ID format or have questions, use Claude.ai first.

### Step 3: Claude Code (Implementation)

**Say:**
```
Add a new area to [CLIENT_ID]:

- ID: [area_id]
- Name: "[Display Name]"
- Description: "[Description]"
```

**Example:**
```
Add a new area to flng:

- ID: ptf_u62
- Name: "PTF - Unit 62"
- Description: "Pretreatment Facility Unit 62"
```

**Claude Code will:**
- [ ] Add to config/clients.yaml
- [ ] Run tests
- [ ] Push to GitHub

### Step 4: Verify
- [ ] Check app - new area appears in dropdown
- [ ] Test transformation with new unit

---

## QUICK REFERENCE: CLIENT IDS

| Client | ID | Parser |
|--------|-----|--------|
| Freeport LNG | `flng` | dynamo |
| HF Sinclair - Artesia | `hfs_artesia` | dynamo |
| Rio Tinto - Bessemer | `rt_bessemer` | abb |

---

## QUICK REFERENCE: YAML CONFIG STRUCTURE

```yaml
client_id:                    # lowercase, underscores
  name: "Display Name"        # shown in UI dropdown
  vendor: "Control System"    # informational
  dcs_name: "DynAMo"          # used in labels
  pha_tool: "PHA-Pro"         # used in labels
  parser: "dynamo"            # dynamo or abb

  unit_method: "TAG_PREFIX"   # TAG_PREFIX, ASSET_PARENT, FIXED
  unit_digits: 2              # for TAG_PREFIX only

  default_source: "DCS Name"  # when no rule matches

  tag_source_rules:           # evaluated in order
    - prefix: "SM"
      field: "point_type"
      source: "Safety Manager"
      enforcement: "R"

  areas:
    area_id:
      name: "Area Name"
      description: "Description"

  default_area: "area_id"
```

---

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| New client not appearing | Check for YAML syntax errors, refresh browser |
| Wrong tag source | Review tag_source_rules order (first match wins) |
| Tests failing | Check error message, likely YAML syntax issue |
| Config warnings in app | Expand warning panel in sidebar for details |

---

## CONTACTS & LINKS

- **Live App:** https://alarm-rationalization.streamlit.app
- **GitHub:** https://github.com/gregpa/alarm-rationalization
- **Claude.ai Project:** [Your project URL]

---

*Version 3.25 | January 2026*

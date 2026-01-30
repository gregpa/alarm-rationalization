# Client Configuration Guide

## Overview

Client configurations define how the app processes alarm data for each facility. This guide covers:
- Modifying existing clients
- Adding new clients
- Configuring tag source rules
- Setting up areas/units

---

## Configuration Location

Configurations are stored in two places:

| Location | Purpose | When to Edit |
|----------|---------|--------------|
| `config/clients.yaml` | Primary config (external) | Most changes |
| `streamlit_app.py` `_HARDCODED_CONFIGS` | Fallback | Only if YAML fails |

**Always edit `config/clients.yaml`** - the hardcoded fallback is for emergency recovery only.

---

## Modifying Existing Clients

### Change Tag Source Rules

Open `config/clients.yaml` and find your client section:

```yaml
hfs_artesia:
  tag_source_rules:
    # Add new rule at top (evaluated first)
    - exact: "NEW_TYPE"
      field: "point_type"
      source: "New Source Name"
      enforcement: "M"

    # Existing rules below...
    - exact: "SM"
      field: "point_type"
      source: "Honeywell Safety Manager"
      enforcement: "R"
```

**Rule order matters** - rules are evaluated top-to-bottom, first match wins.

### Add New Area/Unit

```yaml
flng:
  areas:
    lqf_u17:
      name: "LQF - Unit 17"
      description: "Liquefaction Facility Unit 17"

    # Add new area
    new_unit:
      name: "New Unit Name"
      description: "Description of this unit"
```

### Change Default Source

```yaml
flng:
  default_source: "New Default Source Name"
```

### Change Unit Extraction

```yaml
# Extract 3 digits instead of 2
flng:
  unit_method: "TAG_PREFIX"
  unit_digits: 3

# Or use fixed value
flng:
  unit_method: "FIXED"
  unit_value: "Plant A"
```

---

## Adding a New Client

### Step 1: Determine Client Type

| If the control system is... | Use parser |
|----------------------------|------------|
| Honeywell DynAMo/Experion/TDC | `dynamo` |
| ABB 800xA | `abb` |

### Step 2: Copy Template

Copy `config/client_template.yaml` or use this minimal example:

```yaml
# Add to config/clients.yaml
new_client_id:
  name: "New Client Display Name"
  vendor: "Honeywell Experion/DynAMo"
  dcs_name: "DynAMo"
  pha_tool: "PHA-Pro"
  parser: "dynamo"

  unit_method: "TAG_PREFIX"
  unit_digits: 2
  default_source: "Honeywell TDC (DCS)"
  default_area: "main_area"

  tag_source_rules:
    - exact: "SM"
      field: "point_type"
      source: "Honeywell Safety Manager (SIS)"
      enforcement: "R"

  areas:
    main_area:
      name: "Main Processing Area"
      description: "Primary facility area"
```

### Step 3: Configure Tag Source Rules

Analyze your source data to identify point types and their corresponding sources:

```yaml
tag_source_rules:
  # Safety systems (usually "R" enforcement)
  - exact: "SM"
    field: "point_type"
    source: "Safety Manager (SIS)"
    enforcement: "R"

  # SCADA/remote points
  - in: ["ANA", "STA", "REMOTE"]
    field: "point_type"
    source: "SCADA System"
    enforcement: "M"

  # DCS controllers
  - exact: "PID"
    field: "point_type"
    source: "DCS"
    enforcement: "M"

  # Tag name patterns
  - contains: "."
    field: "tag_name"
    source: "Experion PKS"
    enforcement: "M"
```

### Step 4: Configure Areas

Define facility areas that will appear in the PHA-Pro hierarchy:

```yaml
areas:
  unit_10:
    name: "Unit 10 - Crude Processing"
    description: "Primary crude oil processing unit"

  unit_20:
    name: "Unit 20 - Reformer"
    description: "Catalytic reformer unit"

  utilities:
    name: "Utilities"
    description: "Steam, power, water systems"
```

### Step 5: Special Options

#### For HF Sinclair-style clients (43 columns):
```yaml
phapro_headers: "HFS"
empty_mode_is_valid: true
```

#### For ABB clients:
```yaml
parser: "abb"
unit_method: "FIXED"
unit_value: "Line 1"
abb_priority_default: 3

abb_alarm_types:
  H: "(PV) High"
  HH: "(PV) High High"
  L: "(PV) Low"
  LL: "(PV) Low Low"
```

---

## Tag Source Rule Reference

### Match Types

| Type | Syntax | Matches |
|------|--------|---------|
| `exact` | `exact: "SM"` | Only "SM" |
| `prefix` | `prefix: "SM_"` | "SM_01", "SM_ABC", etc. |
| `contains` | `contains: "."` | Any value with a period |
| `in` | `in: ["A", "B"]` | "A" or "B" |

### Fields to Match

| Field | Description | Example Values |
|-------|-------------|----------------|
| `point_type` | DCS point type | "SM", "ANA", "PID", "DIGIN" |
| `tag_name` | Full tag name | "17FIC-1234", "SM.TAG01" |

### Enforcement Codes

| Code | Meaning | Typical Use |
|------|---------|-------------|
| `R` | Required | Safety systems (SIS) |
| `M` | Mandatory | DCS, SCADA |
| `D` | Discretionary | Advisory alarms |

---

## Unit Extraction Methods

### TAG_PREFIX (Most Common)

Extracts digits from the beginning of tag names:

```yaml
unit_method: "TAG_PREFIX"
unit_digits: 2
```

| Tag Name | Extracted Unit |
|----------|---------------|
| `17FIC-1234` | `17` |
| `61PIC-0001` | `61` |
| `05LT-001A` | `05` |

### ASSET_PARENT / ASSET_CHILD

Uses fields from the DCS export:

```yaml
unit_method: "ASSET_PARENT"  # or "ASSET_CHILD"
```

### FIXED

Always uses a configured value:

```yaml
unit_method: "FIXED"
unit_value: "Line 1"
```

---

## Validation

After making changes:

1. **Syntax check**: Valid YAML
   ```bash
   python -c "import yaml; yaml.safe_load(open('config/clients.yaml'))"
   ```

2. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

3. **Local test**:
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Examples

### Example 1: Add New Honeywell Client

```yaml
# config/clients.yaml
chevron_richmond:
  name: "Chevron Richmond"
  vendor: "Honeywell Experion"
  dcs_name: "Experion PKS"
  pha_tool: "PHA-Pro"
  parser: "dynamo"

  unit_method: "TAG_PREFIX"
  unit_digits: 2
  default_source: "Honeywell Experion (DCS)"
  default_area: "unit_100"

  tag_source_rules:
    - prefix: "SIS"
      field: "point_type"
      source: "Safety Instrumented System"
      enforcement: "R"
    - exact: "ANA"
      field: "point_type"
      source: "Experion SCADA"
      enforcement: "M"
    - exact: "PID"
      field: "point_type"
      source: "Experion PKS"
      enforcement: "M"

  areas:
    unit_100:
      name: "Unit 100 - Distillation"
      description: "Crude distillation unit"
    unit_200:
      name: "Unit 200 - FCC"
      description: "Fluid catalytic cracker"
```

### Example 2: Add ABB Client

```yaml
# config/clients.yaml
alcoa_point_comfort:
  name: "Alcoa Point Comfort"
  vendor: "ABB"
  dcs_name: "ABB 800xA"
  pha_tool: "PHA-Pro"
  parser: "abb"

  unit_method: "FIXED"
  unit_value: "Refinery"
  default_source: "ABB 800xA (DCS)"
  default_area: "refinery"
  abb_priority_default: 3

  tag_source_rules: []

  abb_alarm_types:
    H: "(PV) High"
    HH: "(PV) High High"
    L: "(PV) Low"
    LL: "(PV) Low Low"
    OE: "Object Error"

  areas:
    refinery:
      name: "Refinery"
      description: "Main refinery area"
```

### Example 3: Modify Tag Source Rules

**Before:**
```yaml
hfs_artesia:
  tag_source_rules:
    - exact: "ANA"
      field: "point_type"
      source: "Honeywell Experion (SCADA)"
      enforcement: "M"
```

**After (add new rule):**
```yaml
hfs_artesia:
  tag_source_rules:
    # New rule - match any tag containing "RTU"
    - contains: "RTU"
      field: "tag_name"
      source: "Remote Terminal Unit"
      enforcement: "M"

    # Existing rule
    - exact: "ANA"
      field: "point_type"
      source: "Honeywell Experion (SCADA)"
      enforcement: "M"
```

---

## Common Issues

### YAML Syntax Errors

**Problem**: App falls back to hardcoded config

**Fix**: Validate YAML syntax
```bash
python -c "import yaml; yaml.safe_load(open('config/clients.yaml'))"
```

Common mistakes:
- Missing colons after keys
- Incorrect indentation (use 2 spaces)
- Unquoted special characters

### Client Not Appearing in Dropdown

**Problem**: New client isn't selectable

**Check**:
1. YAML syntax is valid
2. Client ID is at root level (not nested)
3. Required fields present: `name`, `parser`, `default_source`

### Wrong Source Being Applied

**Problem**: Tags getting wrong source assignment

**Fix**: Check rule order - first match wins
```yaml
tag_source_rules:
  # More specific rules first
  - exact: "SM_ALARM"
    field: "point_type"
    source: "Specific Source"
    enforcement: "R"

  # General rules later
  - prefix: "SM"
    field: "point_type"
    source: "General Source"
    enforcement: "R"
```

---

## Updating Hardcoded Fallback

**Only do this if YAML loading is consistently failing.**

In `streamlit_app.py`, find `_HARDCODED_CONFIGS` and update to match your YAML:

```python
_HARDCODED_CONFIGS = {
    "flng": {
        "name": "Freeport LNG",
        # ... copy structure from YAML ...
    },
    "new_client": {
        "name": "New Client",
        # ... add new client ...
    },
}
```

After updating, also update the test to verify:
```python
# tests/test_transformer.py
def test_client_configs_exist(self):
    expected_clients = ["flng", "hfs_artesia", "rt_bessemer", "new_client"]
    # ...
```

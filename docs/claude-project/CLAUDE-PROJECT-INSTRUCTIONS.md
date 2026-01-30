# Alarm Rationalization Platform - Claude Project Instructions

## Project Name
Alarm Rationalization Platform

## Project Description
Development and maintenance of a web-based alarm data transformation tool that converts between DCS alarm management systems (Honeywell DynAMo, ABB 800xA) and PHA-Pro alarm management database formats. Used by Applied Engineering Solutions for alarm rationalization consulting projects.

---

## SYSTEM OVERVIEW

### What This App Does
Transforms alarm configuration data bidirectionally:
- **Forward**: DCS Export → PHA-Pro Import (for rationalization work)
- **Reverse**: PHA-Pro Export → DCS Import (to return rationalized settings)

### Live Application

| Item | Value |
|------|-------|
| URL | https://alarm-rationalization.streamlit.app |
| Source Code | https://github.com/gregpa/alarm-rationalization |
| Hosting | Streamlit Community Cloud (free tier) |

### Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| Framework | Streamlit 1.28+ |
| Data Processing | pandas 2.0+ |
| Excel Support | openpyxl |
| Configuration | YAML (pyyaml 6.0) |
| Hosting | Streamlit Community Cloud |
| Source Control | GitHub |

### Current Version
**v3.24** (January 2026)

---

## PROJECT ARCHITECTURE

### File Structure
```
alarm-rationalization/
├── streamlit_app.py              # Main application (~3500 lines)
├── requirements.txt              # Python dependencies
├── deploy.sh                     # Deployment script
│
├── config/
│   ├── clients.yaml              # CLIENT CONFIGURATIONS (EDIT THIS)
│   └── client_template.yaml      # Template for new clients
│
├── docs/
│   └── claude-project/           # Documentation package
│       ├── 00-README.md
│       ├── 01-DEVELOPER-GUIDE.md
│       ├── 02-USER-GUIDE.md
│       ├── 03-CLIENT-CONFIGURATION-GUIDE.md
│       ├── 04-DELIVERABLES-CHECKLIST.md
│       └── 05-CODE-REFERENCE.md
│
├── backups/                      # Automatic code backups
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   └── test_transformer.py       # 43 behavior tests
│
├── .vscode/
│   ├── tasks.json                # VS Code tasks
│   └── settings.json             # IDE settings
│
├── .github/workflows/
│   ├── validate.yml              # CI/CD for main branch
│   └── staging.yml               # CI/CD for develop branch
│
├── .pre-commit-config.yaml       # Pre-commit hooks
└── .streamlit/
    └── config.toml               # Streamlit theme
```

### Configuration System

**Primary**: `config/clients.yaml` (external YAML file)
**Fallback**: `_HARDCODED_CONFIGS` in `streamlit_app.py` (emergency backup)

**Always edit `config/clients.yaml`** - the app automatically loads it. The hardcoded fallback only activates if the YAML file is missing or corrupted.

---

## SUPPORTED CLIENTS

### 1. Freeport LNG (flng)

| Setting | Value |
|---------|-------|
| Vendor | Honeywell Experion/DynAMo |
| Parser | dynamo |
| Unit Method | TAG_PREFIX, ASSET_PARENT, or ASSET_CHILD |
| Unit Digits | 2 (for TAG_PREFIX) |
| File Format | CSV (Latin-1, multi-schema) |
| Forward Output | 45-column PHA-Pro |
| Reverse Output | DynAMo _Parameter format |

**Tag Source Rules** (evaluated in order):
1. Point type starts with "SM" → Honeywell Safety Manager (SIS), Enforcement: R
2. Tag name contains "." → Honeywell Experion (DCS), Enforcement: M
3. Point type in ["ANA", "STA"] → Honeywell Experion (SCADA), Enforcement: M
4. Default → Honeywell TDC (DCS), Enforcement: M

**Unit Extraction Methods**:

| Method | Example | Result |
|--------|---------|--------|
| TAG_PREFIX | Tag "17TI5879" | Unit "17" |
| ASSET_PARENT | Path "/U17/17_FLARE/17H-2" | Unit "17_FLARE" |
| ASSET_CHILD | Path "/U17/17_FLARE/17H-2" | Unit "17H-2" |

### 2. HF Sinclair - Artesia (hfs_artesia)

| Setting | Value |
|---------|-------|
| Vendor | Honeywell Experion/DynAMo |
| Parser | dynamo |
| Unit Method | TAG_PREFIX |
| Unit Digits | 2 |
| File Format | CSV (multi-schema) |
| Forward Output | 43-column PHA-Pro (HFS variant) |
| Special | empty_mode_is_valid: true |

**Tag Source Rules**: 77 point-type specific rules mapping to:
- Honeywell Safety Manager (SM types)
- Honeywell Experion (SCADA) - ANA, STA
- Honeywell Experion (DCS) - AUTOMAN, PID, etc.
- Honeywell TDC (DCS) - ANALGIN, REGCTL, etc.

### 3. Rio Tinto - Bessemer City (rt_bessemer)

| Setting | Value |
|---------|-------|
| Vendor | ABB |
| Parser | abb |
| Unit Method | FIXED ("Line 1") |
| File Format | Excel (.xlsx) for forward, CSV for reverse |
| Forward Output | 23-column PHA-Pro (ABB format) |
| Reverse Output | 8-column ABB return format |

**ABB Alarm Types**:

| Suffix | PHA-Pro Alarm Type |
|--------|-------------------|
| H | (PV) High |
| HH | (PV) High High |
| HHH | (PV) High High High |
| L | (PV) Low |
| LL | (PV) Low Low |
| LLL | (PV) Low Low Low |
| OE | Object Error |

---

## CONFIGURATION REFERENCE

### YAML Client Structure

```yaml
client_id:
  name: "Display Name"              # Shown in UI dropdown
  vendor: "Control System Vendor"   # Informational
  dcs_name: "DynAMo"               # Used in UI labels
  pha_tool: "PHA-Pro"              # Used in UI labels
  parser: "dynamo"                  # "dynamo" or "abb"

  unit_method: "TAG_PREFIX"         # TAG_PREFIX, ASSET_PARENT, ASSET_CHILD, FIXED
  unit_digits: 2                    # For TAG_PREFIX method
  # unit_value: "Fixed Value"       # For FIXED method only

  default_source: "Source Name"     # When no rules match
  default_area: "area_id"           # Default area selection

  # Optional flags
  empty_mode_is_valid: false        # Allow empty mode values (HFS)
  phapro_headers: "HFS"             # Use 43-column format (HFS)

  tag_source_rules:                 # Evaluated in order - first match wins
    - exact: "SM"
      field: "point_type"
      source: "Safety Manager"
      enforcement: "R"
    - prefix: "SM_"
      field: "point_type"
      source: "Safety Manager"
      enforcement: "R"
    - in: ["ANA", "STA"]
      field: "point_type"
      source: "SCADA"
      enforcement: "M"
    - contains: "."
      field: "tag_name"
      source: "Experion DCS"
      enforcement: "M"

  areas:
    area_id:
      name: "Area Display Name"
      description: "Description text"
```

### Tag Source Rule Types

| Match Type | Syntax | Matches |
|------------|--------|---------|
| `exact` | `exact: "SM"` | Only "SM" |
| `prefix` | `prefix: "SM_"` | "SM_01", "SM_ABC", etc. |
| `contains` | `contains: "."` | Any value with a period |
| `in` | `in: ["A", "B"]` | "A" or "B" |

### Unit Extraction Methods

| Method | Config | Description |
|--------|--------|-------------|
| TAG_PREFIX | `unit_method: "TAG_PREFIX"`, `unit_digits: 2` | First N digits of tag name |
| ASSET_PARENT | `unit_method: "ASSET_PARENT"` | From asset path field |
| ASSET_CHILD | `unit_method: "ASSET_CHILD"` | From asset path field |
| FIXED | `unit_method: "FIXED"`, `unit_value: "X"` | Always returns configured value |

### Enforcement Codes

| Code | Meaning |
|------|---------|
| R (Required) | Safety Manager tags - cannot be changed in field |
| M (Mandatory) | DCS tags - can be changed with approval |
| D (Discretionary) | Advisory alarms |

---

## FILE FORMAT SPECIFICATIONS

### DynAMo Multi-Schema CSV Structure

DynAMo exports contain multiple "schemas" in a single CSV file. Each row starts with `_Variable` and the schema type is in column index [2].

**Schema: _DCSVariable** (Tag existence)
```
[0]  _Variable (marker)
[1]  Tag name
[2]  _DCSVariable
[3]  Asset path (e.g., /Assets/LQF/U17/17_FLARE/17H-2)
[7]  Engineering Units (backup)
[8]  Point type (ANA, STA, SM_AI, etc.)
```

**Schema: _DCS** (Tag configuration)
```
[0]  _Variable
[1]  Tag name
[2]  _DCS
[3]  Engineering Units (primary) ← USE THIS
[4]  Point type (primary)
[5]  PVEUHI (Range Max) - may have commas
[6]  PVEULO (Range Min)
[7]  Description
[10] Unit Name (e.g., 17_FLARE, 17_ELEC) ← USE THIS
```

**Schema: _Parameter** (Alarm settings)
```
[0]  _Variable
[1]  Tag name
[2]  _Parameter
[3]  Mode (NORMAL, IMPORT, Export, EXPORT, Base) ← ONLY PROCESS "NORMAL"
[5]  Alarm type (ControlFail, High, PV High High, etc.)
[7]  Value/setpoint
[10] Priority value (Urgent, Critical, High, Medium, Low, Journal, None)
[12] Consequence/severity (A, B, C, D, E or text)
[13] Time to respond
[16] Purpose of Alarm (Cause)
[17] Consequence of No Action
[18] Board Operator actions (Inside Actions)
[19] Field Operator actions (Outside Actions)
[25] Disabled value (TRUE/FALSE)
[31] OnDelay Value
[34] OffDelay Value
[37] DeadBand Value
[40] DeadBandUnit Value
```

**Schema: _Notes** (Documentation)
```
[0]  _Variable
[1]  Tag name
[2]  _Notes
[11] DocRef1 (P&ID reference) ← USE THIS
```

### PHA-Pro Column Formats

**Standard (45 columns)** - FLNG:
1. Unit, 2. Tag Name, 3. Old Tag Description, 4. New Tag Description, 5. P&ID, 6. Range Min, 7. Range Max, 8. Engineering Units, 9. Tag Source, 10. Rationalization (Tag) Comment, 11. Old Tag Enable Status, 12. New Tag Enable Status, 13. Alarm Type, 14. Old Individual Alarm Enable Status, 15. New Individual Alarm Enable Status, 16. Old (BPCS) Priority, 17. New (BPCS) Priority, 18. Old Limit, 19. New Limit, 20. Old Deadband, 21. New Deadband, 22. Old Deadband Units, 23. New Deadband Units, 24. Old On-Delay Time, 25. New On-Delay Time, 26. Old Off-Delay Time, 27. New Off-Delay Time, 28. Rationalization Status, 29. Alarm Status, 30. Rationalization (Alarm) Comment, 31. Limit Owner, 32. Alarm HAZOP Comment, 33. Alarm Suppression Notes, 34. Alarm Class, 35. Cause(s), 36. Consequence(s), 37. Inside Action(s), 38. Outside Action(s), 39. Health and Safety, 40. Environment, 41. Financial, 42. Reputation, 43. Privilege to Operate, 44. Max Severity, 45. Allowable Time to Respond

**HFS (43 columns)** - HF Sinclair:
Same as standard but missing 2 columns.

**ABB (23 columns)** - Rio Tinto:
1. Unit, 2. Starting Tag Name, 3. New Tag Name, 4. Old Tag Description, 5. New Tag Description, 6. Tag Source, 7. Rationalization (Tag) Comment, 8. Range Min, 9. Range Max, 10. Engineering Units, 11. Starting Alarm Type, 12. New Alarm Type, 13. Old Alarm Enable Status, 14. New Alarm Enable Status, 15. Old Alarm Severity, 16. New Alarm Severity, 17. Old Limit, 18. New Limit, 19. Old (BPCS) Priority, 20. New (BPCS) Priority, 21. Rationalization Status, 22. Alarm Status, 23. Rationalization (Alarm) Comment

---

## MAPPING RULES

### Priority Mapping (DynAMo ↔ PHA-Pro)

| DynAMo | PHA-Pro Code | Alarm Status |
|--------|--------------|--------------|
| Urgent | U | Alarm |
| Critical | C | Alarm |
| High | H | Alarm |
| Medium | M | Alarm |
| Low | L | Alarm |
| Journal | J | Event |
| Journal (disabled) | Jo | Event |
| None | N | None |

### Severity Mapping (DynAMo → PHA-Pro)

| DynAMo Text | PHA-Pro Code |
|-------------|--------------|
| A, CATASTROPHIC | A |
| B, MAJOR | B |
| C, MODERATE | C |
| D, MINOR | D |
| E, INSIGNIFICANT | E |
| (empty, ~, -) | (N) |

### Discrete Alarm Types
These alarm types do NOT have setpoint values (Limit columns are empty):
- ControlFail
- st0, st1, st2, st3 (state alarms)
- Unreasonable, Unreasonable PV
- Bad PV
- Off Normal
- Command Disagree, Command Fail
- cnferr, chofst, offnrm
- C1-C12 pattern alarms
- FlagOffNorm, DevBadPv, DevCmdDis
- DevUncEvt, DevCmdFail, RegBadCtl
- DAQPVHi, DAQPVHiHi, DAQPVLow, DAQPVLoLo

---

## ADDING A NEW CLIENT

### Decision Tree: YAML vs Python Changes

| If you need to... | Edit... |
|-------------------|---------|
| Add client with existing parser (dynamo/abb) | YAML only |
| Change tag source rules | YAML only |
| Add/modify areas | YAML only |
| Change unit extraction settings | YAML only |
| Add new parser type | Python + YAML |
| Add new transformation logic | Python + YAML |
| Add new PHA-Pro column format | Python + YAML |

### YAML-Only Client Addition (Most Common)

**Step 1**: Copy template from `config/client_template.yaml`

**Step 2**: Fill in configuration in `config/clients.yaml`:

```yaml
new_client_id:
  name: "New Client - Site Name"
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
      source: "Safety Manager (SIS)"
      enforcement: "R"
    - in: ["ANA", "STA"]
      field: "point_type"
      source: "SCADA"
      enforcement: "M"

  areas:
    main_area:
      name: "Main Processing"
      description: "Primary processing area"
```

**Step 3**: Commit and push to GitHub → auto-deploys

### Required Information for New Client

When user requests a new client, ask for:

1. **Client Info**: Name, short ID (lowercase, underscores, no spaces)
2. **DCS System**: Vendor, DCS name
3. **Parser**: dynamo (CSV) or abb (Excel)
4. **Unit Method**: TAG_PREFIX (how many digits?) / ASSET_PARENT / ASSET_CHILD / FIXED
5. **Tag Source Rules**: Point types and their source systems
6. **Sample Files**: DCS export file for testing

### Example Request Format

```
Add new client: Chevron Richmond

Control System: Honeywell Experion PKS
Parser: dynamo
PHA-Pro Format: 45 columns (standard)

Unit Extraction:
- Method: TAG_PREFIX
- Digits: 2

Tag Source Rules:
- SIS, SM, SAFETY → "Safety Instrumented System" (R)
- ANA, STA → "Experion SCADA" (M)
- PID, PIDFF → "Experion PKS (DCS)" (M)
- Default: "Experion PKS (DCS)"

Areas:
- unit_10: "Unit 10 - Crude"
- unit_20: "Unit 20 - Reformer"
```

---

## CODE STRUCTURE

### File: streamlit_app.py (~3500 lines)

```
├── IMPORTS & SETUP (1-75)
│   ├── Standard imports
│   ├── SessionLogHandler (logging to session state)
│   └── History tracking functions
│
├── CONFIGURATION LOADING (77-200)
│   ├── load_client_configs() - YAML with fallback
│   └── csv_to_excel() - Export helper
│
├── AlarmTransformer CLASS (200-2600)
│   ├── PHAPRO_HEADERS (45 columns)
│   ├── PHAPRO_HEADERS_HFS (43 columns)
│   ├── ABB_PHAPRO_HEADERS (23 columns)
│   ├── DYNAMO_HEADERS (42 columns)
│   ├── _HARDCODED_CONFIGS (fallback)
│   │
│   ├── __init__(client_id)
│   ├── get_client_configs() - classmethod
│   ├── get_phapro_headers()
│   │
│   ├── parse_dynamo_csv(content)
│   ├── parse_abb_excel(raw_bytes)
│   ├── scan_for_units(content)
│   │
│   ├── extract_unit(tag, method)
│   ├── derive_tag_source(tag, point_type)
│   ├── map_priority(priority, disabled)
│   ├── map_severity(consequence)
│   ├── is_discrete(alarm_type)
│   │
│   ├── transform_forward(content, units, method)
│   ├── transform_forward_abb(raw_bytes)
│   ├── transform_reverse(content, source)
│   ├── transform_reverse_abb(content)
│   │
│   └── generate_change_report(original, source)
│
├── PREVIEW FUNCTION (2600-2650)
│   └── _preview_file_data()
│
├── CSS STYLING (2650-2750)
│
└── STREAMLIT UI - main() (2750-3500)
    ├── Page config
    ├── Sidebar
    │   ├── Client selection
    │   ├── Direction toggle
    │   ├── Transformation History panel
    │   ├── Debug Logs panel
    │   └── Report Issue section
    │
    └── Main content
        ├── Header (dynamic per client)
        ├── File Upload (drag & drop)
        ├── Unit Selection (DynAMo only)
        ├── Transform Button
        ├── Results Display
        ├── Download Buttons (CSV, Excel, Change Report)
        └── Output Preview
```

### Key Methods

| Method | Purpose |
|--------|---------|
| `transform_forward()` | DynAMo CSV → PHA-Pro 45-col |
| `transform_forward_abb()` | ABB Excel → PHA-Pro 23-col |
| `transform_reverse()` | PHA-Pro → DynAMo _Parameter |
| `transform_reverse_abb()` | PHA-Pro → ABB 8-col |
| `parse_dynamo_csv()` | Parse multi-schema DynAMo CSV |
| `parse_abb_excel()` | Parse ABB Excel wide format |
| `scan_for_units()` | Pre-scan for unit detection UI |
| `derive_tag_source()` | Apply rules for tag source |
| `map_priority()` | Priority names ↔ codes |
| `csv_to_excel()` | Convert output to Excel format |
| `add_to_history()` | Track transformations for re-download |

---

## FEATURES (v3.24)

### Structured Logging
- Logs stored in session state
- Viewable in sidebar "Debug Logs" panel
- Tracks transform operations, errors, warnings

### Transformation History
- Last 20 transformations tracked
- Re-download previous outputs
- Shows input file, direction, stats
- Stored in browser session

### Export Options
- **CSV**: Standard comma-separated
- **Excel**: .xlsx with proper formatting
- **Change Report**: Excel summary (reverse transforms)

### Data Preview
- Optional pre-transform validation
- Shows rows to process/skip
- Lists detected units
- Identifies potential issues

---

## TESTING

### Running Tests

```bash
# All 43 tests
pytest tests/ -v

# Specific test class
pytest tests/test_transformer.py::TestPriorityMapping -v

# With coverage
pytest tests/ -v --cov=streamlit_app
```

### Test Categories

| Class | Tests | Purpose |
|-------|-------|---------|
| TestAlarmTransformerInit | 4 | Client loading, headers |
| TestDiscreteAlarmDetection | 2 | Discrete vs analog |
| TestPriorityMapping | 2 | Priority codes |
| TestSeverityMapping | 1 | Consequence → severity |
| TestUnitExtraction | 3 | Unit methods |
| TestTagSourceDerivation | 3 | Source rules |
| TestForwardTransformation | 4 | DynAMo → PHA-Pro |
| TestDynamoParsing | 2 | CSV parsing |
| TestABBSupport | 3 | ABB client |
| TestHFSinclair | 3 | HFS specifics |
| TestExternalConfigLoader | 5 | YAML loading |
| TestDataPreview | 4 | Preview feature |
| TestConfigFallback | 2 | Hardcoded fallback |

---

## DEPLOYMENT

### Automatic (GitHub → Streamlit Cloud)
1. Push to `main` branch
2. GitHub Actions validates (syntax, imports, tests)
3. Streamlit Cloud auto-deploys
4. Live in 1-2 minutes

### Manual Validation
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config/clients.yaml'))"

# Run tests
pytest tests/ -v

# Local test
streamlit run streamlit_app.py
```

---

## TROUBLESHOOTING

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| "Could not decode file" | Encoding not recognized | Save source as UTF-8 or Latin-1 |
| Empty output | No rows matched criteria | Check mode=NORMAL, unit selection |
| Wrong unit numbers | Unit method mismatch | Try different extraction method |
| Wrong tag source | Rules order or values | Check rule order (first match wins) |
| Missing columns (reverse) | PHA-Pro export incomplete | App shows needed columns |
| Client not in dropdown | YAML syntax error | Validate YAML syntax |
| Â°F instead of °F | Encoding mismatch | Fixed in v3.21+ |

### Viewing Logs
1. Open sidebar
2. Expand "Debug Logs" section
3. Review recent log entries

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 3.24 | Jan 2026 | Structured logging, transformation history, Excel export, YAML config |
| 3.23 | Jan 2026 | Fixed Unit column display |
| 3.22 | Jan 2026 | Unit column only on first row per unit group |
| 3.21 | Jan 2026 | Latin-1 encoding output, comma stripping in delays |
| 3.19 | Jan 2026 | Enhanced unit extraction methods |
| 3.18 | Jan 2026 | Forward transform improvements |
| 3.17 | Jan 2026 | Change Report Excel export |
| 3.0 | Jan 2026 | ABB 800xA support, Rio Tinto client |
| 2.0 | Jan 2026 | Severity mapping, HF Sinclair client |
| 1.0 | Jan 2026 | Initial release |

---

## DOCUMENTATION PACKAGE

Full documentation available at: `docs/claude-project/`

| File | Purpose |
|------|---------|
| 01-DEVELOPER-GUIDE.md | Architecture, testing, deployment |
| 02-USER-GUIDE.md | End-user documentation |
| 03-CLIENT-CONFIGURATION-GUIDE.md | Adding/modifying clients |
| 04-DELIVERABLES-CHECKLIST.md | What to provide for changes |
| 05-CODE-REFERENCE.md | Key code structures |
| clients.yaml | Current configurations |
| client_template.yaml | Template for new clients |

---

## CONTACT

| Role | Contact |
|------|---------|
| Application Owner | Greg Pajak |
| Company | Applied Engineering Solutions |
| Email | greg.pajak@aesolutions.com |
| Repository | https://github.com/gregpa/alarm-rationalization |

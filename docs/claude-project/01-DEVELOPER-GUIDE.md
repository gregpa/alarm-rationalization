# Alarm Rationalization Platform - Developer Guide

## Overview

The Alarm Rationalization Platform transforms alarm data between control system formats (Honeywell DynAMo, ABB 800xA) and PHA-Pro's Alarm Management Database format.

**Live URL**: https://alarm-rationalization.streamlit.app
**Repository**: GitHub (deployed via Streamlit Cloud)
**Version**: v3.24+

---

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     Streamlit Web Interface                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Client    │  │  Direction  │  │      File Upload        │ │
│  │  Selector   │  │   Toggle    │  │   (drag & drop CSV)     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AlarmTransformer Class                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Config Loader  │  │  CSV Parsers    │  │  Transformation │ │
│  │  (YAML+fallback)│  │  (DynAMo, ABB)  │  │  Engine         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Output Generation                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  PHA-Pro CSV    │  │  DynAMo CSV     │  │  Change Report  │ │
│  │  (45/43 cols)   │  │  (42 cols)      │  │  (Excel)        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### File Structure

```
alarm-rationalization/
├── streamlit_app.py              # Main application (~3400 lines)
├── requirements.txt              # Python dependencies
├── deploy.sh                     # Deployment script
│
├── config/
│   ├── clients.yaml              # Client configurations (EDITABLE)
│   └── client_template.yaml      # Template for new clients
│
├── docs/
│   └── claude-project/           # Documentation for Claude AI project
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

---

## Key Classes and Functions

### AlarmTransformer Class

The main transformation engine. Located in `streamlit_app.py`.

```python
class AlarmTransformer:
    """Core transformation engine for alarm data."""

    # Class-level constants
    PHAPRO_HEADERS = [...]        # 45-column standard format
    PHAPRO_HEADERS_HFS = [...]    # 43-column HFS format
    ABB_PHAPRO_HEADERS = [...]    # 23-column ABB format
    DYNAMO_HEADERS = [...]        # 42-column DynAMo format
    _HARDCODED_CONFIGS = {...}    # Fallback configurations

    def __init__(self, client_id: str):
        """Initialize with client configuration."""

    @classmethod
    def get_client_configs(cls) -> Dict:
        """Load configs from YAML with fallback to hardcoded."""

    # Forward transformation (DCS → PHA-Pro)
    def transform_forward(self, content, units, method) -> Tuple[bytes, Dict]:
    def transform_forward_abb(self, raw_bytes) -> Tuple[bytes, Dict]:

    # Reverse transformation (PHA-Pro → DCS)
    def transform_reverse(self, content, source) -> Tuple[bytes, Dict]:
    def transform_reverse_abb(self, content) -> Tuple[bytes, Dict]:

    # Change Reports (all clients)
    def generate_change_report(self, pha_content, source_data) -> bytes:
    def generate_change_report_abb(self, pha_content, source_bytes) -> bytes:

    # Parsing
    def parse_dynamo_csv(self, content) -> Dict:

    # Mapping functions
    def map_priority(self, priority, disabled) -> Tuple[str, str]:
    def map_severity(self, consequence) -> str:
    def derive_tag_source(self, tag, point_type) -> Tuple[str, str]:
    def extract_unit(self, tag, method) -> str:
```

### Configuration Loading

```python
def load_client_configs() -> Dict[str, Any]:
    """
    Load client configurations from external YAML file.
    Falls back to hardcoded defaults if YAML loading fails.

    Priority:
    1. config/clients.yaml (relative to script)
    2. /workspaces/alarm-rationalization/config/clients.yaml
    3. _HARDCODED_CONFIGS (always available)
    """
```

### Logging and History

```python
# Session-based logging
class SessionLogHandler(logging.Handler):
    """Stores logs in Streamlit session state."""

app_logger = setup_logger()  # Global logger instance

# Transformation history
def add_to_history(filename, direction, client, stats, output_data, output_filename):
    """Track transformations for re-download."""

# Configuration validation
def validate_client_configs(configs) -> List[Dict]:
    """Validate YAML configs, returns list of warnings/errors."""
```

---

## Transformation Logic

### Forward: DynAMo → PHA-Pro

1. **Parse** multi-schema CSV (\_DCSVariable, \_DCS, \_Parameter, \_Notes)
2. **Filter** by mode (NORMAL only) and unit selection
3. **Map** fields:
   - Priority → Single letter code (U, C, H, M, L, Jo)
   - Consequence → Severity (A-E)
   - Point Type → Tag Source + Enforcement
4. **Generate** 45-column (or 43 for HFS) hierarchical CSV

### Reverse: PHA-Pro → DynAMo

1. **Parse** PHA-Pro MADB export
2. **Match** to original DynAMo export (if provided)
3. **Preserve** client-specific values from original
4. **Map** rationalized values back to DynAMo fields
5. **Generate** 42-column DynAMo import CSV

### ABB Transformations

- Uses Excel input instead of CSV
- Fixed 23-column PHA-Pro output
- Simpler tag source rules (typically single source)

---

## Configuration System

### YAML Structure (config/clients.yaml)

```yaml
client_id:
  name: "Display Name"              # Shown in UI
  vendor: "Control System Vendor"   # Informational
  dcs_name: "DynAMo"               # Used in labels
  pha_tool: "PHA-Pro"              # Used in labels
  parser: "dynamo"                  # "dynamo" or "abb"

  unit_method: "TAG_PREFIX"         # How to extract unit
  unit_digits: 2                    # For TAG_PREFIX method
  # unit_value: "Fixed Value"       # For FIXED method

  default_source: "Source Name"     # When no rules match
  default_area: "area_id"           # Default area selection

  # Optional flags
  empty_mode_is_valid: false        # Allow empty mode values
  phapro_headers: "HFS"             # Use alternate headers

  tag_source_rules:                 # Evaluated in order
    - exact: "SM"
      field: "point_type"
      source: "Safety Manager"
      enforcement: "R"

  areas:
    area_id:
      name: "Area Name"
      description: "Description"
```

### Tag Source Rule Types

| Match Type | Example | Description |
|------------|---------|-------------|
| `exact` | `"SM"` | Exact string match |
| `prefix` | `"SM_"` | Starts with string |
| `contains` | `"."` | Contains substring |
| `in` | `["ANA", "STA"]` | Value in list |

### Unit Extraction Methods

| Method | Description | Example |
|--------|-------------|---------|
| `TAG_PREFIX` | First N digits of tag | `17FIC-123` → `17` |
| `ASSET_PARENT` | Use asset parent field | Direct from data |
| `ASSET_CHILD` | Use asset child field | Direct from data |
| `FIXED` | Fixed value | Always returns configured value |

---

## Testing

### Running Tests

```bash
# All tests (43 total)
pytest tests/ -v

# Specific test class
pytest tests/test_transformer.py::TestPriorityMapping -v

# With coverage
pytest tests/ -v --cov=streamlit_app
```

### Test Categories

| Class | Tests | Purpose |
|-------|-------|---------|
| `TestAlarmTransformerInit` | 4 | Client loading, headers |
| `TestDiscreteAlarmDetection` | 2 | Discrete vs analog |
| `TestPriorityMapping` | 2 | Priority codes |
| `TestSeverityMapping` | 1 | Consequence → severity |
| `TestUnitExtraction` | 3 | Unit methods |
| `TestTagSourceDerivation` | 3 | Source rules |
| `TestForwardTransformation` | 4 | DynAMo → PHA-Pro |
| `TestDynamoParsing` | 2 | CSV parsing |
| `TestEncodingHandling` | 1 | Special characters |
| `TestClientAreas` | 2 | Area configuration |
| `TestDynamoHeaders` | 2 | Output headers |
| `TestABBSupport` | 3 | ABB client |
| `TestHFSinclair` | 3 | HFS specifics |
| `TestExternalConfigLoader` | 5 | YAML loading |
| `TestDataPreview` | 4 | Preview feature |
| `TestConfigFallback` | 2 | Hardcoded fallback |

---

## Deployment

### Automatic (Recommended)

Push to `main` branch triggers:
1. Syntax validation
2. Import checks
3. Test suite (43 tests)
4. Auto-deploy to Streamlit Cloud

### Manual

```bash
# Validate first
pytest tests/ -v

# Then deploy
./deploy.sh
```

### VS Code Tasks

| Task | Shortcut | Description |
|------|----------|-------------|
| Run Tests + Deploy | - | Safest option |
| Validate + Deploy | - | Quick deploy |
| Run Tests | - | Verify only |

---

## Error Handling

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| Missing columns | Wrong file format | Check file has required schemas |
| Encoding errors | Special characters | App auto-tries multiple encodings |
| YAML parse error | Invalid config | Falls back to hardcoded |
| Empty output | Wrong mode filter | Check mode values in source |

### Logging

Logs are stored in session state and viewable in sidebar:
- `app_logger.info()` - Normal operations
- `app_logger.warning()` - Non-fatal issues
- `app_logger.error()` - Failures

---

## Version History

| Version | Changes |
|---------|---------|
| v3.25 | Configuration validator |
| v3.24 | Structured logging, transformation history, Excel export, Change Reports for all clients |
| v3.23 | Fixed Unit column display |
| v3.22 | Unit display refinement |
| v3.21 | Encoding & comma stripping fixes |
| v3.19 | Enhanced unit extraction options |

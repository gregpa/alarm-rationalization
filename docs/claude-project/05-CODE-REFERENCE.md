# Code Reference

## File: streamlit_app.py

This is the main application file (~3400 lines). Key sections:

### Imports and Setup (Lines 1-75)

```python
import streamlit as st
import pandas as pd
import io
import csv
import os
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Set

# Logging setup
class SessionLogHandler(logging.Handler):
    """Custom log handler that stores logs in Streamlit session state."""

app_logger = setup_logger()

# History tracking
def add_to_history(filename, direction, client, stats, output_data, output_filename):
def get_history():
def clear_history():
```

### Configuration Loading (Lines 77-200)

```python
def load_client_configs() -> Dict[str, Any]:
    """
    Load client configurations from external YAML file.
    Falls back to hardcoded defaults if YAML loading fails.
    """
    # Tries: config/clients.yaml, then _HARDCODED_CONFIGS
```

### AlarmTransformer Class (Lines ~200-2600)

```python
class AlarmTransformer:
    # Column headers
    PHAPRO_HEADERS = [...]        # 45 columns - standard
    PHAPRO_HEADERS_HFS = [...]    # 43 columns - HFS variant
    ABB_PHAPRO_HEADERS = [...]    # 23 columns - ABB
    DYNAMO_HEADERS = [...]        # 42 columns - DynAMo output

    # Hardcoded fallback configs
    _HARDCODED_CONFIGS = {
        "flng": {...},
        "hfs_artesia": {...},
        "rt_bessemer": {...},
    }

    def __init__(self, client_id: str):
        self.client_id = client_id
        self.config = self.get_client_configs()[client_id]
        self.stats = {}

    @classmethod
    def get_client_configs(cls) -> Dict:
        """Load configs with YAML priority, hardcoded fallback."""

    # Transformation methods
    def transform_forward(self, content, units, method) -> Tuple[bytes, Dict]:
    def transform_forward_abb(self, raw_bytes) -> Tuple[bytes, Dict]:
    def transform_reverse(self, content, source) -> Tuple[bytes, Dict]:
    def transform_reverse_abb(self, content) -> Tuple[bytes, Dict]:

    # Mapping methods
    def map_priority(self, priority, disabled) -> Tuple[str, str]:
        """Map priority name to code: Urgent→U, Critical→C, etc."""

    def map_severity(self, consequence) -> str:
        """Map consequence to severity letter: A-E."""

    def derive_tag_source(self, tag, point_type) -> Tuple[str, str]:
        """Apply tag_source_rules to determine source and enforcement."""

    def extract_unit(self, tag, method) -> str:
        """Extract unit using configured method."""

    # Parsing
    def parse_dynamo_csv(self, content) -> Dict:
        """Parse multi-schema DynAMo CSV into dict by schema."""

    # Headers
    def get_phapro_headers(self) -> List[str]:
        """Get appropriate headers based on client config."""
```

### Streamlit UI (Lines ~2600-3400)

```python
# Page config
st.set_page_config(page_title="Alarm Rationalization", layout="wide")

# Custom CSS
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Client selection
    # Direction toggle
    # History panel
    # Logs panel

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    # File upload section
    uploaded_file = st.file_uploader(...)

    # Unit selection (for DynAMo)
    # Preview option

with col2:
    # Transform button
    if st.button("Transform"):
        # Execute transformation
        # Display results
        # Download buttons (CSV, Excel)
```

---

## File: config/clients.yaml

YAML configuration for all clients:

```yaml
flng:
  name: "Freeport LNG"
  vendor: "Honeywell Experion/DynAMo"
  parser: "dynamo"
  unit_method: "TAG_PREFIX"
  unit_digits: 2
  default_source: "Honeywell TDC (DCS)"
  tag_source_rules:
    - prefix: "SM"
      field: "point_type"
      source: "Honeywell Safety Manager (SIS)"
      enforcement: "R"
  areas:
    lqf_u17:
      name: "LQF - Unit 17"

hfs_artesia:
  name: "HF Sinclair - Artesia"
  # ... 77 tag source rules ...
  phapro_headers: "HFS"  # Uses 43-column format

rt_bessemer:
  name: "Rio Tinto - Bessemer City"
  parser: "abb"
  unit_method: "FIXED"
  unit_value: "Line 1"
```

---

## File: tests/test_transformer.py

43 tests organized by category:

```python
class TestAlarmTransformerInit:
    def test_flng_client_loads(self):
    def test_hfs_client_loads(self):
    def test_client_configs_exist(self):
    def test_phapro_headers_correct_length(self):

class TestPriorityMapping:
    def test_priority_mappings(self):
    def test_disabled_alarm_priority(self):

class TestTagSourceDerivation:
    def test_safety_manager_detection(self):
    def test_scada_detection(self):
    def test_default_source(self):

class TestForwardTransformation:
    def test_basic_forward_transform(self):
    def test_forward_transform_returns_bytes(self):

class TestExternalConfigLoader:
    def test_get_client_configs_returns_dict(self):
    def test_configs_have_required_clients(self):
    def test_yaml_config_is_loadable(self):

class TestConfigFallback:
    def test_hardcoded_configs_exist(self):
    def test_hardcoded_matches_yaml_structure(self):
```

---

## Key Data Structures

### Priority Mapping

```python
PRIORITY_MAP = {
    "Urgent": "U",
    "Critical": "C",
    "High": "H",
    "Medium": "M",
    "Low": "L",
    "Journal": "Jo",
}
```

### Severity Mapping

```python
SEVERITY_MAP = {
    "A": "A",  # Highest
    "B": "B",
    "C": "C",
    "D": "D",
    "E": "E",  # Lowest
}
# Default: "E" for unknown consequences
```

### Tag Source Rule Evaluation

```python
def derive_tag_source(self, tag_name, point_type):
    for rule in self.config.get("tag_source_rules", []):
        match = False
        field_value = point_type if rule["field"] == "point_type" else tag_name

        if "exact" in rule:
            match = field_value == rule["exact"]
        elif "prefix" in rule:
            match = field_value.startswith(rule["prefix"])
        elif "contains" in rule:
            match = rule["contains"] in field_value
        elif "in" in rule:
            match = field_value in rule["in"]

        if match:
            return rule["source"], rule["enforcement"]

    return self.config["default_source"], "M"
```

### Unit Extraction

```python
def extract_unit(self, tag_name, method):
    if method == "TAG_PREFIX":
        digits = self.config.get("unit_digits", 2)
        return tag_name[:digits]
    elif method == "FIXED":
        return self.config.get("unit_value", "")
    elif method == "ASSET_PARENT":
        # From DCS data
    elif method == "ASSET_CHILD":
        # From DCS data
```

---

## PHA-Pro Column Formats

### Standard (45 columns) - FLNG

```
Node, Function, Equipment, Field Device, Alarm, Tag, Tag Description,
Alarm Priority, Alarm Type, Setpoint, Deadband, On Delay, Off Delay,
Alarm Status, Source, Enforcement, etc...
```

### HFS (43 columns) - HF Sinclair

Same as standard but missing 2 columns.

### ABB (23 columns) - Rio Tinto

Simplified format for ABB 800xA systems.

---

## DynAMo Output Format (42 columns)

```
VARIABLE, DCS, Parameter, Point Type, Alarm Type, HiHi, Hi, Lo, LoLo,
Priority, Enabled, Deadband, etc...
```

---

## Mode Filtering

Only `NORMAL` mode rows are processed. Skipped modes:
- IMPORT
- Export / EXPORT
- Base
- Startup
- Shutdown

This prevents duplicate alarms and focuses on active configurations.

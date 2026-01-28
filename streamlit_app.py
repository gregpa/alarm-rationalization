"""
Alarm Rationalization Platform - Web Interface
Professional web application for transforming alarm data between DynAMo and PHA-Pro formats.
"""

import streamlit as st
import pandas as pd
import io
import csv
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Alarm Rationalization Platform",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    /* Status indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .status-info {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
    }
    .status-warning {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }
    
    /* Stats boxes */
    .stat-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a5f;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #1e3a5f;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Professional table styling */
    .dataframe {
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# CORE TRANSFORMATION LOGIC (embedded for single-file deployment)
# ============================================================

class AlarmTransformer:
    """Core transformation engine."""
    
    # PHA-Pro 45-column headers
    PHAPRO_HEADERS = [
        "Unit", "Tag Name", "Old Tag Description", "New Tag Description", "P&ID",
        "Range Min", "Range Max", "Engineering Units", "Tag Source",
        "Rationalization (Tag) Comment", "Old Tag Enable Status", "New Tag Enable Status",
        "Alarm Type", "Old Individual Alarm Enable Status", "New Individual Alarm Enable Status",
        "Old (BPCS) Priority", "New (BPCS) Priority", "Old Limit", "New Limit",
        "Old Deadband", "New Deadband", "Old Deadband Units", "New Deadband Units",
        "Old On-Delay Time", "New On-Delay Time", "Old Off-Delay Time", "New Off-Delay Time",
        "Rationalization Status", "Alarm Status", "Rationalization (Alarm) Comment",
        "Limit Owner", "Alarm HAZOP Comment", "Alarm Suppression Notes", "Alarm Class",
        "Cause(s)", "Consequence(s)", "Inside Action(s)", "Outside Action(s)",
        "Health and Safety", "Environment", "Financial", "Reputation",
        "Privilege to Operate", "Max Severity", "Allowable Time to Respond"
    ]
    
    # DynAMo 42-column headers
    DYNAMO_HEADERS = [
        "'_Variable", "name", "_Parameter", "mode", "boundary", "alarmType", "alarmName",
        "value", "enforcement", "priorityName", "priorityValue", "priorityEnforcement",
        "consequence", "TimeToRespond", "pre-Alarm", "historyTag", "Purpose of Alarm",
        "Consequence of No Action", "Board Operator", "Field Operator", "Supporting Notes",
        "TypeParameter", "TypeValue", "TypeEnforcement", "DisabledParameter", "DisabledValue",
        "DisabledEnforcement", "SuppressedParameter", "SuppressedValue", "SuppressedEnforcement",
        "OnDelayParameter", "OnDelayValue", "OnDelayEnforcement", "OffDelayParameter",
        "OffDelayValue", "OffDelayEnforcement", "DeadBandParameter", "DeadBandValue",
        "DeadBandEnforcement", "DeadBandUnitParameter", "DeadBandUnitValue", "DeadBandUnitEnforcement"
    ]
    
    # Client configurations
    CLIENT_CONFIGS = {
        "flng": {
            "name": "Freeport LNG",
            "vendor": "Honeywell Experion/DynAMo",
            "unit_method": "TAG_PREFIX",
            "unit_digits": 2,
            "tag_source_rules": [
                {"prefix": "SM", "field": "point_type", "source": "Honeywell Safety Manager (SIS)", "enforcement": "R"},
                {"contains": ".", "field": "tag_name", "source": "Honeywell Experion (DCS)", "enforcement": "M"},
                {"in": ["ANA", "STA"], "field": "point_type", "source": "Honeywell Experion (SCADA)", "enforcement": "M"},
            ],
            "default_source": "Honeywell TDC (DCS)",
        },
        "hf_sinclair": {
            "name": "HF Sinclair",
            "vendor": "Honeywell Experion/DynAMo",
            "unit_method": "TAG_PREFIX",
            "unit_digits": 2,
            "tag_source_rules": [
                {"prefix": "SM", "field": "point_type", "source": "Honeywell Safety Manager (SIS)", "enforcement": "R"},
            ],
            "default_source": "Honeywell Experion (DCS)",
        },
    }
    
    DISCRETE_ALARM_TYPES = [
        "controlfail", "st0", "st1", "st2", "st3", "unreasonable", "bad pv",
        "off normal", "command disagree", "command fail", "cnferr", "chofst", "offnrm"
    ]
    
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.config = self.CLIENT_CONFIGS.get(client_id, self.CLIENT_CONFIGS["flng"])
        self.stats = {"tags": 0, "alarms": 0, "units": set()}
    
    def parse_dynamo_csv(self, file_content: str) -> Dict:
        """Parse DynAMo multi-schema CSV file."""
        lines = file_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        reader = csv.reader(lines)
        
        schemas = {
            '_DCSVariable': {},
            '_DCS': {},
            '_Parameter': {},
            '_Notes': {},
        }
        
        for row in reader:
            if not row or len(row) < 3:
                continue
            
            if row[0].strip() == "_Variable":
                tag_name = row[1].strip()
                schema_type = row[2].strip()
                
                if schema_type == "_DCSVariable":
                    schemas['_DCSVariable'][tag_name] = {
                        'assetPath': row[3] if len(row) > 3 else "",
                        'pointType': row[8] if len(row) > 8 else "",
                    }
                elif schema_type == "_DCS":
                    schemas['_DCS'][tag_name] = {
                        'pointType': row[4] if len(row) > 4 else "",
                        'PVEUHI': row[5] if len(row) > 5 else "",
                        'PVEULO': row[6] if len(row) > 6 else "",
                        'desc': row[7] if len(row) > 7 else "",
                    }
                elif schema_type == "_Parameter":
                    if tag_name not in schemas['_Parameter']:
                        schemas['_Parameter'][tag_name] = []
                    schemas['_Parameter'][tag_name].append({
                        'mode': row[3] if len(row) > 3 else "Base",
                        'alarmType': row[5] if len(row) > 5 else "",
                        'value': row[7] if len(row) > 7 else "",
                        'priorityValue': row[10] if len(row) > 10 else "",
                        'consequence': row[12] if len(row) > 12 else "",
                        'TimeToRespond': row[13] if len(row) > 13 else "",
                        'PurposeOfAlarm': row[16] if len(row) > 16 else "",
                        'ConsequenceOfNoAction': row[17] if len(row) > 17 else "",
                        'BoardOperator': row[18] if len(row) > 18 else "",
                        'FieldOperator': row[19] if len(row) > 19 else "",
                        'SupportingNotes': row[20] if len(row) > 20 else "",
                        'DisabledValue': row[25] if len(row) > 25 else "",
                    })
                elif schema_type == "_Notes":
                    schemas['_Notes'][tag_name] = {
                        'DocRef1': row[11] if len(row) > 11 else "",
                    }
        
        return schemas
    
    def extract_unit(self, tag_name: str, asset_path: str = "", method: str = None) -> str:
        """Extract unit number from tag name or asset path.
        
        Args:
            tag_name: The tag name
            asset_path: The asset path (optional)
            method: Override method - "tag_prefix" or "asset_path" (optional)
        """
        import re
        
        # Determine which method to use
        use_method = method or self.config.get("unit_method", "TAG_PREFIX")
        
        if use_method.upper() == "TAG_PREFIX":
            unit = ""
            for ch in tag_name:
                if ch.isdigit():
                    unit += ch
                    if len(unit) >= self.config["unit_digits"]:
                        break
                elif unit:
                    break
            return unit
        
        elif use_method.upper() == "ASSET_PATH" and asset_path:
            # Look for /Uxx/ pattern
            match = re.search(r'/U(\d+)/', asset_path, re.IGNORECASE)
            if match:
                return match.group(1)
            # Try /Unitxx/ pattern
            match = re.search(r'/Unit\s*(\d+)/', asset_path, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""
    
    def derive_tag_source(self, tag_name: str, point_type: str) -> Tuple[str, str]:
        """Derive tag source and enforcement from rules."""
        for rule in self.config.get("tag_source_rules", []):
            if "prefix" in rule and rule["field"] == "point_type":
                if point_type.upper().startswith(rule["prefix"]):
                    return rule["source"], rule.get("enforcement", "M")
            if "contains" in rule and rule["field"] == "tag_name":
                if rule["contains"] in tag_name:
                    return rule["source"], rule.get("enforcement", "M")
            if "in" in rule and rule["field"] == "point_type":
                if point_type.upper() in rule["in"]:
                    return rule["source"], rule.get("enforcement", "M")
        
        return self.config.get("default_source", "Unknown"), "M"
    
    def map_priority(self, priority: str, disabled_value: str = "") -> Tuple[str, str]:
        """Map priority to code and alarm status."""
        p = priority.strip().lower() if priority else ""
        
        mapping = {
            'urgent': ('U', 'Alarm'),
            'critical': ('C', 'Alarm'),
            'high': ('H', 'Alarm'),
            'medium': ('M', 'Alarm'),
            'low': ('L', 'Alarm'),
            'journal': ('J', 'Event'),
            'none': ('N', 'None'),
        }
        
        code, status = mapping.get(p, ('N', 'None'))
        
        # Jo for disabled Journal alarms
        if code == 'J' and disabled_value.upper() == 'FALSE':
            code = 'Jo'
        
        return code, status
    
    def map_severity(self, consequence: str) -> str:
        """Map consequence to severity code."""
        if not consequence or consequence in ["~", ""]:
            return "(N)"
        
        c = consequence.strip().upper()
        if c in ['A', 'B', 'C', 'D', 'E']:
            return c
        return "(N)"
    
    def is_discrete(self, alarm_type: str) -> bool:
        """Check if alarm type is discrete."""
        at_lower = alarm_type.lower()
        return any(d in at_lower for d in self.DISCRETE_ALARM_TYPES)
    
    def transform_forward(self, file_content: str, selected_units: List[str] = None, unit_method: str = None) -> Tuple[str, Dict]:
        """Transform DynAMo to PHA-Pro format.
        
        Args:
            file_content: The CSV file content
            selected_units: List of units to filter (optional)
            unit_method: "tag_prefix" or "asset_path" (optional, uses config default)
        """
        schemas = self.parse_dynamo_csv(file_content)
        
        rows = []
        self.stats = {"tags": 0, "alarms": 0, "units": set()}
        
        # Build tag list sorted by unit and name
        tags = []
        for tag_name in schemas['_DCSVariable'].keys():
            var_data = schemas['_DCSVariable'].get(tag_name, {})
            dcs_data = schemas['_DCS'].get(tag_name, {})
            params = schemas['_Parameter'].get(tag_name, [])
            notes = schemas['_Notes'].get(tag_name, {})
            
            if not params:
                continue
            
            point_type = dcs_data.get('pointType', '') or var_data.get('pointType', '')
            unit = self.extract_unit(tag_name, var_data.get('assetPath', ''), unit_method)
            
            if selected_units and unit not in selected_units:
                continue
            
            self.stats["units"].add(unit)
            
            tags.append({
                'tag_name': tag_name,
                'unit': unit,
                'point_type': point_type,
                'desc': dcs_data.get('desc', ''),
                'range_min': dcs_data.get('PVEULO', '0'),
                'range_max': dcs_data.get('PVEUHI', '1'),
                'pid': notes.get('DocRef1', ''),
                'params': params,
            })
        
        # Sort by unit, then tag name
        tags.sort(key=lambda t: (t['unit'], t['tag_name']))
        
        last_unit = None
        
        for tag in tags:
            self.stats["tags"] += 1
            tag_source, enforcement = self.derive_tag_source(tag['tag_name'], tag['point_type'])
            
            is_first_tag_for_unit = (tag['unit'] != last_unit)
            is_first_alarm_for_tag = True
            
            for param in tag['params']:
                if not param.get('alarmType'):
                    continue
                
                self.stats["alarms"] += 1
                priority_code, alarm_status = self.map_priority(
                    param.get('priorityValue', ''),
                    param.get('DisabledValue', '')
                )
                
                # Derive individual enable
                at_lower = param.get('alarmType', '').lower()
                if 'controlfail' in at_lower:
                    indiv_enable = "~"
                elif at_lower.startswith('st') and param.get('DisabledValue'):
                    indiv_enable = param.get('DisabledValue', '~').upper()
                else:
                    indiv_enable = "~"
                
                row = [
                    tag['unit'] if is_first_tag_for_unit and is_first_alarm_for_tag else "",
                    tag['tag_name'] if is_first_alarm_for_tag else "",
                    tag['desc'] or "~" if is_first_alarm_for_tag else "",
                    tag['desc'] or "~" if is_first_alarm_for_tag else "",
                    tag['pid'] if is_first_alarm_for_tag else "",
                    tag['range_min'] or "0" if is_first_alarm_for_tag else "",
                    tag['range_max'] or "1" if is_first_alarm_for_tag else "",
                    "~" if is_first_alarm_for_tag else "",
                    tag_source if is_first_alarm_for_tag else "",
                    f"Point Type = {tag['point_type']}" if is_first_alarm_for_tag else "",
                    "Enabled" if is_first_alarm_for_tag else "",
                    "Enabled" if is_first_alarm_for_tag else "",
                    param.get('alarmType', ''),
                    indiv_enable,
                    indiv_enable,
                    priority_code,
                    priority_code,
                    param.get('value', '') if not self.is_discrete(param.get('alarmType', '')) else "",
                    param.get('value', '') if not self.is_discrete(param.get('alarmType', '')) else "",
                    "", "",  # Deadband
                    "~", "~",  # Deadband units
                    "", "",  # On-delay
                    "", "",  # Off-delay
                    "Not Started_x",
                    alarm_status,
                    "",  # Alarm comment
                    "",  # Limit owner
                    "",  # HAZOP
                    "",  # Suppression
                    "",  # Class
                    param.get('PurposeOfAlarm', '~') or "~",
                    param.get('ConsequenceOfNoAction', '~') or "~",
                    param.get('BoardOperator', '~') or "~",
                    param.get('FieldOperator', '~') or "~",
                    "",  # H&S
                    "",  # Environment
                    self.map_severity(param.get('consequence', '')),
                    "",  # Reputation
                    "",  # Privilege
                    self.map_severity(param.get('consequence', '')),
                    param.get('TimeToRespond', '') or "",
                ]
                
                rows.append(row)
                
                if is_first_tag_for_unit and is_first_alarm_for_tag:
                    last_unit = tag['unit']
                is_first_alarm_for_tag = False
        
        # Convert to CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(self.PHAPRO_HEADERS)
        writer.writerows(rows)
        
        return output.getvalue(), self.stats
    
    def transform_reverse(self, file_content: str, source_modes: Dict = None) -> Tuple[str, Dict]:
        """Transform PHA-Pro export back to DynAMo format."""
        lines = file_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        reader = csv.reader(lines)
        
        headers = next(reader)
        
        # Map column names to indices
        col_map = {h.strip(): i for i, h in enumerate(headers)}
        
        rows = []
        self.stats = {"tags": 0, "alarms": 0, "units": set()}
        seen_tags = set()
        
        last_tag_name = ""
        last_tag_source = ""
        
        for row in reader:
            if not row or not any(row):
                continue
            
            # Get tag name (propagate from previous row if blank)
            tag_name_idx = col_map.get('Tag Name', 1)
            tag_name = row[tag_name_idx].strip() if tag_name_idx < len(row) else ""
            if tag_name:
                last_tag_name = tag_name
                tag_source_idx = col_map.get('Tag Source', 8)
                if tag_source_idx < len(row) and row[tag_source_idx].strip():
                    last_tag_source = row[tag_source_idx].strip()
            else:
                tag_name = last_tag_name
            
            if tag_name not in seen_tags:
                seen_tags.add(tag_name)
                self.stats["tags"] += 1
            
            # Get alarm type
            alarm_type_idx = col_map.get('Alarm Type', 12)
            alarm_type = row[alarm_type_idx].strip() if alarm_type_idx < len(row) else ""
            
            if not alarm_type:
                continue
            
            self.stats["alarms"] += 1
            
            # Get other fields
            def get_col(name, default=""):
                idx = col_map.get(name)
                if idx is not None and idx < len(row):
                    return row[idx].strip() or default
                return default
            
            new_priority = get_col('New (BPCS) Priority', '')
            new_limit = get_col('New Limit', '')
            alarm_status = get_col('Alarm Status', '')
            causes = get_col('Cause(s)', '~')
            consequences = get_col('Consequence(s)', '~')
            inside_actions = get_col('Inside Action(s)', '~')
            outside_actions = get_col('Outside Action(s)', '~')
            max_severity = get_col('Max Severity', '')
            ttr = get_col('Allowable Time to Respond', '~')
            
            # Determine if Safety Manager
            is_sm = "safety manager" in last_tag_source.lower()
            enforcement = "R" if is_sm else "M"
            
            # Derive alarm name (PV alarms only)
            at_lower = alarm_type.lower()
            alarm_name = ""
            if "pv high high" in at_lower:
                alarm_name = "PVHHALMTP"
            elif "pv low low" in at_lower:
                alarm_name = "PVLLALMTP"
            elif "pv high" in at_lower:
                alarm_name = "PVHIALMTP"
            elif "pv low" in at_lower:
                alarm_name = "PVLOALMTP"
            
            # Derive priority name
            if "controlfail" in at_lower:
                priority_name = "ControlFailAlarmPriority"
            elif "st0" in at_lower:
                priority_name = "State0AlarmPriority"
            elif "st1" in at_lower:
                priority_name = "State1AlarmPriority"
            elif "st2" in at_lower:
                priority_name = "State2AlarmPriority"
            elif "st3" in at_lower:
                priority_name = "State3AlarmPriority"
            elif "pv high high" in at_lower:
                priority_name = "PVHHALMPR"
            elif "pv low low" in at_lower:
                priority_name = "PVLLALMPR"
            elif "pv high" in at_lower:
                priority_name = "PVHIALMPR"
            elif "pv low" in at_lower:
                priority_name = "PVLOALMPR"
            else:
                priority_name = f"{alarm_type}AlarmPriority"
            
            # Map priority back to DynAMo names
            priority_map = {
                'U': 'Urgent', 'C': 'Critical', 'H': 'High', 'M': 'Medium',
                'L': 'Low', 'J': 'Journal', 'JO': 'Journal', 'N': 'NONE'
            }
            priority_value = priority_map.get(new_priority.upper(), new_priority)
            
            # Value
            if self.is_discrete(alarm_type):
                value = "~"
            elif new_limit and new_limit not in ["~", "", "-9999999"]:
                value = new_limit
            else:
                value = "--------"
            
            # Consequence
            status_lower = alarm_status.lower() if alarm_status else ""
            if status_lower == "none":
                consequence = "(None)"
            elif max_severity in ['A', 'B', 'C', 'D', 'E']:
                consequence = max_severity
            elif status_lower in ["alarm", "event"]:
                consequence = "(None)"
            else:
                consequence = "~"
            
            # Disabled parameter (state alarms only)
            disabled_param = ""
            disabled_value = "~"
            disabled_enf = ""
            if "st0" in at_lower:
                disabled_param = "State0AlarmEnabled"
            elif "st1" in at_lower:
                disabled_param = "State1AlarmEnabled"
            elif "st2" in at_lower:
                disabled_param = "State2AlarmEnabled"
            elif "st3" in at_lower:
                disabled_param = "State3AlarmEnabled"
            
            if disabled_param:
                p = new_priority.upper()
                if p == "JO" or status_lower == "none":
                    disabled_value = "FALSE"
                elif status_lower in ["alarm", "event"]:
                    disabled_value = "TRUE"
                disabled_enf = enforcement
            
            # Delay parameters (state alarms only)
            on_delay_param = ""
            off_delay_param = ""
            if "st0" in at_lower:
                on_delay_param = "State0OnDelay"
                off_delay_param = "State0OffDelay"
            elif "st1" in at_lower:
                on_delay_param = "State1OnDelay"
                off_delay_param = "State1OffDelay"
            elif "st2" in at_lower:
                on_delay_param = "State2OnDelay"
                off_delay_param = "State2OffDelay"
            elif "st3" in at_lower:
                on_delay_param = "State3OnDelay"
                off_delay_param = "State3OffDelay"
            
            # Build row
            output_row = [
                "_Variable",
                tag_name,
                "_Parameter",
                source_modes.get((tag_name, alarm_type), "Base") if source_modes else "Base",
                "~",
                alarm_type,
                alarm_name,
                value,
                enforcement if alarm_name else "",
                priority_name,
                priority_value,
                enforcement,
                consequence,
                ttr if ttr and ttr != "~" else "~",
                "N",
                "~",
                causes if causes and causes != "~" else "~",
                consequences if consequences and consequences != "~" else "~",
                inside_actions if inside_actions and inside_actions != "~" else "~",
                outside_actions if outside_actions and outside_actions != "~" else "~",
                "-",
                "", "", "",  # Type params
                disabled_param,
                disabled_value,
                disabled_enf,
                "", "~", "~",  # Suppressed
                on_delay_param,
                "0" if on_delay_param else "~",
                enforcement if on_delay_param else "",
                off_delay_param,
                "0" if off_delay_param else "~",
                enforcement if off_delay_param else "",
                "", "~", "",  # Deadband
                "", "~", "",  # Deadband unit
            ]
            
            rows.append(output_row)
        
        # Convert to CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(self.DYNAMO_HEADERS)
        writer.writerows(rows)
        
        return output.getvalue(), self.stats


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def scan_for_units(file_content: str, client_id: str) -> Tuple[set, set]:
    """
    Scan a DynAMo file and extract available units using both methods.
    
    Returns:
        Tuple of (units_by_tag_prefix, units_by_asset_path)
    """
    import re
    
    lines = file_content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    reader = csv.reader(lines)
    
    units_by_prefix = set()
    units_by_asset = set()
    
    # Get config for unit extraction
    config = AlarmTransformer.CLIENT_CONFIGS.get(client_id, AlarmTransformer.CLIENT_CONFIGS["flng"])
    unit_digits = config.get("unit_digits", 2)
    
    for row in reader:
        if not row or len(row) < 4:
            continue
        
        if row[0].strip() == "_Variable" and len(row) > 2:
            tag_name = row[1].strip()
            schema_type = row[2].strip()
            
            if schema_type == "_DCSVariable":
                # Extract unit from tag prefix
                unit = ""
                for ch in tag_name:
                    if ch.isdigit():
                        unit += ch
                        if len(unit) >= unit_digits:
                            break
                    elif unit:
                        break
                if unit:
                    units_by_prefix.add(unit)
                
                # Extract unit from asset path
                asset_path = row[3] if len(row) > 3 else ""
                if asset_path:
                    # Look for /Uxx/ or /Unitxx/ pattern
                    match = re.search(r'/U(\d+)/', asset_path, re.IGNORECASE)
                    if match:
                        units_by_asset.add(match.group(1))
                    else:
                        # Try other patterns like /Unit67/
                        match = re.search(r'/Unit\s*(\d+)/', asset_path, re.IGNORECASE)
                        if match:
                            units_by_asset.add(match.group(1))
    
    return units_by_prefix, units_by_asset


# ============================================================
# STREAMLIT UI
# ============================================================

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔔 Alarm Rationalization Platform</h1>
        <p>Transform alarm data between DynAMo and PHA-Pro formats</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Client selection
        client_options = {
            "flng": "Freeport LNG",
            "hf_sinclair": "HF Sinclair",
        }
        selected_client = st.selectbox(
            "Select Client Profile",
            options=list(client_options.keys()),
            format_func=lambda x: client_options[x],
            help="Choose the client configuration for tag source rules and mappings"
        )
        
        # Transformation direction
        direction = st.radio(
            "Transformation Direction",
            options=["forward", "reverse"],
            format_func=lambda x: "DynAMo → PHA-Pro" if x == "forward" else "PHA-Pro → DynAMo",
            help="Forward: Create PHA-Pro import from DynAMo export\nReverse: Create DynAMo import from PHA-Pro export"
        )
        
        st.markdown("---")
        
        # Help section
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            **Forward Transformation (DynAMo → PHA-Pro)**
            1. Export your alarm database from DynAMo as CSV
            2. Upload the CSV file below
            3. Select units to process (optional)
            4. Click Transform
            5. Download the PHA-Pro import file
            
            **Reverse Transformation (PHA-Pro → DynAMo)**
            1. Export from PHA-Pro MADB as CSV
            2. Upload the CSV file below
            3. Optionally upload original DynAMo file for mode preservation
            4. Click Transform
            5. Download the DynAMo _Parameter import file
            """)
        
        st.markdown("---")
        st.markdown("### 📊 About")
        st.markdown(f"""
        **Version:** 2.0  
        **Client:** {client_options.get(selected_client, 'Unknown')}  
        **Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 Upload Files")
        
        if direction == "forward":
            st.info("Upload your DynAMo database export CSV file")
            uploaded_file = st.file_uploader(
                "DynAMo Export CSV",
                type=['csv'],
                help="The CSV file exported from DynAMo containing _DCSVariable, _DCS, _Parameter schemas"
            )
            
            # Unit detection and selection
            unit_filter = ""
            unit_method_choice = "tag_prefix"  # default
            
            if uploaded_file is not None:
                # Scan file for available units
                raw_bytes = uploaded_file.read()
                uploaded_file.seek(0)  # Reset for later use
                
                file_content = None
                for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                    try:
                        file_content = raw_bytes.decode(enc)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if file_content:
                    # Extract units using both methods
                    units_by_prefix, units_by_asset = scan_for_units(file_content, selected_client)
                    
                    # Show unit detection results
                    st.markdown("### 📊 Units Detected")
                    
                    # For FLNG, show both methods and let user choose
                    if selected_client == "flng":
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown("**By Tag Prefix:**")
                            if units_by_prefix:
                                st.code(", ".join(sorted(units_by_prefix, key=lambda x: (len(x), x))))
                            else:
                                st.write("None found")
                        
                        with col_b:
                            st.markdown("**By Asset Path:**")
                            if units_by_asset:
                                st.code(", ".join(sorted(units_by_asset, key=lambda x: (len(x), x))))
                            else:
                                st.write("None found")
                        
                        # Let user choose method if they differ
                        if units_by_prefix != units_by_asset:
                            unit_method_choice = st.radio(
                                "Which unit extraction method should be used?",
                                options=["tag_prefix", "asset_path"],
                                format_func=lambda x: "Tag Prefix (first digits of tag name)" if x == "tag_prefix" else "Asset Path (from /Uxx/ in path)",
                                help="Tag Prefix: Uses first 2 digits of tag name (e.g., 67FIC0101 → Unit 67)\nAsset Path: Uses unit from asset hierarchy (e.g., /Assets/U67/ → Unit 67)",
                                horizontal=True
                            )
                        
                        # Show the units for selected method
                        available_units = units_by_prefix if unit_method_choice == "tag_prefix" else units_by_asset
                    else:
                        # For other clients, just show detected units
                        available_units = units_by_prefix
                        st.markdown(f"**Available Units:** {', '.join(sorted(available_units, key=lambda x: (len(x), x))) if available_units else 'None detected'}")
                    
                    st.markdown("---")
            
            # Unit filter input
            unit_filter = st.text_input(
                "Filter by Unit(s)",
                placeholder="e.g., 67 or 67,68,70 (leave blank for all)",
                help="Enter unit numbers separated by commas to filter. Leave blank to process all units."
            )
            
            # Store the method choice in session state for use during transform
            if 'unit_method_choice' not in st.session_state:
                st.session_state.unit_method_choice = "tag_prefix"
            if uploaded_file is not None and selected_client == "flng":
                st.session_state.unit_method_choice = unit_method_choice
            
            source_file = None
            
        else:
            st.info("Upload your PHA-Pro MADB export CSV file")
            uploaded_file = st.file_uploader(
                "PHA-Pro Export CSV",
                type=['csv'],
                help="The CSV file exported from PHA-Pro Alarm Management Database"
            )
            
            st.markdown("**Optional: Original DynAMo file for mode preservation**")
            source_file = st.file_uploader(
                "Original DynAMo Export (optional)",
                type=['csv'],
                help="Upload the original DynAMo export to preserve mode values"
            )
            
            unit_filter = None
    
    with col2:
        st.markdown("### 📋 Output Format")
        
        if direction == "forward":
            st.markdown("""
            **PHA-Pro 45-Column Import**
            - Hierarchical format
            - Unit/Tag/Alarm structure
            - Ready for MADB import
            """)
        else:
            st.markdown("""
            **DynAMo _Parameter 42-Column**
            - Flat format
            - Direct DynAMo import
            - Mode preservation supported
            """)
    
    st.markdown("---")
    
    # Transform button
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            transform_clicked = st.button(
                "🚀 Transform",
                use_container_width=True,
                type="primary"
            )
        
        if transform_clicked:
            with st.spinner("Processing..."):
                try:
                    # Read file with encoding detection
                    raw_bytes = uploaded_file.read()
                    file_content = None
                    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                        try:
                            file_content = raw_bytes.decode(enc)
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if file_content is None:
                        st.error("Could not decode file. Please ensure it's a valid CSV file.")
                        st.stop()
                    
                    # Create transformer
                    transformer = AlarmTransformer(selected_client)
                    
                    if direction == "forward":
                        # Parse unit filter
                        selected_units = None
                        if unit_filter and unit_filter.strip():
                            selected_units = [u.strip() for u in unit_filter.split(',')]
                        
                        # Get unit method from session state (for FLNG)
                        unit_method = st.session_state.get('unit_method_choice', 'tag_prefix')
                        
                        # Transform
                        output_csv, stats = transformer.transform_forward(file_content, selected_units, unit_method)
                        output_filename = f"{selected_client.upper()}_PHA-Pro_Import.csv"
                        
                    else:
                        # Load source modes if provided
                        source_modes = {}
                        if source_file:
                            source_raw = source_file.read()
                            source_content = None
                            for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                                try:
                                    source_content = source_raw.decode(enc)
                                    break
                                except UnicodeDecodeError:
                                    continue
                            
                            if source_content:
                                # Parse source modes
                                lines = source_content.replace('\r\n', '\n').split('\n')
                                reader = csv.reader(lines)
                                for row in reader:
                                    if len(row) >= 6 and row[0] == "_Variable" and row[2] == "_Parameter":
                                        source_modes[(row[1], row[5])] = row[3]
                        
                        # Transform
                        output_csv, stats = transformer.transform_reverse(file_content, source_modes)
                        output_filename = f"{selected_client.upper()}_DynAMo_Return.csv"
                    
                    # Show success
                    st.markdown("""
                    <div class="status-success">
                        <strong>✅ Transformation Complete!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Stats
                    st.markdown("### 📊 Results")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-number">{stats['tags']:,}</div>
                            <div class="stat-label">Tags Processed</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-number">{stats['alarms']:,}</div>
                            <div class="stat-label">Alarms Processed</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        units_str = len(stats.get('units', set())) if isinstance(stats.get('units'), set) else "N/A"
                        st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-number">{units_str}</div>
                            <div class="stat-label">Units Found</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Download button
                    st.markdown("### 📥 Download")
                    st.download_button(
                        label=f"⬇️ Download {output_filename}",
                        data=output_csv,
                        file_name=output_filename,
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Preview
                    with st.expander("👁️ Preview Output (first 20 rows)"):
                        preview_df = pd.read_csv(io.StringIO(output_csv), nrows=20)
                        st.dataframe(preview_df, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error during transformation: {str(e)}")
                    st.exception(e)
    
    else:
        st.markdown("""
        <div class="status-info">
            <strong>👆 Upload a file to get started</strong><br>
            Select your client profile and transformation direction in the sidebar, then upload your CSV file.
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #6c757d; font-size: 0.85rem;'>"
        "Alarm Rationalization Platform • Applied Engineering Solutions • "
        f"Built with Streamlit • {datetime.now().year}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

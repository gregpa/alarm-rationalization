# Column Mapping Reference

This document provides a complete reference for how fields are mapped between DCS formats and PHA-Pro.

**Keep this document current whenever clients are added or column mappings change.**

---

## PHA-Pro Output Formats

### FLNG Format (45 columns) - `PHAPRO_HEADERS`

| Index | Column Name | Source |
|-------|-------------|--------|
| 0 | Unit | Extracted from tag (TAG_PREFIX method) |
| 1 | Tag Name | _DCSVariable name |
| 2 | Old Tag Description | _DCS desc |
| 3 | New Tag Description | _DCS desc (copy) |
| 4 | P&ID | Set to "UNKNOWN" for review |
| 5 | Range Min | _DCS PVEULO |
| 6 | Range Max | _DCS PVEUHI |
| 7 | Engineering Units | _DCS engUnits |
| 8 | Tag Source | Derived from tag_source_rules |
| 9 | Rationalization (Tag) Comment | Empty |
| 10 | Old Tag Enable Status | Empty |
| 11 | New Tag Enable Status | Empty |
| 12 | Alarm Type | _Parameter alarmType |
| 13 | Old Individual Alarm Enable Status | Based on DisabledValue |
| 14 | New Individual Alarm Enable Status | Based on DisabledValue |
| 15 | Old (BPCS) Priority | Mapped from priorityValue |
| 16 | New (BPCS) Priority | Mapped from priorityValue |
| 17 | Old Limit | _Parameter value (analog) or {n/a} (discrete) |
| 18 | New Limit | _Parameter value (analog) or {n/a} (discrete) |
| 19 | Old Deadband | _Parameter DeadBandValue |
| 20 | New Deadband | _Parameter DeadBandValue |
| 21 | Old Deadband Units | _Parameter DeadBandUnitValue |
| 22 | New Deadband Units | _Parameter DeadBandUnitValue |
| 23 | Old On-Delay Time | _Parameter OnDelayValue |
| 24 | New On-Delay Time | _Parameter OnDelayValue |
| 25 | Old Off-Delay Time | _Parameter OffDelayValue |
| 26 | New Off-Delay Time | _Parameter OffDelayValue |
| 27 | Rationalization Status | "Not Started_x" |
| 28 | Alarm Status | Mapped from priority (Active/Shelved/Journal) |
| 29 | Rationalization (Alarm) Comment | Empty |
| 30 | Limit Owner | Empty |
| 31 | Alarm HAZOP Comment | Empty |
| 32 | Alarm Suppression Notes | Empty |
| 33 | Alarm Class | Empty |
| 34 | Cause(s) | _Parameter PurposeOfAlarm |
| 35 | Consequence(s) | _Parameter ConsequenceOfNoAction |
| 36 | Inside Action(s) | _Parameter BoardOperator |
| 37 | Outside Action(s) | _Parameter FieldOperator |
| 38 | Health and Safety | Empty |
| 39 | Environment | Empty |
| 40 | Financial | Empty |
| 41 | Reputation | Empty |
| 42 | Privilege to Operate | Empty |
| 43 | Max Severity | Mapped from consequence |
| 44 | Allowable Time to Respond | _Parameter TimeToRespond |

### HFS Format (43 columns) - `HFS_PHAPRO_HEADERS`

| Index | Column Name | Source |
|-------|-------------|--------|
| 0 | Unit | Extracted from tag (TAG_PREFIX method) |
| 1 | Starting Tag Name | _DCSVariable name |
| 2 | New Tag Name | _DCSVariable name (copy) |
| 3 | Old Tag Description | _DCS desc |
| 4 | New Tag Description | _DCS desc (copy) |
| 5 | P&ID | Set to "UNKNOWN" for review |
| 6 | Range Min | _DCS PVEULO |
| 7 | Range Max | _DCS PVEUHI |
| 8 | Engineering Units | _DCS engUnits |
| 9 | Tag Source | Derived from tag_source_rules |
| 10 | Rationalization (Tag) Comment | Empty |
| 11 | Old Tag Enable Status | Empty |
| 12 | New Tag Enable Status | Empty |
| 13 | Starting Alarm Type | _Parameter alarmType |
| 14 | New Alarm Type | _Parameter alarmType (copy) |
| 15 | Old Alarm Enable Status | Based on DisabledValue |
| 16 | New Alarm Enable Status | Based on DisabledValue |
| 17 | Old (BPCS) Priority | Mapped from priorityValue |
| 18 | New (BPCS) Priority | Mapped from priorityValue |
| 19 | Old Limit | _Parameter value (analog) or {n/a} (discrete) |
| 20 | New Limit | _Parameter value (analog) or {n/a} (discrete) |
| 21 | Old Deadband | _Parameter DeadBandValue |
| 22 | New Deadband | _Parameter DeadBandValue |
| 23 | Old Deadband Units | _Parameter DeadBandUnitValue |
| 24 | New Deadband Units | _Parameter DeadBandUnitValue |
| 25 | Old On-Delay Time | _Parameter OnDelayValue |
| 26 | New On-Delay Time | _Parameter OnDelayValue |
| 27 | Old Off-Delay Time | _Parameter OffDelayValue |
| 28 | New Off-Delay Time | _Parameter OffDelayValue |
| 29 | Rationalization Status | "Not Started_x" |
| 30 | Alarm Status | Mapped from priority (Active/Shelved/Journal) |
| 31 | Rationalization (Alarm) Comment | Empty |
| 32 | Alarm Class | Empty |
| 33 | Cause(s) | _Parameter PurposeOfAlarm |
| 34 | Consequence(s) | _Parameter ConsequenceOfNoAction |
| 35 | Inside Action(s) | _Parameter BoardOperator |
| 36 | Outside Action(s) | _Parameter FieldOperator |
| 37 | Escalation | Empty |
| 38 | Limit Owner | Empty |
| 39 | Personnel | Empty |
| 40 | Public or Environment | Empty |
| 41 | Costs / Production | Empty |
| 42 | Maximum Time to Resolve | _Parameter TimeToRespond |

### Petrostar Format (27 columns) - `PHAPRO_HEADERS_PETROSTAR`

| Index | Column Name | Source |
|-------|-------------|--------|
| 0 | Unit | Extracted from DeltaV Path/tag (PATH_PREFIX method) |
| 1 | Tag Name | AlarmSourceName |
| 2 | Old Tag Description | AlarmSourceDescription |
| 3 | New Tag Description | AlarmSourceDescription (copy) |
| 4 | P&ID | Empty |
| 5 | Range Min | Empty |
| 6 | Range Max | Empty |
| 7 | Engineering Units | Empty |
| 8 | Tag Source | "Emerson DeltaV (DCS)" (single source) |
| 9 | Rationalization (Tag) Comment | Path top-level area (e.g., "14_DHT") |
| 10 | Alarm Type | Attribute (e.g., HI_ALM, LO_LO_ALM) |
| 11 | Old Individual Alarm Enable Status | Enable (True/False) |
| 12 | New Individual Alarm Enable Status | Enable (copy) |
| 13 | Old (BPCS) Priority | Mapped from DeltaV Priority (C/W/Ad/O/Lg/N) |
| 14 | New (BPCS) Priority | Mapped from DeltaV Priority (copy) |
| 15 | Old Limit | LimitValue |
| 16 | New Limit | LimitValue (copy) |
| 17 | Old Deadband | Hysteresis |
| 18 | New Deadband | Hysteresis (copy) |
| 19 | Old On-Delay Time | OnDelay |
| 20 | New On-Delay Time | OnDelay (copy) |
| 21 | Old Off-Delay Time | OffDelay |
| 22 | New Off-Delay Time | OffDelay (copy) |
| 23 | Rationalization Status | "Not Started_x" |
| 24 | Alarm Status | Derived from priority (Alarm/Event/"") |
| 25 | Rationalization (Alarm) Comment | Empty |
| 26 | Alarm Class | FunctionalClassificationName (mapped) |

### ABB Format (23 columns) - `ABB_PHAPRO_HEADERS`

| Index | Column Name | Source |
|-------|-------------|--------|
| 0 | Unit | From ABB Unit column |
| 1 | Starting Tag Name | ABB Tag Name |
| 2 | New Tag Name | ABB Tag Name (copy) |
| 3 | Old Tag Description | ABB Description |
| 4 | New Tag Description | ABB Description (copy) |
| 5 | Tag Source | From client default_source |
| 6 | Rationalization (Tag) Comment | Empty |
| 7 | Range Min | ABB Min Range |
| 8 | Range Max | ABB Max Range |
| 9 | Engineering Units | ABB Units |
| 10 | Starting Alarm Type | ABB Alarm Type |
| 11 | New Alarm Type | ABB Alarm Type (copy) |
| 12 | Old Alarm Enable Status | ABB Enable Status |
| 13 | New Alarm Enable Status | ABB Enable Status (copy) |
| 14 | Old Alarm Severity | ABB Severity |
| 15 | New Alarm Severity | ABB Severity (copy) |
| 16 | Old Limit | ABB Limit |
| 17 | New Limit | ABB Limit (copy) |
| 18 | Old (BPCS) Priority | ABB Priority |
| 19 | New (BPCS) Priority | ABB Priority (copy) |
| 20 | Rationalization Status | "Not Started_x" |
| 21 | Alarm Status | "Active" |
| 22 | Rationalization (Alarm) Comment | Empty |

---

## DynAMo Source Schema (_Parameter)

The DynAMo CSV contains multiple schemas. The `_Parameter` schema has 42+ columns with these key indices:

| Index | Field Name | Description |
|-------|------------|-------------|
| 0 | '_Variable | Schema identifier |
| 1 | name | Tag name |
| 2 | _Parameter | Schema type marker |
| 3 | mode | NORMAL, IMPORT, Export, etc. |
| 4 | boundary | Alarm boundary |
| 5 | alarmType | HI, LO, HIHI, LOLO, etc. |
| 6 | alarmName | Alarm name |
| 7 | value | Alarm setpoint/limit |
| 8 | enforcement | Value enforcement flag |
| 9 | priorityName | Priority name |
| 10 | priorityValue | Priority code (1-12) |
| 11 | priorityEnforcement | Priority enforcement flag |
| 12 | consequence | Severity/consequence code |
| 13 | TimeToRespond | TTR in minutes |
| 14 | pre-Alarm | Pre-alarm flag |
| 15 | historyTag | History tag reference |
| 16 | Purpose of Alarm | Cause description |
| 17 | Consequence of No Action | Consequence description |
| 18 | Board Operator | Inside operator actions |
| 19 | Field Operator | Outside operator actions |
| 20 | Supporting Notes | Additional notes |
| 21 | TypeParameter | Type parameter name |
| 22 | TypeValue | Type value |
| 23 | TypeEnforcement | Type enforcement flag |
| 24 | DisabledParameter | Disabled parameter name |
| 25 | DisabledValue | TRUE=disabled, FALSE=enabled |
| 26 | DisabledEnforcement | Disabled enforcement flag |
| 27 | SuppressedParameter | Suppressed parameter name |
| 28 | SuppressedValue | Suppressed value |
| 29 | SuppressedEnforcement | Suppressed enforcement flag |
| 30 | OnDelayParameter | On-delay parameter name |
| 31 | OnDelayValue | On-delay time value |
| 32 | OnDelayEnforcement | On-delay enforcement flag |
| 33 | OffDelayParameter | Off-delay parameter name |
| 34 | OffDelayValue | Off-delay time value |
| 35 | OffDelayEnforcement | Off-delay enforcement flag |
| 36 | DeadBandParameter | Deadband parameter name |
| 37 | DeadBandValue | Deadband value |
| 38 | DeadBandEnforcement | Deadband enforcement flag |
| 39 | DeadBandUnitParameter | Deadband unit parameter |
| 40 | DeadBandUnitValue | Deadband unit (%, EU, etc.) |
| 41 | DeadBandUnitEnforcement | Deadband unit enforcement |

---

## DynAMo Output Format (42 columns) - `DYNAMO_HEADERS`

For reverse transformations (PHA-Pro to DynAMo), the output uses these headers:

| Index | Column Name |
|-------|-------------|
| 0 | '_Variable |
| 1 | name |
| 2 | _Parameter |
| 3 | mode |
| 4 | boundary |
| 5 | alarmType |
| 6 | alarmName |
| 7 | value |
| 8 | enforcement |
| 9 | priorityName |
| 10 | priorityValue |
| 11 | priorityEnforcement |
| 12 | consequence |
| 13 | TimeToRespond |
| 14 | pre-Alarm |
| 15 | historyTag |
| 16 | Purpose of Alarm |
| 17 | Consequence of No Action |
| 18 | Board Operator |
| 19 | Field Operator |
| 20 | Supporting Notes |
| 21 | TypeParameter |
| 22 | TypeValue |
| 23 | TypeEnforcement |
| 24 | DisabledParameter |
| 25 | DisabledValue |
| 26 | DisabledEnforcement |
| 27 | SuppressedParameter |
| 28 | SuppressedValue |
| 29 | SuppressedEnforcement |
| 30 | OnDelayParameter |
| 31 | OnDelayValue |
| 32 | OnDelayEnforcement |
| 33 | OffDelayParameter |
| 34 | OffDelayValue |
| 35 | OffDelayEnforcement |
| 36 | DeadBandParameter |
| 37 | DeadBandValue |
| 38 | DeadBandEnforcement |
| 39 | DeadBandUnitParameter |
| 40 | DeadBandUnitValue |
| 41 | DeadBandUnitEnforcement |

---

## Priority Mapping

### DynAMo Priority Mapping

| DynAMo Priority | PHA-Pro Code | Alarm Status |
|-----------------|--------------|--------------|
| URGENT (1-2) | U | Active |
| CRITICAL (3-4) | C | Active |
| HIGH (5-6) | H | Active |
| MEDIUM (7-8) | M | Active |
| LOW (9-10) | L | Active |
| JOURNAL (11-12) | J | Journal |
| JOURNAL (disabled) | Jo | Shelved |

### DeltaV Priority Mapping (Petrostar)

Suffixes `_N` and `_FG` are stripped before mapping.

| DeltaV Priority | PHA-Pro Code | Alarm Status |
|-----------------|--------------|--------------|
| CRITICAL | C | Alarm |
| CRITICAL_N | C | Alarm |
| CRITICAL_FG | C | Alarm |
| WARNING | W | Alarm |
| WARNING_N | W | Alarm |
| WARNING_FG | W | Alarm |
| ADVISORY | Ad | Alarm |
| ADVISORY_N | Ad | Alarm |
| SOL_ALARM | O | Alarm |
| NOL_ALARM | O | Alarm |
| LOG | Lg | Event |
| (unknown) | N | (empty) |

---

## Severity Mapping (Consequence to Max Severity)

| Consequence | Severity |
|-------------|----------|
| CATASTROPHIC | A |
| SEVERE, MAJOR | B |
| MODERATE | C |
| MINOR | D |
| INCIDENTAL, NEGLIGIBLE | E |
| Empty/None | (None) |

---

## Discrete vs Analog Alarm Types

### Discrete Alarm Types (use `{n/a}` for limit values)
- ControlFail, CNTLFAIL
- Deviation (DEV, DEVHI, DEVLO)
- RateOfChange (ROC)
- Digital types (DIGALARM, STATE)
- Bad PV types (BADPVAL, BADPV)
- Out of Range types (OORANGE, OORHI, OORLO)

### Analog Alarm Types (use actual setpoint values)
- HI, LO, HIHI, LOLO
- HIGH, LOW

---

## Version History

| Date | Changes |
|------|---------|
| 2026-01 | Initial creation with verified mappings |
| 2026-01 | Added HFS format (43 columns with delay fields) |
| 2026-01 | Added ABB format (23 columns) |
| 2026-02 | Added Petrostar/DeltaV format (27 columns) with DeltaV priority mapping |

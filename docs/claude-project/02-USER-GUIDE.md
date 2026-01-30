# Alarm Rationalization Platform - User Guide

## Quick Start

**Access the app**: https://alarm-rationalization.streamlit.app

### Basic Workflow

1. **Select Client** - Choose your facility from the dropdown
2. **Choose Direction** - Forward (DCS→PHA-Pro) or Reverse (PHA-Pro→DCS)
3. **Upload File** - Drag & drop or click to browse
4. **Click Transform** - Process the data
5. **Download Result** - CSV or Excel format

---

## Supported Clients

| Client | Control System | Parser | Output Columns |
|--------|---------------|--------|----------------|
| Freeport LNG | Honeywell Experion/TDC | DynAMo | 45 |
| HF Sinclair - Artesia | Honeywell Experion | DynAMo | 43 |
| Rio Tinto - Bessemer | ABB 800xA | ABB Excel | 23 |

---

## Forward Transformation (DCS → PHA-Pro)

### Purpose
Convert alarm database exports from your control system into PHA-Pro's MADB import format for alarm rationalization.

### Input Requirements

**For DynAMo clients (FLNG, HFS):**
- File type: CSV
- Required schemas: `_DCSVariable`, `_DCS`, `_Parameter`, `_Notes`
- Export from: DynAMo Alarm Configuration

**For ABB clients (Rio Tinto):**
- File type: Excel (.xlsx)
- Export from: ABB 800xA alarm database

### Steps

1. Select your client
2. Ensure "Forward" direction is selected
3. Upload your DCS export file
4. (Optional) Select specific units or "All Units"
5. (Optional) Enable "Preview data before transforming"
6. Click **Transform**
7. Download the result (CSV or Excel)

### Output

The output file is formatted for PHA-Pro MADB import:
- Hierarchical structure (Node, Function, Equipment, Alarm)
- Priority codes mapped (U, C, H, M, L, Jo)
- Tag source and enforcement populated
- Ready for direct import

### P&ID Review Note
Tags without P&ID data are marked as "UNKNOWN". Review and update these before importing to PHA-Pro.

---

## Reverse Transformation (PHA-Pro → DCS)

### Purpose
After completing alarm rationalization in PHA-Pro, convert the updated alarm data back to your control system's import format.

### Input Requirements

**Primary file:**
- PHA-Pro MADB export (CSV)
- Contains rationalized alarm settings

**Secondary file (DynAMo clients only):**
- Original DCS export file
- Required to preserve client-specific values (mode, etc.)

### Steps

1. Select your client
2. Select "Reverse" direction
3. Upload your PHA-Pro MADB export
4. Upload your original DCS export (DynAMo clients)
5. Click **Transform**
6. Download the result

### Mode Handling

The app only processes alarms with **NORMAL** mode. Other modes (IMPORT, Export, etc.) are skipped because:
- NORMAL is the active operating configuration
- Other modes are administrative/backup rows
- Including all modes would create duplicates

The skipped row count is displayed after transformation.

---

## Unit Selection

### Methods

| Method | How it works |
|--------|--------------|
| Tag Prefix | Extracts first N digits from tag name (e.g., `17FIC-123` → `17`) |
| Asset Parent | Uses the asset parent field from DCS data |
| Asset Child | Uses the asset child field from DCS data |
| Fixed | Uses a pre-configured value (ABB clients) |

### Selecting Units

After uploading a file:
1. The app scans for available units
2. Select specific units from the dropdown, OR
3. Choose "All Units" to process everything

---

## Data Preview

Enable preview to see before transforming:
- Total rows in file
- Rows that will be processed
- Rows that will be skipped (and why)
- Units detected in the file
- Potential issues (encoding, format)

This is optional and off by default.

---

## Download Options

After transformation, download in:
- **CSV** - Standard comma-separated format
- **Excel** - .xlsx format with proper formatting

For reverse transformations (all clients), you can also download:
- **Change Report** - Excel showing what changed from original

### Change Report
The Change Report compares original values with rationalized values and highlights:
- Limit changes
- Priority changes
- Severity changes
- Enable status changes
- (DynAMo only) TTR, Cause, Consequence, Operator actions

**Requirements:**
- DynAMo clients: Original DCS export file (required)
- ABB clients: Original ABB Excel export (optional, but needed for Change Report)

---

## Transformation History

View recent transformations in the sidebar:
- Input file name
- Direction and client
- Tags and alarms processed
- Re-download previous results

History is stored in your browser session (cleared on page refresh).

---

## Troubleshooting

### "Missing Required Columns" Error

**Cause**: Your file doesn't have the expected column structure.

**Solutions**:
- Verify you're uploading the correct file type
- Check that the export includes all required schemas
- Try re-exporting from your DCS/PHA-Pro

### Empty Output

**Cause**: No rows matched the processing criteria.

**Solutions**:
- Check if your file has rows with mode=NORMAL
- Verify unit selection includes your data
- Try selecting "All Units"

### Encoding Errors / Garbled Characters

**Cause**: Special characters (°, ±, etc.) in source data.

**Solution**: The app automatically tries multiple encodings (UTF-8, Latin-1, CP1252). If you still see issues, try saving your source file with UTF-8 encoding.

### "Please upload original DCS export"

**Cause**: DynAMo reverse transforms need the original file to preserve client-specific values.

**Solution**: Upload the same file you used for the forward transformation.

### Configuration Warnings/Errors

**Cause**: The client configuration file (clients.yaml) has issues.

**Solution**:
- Errors (red): Contact administrator - these block functionality
- Warnings (yellow): Non-critical issues, app still works but may have unexpected behavior
- Look for details in the sidebar "Config Error(s)" or "Config Warning(s)" expanders

---

## Tips

1. **Keep your original files** - You'll need them for reverse transformations
2. **Use Preview** - Check data before transforming large files
3. **Check skipped rows** - Click the info expander to understand why rows were skipped
4. **Review P&IDs** - Mark any "UNKNOWN" P&ID references before PHA-Pro import
5. **Download both formats** - CSV for import, Excel for review

---

## Getting Help

- Click "Report Issue" in the sidebar to submit feedback
- Contact Applied Engineering Solutions for support

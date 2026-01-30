# Alarm Rationalization Platform

A professional web application for transforming alarm data between Honeywell DynAMo and PHA-Pro formats.

## Live Application

**Access the app:** [https://alarm-rationalization.streamlit.app](https://alarm-rationalization.streamlit.app)

## Features

- **Forward Transformation**: Convert DynAMo exports to PHA-Pro 45-column import format
- **Reverse Transformation**: Convert PHA-Pro exports back to DynAMo _Parameter format
- **Multi-Client Support**: Configurations for FLNG, HF Sinclair, and more
- **Unit Filtering**: Process specific units or all units at once
- **Mode Preservation**: Maintain original mode values when transforming back to DynAMo
- **Professional UI**: Modern, intuitive web interface

## Quick Start

### Using the Web App

1. Visit the application URL
2. Select your client profile (FLNG, HF Sinclair, etc.)
3. Choose transformation direction
4. Upload your CSV file
5. Click Transform
6. Download the result

### Running Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/alarm-rationalization.git
cd alarm-rationalization

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

---

## Development Workflow

This section documents the development tools, testing, and deployment processes.

### Project Structure

```
alarm-rationalization/
├── streamlit_app.py              # Main application (v3.23+)
├── requirements.txt              # Python dependencies
├── deploy.sh                     # Deployment script
│
├── config/
│   └── clients.yaml              # External client configurations (editable)
│
├── backups/                      # Code backups (created automatically)
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   └── test_transformer.py       # 43 tests for behavior validation
│
├── .vscode/
│   └── tasks.json                # VS Code tasks
│
├── .github/workflows/
│   ├── validate.yml              # CI/CD for main branch
│   └── staging.yml               # CI/CD for develop branch
│
├── .pre-commit-config.yaml       # Pre-commit hooks
└── .streamlit/
    └── config.toml               # Streamlit theme config
```

### VS Code Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task"

| Task | Description | When to Use |
|------|-------------|-------------|
| **Run App Locally** | Starts Streamlit on localhost:8501 | Local testing |
| **Validate Code** | Checks Python syntax only | Quick syntax check |
| **Run Tests** | Runs full test suite (43 tests) | Verify nothing broke |
| **Validate + Deploy** | Syntax check → deploy | Quick deploy for small changes |
| **Run Tests + Deploy** | Full tests → deploy | **Recommended** - safest option |
| **Quick Commit** | Validates then commits | Fast commits with safety |
| **Deploy to Production** | Runs deploy.sh | Manual deploy |
| **Git Status** | Shows status + recent commits | Check repo state |
| **Install Test Dependencies** | Installs pytest | First-time setup |

### Testing

The test suite captures v3.23 behavior to prevent regressions.

```bash
# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/test_transformer.py::TestPriorityMapping -v

# Run with coverage
pytest tests/ -v --cov=streamlit_app
```

**Test Categories:**
- `TestAlarmTransformerInit` - Client configuration loading
- `TestDiscreteAlarmDetection` - Discrete vs analog classification
- `TestPriorityMapping` - Priority code mapping (U, C, H, M, L, Jo)
- `TestSeverityMapping` - Consequence to severity (A-E)
- `TestUnitExtraction` - Unit extraction methods
- `TestTagSourceDerivation` - Tag source rules
- `TestForwardTransformation` - DynAMo → PHA-Pro
- `TestDynamoParsing` - CSV parsing
- `TestABBSupport` - ABB 800xA client
- `TestHFSinclair` - HF Sinclair specifics
- `TestExternalConfigLoader` - YAML config loading with fallback
- `TestDataPreview` - Data validation preview feature
- `TestConfigFallback` - Hardcoded fallback configuration

### External Configuration

Client configurations can be edited without touching Python code.

**Edit:** `config/clients.yaml`

```yaml
# Example: Add a new client
new_client:
  name: "New Client Name"
  vendor: "Control System"
  parser: "dynamo"
  unit_method: "TAG_PREFIX"
  unit_digits: 2
  default_source: "DCS Name"
  tag_source_rules:
    - exact: "SM"
      field: "point_type"
      source: "Safety Manager"
      enforcement: "R"
  areas:
    main_area:
      name: "Main Area"
      description: "Primary processing area"
```

**Fallback:** If the YAML file is missing or corrupted, the app automatically falls back to hardcoded defaults in `streamlit_app.py`.

### Data Validation Preview

Before transforming, you can preview what will happen:

1. Upload your file
2. Check "Preview data before transforming"
3. Review:
   - Total rows vs rows to process
   - Rows that will be skipped (and why)
   - Units found in the file
   - Potential issues (encoding, format)

This is **off by default** - the original Transform workflow is unchanged.

### Pre-commit Hooks

Validates code before every commit.

```bash
# Install (one-time setup)
pip install pre-commit
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

**Checks performed:**
- Python syntax validation
- Streamlit imports check
- Trailing whitespace
- YAML/JSON validation
- Large file detection
- Merge conflict markers
- Private key detection

### Deployment

#### Recommended: Test-First Deploy

```bash
# From VS Code: Run "Run Tests + Deploy" task
# Or manually:
pytest tests/ -v && ./deploy.sh
```

#### Quick Deploy (syntax check only)

```bash
./deploy.sh
```

#### Branch Strategy

| Branch | Purpose | Auto-Deploy |
|--------|---------|-------------|
| `main` | Production | Yes → alarm-rationalization.streamlit.app |
| `develop` | Staging/Testing | Validates only (no deploy) |

**Workflow:**
1. Create feature branch from `main`
2. Make changes
3. Run tests locally: `pytest tests/ -v`
4. Push to `develop` for CI validation
5. Merge to `main` for production deploy

### GitHub Actions

**On push to `main`:**
1. Validates Python syntax
2. Checks imports
3. Runs test suite
4. Validates AST structure
5. (Optional) Sends Slack/Teams notification

**To enable notifications:**
1. Create webhook URL (Slack or Teams)
2. Add as GitHub secret: `SLACK_WEBHOOK_URL` or `TEAMS_WEBHOOK_URL`
3. Uncomment notification step in `.github/workflows/validate.yml`

### Adding New Features Safely

1. **Before coding:** Run tests to establish baseline
   ```bash
   pytest tests/ -v
   ```

2. **After coding:** Run tests to verify no regressions
   ```bash
   pytest tests/ -v
   ```

3. **Deploy:** Use test-first deploy
   ```bash
   # VS Code: "Run Tests + Deploy" task
   ```

4. **If tests fail:** Fix the issue or update tests if behavior change is intentional

---

## Supported Formats

### Forward (DynAMo → PHA-Pro)

**Input**: DynAMo multi-schema CSV export containing:
- `_DCSVariable` - Tag definitions
- `_DCS` - DCS properties
- `_Parameter` - Alarm parameters
- `_Notes` - Documentation

**Output**: PHA-Pro 45-column hierarchical import format (43 for HFS)

### Reverse (PHA-Pro → DynAMo)

**Input**: PHA-Pro MADB export CSV

**Output**: DynAMo _Parameter 42-column import format

## Supported Clients

| Client | Control System | Parser | Columns | Tag Source Rules |
|--------|---------------|--------|---------|------------------|
| Freeport LNG | Honeywell Experion/TDC | DynAMo | 45 | SM→SIS, ANA/STA→SCADA |
| HF Sinclair - Artesia | Honeywell Experion | DynAMo | 43 | 77 point-type rules |
| Rio Tinto - Bessemer | ABB 800xA | ABB Excel | 23 | Fixed source |

## Adding New Clients

Modify the `CLIENT_CONFIGS` dictionary in `streamlit_app.py`:

```python
CLIENT_CONFIGS = {
    "new_client": {
        "name": "New Client Name",
        "vendor": "Control System Vendor",
        "parser": "dynamo",  # or "abb"
        "unit_method": "TAG_PREFIX",
        "unit_digits": 2,
        "tag_source_rules": [
            {"prefix": "SM", "field": "point_type", "source": "Safety System", "enforcement": "R"},
        ],
        "default_source": "Default DCS Name",
        "areas": {
            "area_id": {"name": "Area Name", "description": "Area Description"},
        },
    },
}
```

**After adding a client:** Add corresponding tests in `tests/test_transformer.py`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v3.23 | Jan 2026 | Fixed Unit column display |
| v3.22 | Jan 2026 | Unit display refinement |
| v3.21 | Jan 2026 | Encoding & comma stripping fixes |
| v3.19 | Jan 2026 | Enhanced unit extraction options |

---

## License

Proprietary - Applied Engineering Solutions

## Support

For support or questions, contact Applied Engineering Solutions.

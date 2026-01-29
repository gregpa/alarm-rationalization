# 🔔 Alarm Rationalization Platform

A professional web application for transforming alarm data between Honeywell DynAMo and PHA-Pro formats.

## 🌐 Live Application

**Access the app:** [https://alarm-rationalization.streamlit.app](https://alarm-rationalization.streamlit.app)

## ✨ Features

- **Forward Transformation**: Convert DynAMo exports to PHA-Pro 45-column import format
- **Reverse Transformation**: Convert PHA-Pro exports back to DynAMo _Parameter format
- **Multi-Client Support**: Configurations for FLNG, HF Sinclair, and more
- **Unit Filtering**: Process specific units or all units at once
- **Mode Preservation**: Maintain original mode values when transforming back to DynAMo
- **Professional UI**: Modern, intuitive web interface

## 🚀 Quick Start

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

## 🚀 Deployment

This project features automatic deployment to Streamlit Cloud.

### Quick Deploy
```bash
./deploy.sh
```

The deploy script will guide you through committing and pushing changes. Any push to the `main` branch automatically triggers deployment to production.

**For detailed deployment instructions**, see [DEPLOYMENT.md](DEPLOYMENT.md)

### Manual Deploy
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Changes will be live at https://alarm-rationalization.streamlit.app within 2-5 minutes.

## 📋 Supported Formats

### Forward (DynAMo → PHA-Pro)

**Input**: DynAMo multi-schema CSV export containing:
- `_DCSVariable` - Tag definitions
- `_DCS` - DCS properties  
- `_Parameter` - Alarm parameters
- `_Notes` - Documentation

**Output**: PHA-Pro 45-column hierarchical import format

### Reverse (PHA-Pro → DynAMo)

**Input**: PHA-Pro MADB export CSV

**Output**: DynAMo _Parameter 42-column import format

## 🏭 Supported Clients

| Client | Control System | Tag Source Rules |
|--------|---------------|------------------|
| Freeport LNG | Honeywell Experion/TDC | SM→SIS, ANA/STA→SCADA |
| HF Sinclair | Honeywell Experion | Configurable |

## 📁 Project Structure

```
alarm-rationalization/
├── streamlit_app.py      # Main web application
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── config/              # Client configurations (optional)
```

## 🔧 Adding New Clients

To add a new client, modify the `CLIENT_CONFIGS` dictionary in `streamlit_app.py`:

```python
CLIENT_CONFIGS = {
    "new_client": {
        "name": "New Client Name",
        "vendor": "Control System Vendor",
        "unit_method": "TAG_PREFIX",
        "unit_digits": 2,
        "tag_source_rules": [
            {"prefix": "SM", "field": "point_type", "source": "Safety System", "enforcement": "R"},
        ],
        "default_source": "Default DCS Name",
    },
}
```

## 📄 License

Proprietary - Applied Engineering Solutions

## 👥 Support

For support or questions, contact Applied Engineering Solutions.

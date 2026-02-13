# Alarm Rationalization Platform
## Self-Hosted Deployment Guide

---

## Overview

This guide provides instructions for deploying the Alarm Rationalization Platform on your own infrastructure. This setup keeps all client data behind your firewall while allowing the application developer to push updates directly via GitHub.

**Application Version:** 3.25
**Last Updated:** January 2026

---

## Responsibilities

| Task | Responsibility |
|------|----------------|
| Server setup & maintenance | IT |
| Firewall, network, SSL | IT |
| User password management | IT |
| Backups & monitoring | IT |
| Application code updates | Developer |
| Bug fixes & new features | Developer |
| Adding new clients/units | Developer |

---

## How It Works

The auto-update mechanism:

```
Developer updates code on GitHub
          ↓
Server detects change (every 2 minutes)
          ↓
Server pulls new code automatically
          ↓
Service restarts
          ↓
Users see updated app
```

**Passwords are managed separately by IT - they never go through GitHub.**

---

## Server Requirements

| Requirement | Specification |
|-------------|---------------|
| Operating System | Windows Server 2016+ or Linux (Ubuntu 20.04+, RHEL 8+) |
| Python | 3.9 or higher |
| Git | Latest version |
| RAM | 2GB minimum (4GB recommended) |
| Disk Space | 1GB for application + data |
| Network | Internal network access for users |
| Port | 8501 (or configure reverse proxy) |
| Outbound Access | HTTPS to github.com |

---

## Installation Steps

### Step 1: Install Prerequisites

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

**Linux (RHEL/CentOS)**
```bash
sudo dnf install python3 python3-pip git
```

**Windows Server**
- Install Python from https://python.org (check "Add to PATH")
- Install Git from https://git-scm.com/download/win

### Step 2: Clone the Repository

**Linux**
```bash
cd /opt
sudo git clone https://github.com/gregpa/alarm-rationalization.git alarm-platform
sudo chown -R www-data:www-data /opt/alarm-platform
cd /opt/alarm-platform
```

**Windows**
```cmd
cd C:\Apps
git clone https://github.com/gregpa/alarm-rationalization.git alarm-platform
cd alarm-platform
```

### Step 3: Set Up Python Environment

**Linux**
```bash
cd /opt/alarm-platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows**
```cmd
cd C:\Apps\alarm-platform
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** The requirements.txt includes: streamlit, pandas, openpyxl, pyyaml

### Step 4: Create Configuration Files

Create the `.streamlit` directory:

**Linux**
```bash
mkdir -p /opt/alarm-platform/.streamlit
```

**Windows**
```cmd
mkdir C:\Apps\alarm-platform\.streamlit
```

**config.toml** - Server configuration:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1e3a5f"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

**secrets.toml** - User passwords:
```toml
[passwords]
admin = "SecureAdminPass123!"
jsmith = "SmithPass456!"
mjones = "JonesPass789!"
# Add more users as needed
```

**Important** - Set file permissions (Linux):
```bash
chmod 600 /opt/alarm-platform/.streamlit/secrets.toml
```

**The secrets.toml file must NOT be committed to Git. It stays on the server only.**

### Step 5: Create Auto-Update Script

**Linux: /opt/alarm-platform/update.sh**
```bash
#!/bin/bash
cd /opt/alarm-platform
git fetch origin main
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): New version detected, updating..."
    git pull origin main
    # Reinstall dependencies in case they changed
    source venv/bin/activate
    pip install -r requirements.txt --quiet
    systemctl restart alarm-platform
    echo "$(date): Update complete"
fi
```

Make executable:
```bash
chmod +x /opt/alarm-platform/update.sh
```

**Windows: C:\Apps\alarm-platform\update.bat**
```batch
@echo off
cd C:\Apps\alarm-platform
git fetch origin main
for /f %%i in ('git rev-parse HEAD') do set LOCAL=%%i
for /f %%i in ('git rev-parse origin/main') do set REMOTE=%%i
if not "%LOCAL%"=="%REMOTE%" (
    echo %date% %time%: Updating...
    git pull origin main
    call venv\Scripts\activate
    pip install -r requirements.txt --quiet
    nssm restart AlarmPlatform
)
```

### Step 6: Set Up Application Service

**Linux - systemd service**

Create `/etc/systemd/system/alarm-platform.service`:
```ini
[Unit]
Description=Alarm Rationalization Platform
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/alarm-platform
ExecStart=/opt/alarm-platform/venv/bin/streamlit run streamlit_app.py
Restart=always
RestartSec=10
Environment=HOME=/opt/alarm-platform

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable alarm-platform
sudo systemctl start alarm-platform
```

**Windows - NSSM Service**

Download NSSM from https://nssm.cc/download, then run as Administrator:
```cmd
nssm install AlarmPlatform
# Configure:
# Path: C:\Apps\alarm-platform\venv\Scripts\streamlit.exe
# Startup directory: C:\Apps\alarm-platform
# Arguments: run streamlit_app.py
nssm start AlarmPlatform
```

### Step 7: Schedule Auto-Updates

**Linux (cron)**
```bash
crontab -e
# Add this line:
*/2 * * * * /opt/alarm-platform/update.sh >> /var/log/alarm-platform-updates.log 2>&1
```

**Windows (Task Scheduler)**
- Open Task Scheduler
- Create Basic Task: "Alarm Platform Auto-Update"
- Trigger: Daily, repeat every 2 minutes
- Action: Start `C:\Apps\alarm-platform\update.bat`

### Step 8: Configure Firewall

**Linux (UFW)**
```bash
sudo ufw allow 8501/tcp
```

**Linux (firewalld)**
```bash
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

**Windows**
```cmd
netsh advfirewall firewall add rule name="Alarm Platform" ^
    dir=in action=allow protocol=tcp localport=8501
```

### Step 9: Verify Installation

1. Check service is running
2. Access the application: `http://your-server:8501`
3. Test login with a configured username/password
4. Test a transformation with sample data

Check service status:
```bash
# Linux
sudo systemctl status alarm-platform

# Windows
nssm status AlarmPlatform
```

---

## Optional: HTTPS with Reverse Proxy

For production, run behind nginx or IIS for SSL/HTTPS.

**nginx example:**
```nginx
server {
    listen 443 ssl;
    server_name alarm-platform.yourcompany.com;

    ssl_certificate /etc/ssl/certs/your-cert.crt;
    ssl_certificate_key /etc/ssl/private/your-key.key;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    location /_stcore/stream {
        proxy_pass http://localhost:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

---

## IT Administration

### User Management

All user credentials are stored in `.streamlit/secrets.toml`

**Add a User**
```bash
# Edit secrets.toml
nano /opt/alarm-platform/.streamlit/secrets.toml

# Add line:
newuser = "NewUserPassword123!"

# Restart service
sudo systemctl restart alarm-platform
```

**Reset a Password**
Edit `secrets.toml`, change the password, restart service.

**Remove a User**
Delete their line from `secrets.toml`, restart service.

**Password Guidelines**
- Minimum 8 characters
- Mix of letters, numbers, symbols
- Unique per user
- Case-sensitive

### Monitoring

| Task | Command (Linux) |
|------|-----------------|
| Start service | `sudo systemctl start alarm-platform` |
| Stop service | `sudo systemctl stop alarm-platform` |
| Restart service | `sudo systemctl restart alarm-platform` |
| Check status | `sudo systemctl status alarm-platform` |
| View app logs | `sudo journalctl -u alarm-platform -f` |
| View update logs | `tail -f /var/log/alarm-platform-updates.log` |
| Force update now | `/opt/alarm-platform/update.sh` |

### Backup

What to backup:

| Item | Location | Frequency |
|------|----------|-----------|
| User passwords | `.streamlit/secrets.toml` | After user changes |
| Server config | `.streamlit/config.toml` | After config changes |

**Note:** Application code and client configurations do not need backup - they're in GitHub.

---

## Troubleshooting

### App Won't Start
- Check Python version: `python3 --version` (need 3.9+)
- Check dependencies: `pip list` (need streamlit, pandas, openpyxl, pyyaml)
- Check logs for errors
- Verify secrets.toml syntax (TOML format - use quotes around passwords)

### Can't Connect
- Check service is running
- Check firewall rules (port 8501)
- Test locally first: `http://localhost:8501`
- Check server IP/hostname is correct

### Login Not Working
- Usernames are case-sensitive
- Passwords need quotes in secrets.toml
- Restart service after changes
- Check for typos in TOML syntax

### Auto-Updates Not Working
- Check server can reach github.com (test with: `git ls-remote origin`)
- Check update script permissions (`chmod +x`)
- Check cron/Task Scheduler is running
- Review `/var/log/alarm-platform-updates.log` for errors

### Configuration Warnings in App
- The app validates client configurations on startup
- Warnings appear in the sidebar under "Config Warning(s)"
- Errors appear under "Config Error(s)" and may block functionality
- Contact developer if configuration issues appear

### Transformation Errors
- Check file encoding (app handles Latin-1, UTF-8, CP1252 automatically)
- Verify file format matches client type (CSV for DynAMo, Excel for ABB)
- Check for required columns in PHA-Pro export
- Use "Preview data before transforming" to check file structure
- Review error message in application
- Use the in-app "Report Issue" button for developer support

---

## Supported Clients (v3.25)

| Client ID | Name | DCS System | PHA-Pro Columns |
|-----------|------|------------|-----------------|
| flng | Freeport LNG | Honeywell Experion/DynAMo | 45 |
| hfs_artesia | HF Sinclair - Artesia | Honeywell Experion/DynAMo | 43 |
| rt_bessemer | Rio Tinto - Bessemer City | ABB 800xA | 23 |

**Note:** New clients can be added by the developer without server changes.

---

## Application Features (v3.25)

### Core Transformations
- Forward transformation: DCS → PHA-Pro import file
- Reverse transformation: PHA-Pro → DCS import file
- Change Report: Excel comparison of original vs rationalized values (all clients)

### Supported Formats
- DynAMo multi-schema CSV parsing (_DCSVariable, _DCS, _Parameter, _Notes)
- ABB 800xA Excel format
- PHA-Pro MADB CSV export

### User Interface Features
- Progress indicators during transformations
- Data preview before transforming
- Transformation history (last 20, re-downloadable)
- Export options: CSV or Excel format
- Configuration validation with warnings/errors display

### Technical Features
- External YAML configuration (no code changes for new clients)
- Automatic encoding detection (UTF-8, Latin-1, CP1252)
- 48 automated tests for reliability
- Structured logging for troubleshooting

### Security Features
- Authentication required (no anonymous access)
- No data storage (files exist only in memory during session)
- No database (nothing saved to server)
- Session isolation (users can't see each other's data)
- HTTPS support via reverse proxy

---

## Quick Reference

### File Locations

| File | Linux | Windows |
|------|-------|---------|
| Application | `/opt/alarm-platform/` | `C:\Apps\alarm-platform\` |
| Main code | `streamlit_app.py` | `streamlit_app.py` |
| Client configs | `config/clients.yaml` | `config\clients.yaml` |
| Server config | `.streamlit/config.toml` | `.streamlit\config.toml` |
| Passwords | `.streamlit/secrets.toml` | `.streamlit\secrets.toml` |
| Update script | `update.sh` | `update.bat` |
| Service file | `/etc/systemd/system/alarm-platform.service` | NSSM service |
| Update log | `/var/log/alarm-platform-updates.log` | `update.log` |

### Common Commands

| Action | Linux | Windows |
|--------|-------|---------|
| Start | `systemctl start alarm-platform` | `nssm start AlarmPlatform` |
| Stop | `systemctl stop alarm-platform` | `nssm stop AlarmPlatform` |
| Restart | `systemctl restart alarm-platform` | `nssm restart AlarmPlatform` |
| Status | `systemctl status alarm-platform` | `nssm status AlarmPlatform` |
| Logs | `journalctl -u alarm-platform -f` | Event Viewer |
| Force update | `/opt/alarm-platform/update.sh` | `update.bat` |

### Health Check

Quick verification checklist:
- [ ] Service is running (`systemctl status` shows active)
- [ ] Web interface loads (`http://server:8501`)
- [ ] Login works with test credentials
- [ ] Client dropdown shows all clients
- [ ] Sample transformation completes successfully

---

## Support Contacts

| Issue Type | Contact |
|------------|---------|
| Application bugs/features | greg.pajak@aesolutions.com |
| New clients/units | greg.pajak@aesolutions.com |
| In-app reporting | Use "Report Issue" button in sidebar |
| Infrastructure (server, network) | Your IT department |
| User passwords | Your IT department |

---

## Version History

| Version | Changes |
|---------|---------|
| 3.25 | Configuration validator, UI improvements |
| 3.24 | Structured logging, transformation history, Excel export, Change Reports for all clients |
| 3.23 | HFS 43-column format, flexible column mapping |
| 3.22 | Unit display refinement |
| 3.21 | Encoding fixes, comma stripping |

---

**Document Version:** 4.0
**Application Version:** 3.25
**Last Updated:** January 2026

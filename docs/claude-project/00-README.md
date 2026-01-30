# Claude Project Knowledge Base Files

## Alarm Rationalization Platform

Upload all files in this folder to your Claude project's knowledge base.

---

## Files Included

| File | Purpose |
|------|---------|
| `00-README.md` | This file - overview |
| `01-DEVELOPER-GUIDE.md` | Architecture, testing, deployment |
| `02-USER-GUIDE.md` | End-user documentation |
| `03-CLIENT-CONFIGURATION-GUIDE.md` | How to add/modify clients |
| `04-DELIVERABLES-CHECKLIST.md` | What to provide for changes |
| `05-CODE-REFERENCE.md` | Key code structures |
| `clients.yaml` | Current client configurations |
| `client_template.yaml` | Template for new clients |

---

## How to Use

### Adding to Claude Project

1. Create or open your Claude project
2. Go to Project Knowledge
3. Upload all `.md` and `.yaml` files from this folder
4. Claude will now have context for the Alarm Rationalization Platform

### Making Requests

When asking Claude to make changes:

1. **Reference the checklist**: "Per the deliverables checklist..."
2. **Provide required info**: Sample files, mappings, etc.
3. **Specify the change type**: Add client, modify rules, fix bug, etc.

### Example Prompts

**Add a new client:**
```
I need to add a new client for [Client Name].
Per the deliverables checklist, here's the information:

Control System: [Honeywell/ABB]
Parser: [dynamo/abb]
[... rest of info ...]

[Attach sample files]
```

**Modify tag source rules:**
```
I need to update tag source rules for [client_id].

Changes:
1. Add rule for point type "XYZ" → "New Source"
2. Modify "ANA" source to "Updated Name"

This follows the format from the client configuration guide.
```

**Add areas:**
```
Add these areas to [client_id]:

- area_id: "unit_50"
  name: "Unit 50 - New Processing"
  description: "New processing unit"
```

---

## Getting Changes Committed

After Claude provides modified files:

1. Copy the YAML content to `config/clients.yaml` in your repo
2. (If Python changes) Copy to `streamlit_app.py`
3. Run tests: `pytest tests/ -v`
4. Commit and push to main branch
5. Streamlit Cloud auto-deploys

---

## Version

These files are for Alarm Rationalization Platform v3.24+
Generated: January 2026

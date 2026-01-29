# Deployment Guide

This project is automatically deployed to Streamlit Cloud. Any push to the `main` branch triggers an automatic redeployment.

## Quick Deploy

### Option 1: Using the Deploy Script (Easiest)

```bash
./deploy.sh
```

This script will:
1. Show your current changes
2. Prompt for a commit message
3. Stage, commit, and push your changes
4. Trigger automatic deployment to Streamlit Cloud

### Option 2: Manual Git Commands

```bash
# 1. Check your changes
git status

# 2. Stage your changes
git add .

# 3. Commit with a message
git commit -m "Your commit message here"

# 4. Push to GitHub (triggers deployment)
git push origin main
```

## How Automatic Deployment Works

### Streamlit Cloud
- **Automatic**: Streamlit Cloud watches your GitHub repository
- **Trigger**: Any push to the `main` branch automatically redeploys
- **Duration**: Typically takes 2-5 minutes
- **URL**: https://alarm-rationalization.streamlit.app

### GitHub Actions
- **Validation**: Runs automatic code validation on every push
- **Checks**:
  - Python syntax validation
  - Import verification
  - Streamlit app structure validation
- **Status**: View at https://github.com/YOUR_REPO/actions

## Deployment Workflow

```
Local Changes
    ↓
git commit & push
    ↓
GitHub Repository (main branch)
    ↓
    ├─→ GitHub Actions (validates code)
    └─→ Streamlit Cloud (auto-deploys)
         ↓
    Live Application Updated
```

## Testing Before Deployment

### Run Locally
```bash
# Start the Streamlit app locally
streamlit run streamlit_app.py
```

Open http://localhost:8501 to test your changes before deploying.

### Validate Code
```bash
# Check Python syntax
python -m py_compile streamlit_app.py

# Test imports
python -c "import streamlit; import pandas; print('✅ Imports OK')"
```

## Common Deployment Scenarios

### Scenario 1: Quick Bug Fix
```bash
# Make your changes in streamlit_app.py
./deploy.sh
# Enter commit message: "Fix unit extraction bug"
# Confirm push: Y
```

### Scenario 2: Adding a New Feature
```bash
# Make your changes
git add streamlit_app.py
git commit -m "Add support for new client XYZ"
git push origin main
```

### Scenario 3: Update Dependencies
```bash
# Edit requirements.txt
git add requirements.txt
git commit -m "Update pandas to 2.1.0"
git push origin main
# Note: Streamlit Cloud will automatically install new dependencies
```

## Monitoring Deployment

### Check Deployment Status

1. **Streamlit Cloud Dashboard**
   - Go to https://share.streamlit.io/
   - Sign in with your GitHub account
   - View deployment logs and status

2. **GitHub Actions**
   - Go to your repository on GitHub
   - Click "Actions" tab
   - View validation workflow runs

3. **Live Application**
   - Visit https://alarm-rationalization.streamlit.app
   - Verify your changes are live
   - Check browser console for errors (F12)

## Rollback a Deployment

If something goes wrong, you can rollback:

```bash
# View recent commits
git log --oneline -5

# Rollback to previous commit
git revert HEAD

# Push the revert
git push origin main
```

Or use Streamlit Cloud dashboard to redeploy a previous version.

## Troubleshooting

### Deployment Failed

1. **Check GitHub Actions**
   - View the Actions tab for error messages
   - Fix the validation errors shown

2. **Check Streamlit Cloud Logs**
   - Go to Streamlit Cloud dashboard
   - View deployment logs for errors

3. **Common Issues**
   - Missing dependencies in requirements.txt
   - Python syntax errors
   - Import errors

### Changes Not Appearing

1. **Hard refresh** the browser: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
2. **Check Streamlit Cloud** dashboard to confirm deployment completed
3. **Wait a few minutes** - deployment can take 2-5 minutes

### GitHub Actions Failing

1. **View the error** in the Actions tab
2. **Fix locally** and test with `python -m py_compile streamlit_app.py`
3. **Push the fix** to trigger a new validation run

## Development Best Practices

### Before Deploying
- [ ] Test changes locally with `streamlit run streamlit_app.py`
- [ ] Validate Python syntax
- [ ] Test with sample files
- [ ] Check browser console for errors

### Commit Messages
Use clear, descriptive commit messages:
- ✅ "Fix unit extraction for FLNG tags with special characters"
- ✅ "Add support for ABB 800xA reverse transformation"
- ❌ "fix bug"
- ❌ "update"

### Branch Strategy
- `main` - Production branch (auto-deploys to Streamlit Cloud)
- `develop` - Development branch (optional, for testing)

Create feature branches for major changes:
```bash
git checkout -b feature/new-client-support
# Make changes
git commit -m "Add support for Client XYZ"
# When ready, merge to main
git checkout main
git merge feature/new-client-support
git push origin main
```

## Environment Variables

If you need to add secrets or environment variables:

1. Go to Streamlit Cloud dashboard
2. Select your app
3. Click "Settings" → "Secrets"
4. Add secrets in TOML format:
   ```toml
   API_KEY = "your-secret-key"
   ```
5. Access in code: `st.secrets["API_KEY"]`

## Emergency Contacts

- **Streamlit Cloud Support**: https://docs.streamlit.io/
- **GitHub Support**: https://support.github.com/

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./deploy.sh` | Quick deploy with prompts |
| `git status` | Check current changes |
| `git log` | View commit history |
| `git push origin main` | Deploy to production |
| `streamlit run streamlit_app.py` | Test locally |

---

**Remember**: Every push to `main` = Automatic deployment to production!

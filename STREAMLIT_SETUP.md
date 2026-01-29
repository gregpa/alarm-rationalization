# Streamlit Cloud Setup Guide

Your app is ready to deploy! Follow these steps to connect it to Streamlit Cloud.

## Step 1: Sign in to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "Sign in" (top right)
3. Sign in with your GitHub account (gregpa)

## Step 2: Deploy Your App

1. Click "New app" button
2. Select your repository: `gregpa/alarm-rationalization`
3. Set the branch: `main`
4. Set the main file path: `streamlit_app.py`
5. Click "Deploy!"

## Step 3: Wait for Deployment

- First deployment takes 2-5 minutes
- You'll see a build log showing progress
- When complete, your app will be live at: https://alarm-rationalization.streamlit.app

## Troubleshooting

### "Redirected too many times" Error
This means the app isn't deployed yet. Complete steps 1-3 above to deploy it.

### Build Fails
- Check the build logs on Streamlit Cloud
- Verify all dependencies are in requirements.txt
- Make sure Python version is compatible (3.11)

### App Won't Start
- Check for syntax errors: `python -m py_compile streamlit_app.py`
- Test locally: `streamlit run streamlit_app.py`
- Review Streamlit Cloud logs for error messages

## After Initial Setup

Once deployed, any push to the `main` branch will automatically redeploy your app:

```bash
# Make your changes
./deploy.sh

# Or manually
git add .
git commit -m "Your changes"
git push origin main
```

Streamlit Cloud will detect the push and redeploy automatically!

## Settings (Optional)

In Streamlit Cloud dashboard, you can:
- Add secrets (Settings → Secrets)
- Change Python version
- Configure custom domains
- View deployment logs
- Reboot or delete the app

## Need Help?

- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Forum: https://discuss.streamlit.io/

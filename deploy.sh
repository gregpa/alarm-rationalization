#!/bin/bash

# Alarm Rationalization - Quick Deploy Script
# Commits changes and pushes to GitHub, triggering automatic Streamlit Cloud deployment

set -e  # Exit on error

echo "🔔 Alarm Rationalization - Deploy to Production"
echo "================================================"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Check current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current branch: $BRANCH"
echo ""

# Show git status
echo "📊 Current changes:"
git status --short
echo ""

# Check if there are any changes
if git diff-index --quiet HEAD --; then
    echo "ℹ️  No changes to commit"
    echo ""
    read -p "Do you want to push anyway? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✋ Deployment cancelled"
        exit 0
    fi
else
    # Ask for commit message
    echo "💬 Enter commit message (or press Ctrl+C to cancel):"
    read -r COMMIT_MSG

    if [ -z "$COMMIT_MSG" ]; then
        echo "❌ Commit message cannot be empty"
        exit 1
    fi

    # Stage all changes
    echo ""
    echo "📦 Staging changes..."
    git add .

    # Create commit
    echo "💾 Creating commit..."
    git commit -m "$COMMIT_MSG"
    echo "✅ Commit created"
    echo ""
fi

# Confirm push
echo "🚀 Ready to push to GitHub and deploy to Streamlit Cloud"
echo "   Branch: $BRANCH"
echo "   Remote: origin"
echo ""
read -p "Continue with deployment? (Y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "✋ Deployment cancelled"
    exit 0
fi

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push origin "$BRANCH"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📡 GitHub Actions will validate your code"
echo "🌐 Streamlit Cloud will automatically redeploy your app"
echo "🔗 Live URL: https://alarm-rationalization.streamlit.app"
echo ""
echo "You can monitor deployment at:"
echo "   GitHub Actions: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"
echo "   Streamlit Cloud: https://share.streamlit.io/"
echo ""

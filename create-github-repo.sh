#!/bin/bash

# GitHub repository creation script for MailMind

echo "Creating GitHub repository for MailMind..."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed. Please install it first:"
    echo "brew install gh"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Please authenticate with GitHub CLI first:"
    echo "gh auth login"
    exit 1
fi

# Create repository
gh repo create MailMind \
    --description "Intelligent Email Client with RAG Implementation" \
    --public \
    --clone=false

# Add remote origin
git remote add origin https://github.com/$(gh api user --jq .login)/MailMind.git

# Push to GitHub
git push -u origin master

echo "Repository created and pushed successfully!"
echo "Visit: https://github.com/$(gh api user --jq .login)/MailMind"

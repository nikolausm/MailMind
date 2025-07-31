#!/bin/bash

# Setup GitHub for MailMind project

echo "Setting up GitHub repository for MailMind..."

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d ".git" ]; then
    echo "Error: Please run this script from the MailMind project root"
    exit 1
fi

# Instructions for manual setup
echo "To set up the GitHub repository, please follow these steps:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'MailMind'"
echo "3. Set description: 'Intelligent Email Client with RAG Implementation'"
echo "4. Choose Public or Private"
echo "5. Do NOT initialize with README, .gitignore, or license"
echo ""
echo "After creating the repository, run these commands:"
echo ""
echo "git remote add origin https://github.com/YOUR_USERNAME/MailMind.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "Replace YOUR_USERNAME with your GitHub username"

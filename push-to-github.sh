#!/bin/bash

echo "========================================"
echo "Push Agentcore Demo to GitHub"
echo "========================================"
echo ""

read -p "Enter your GitHub username: " username

if [ -z "$username" ]; then
    echo "ERROR: Username cannot be empty"
    exit 1
fi

echo ""
echo "Setting up remote repository..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/$username/agentcore-memory-demo.git

echo ""
echo "Renaming branch to main..."
git branch -M main

echo ""
echo "Pushing to GitHub..."
if git push -u origin main; then
    echo ""
    echo "========================================"
    echo "Success! Repository pushed to:"
    echo "https://github.com/$username/agentcore-memory-demo"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Push failed! Please check:"
    echo "1. Repository exists on GitHub"
    echo "2. You have access permissions"
    echo "3. GitHub credentials are configured"
    echo "========================================"
    echo ""
    echo "To create the repository:"
    echo "1. Go to: https://github.com/new"
    echo "2. Name: agentcore-memory-demo"
    echo "3. Don't initialize with README"
    echo "4. Click Create"
    echo "5. Run this script again"
    echo "========================================"
fi

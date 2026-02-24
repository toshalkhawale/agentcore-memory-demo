# GitHub Authentication Guide

## Create Personal Access Token (PAT)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Agentcore Demo"
4. Select scopes:
   - ✅ repo (all)
   - ✅ workflow
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)

## Use Token to Push

```bash
# When prompted for password, paste your token instead
git push -u origin main

Username: toshalkhawale
Password: [paste your token here]
```

## Or Set Token in Remote URL

```bash
# Remove old remote
git remote remove origin

# Add with token
git remote add origin https://toshalkhawale:YOUR_TOKEN@github.com/toshalkhawale/agentcore-memory-demo.git

# Push
git push -u origin main
```

## Alternative: Use GitHub CLI

```bash
# Install GitHub CLI: https://cli.github.com/
gh auth login
git push -u origin main
```

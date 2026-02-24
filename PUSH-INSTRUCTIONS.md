# Manual Push Instructions

## The Error
The 403 error means either:
1. The repository doesn't exist on GitHub
2. The token doesn't have the right permissions
3. The repository is private and token lacks access

## Solution: Push Manually

### Step 1: Verify Repository Exists
Go to: https://github.com/toshalkhawale/agentcore-memory-demo

If it doesn't exist or shows 404, create it:
- Go to: https://github.com/new
- Name: `agentcore-memory-demo`
- Visibility: **Public** (important!)
- Don't initialize with README
- Click "Create repository"

### Step 2: Create New Token with Correct Permissions
1. Go to: https://github.com/settings/tokens/new
2. Note: `Agentcore Demo`
3. Expiration: 90 days
4. **Important**: Check these scopes:
   - ✅ **repo** (all sub-items)
   - ✅ **workflow**
5. Generate token and copy it

### Step 3: Push Using Command Line

Open PowerShell or Git Bash in the project folder and run:

```bash
cd agentcore-memory-demo

# Remove old remote
git remote remove origin

# Add new remote with your token
git remote add origin https://toshalkhawale:YOUR_NEW_TOKEN@github.com/toshalkhawale/agentcore-memory-demo.git

# Push
git push -u origin main
```

### Alternative: Use GitHub Desktop
1. Download GitHub Desktop: https://desktop.github.com/
2. File → Add Local Repository
3. Choose: agentcore-memory-demo folder
4. Click "Publish repository"
5. Sign in with your GitHub account

### Alternative: Use GitHub CLI
```bash
# Install: https://cli.github.com/
gh auth login
cd agentcore-memory-demo
git push -u origin main
```

## Verify Success
After pushing, visit:
https://github.com/toshalkhawale/agentcore-memory-demo

You should see all your files!

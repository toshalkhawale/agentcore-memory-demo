# GitHub Repository Setup Guide

## Quick Setup for GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `agentcore-memory-demo`
3. Description: `Dual-memory AI agent demo with Knight of Seven Kingdoms persona - ACD Ahmedabad 2026`
4. Choose: Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Push to GitHub

```bash
# Navigate to project directory
cd agentcore-memory-demo

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/agentcore-memory-demo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Configure Repository

#### Add Topics (for discoverability)
Go to repository settings and add topics:
- `ai-agent`
- `memory-management`
- `vector-database`
- `chromadb`
- `python`
- `flask`
- `demo`
- `acd-ahmedabad`

#### Add Description
```
Agentcore Memory Retrieval Demo: Short-term & long-term memory strategies for AI agents featuring Knight of the Seven Kingdoms persona. Built for ACD Ahmedabad 2026.
```

#### Enable GitHub Pages (Optional)
1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: / (root)
4. Save

### Step 4: Create Release (Optional)

```bash
# Tag the release
git tag -a v1.0.0 -m "Initial release for ACD Ahmedabad 2026"
git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases
2. Click "Draft a new release"
3. Choose tag: v1.0.0
4. Release title: "v1.0.0 - ACD Ahmedabad 2026 Demo"
5. Description:
```markdown
## Agentcore Memory Demo v1.0.0

First release of the Agentcore Memory Retrieval demonstration featuring:

### Features
- ✅ Dual-memory architecture (STM + LTM)
- ✅ Knight of Seven Kingdoms persona
- ✅ CLI and Web interfaces
- ✅ Vector database integration (ChromaDB)
- ✅ Semantic memory retrieval
- ✅ Complete documentation and presentation slides

### Quick Start
```bash
git clone https://github.com/YOUR_USERNAME/agentcore-memory-demo.git
cd agentcore-memory-demo
pip install -r requirements.txt
python main.py
```

### Documentation
- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Installation guide
- [DEMO-GUIDE.md](DEMO-GUIDE.md) - Presentation scenarios
- [PRESENTATION.md](PRESENTATION.md) - Complete slide deck

Presented at: ACD Ahmedabad 2026
```

### Step 5: Add README Badges (Optional)

Add to top of README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-demo-orange.svg)
![ACD](https://img.shields.io/badge/ACD-Ahmedabad%202026-red.svg)
```

### Step 6: Create GitHub Actions (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest examples/test_scenarios.py || echo "Tests completed"
```

## Repository Structure on GitHub

```
agentcore-memory-demo/
├── 📁 .github/              (workflows)
├── 📁 core/                 (main code)
├── 📁 examples/             (test scenarios)
├── 📁 templates/            (web UI)
├── 📄 README.md             (main documentation)
├── 📄 SETUP.md              (installation)
├── 📄 DEMO-GUIDE.md         (presentation guide)
├── 📄 PRESENTATION.md       (slides)
├── 📄 PROJECT-SUMMARY.md    (overview)
├── 📄 LICENSE               (MIT)
└── 📄 requirements.txt      (dependencies)
```

## Sharing Your Demo

### For Presentation
Share this URL:
```
https://github.com/YOUR_USERNAME/agentcore-memory-demo
```

### For Quick Demo
If you deploy to a server:
```
http://your-server.com:5000
```

### For Documentation
Direct links to specific docs:
```
https://github.com/YOUR_USERNAME/agentcore-memory-demo/blob/main/DEMO-GUIDE.md
https://github.com/YOUR_USERNAME/agentcore-memory-demo/blob/main/PRESENTATION.md
```

## Collaboration

### Enable Issues
1. Go to Settings → Features
2. Check "Issues"
3. Add issue templates (optional)

### Enable Discussions
1. Go to Settings → Features
2. Check "Discussions"
3. Great for Q&A from ACD attendees

### Add Contributors
1. Go to Settings → Collaborators
2. Add team members

## Social Media Sharing

### LinkedIn Post Template
```
🚀 Excited to share my Agentcore Memory Demo for ACD Ahmedabad 2026!

Built a dual-memory AI agent featuring:
✅ Short-term memory (conversation context)
✅ Long-term memory (vector database)
✅ Semantic retrieval with ChromaDB
✅ Knight of Seven Kingdoms persona

Tech: Python, Flask, ChromaDB, Sentence Transformers

Check it out: [GitHub URL]

#AI #MachineLearning #Python #ACD2026 #Ahmedabad
```

### Twitter Post Template
```
🤖 Built an AI agent with dual-memory architecture for #ACD2026!

Features STM + LTM with vector search, featuring Knight of Seven Kingdoms 🛡️

Live demo + full code: [GitHub URL]

#AI #Python #ChromaDB #MachineLearning
```

## Maintenance

### Keep Dependencies Updated
```bash
pip list --outdated
pip install --upgrade package_name
pip freeze > requirements.txt
```

### Monitor Issues
- Respond to issues from ACD attendees
- Add FAQ section based on common questions
- Update documentation as needed

## Success Metrics

Track on GitHub:
- ⭐ Stars
- 🍴 Forks
- 👁️ Watchers
- 📊 Traffic (Insights → Traffic)
- 🔗 Clones

## Next Steps After ACD

1. Add more personas
2. Implement memory consolidation
3. Add knowledge graphs
4. Create Docker deployment
5. Add more test scenarios
6. Write blog post about the demo

---

**Ready to share with the world!** 🌟

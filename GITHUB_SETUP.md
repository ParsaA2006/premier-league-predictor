# Adding Project to GitHub

## Step-by-Step Guide

### Step 1: Create a GitHub Repository

1. Go to https://github.com and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Name it: `Premier-League-Project` (or any name you prefer)
4. **DO NOT** check "Initialize this repository with a README" (we already have files)
5. Click **"Create repository"**
6. Copy the repository URL (it will look like: `https://github.com/yourusername/Premier-League-Project.git`)

### Step 2: Initialize Git Locally

Open your terminal in the project folder and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Premier League Predictor with AI/ML"

# Add your GitHub repository as remote (replace with your actual URL)
git remote add origin https://github.com/yourusername/Premier-League-Project.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: That's It!

Your code is now on GitHub! 🎉

---

## Alternative: Using GitHub CLI (if installed)

If you have GitHub CLI installed:

```bash
git init
git add .
git commit -m "Initial commit: Premier League Predictor with AI/ML"
gh repo create Premier-League-Project --public --source=. --remote=origin --push
```

---

## Important Notes

### What's Already Excluded (in .gitignore)
- Virtual environments (`venv/`)
- Database files (`.db`, `.sqlite`)
- Trained models (`*.pkl`)
- Environment files (`.env`)
- Node modules (`node_modules/`)
- Build files (`dist/`, `build/`)

### What Gets Pushed
- ✅ All source code
- ✅ Configuration files
- ✅ Documentation
- ✅ Requirements files

### What Doesn't Get Pushed (important!)
- ❌ `.env` file with API keys (keep this private!)
- ❌ Trained models (users can train their own)
- ❌ Virtual environments
- ❌ Database files

---

## Updating Your Repository

After making changes:

```bash
git add .
git commit -m "Description of your changes"
git push
```

---

## Adding a License (Optional)

You might want to add a LICENSE file. Common options:
- MIT License (most permissive)
- Apache 2.0
- GPL v3

---

## Adding a Badge to README (Optional)

You can add badges to your README.md to show:
- Build status
- Python version
- License

Example:
```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-blue.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
```


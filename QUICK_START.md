# Quick Start Guide

## ✅ What's Ready

1. **GitHub Actions Workflow** - Ready to add (see GITHUB_ACTIONS_SETUP.md)
2. **Landing Page** - Live at https://smic-gcsu.github.io/ with download links
3. **Build Scripts** - Ready for local builds
4. **Data Packaging** - transaction.csv will be included automatically

## 🚀 To Enable Automated Builds

### Step 1: Add Workflow File
1. Go to: https://github.com/SMIC-GCSU/portfolio
2. Click "Add file" → "Create new file"
3. Path: `.github/workflows/build-release.yml`
4. Copy content from: `.github/workflows/build-release.yml` (in your local repo)
5. Commit

### Step 2: Create First Release
```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will automatically:
- ✅ Build Windows .exe
- ✅ Build macOS .app
- ✅ Create GitHub Release
- ✅ Upload both files

### Step 3: Downloads Go Live
- Landing page: https://smic-gcsu.github.io/
- Download links will work automatically
- Status indicators show availability

## 📦 What Gets Built

**Windows:**
- File: `SMIC_Portfolio_Analysis.exe`
- Includes: All dependencies + transaction.csv
- Publisher: Joel Saucedo - GCSU SMIC Managing Director

**macOS:**
- File: `SMIC_Portfolio_Analysis_macos.zip`
- Includes: Application bundle + transaction.csv
- Publisher: Joel Saucedo - GCSU SMIC Managing Director

## 🔗 Download URLs (After Release)

- Windows: `https://github.com/SMIC-GCSU/portfolio/releases/latest/download/SMIC_Portfolio_Analysis.exe`
- macOS: `https://github.com/SMIC-GCSU/portfolio/releases/latest/download/SMIC_Portfolio_Analysis_macos.zip`

These are already embedded in the landing page!


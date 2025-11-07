# Setup Instructions

## ✅ What's Been Completed

1. **All website files removed** from portfolio repository
2. **Landing page created** at https://smic-gcsu.github.io/ with download links prominently displayed
3. **Executable packaging configured** with proper metadata:
   - Publisher: Joel Saucedo - GCSU Student Managed Investment Committee Managing Director
   - Copyright: Copyright (C) 2024-2025 Joel Saucedo, GCSU Student Managed Investment Committee
   - transaction.csv included in all distributions
4. **Build scripts created** for Windows and macOS

## 🔧 Manual Steps Required

### 1. Add GitHub Actions Workflow

The workflow file needs to be added manually through GitHub's web interface:

1. Go to: https://github.com/SMIC-GCSU/portfolio
2. Click "Add file" > "Create new file"
3. Path: `.github/workflows/build-release.yml`
4. Copy the content from the file in your local repo: `.github/workflows/build-release.yml`
5. Commit the file

### 2. Build Executables Locally (Optional)

**Windows:**
```bash
build_windows.bat
```

**macOS:**
```bash
./build_macos.sh
```

### 3. Create First Release

Once the workflow is added:

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will automatically:
- Build Windows executable
- Build macOS application
- Create a GitHub Release
- Make download links available

### 4. Download Links

The landing page at https://smic-gcsu.github.io/ will automatically link to:
- Windows: `https://github.com/SMIC-GCSU/portfolio/releases/latest/download/SMIC_Portfolio_Analysis.exe`
- macOS: `https://github.com/SMIC-GCSU/portfolio/releases/latest/download/SMIC_Portfolio_Analysis_macos.zip`

## 📋 Metadata Included

All executables include:
- **Publisher:** Joel Saucedo - GCSU Student Managed Investment Committee Managing Director
- **Copyright:** Copyright (C) 2024-2025 Joel Saucedo, GCSU Student Managed Investment Committee. All rights reserved.
- **Company:** GCSU Student Managed Investment Committee
- **transaction.csv** data file
- **GitHub repository** information

## 🌐 Landing Page

The landing page is live at: https://smic-gcsu.github.io/

Features:
- Download links prominently displayed (blue highlighted text)
- Publisher and copyright information
- Installation instructions
- GitHub repository link
- Feature descriptions


# Building and Distributing SMIC Portfolio Analysis

## Quick Start

**Windows:**
```bash
build_windows.bat
```

**macOS:**
```bash
./build_macos.sh
```

## Prerequisites

- Python 3.10 or higher
- All dependencies from `requirements.txt`
- PyInstaller: `pip install pyinstaller`

## Build Process

### Windows Build

The build script (`build_windows.bat`) will:
1. Verify `data/transactions.csv` exists
2. Clean previous builds
3. Build executable with proper metadata
4. Output: `dist/SMIC_Portfolio_Analysis.exe`

### macOS Build

The build script (`build_macos.sh`) will:
1. Verify `data/transactions.csv` exists
2. Clean previous builds
3. Build application bundle
4. Output: `dist/SMIC Portfolio Analysis.app`

## Included in Distribution

- Application executable/bundle
- All Python dependencies
- `data/transactions.csv` file (automatically included)
- Publisher metadata: Joel Saucedo - GCSU SMIC Managing Director
- Copyright: Copyright (C) 2024-2025 Joel Saucedo, GCSU Student Managed Investment Committee

## Creating a GitHub Release

1. Tag the release: `git tag v1.0.0`
2. Push the tag: `git push origin v1.0.0`
3. GitHub Actions will automatically build and create a release
4. Download links will be available on the landing page: https://smic-gcsu.github.io/

## Manual Build (Alternative)

**Windows:**
```bash
pyinstaller SMIC_Portfolio_Analysis.spec --clean
```

**macOS:**
```bash
python3 -m PyInstaller SMIC_Portfolio_Analysis_macos.spec --clean
cd dist
zip -r SMIC_Portfolio_Analysis_macos.zip "SMIC Portfolio Analysis.app"
```

## Troubleshooting

### Data file not found
- Ensure `data/transactions.csv` exists before building
- The spec files automatically include the data directory

### Build fails
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify PyInstaller is installed: `pip install pyinstaller`


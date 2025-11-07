#!/bin/bash
# Script to help build executables via GitHub Actions

echo "=========================================="
echo "SMIC Portfolio Analysis - Build Executables"
echo "=========================================="
echo ""

# Check if workflow exists on GitHub
if gh workflow list 2>/dev/null | grep -q "Build and Release"; then
    echo "✓ Workflow found on GitHub!"
    echo ""
    echo "Triggering build..."
    gh workflow run "Build and Release Executables" --ref main
    echo ""
    echo "Build triggered! Check status at:"
    echo "https://github.com/SMIC-GCSU/portfolio/actions"
else
    echo "⚠ Workflow not found on GitHub yet."
    echo ""
    echo "STEP 1: Add the workflow file"
    echo "----------------------------------------"
    echo "1. Open: https://github.com/SMIC-GCSU/portfolio/new/main?filename=.github/workflows/build-release.yml"
    echo "2. Copy content from: .github/workflows/build-release.yml"
    echo "3. Paste and commit"
    echo ""
    echo "STEP 2: Run this script again, or:"
    echo "  git push origin v1.0.0"
    echo ""
fi

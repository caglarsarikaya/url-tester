#!/bin/bash
# Build script for URL Tester executable (Linux/Mac)
# Optimized for minimal size

echo "======================================"
echo " Building URL Tester Executable"
echo "======================================"
echo

# Check if PyInstaller is installed
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "[ERROR] PyInstaller not found. Installing..."
    pip install pyinstaller
    echo
fi

# Clean previous build
echo "[1/3] Cleaning previous build..."
rm -rf build dist url_tester
echo "[OK] Clean complete"
echo

# Build executable
echo "[2/3] Building executable (this may take a few minutes)..."
pyinstaller build_config.spec --clean
echo "[OK] Build complete"
echo

# Copy to root directory
echo "[3/3] Copying executable to root directory..."
if [ -f "dist/url_tester" ]; then
    cp "dist/url_tester" "url_tester"
    chmod +x "url_tester"
    echo "[OK] url_tester created successfully!"
else
    echo "[ERROR] Build failed - executable not found"
    exit 1
fi

echo
echo "======================================"
echo " Build Complete!"
echo "======================================"
echo
echo "File: url_tester"
if [ -f "url_tester" ]; then
    ls -lh url_tester | awk '{print "Size:", $5}'
fi
echo
echo "To reduce size further:"
echo "- Install UPX: sudo apt install upx (Ubuntu) or brew install upx (Mac)"
echo "- Rebuild with: pyinstaller build_config.spec"
echo


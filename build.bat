@echo off
REM Build script for URL Tester executable
REM Optimized for minimal size

echo ======================================
echo  Building URL Tester Executable
echo ======================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Clean previous build
echo [1/3] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "url_tester.exe" del /q "url_tester.exe"
echo [OK] Clean complete
echo.

REM Build executable
echo [2/3] Building executable (this may take a few minutes)...
echo [INFO] Some warnings are normal and can be ignored
echo.
pyinstaller build_config.spec --clean 2>&1 | findstr /V "WARNING: Failed to run strip"
if errorlevel 1 (
    echo [WARNING] Build completed with some warnings (this is normal^)
) else (
    echo [OK] Build complete
)
echo.

REM Copy to root directory
echo [3/3] Copying executable to root directory...
if exist "dist\url_tester.exe" (
    copy "dist\url_tester.exe" "url_tester.exe"
    echo [OK] url_tester.exe created successfully!
) else (
    echo [ERROR] Build failed - executable not found
    pause
    exit /b 1
)

echo.
echo ======================================
echo  Build Complete!
echo ======================================
echo.
echo File: url_tester.exe
if exist "url_tester.exe" (
    for %%A in ("url_tester.exe") do echo Size: %%~zA bytes
)
echo.
echo To reduce size further:
echo - Install UPX: https://upx.github.io/
echo - Place upx.exe in PATH or same folder
echo - Rebuild with: pyinstaller build_config.spec
echo.
pause


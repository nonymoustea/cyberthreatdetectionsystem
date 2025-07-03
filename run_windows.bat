@echo off
title AI Email Threat Detector
echo.
echo ============================================
echo   🛡️  AI Email Threat Detector
echo ============================================
echo.

REM Set error handling
setlocal EnableDelayedExpansion

REM Check if Python is installed
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found: !PYTHON_VERSION!

REM Check if required files exist
if not exist "app.py" (
    echo ❌ app.py not found in current directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)

echo ✅ Required files found
echo 📦 Installing/updating dependencies...
echo.

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

REM Install dependencies with Windows-specific approach
echo Installing Python packages (Windows optimized)...

REM First try Windows-specific requirements if available
if exist "requirements_windows.txt" (
    echo Using Windows-optimized requirements...
    pip install --user -r requirements_windows.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Windows-optimized dependencies
        goto :try_regular_requirements
    )
    echo ✅ Windows-optimized packages installed
    goto :dependencies_done
)

:try_regular_requirements
echo Using standard requirements...
pip install --user -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install some dependencies
    echo This might be due to Windows-specific package issues
    echo Trying alternative installation method...
    echo.
    
    REM Try installing without problematic packages first
    pip install --user pandas scikit-learn joblib Flask Werkzeug Pillow
    if %errorlevel% neq 0 (
        echo ❌ Critical dependencies failed to install
        echo Please check your Python installation
        pause
        exit /b 1
    )
    
    REM Try installing remaining packages individually
    echo Installing additional packages...
    pip install --user pdfminer.six
    pip install --user pytesseract
    
    REM Skip python-magic and libmagic on Windows as they can be problematic
    echo ⚠️  Note: Some file type detection features may be limited on Windows
)

:dependencies_done
echo.
echo ✅ Dependencies installed successfully
echo 🚀 Starting AI Email Threat Detector...
echo.
echo 📡 Navigate to: http://localhost:5050
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Create uploads directory if it doesn't exist
if not exist "uploads" (
    mkdir uploads
    echo ✅ Created uploads directory
)

REM Start the Flask application
echo Starting server...
python app.py

echo.
echo 🛑 Server stopped
echo Press any key to exit...
pause >nul 
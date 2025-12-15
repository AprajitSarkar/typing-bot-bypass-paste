@echo off
echo ========================================
echo TypingBot - EXE Builder
echo ========================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python is installed
echo.

REM Check if pip is installed
echo [2/5] Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed
    echo Please install pip
    pause
    exit /b 1
)
echo [OK] pip is installed
echo.

REM Install required packages
echo [3/5] Installing required dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check if PyInstaller is installed, install if not
echo [4/5] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller is ready
echo.

REM Build EXE
echo [5/5] Building EXE file...
echo This may take a few minutes...
pyinstaller --onefile --windowed --name "TypingBot" --icon=NONE ^
    --add-data "requirements.txt;." ^
    floating_typing_bot.py

if %errorlevel% neq 0 (
    echo [ERROR] Failed to build EXE
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] EXE file created successfully!
echo ========================================
echo.
echo Location: dist\TypingBot.exe
echo.
echo You can now run the application by double-clicking TypingBot.exe
echo.
pause

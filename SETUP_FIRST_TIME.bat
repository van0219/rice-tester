@echo off
echo ========================================
echo RICE Tester - First Time Setup
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Testing installation...
python -c "import matplotlib, numpy, pandas, rich, selenium" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies may not be installed correctly.
    echo Please run this setup again if you encounter issues.
)

echo.
echo ✅ Setup complete! You can now run RICE Tester.
echo.
echo To start RICE Tester, run: python RICE_Tester.py
echo Or use: RUN_RICE_TESTER.bat
echo.
pause
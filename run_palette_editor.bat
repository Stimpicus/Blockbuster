@echo off
REM Launch script for Character Palette Editor on Windows

set SCRIPT_DIR=%~dp0

REM Check if Python 3 is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python 3 is not installed
    echo Please install Python 3.9 or later to run this application
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "%SCRIPT_DIR%venv" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%venv"
)

REM Activate virtual environment
call "%SCRIPT_DIR%venv\Scripts\activate.bat"

REM Check if dependencies are installed
python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r "%SCRIPT_DIR%requirements.txt"
)

REM Launch the application
echo Launching Character Palette Editor...
python "%SCRIPT_DIR%palette_editor.py"

REM Deactivate virtual environment
call deactivate

pause

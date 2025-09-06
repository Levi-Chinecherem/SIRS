@echo off
setlocal

REM === Move to the folder where the script is located ===
cd /d "%~dp0"

set VENV_DIR=.venv
set PYTHON=%VENV_DIR%\Scripts\python.exe
set PIP=%VENV_DIR%\Scripts\pip.exe

REM === 1. Check if venv exists, else create it ===
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    py -m venv %VENV_DIR%
)

REM === 2. Install requirements ===
echo Installing requirements...
"%PIP%" install --upgrade pip >nul
if exist requirements.txt (
    "%PIP%" install -r requirements.txt --timeout 6000
)

REM === 3. Start Django server in background ===
echo Starting Django server...
start "" /b "%PYTHON%" manage.py runserver

REM === 4. Wait until server is up ===
:waitloop
ping 127.0.0.1 -n 2 >nul
curl -s http://127.0.0.1:8000/dashboard >nul 2>&1
if errorlevel 1 (
    goto waitloop
)

REM === 5. Beep twice to signal ready ===
echo [char]7
echo [char]7

REM === 6. Open browser ===
start http://127.0.0.1:8000

REM === 7. Wait for user to close browser (simple way: wait until all browsers closed) ===
:checkbrowser
tasklist | findstr /i "chrome.exe firefox.exe msedge.exe" >nul
if not errorlevel 1 (
    timeout /t 3 >nul
    goto checkbrowser
)

REM === 8. Kill Django server ===
echo Stopping Django server...
taskkill /im python.exe /f >nul 2>&1

endlocal
exit

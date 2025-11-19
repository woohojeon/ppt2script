@echo off
echo Checking for LibreOffice installation...
echo.

REM Check common installation paths
set LIBREOFFICE_FOUND=0

if exist "C:\Program Files\LibreOffice\program\soffice.exe" (
    echo [OK] Found LibreOffice at: C:\Program Files\LibreOffice\program\soffice.exe
    set LIBREOFFICE_FOUND=1
)

if exist "C:\Program Files (x86)\LibreOffice\program\soffice.exe" (
    echo [OK] Found LibreOffice at: C:\Program Files ^(x86^)\LibreOffice\program\soffice.exe
    set LIBREOFFICE_FOUND=1
)

REM Check in PATH
where soffice >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] LibreOffice found in PATH
    where soffice
    set LIBREOFFICE_FOUND=1
)

where libreoffice >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] LibreOffice found in PATH
    where libreoffice
    set LIBREOFFICE_FOUND=1
)

echo.
if %LIBREOFFICE_FOUND% EQU 1 (
    echo LibreOffice is installed and ready to use!
    echo You can now run: python web_app.py
) else (
    echo [ERROR] LibreOffice not found!
    echo Please install LibreOffice from: https://www.libreoffice.org/download/download-libreoffice/
    echo After installation, you may need to restart your command prompt.
)

echo.
pause

@echo off
echo Setting up environment...
set PATH=%PATH%;C:\Users\krisg\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts

echo Building the executable with PyInstaller...

pyinstaller --onefile --windowed --name "Omega Verksted" --icon "./ov_logo.ico" --add-data "./ov_logo.ico;." "./main.py"

if %ERRORLEVEL% neq 0 (
    echo Build process failed.
    pause
    exit /b
) else (
    echo Build process complete.
)

pause

@echo off
echo Setting up environment...
set "PATH=%PATH%;C:\Users\krisg\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts"

echo Cleaning up previous builds...
rd /s /q build
rd /s /q dist
del /q *.spec

echo Creating a new virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install pyinstaller pystray pillow requests

echo Building the executable with PyInstaller...
pyinstaller --onefile --windowed --name "Omega Verksted" --icon "./ov_logo.ico" --add-data "./ov_logo.ico;." --version-file "./version.txt" "./main.py" --hidden-import pystray --hidden-import PIL --hidden-import requests

if %ERRORLEVEL% neq 0 (
    echo Build process failed.
    pause
    exit /b
) else (
    echo Build process complete.
)

pause

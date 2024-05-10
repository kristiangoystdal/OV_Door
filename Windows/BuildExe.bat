@echo off
echo Setting up environment...
set PATH=%PATH%;C:\Users\krisg\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts

echo Building the executable with PyInstaller...
pyinstaller --clean --noupx --windowed --icon="C:\Users\krisg\Documents\Git\OV_Door\Windows\ov_logo.ico" --name="Omega Verksted" ov_door.py

echo Build process complete.

echo Compressing the dist folder...
PowerShell -Command "Compress-Archive -Path '.\dist\Omega Verksted\*' -DestinationPath '.\Omega_Verksted.zip'"

echo Compression complete.
pause

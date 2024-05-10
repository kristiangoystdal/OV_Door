@echo off
echo Setting up environment...
set PATH=%PATH%;C:\Users\krisg\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts

echo Building the executable with PyInstaller...
pyinstaller --clean --onefile --noupx --windowed --icon="C:\Users\krisg\Documents\Git\OV_Door\Windows\ov_logo.ico" --name="installer_omega_verksted" installer.py

@REM echo Building the executable with PyInstaller...
@REM pyinstaller --clean --onefile --noupx --windowed --icon="C:\Users\krisg\Documents\Git\OV_Door\Windows\ov_logo.ico" --name="uninstaller" uninstaller.py

echo Build process complete.

pause
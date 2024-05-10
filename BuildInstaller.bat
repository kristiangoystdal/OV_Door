@echo off
echo Setting up environment...
set PATH=%PATH%;C:\Users\krisg\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts

echo Building the executable with PyInstaller...
pyinstaller --clean --onefile --noupx --windowed --add-data="C:\Users\krisg\Documents\Git\OV_Door\ov_logo.ico;." --icon="C:\Users\krisg\Documents\Git\OV_Door\ov_logo.ico" --name="installer_omega_verksted" .\installer.py

echo Build process complete.

echo Moving spec file to spec folder...
move ".\installer_omega_verksted.spec" ".\specs\installer_omega_verksted.spec"
if %ERRORLEVEL% neq 0 (
    echo Error moving file.
) else (
    echo File moved successfully.
)

pause

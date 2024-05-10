@echo off
echo Setting up environment...
set PATH=%PATH%;C:\Users\krisg\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts

echo Building the executable with PyInstaller...
pyinstaller --clean --noupx --windowed --icon="C:\Users\krisg\Documents\Git\OV_Door\ov_logo.ico" --name="Omega Verksted" main.py

echo Build process complete.

echo Checking if dist folder exists...
set RETRIES=0
:compress
PowerShell -Command "Compress-Archive -Path '.\dist\Omega Verksted\*' -DestinationPath '.\dist\Omega_Verksted.zip'"
if %ERRORLEVEL% neq 0 (
    set /a RETRIES+=1
    if !RETRIES! lss 5 (
        echo Attempt !RETRIES! failed, retrying in 5 seconds...
        timeout /t 5 /nobreak
        goto compress
    ) else (
        echo Failed to compress after multiple attempts.
    )
) else (
    echo Compression complete.
)

pause

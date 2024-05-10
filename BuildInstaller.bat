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

echo Checking if executable exists...
if exist ".\dist\installer_omega_verksted.exe" (
    echo Existing archive found, attempting to remove...
    del ".\dist\installer_omega_verksted.zip"
    if %ERRORLEVEL% neq 0 (
        echo Failed to delete existing archive. Please check for any open files and try again.
        pause
        exit /b
    ) else (
        echo Existing archive removed.
    )

    set RETRIES=0
    :compress
    PowerShell -Command "Compress-Archive -Path '.\dist\installer_omega_verksted.exe' -DestinationPath '.\dist\installer_omega_verksted.zip'"
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
) else (
    echo Error: The executable .\dist\installer_omega_verksted.exe does not exist.
)
pause

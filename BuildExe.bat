@echo off
echo Setting up environment...
set PATH=%PATH%;C:\Users\krisg\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts

echo Checking if spec file exists...
if exist ".\specs\Omega Verksted.spec" (
    echo Spec file found.
) else (
    echo Spec file not found! Please check the path and filename.
    pause
    exit /b
)

echo Building the executable with PyInstaller...
pyinstaller ".\specs\Omega Verksted.spec"

if %ERRORLEVEL% neq 0 (
    echo Build process failed.
    pause
    exit /b
) else (
    echo Build process complete.
)

echo Checking if dist folder exists...
if exist ".\dist\Omega Verksted\" (
    echo Existing archive found, attempting to remove...
    del ".\dist\Omega_Verksted.zip"
    if %ERRORLEVEL% neq 0 (
        echo Failed to delete existing archive. Please check for any open files and try again.
        pause
        exit /b
    ) else (
        echo Existing archive removed.
    )
    
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
) else (
    echo Error: The directory .\dist\Omega Verksted\ does not exist.
)

pause

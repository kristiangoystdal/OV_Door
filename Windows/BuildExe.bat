@echo off
echo Building the Omega Verksted executable using cx_Freeze...
python setup.py build
echo Build process complete.

:: Create the dist directory if it does not exist
if not exist "dist\" mkdir "dist"

:: Define the source directory and file name based on your actual build output
:: This needs to be adjusted according to your actual output path and Python environment
set "source_dir=build\exe.win-amd64-3.11"
set "executable_name=ov_door.exe"

:: Check if the executable exists and move it if it does
if exist "%source_dir%\%executable_name%" (
    move "%source_dir%\%executable_name%" "dist\Omega Verksted.exe"
    if "%ERRORLEVEL%" == "0" (
        echo Executable moved and renamed successfully.
    ) else (
        echo Failed to move executable.
    )
) else (
    echo Error: Executable not found in the expected directory.
)

pause

@echo off

rem Set the path to the Python interpreter
set "PYTHON_EXECUTABLE=python.exe"

rem Set the path to the icon file
set "ICON_FILE=C:\Users\krisg\Documents\Git\OV_Door\Windows\ov_logo.ico"

rem Remove the 'dist' directory if it exists
if exist dist rmdir /s /q dist

rem Build the executable using PyInstaller
echo Building the Omega Verksted executable using PyInstaller...
"%PYTHON_EXECUTABLE%" -m PyInstaller ^
    --onefile ^
    --noconsole ^
    --name "Omega Verksted" ^
    --icon "%ICON_FILE%" ^
    ov_door.py

pause

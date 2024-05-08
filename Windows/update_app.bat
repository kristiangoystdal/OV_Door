@echo off
set "current_exe_path=%~1"
set "new_exe_path=%~2"

echo Waiting for the application to close...
:loop
tasklist | findstr /I /C:"%current_exe_path%"
if errorlevel 1 (
    goto proceed
) else (
    timeout /t 1
    goto loop
)

:proceed
echo Updating the application...
move /Y "%new_exe_path%" "%current_exe_path%"

echo Starting the updated application...
start "" "%current_exe_path%"
echo Update and restart completed.

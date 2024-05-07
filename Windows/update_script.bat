@echo off
timeout /t 5
move /y "{new_exe_path}" "{current_exe_path}"
start "" "{current_exe_path}"
del "%~f0"

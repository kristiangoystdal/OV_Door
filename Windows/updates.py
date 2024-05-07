import requests
import tempfile
import os
import sys
import subprocess

from user_interactions import user_confirm


def download_new_version(url):
    """
    Downloads the new executable to a temp directory.
    """
    response = requests.get(url, stream=True)  # Use stream to handle large files
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name
    else:
        raise Exception("Failed to download new version")


def apply_update(new_exe_path):
    current_exe_path = sys.executable
    script_path = os.path.join(tempfile.gettempdir(), "update_script.bat")

    with open(script_path, "w") as script:
        script.write(
            f"""
@echo off
echo Checking for administrative privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process 'cmd.exe' -ArgumentList '/c ^""%~f0^""' -Verb RunAs"
    exit
)

echo Waiting for the application to close...
timeout /t 10
echo Attempting to replace the old executable...
move /y "{new_exe_path}" "{current_exe_path}"
if %errorlevel% neq 0 (
    echo Failed to move file. Error level: %errorlevel%
    pause
) else (
    echo Successfully updated.
    start "" "{current_exe_path}"
)
del "%~f0"
"""
        )

    # Running the script with elevated privileges
    subprocess.run(["cmd.exe", "/c", script_path], shell=True)
    try:
        sys.exit()  # Attempt to close the current instance gracefully
    except SystemExit:
        pass  # Ensures a clean exit without propagating the SystemExit exception


def check_for_updates():
    """
    Check GitHub for updates and prompt user if available.
    """
    latest_version_url = "https://github.com/kristiangoystdal/OV_Door/raw/main/Windows/dist/Omega%20Verksted.exe"
    if user_confirm("Update available. Do you want to update now?"):
        new_exe_path = download_new_version(latest_version_url)
        apply_update(new_exe_path)

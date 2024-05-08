import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
import requests
import tempfile
import psutil


def user_confirm(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    response = messagebox.askyesno("Update Confirmation", message)
    root.destroy()
    return response


def show_message(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Update Information", message)
    root.destroy()


def download_new_version(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name
    else:
        show_message("Failed to download new version")
        raise Exception("Failed to download new version")


def run_update_script(current_exe_path, new_exe_path):
    # Path to the batch file
    batch_file = "update_app.bat"
    # Running the batch file with necessary arguments
    subprocess.Popen([batch_file, current_exe_path, new_exe_path], shell=True)


def apply_update(new_exe_path):
    current_exe_path = sys.executable
    try:
        # Run the batch file that handles the update process
        run_update_script(current_exe_path, new_exe_path)

        # Request application closure
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()  # Attempt to terminate the process

        # Wait until the process has been terminated
        p.wait()

    except Exception as e:
        # If there's an error after the program has terminated, show a message on restart
        subprocess.Popen(
            [current_exe_path, "--error", str(e)],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )


def check_for_updates():
    latest_version_url = "https://github.com/kristiangoystdal/OV_Door/raw/main/Windows/dist/Omega%20Verksted.exe"
    if user_confirm("Update available. Do you want to update now?"):
        new_exe_path = download_new_version(latest_version_url)
        apply_update(new_exe_path)


# This function can be called to start the update process.

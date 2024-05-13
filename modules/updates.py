import os
import requests
import subprocess
import sys
import tkinter as tk
import threading
from tkinter import messagebox
from win32api import GetFileVersionInfo, LOWORD, HIWORD
from modules.tools import resource_path  # Ensure this is correctly imported


def get_version_number(filename):
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info["FileVersionMS"]
        ls = info["FileVersionLS"]
        version = f"{HIWORD(ms)}.{LOWORD(ms)}.{HIWORD(ls)}.{LOWORD(ls)}"
        return version
    except Exception as e:
        return f"No version information available: {e}"


def compare_versions(version1, version2, button_update):
    v1 = tuple(map(int, version1.split(".")))
    v2 = tuple(map(int, version2.split(".")))
    if v1 < v2:
        button_update["state"] = "normal"
        return f"Update available from version {version1} to {version2}"
    else:
        button_update["state"] = "normal"
        return "Newest version is already installed"


def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def check_exe_version_on_github(url):
    user_directory = os.path.expanduser("~")
    local_exe_path = os.path.join(user_directory, "Downloads", "downloaded_exe.exe")
    try:
        download_file(url, local_exe_path)
        version = get_version_number(local_exe_path)
        os.remove(local_exe_path)
        return version
    except Exception as e:
        return f"Error: {e}"


def start_gui():
    window = tk.Tk()
    window.title("Omega Verksted Updater")
    window.geometry("350x150")
    window.iconbitmap(resource_path("ov_logo.ico"))
    window.resizable(False, False)

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    label_feedback = tk.Label(window, text="Click 'Check for Updates' to begin.")
    label_feedback.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    button_update = tk.Button(
        window,
        text="Update",
        command=lambda: threading.Thread(
            target=update_version, args=(label_feedback, button_update)
        ).start(),
        state="disabled",
    )
    button_update.grid(row=1, column=0, padx=40, pady=10, sticky="e")

    button_cancel = tk.Button(window, text="Cancel", command=window.destroy)
    button_cancel.grid(row=1, column=1, padx=40, pady=10, sticky="w")

    def run_updater():
        label_feedback.config(text="Checking version...")
        github_url = "https://github.com/kristiangoystdal/OV_Door/raw/updates/dist/Omega%20Verksted/Omega%20Verksted.exe"
        updated_version = check_exe_version_on_github(github_url)
        current_version = get_version_number(
            r"C:\Program Files\Omega Verksted\Omega Verksted.exe"
        )
        feedback_text = compare_versions(
            current_version, updated_version, button_update
        )
        label_feedback.config(text=feedback_text)

    threading.Thread(target=run_updater, daemon=True).start()
    window.mainloop()


def update_version(label_feedback, button_update):
    try:
        # Define the URL of the GitHub repository
        url = "https://github.com/kristiangoystdal/OV_Door/raw/main/dist/Omega_Verksted.zip"
        label_feedback.config(text="Downloading update...")
        button_update["state"] = "disabled"

        # Send a GET request to download the zip file
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        label_feedback.config(text="Download complete. Updating...")

        # Save the zip file to a temporary location
        zip_path = os.path.join(os.getenv("TEMP"), "Omega_Verksted.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Path to the application executable directory
        app_executable_dir = r"C:\Program Files\Omega Verksted"

        # Create a batch file to handle the update process
        batch_script = f"""
        @echo off
        echo Stopping Omega Verksted application...
        taskkill /f /im "Omega Verksted.exe" 2>nul
        timeout /t 5 /nobreak
        echo Extracting update...
        tar -xf "{zip_path}" -C "{app_executable_dir}"
        echo Update completed. Restarting application...
        start "" "{os.path.join(app_executable_dir, 'Omega Verksted.exe')}"
        exit
        """

        # Write the batch script to a temporary file
        batch_file_path = os.path.join(os.getenv("TEMP"), "update.bat")
        with open(batch_file_path, "w") as batch_file:
            batch_file.write(batch_script)

        # Execute the batch script
        print("Executing batch script for update process.")
        subprocess.Popen(batch_file_path, shell=True)
        sys.exit()

    except requests.RequestException as e:
        messagebox.showerror("Update", f"Failed to download update: {e}")
        print(f"Failed to download update: {e}")
        label_feedback.config(text=f"Failed to download update: {e}")
        button_update["state"] = "normal"
    except Exception as e:
        messagebox.showerror("Update", f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        label_feedback.config(text=f"An error occurred: {e}")
        button_update["state"] = "normal"

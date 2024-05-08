import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
import requests
import tempfile
import psutil
import pefile


def get_exe_version(file_path):
    try:
        pe = pefile.PE(file_path)
        if hasattr(pe, "VS_FIXEDFILEINFO"):
            ms = pe.VS_FIXEDFILEINFO[0]
            version = f"{ms.FileVersionMS >> 16 & 0xffff}.{ms.FileVersionMS & 0xffff}.{ms.FileVersionLS >> 16 & 0xffff}.{ms.FileVersionLS & 0xffff}"
            pe.close()
            return version
        else:
            pe.close()
            return "0.0.0.0"  # Return a default version if no version info is found
    except Exception as e:
        print(f"Error reading version from {file_path}: {e}")
        return "0.0.0.0"  # Return a default version on error


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
    batch_file = "update_app.bat"
    subprocess.Popen([batch_file, current_exe_path, new_exe_path], shell=True)


def apply_update(new_exe_path):
    current_exe_path = sys.executable
    try:
        run_update_script(current_exe_path, new_exe_path)
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()
        p.wait()
    except Exception as e:
        subprocess.Popen(
            [current_exe_path, "--error", str(e)],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )


def check_for_updates():
    current_version = get_exe_version(sys.executable)
    latest_version_url = "https://github.com/kristiangoystdal/OV_Door/blob/main/Windows/dist/Omega%20Verksted.exe"
    temp_exe_path = download_new_version(latest_version_url)
    latest_version = get_exe_version(temp_exe_path)

    if latest_version > current_version:
        if user_confirm(
            f"Update available. Version {latest_version} is newer than {current_version}. Update now?"
        ):
            apply_update(temp_exe_path)
        else:
            os.unlink(temp_exe_path)  # Remove the downloaded file if not updating
    else:
        show_message("No updates are available.")
        os.unlink(temp_exe_path)  # Remove the downloaded file


# This function can be called to start the update process.

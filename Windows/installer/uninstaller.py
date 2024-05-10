import os
import shutil
import winreg as reg
import tkinter as tk
from tkinter import messagebox
import sys
import ctypes


def remove_files_and_directories(install_path):
    """Remove the installed directory and all its contents."""
    try:
        if os.path.exists(install_path):
            shutil.rmtree(install_path)
            return True
    except Exception as e:
        print(f"Error removing directory {install_path}: {e}")
        return False


def remove_registry_entry():
    """Remove the registry entry for the application."""
    try:
        key = reg.OpenKey(
            reg.HKEY_LOCAL_MACHINE,
            r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Omega Verksted",
            0,
            reg.KEY_ALL_ACCESS,
        )
        reg.DeleteKey(key, "")
        reg.CloseKey(key)
        return True
    except WindowsError as e:
        print(f"Failed to remove registry entry: {e}")
        return False


def uninstall():
    if is_admin():
        install_path = os.path.join(os.environ["PROGRAMFILES"], "Omega Verksted")
        if remove_files_and_directories(install_path) and remove_registry_entry():
            messagebox.showinfo(
                "Uninstallation", "Uninstallation completed successfully."
            )
        else:
            messagebox.showinfo(
                "Uninstallation", "Uninstallation failed. Please check the logs."
            )
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    uninstall()

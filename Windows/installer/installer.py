import tkinter as tk
from tkinter import messagebox, ttk, Checkbutton, IntVar
import requests
import zipfile
import os
from io import BytesIO
import winreg as reg
import threading
import time
import ctypes
import sys


def download_and_extract(
    url, extract_to, progress_bar, status_label, install_button, finish_button
):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        total_length = int(response.headers.get("content-length"))
        downloaded = 0
        start_time = time.time()

        with open("temp.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    downloaded += len(chunk)
                    elapsed_time = time.time() - start_time
                    percent_done = int((downloaded / total_length) * 100)
                    progress_bar["value"] = percent_done
                    status_label.config(text=f"Downloading... {percent_done}% complete")
                    root.update_idletasks()

        status_label.config(text="Extracting files...")
        root.update_idletasks()

        extract_files(
            "temp.zip",
            extract_to,
            progress_bar,
            status_label,
            install_button,
            finish_button,
        )

    except requests.RequestException as e:
        status_label.config(text="Download failed!")
        messagebox.showerror("Installation", f"Failed to download: {e}")
        install_button.config(state=tk.NORMAL)
    except zipfile.BadZipFile:
        status_label.config(text="Extraction failed!")
        messagebox.showerror("Installation", "Failed to extract the ZIP file.")
        install_button.config(state=tk.NORMAL)


def extract_files(
    zip_path, extract_to, progress_bar, status_label, install_button, finish_button
):
    with zipfile.ZipFile(zip_path) as z:
        total_files = len(z.infolist())
        for i, file_info in enumerate(z.infolist(), start=1):
            z.extract(file_info, path=extract_to)
            if i % 10 == 0 or i == total_files:
                progress_bar["value"] = 50 + 50 * (i / total_files)
                status_label.config(
                    text=f"Extracting files... {int(50 + 50 * (i / total_files))}% complete"
                )
                root.update_idletasks()

    os.remove(zip_path)
    status_label.config(text="Installation completed successfully!")
    add_to_registry()
    install_button.pack_forget()  # Remove the install button
    finish_button.pack(fill="x")  # Show the finish button


def run_installer():
    if is_admin():
        global root
        root = tk.Tk()
        root.title("Installer")
        root.geometry("350x250")  # Increased size to accommodate checkbox

        frame = tk.Frame(root)
        frame.pack(pady=20, padx=20)

        status_label = tk.Label(frame, text="", font=("Helvetica", 10))
        status_label.pack(pady=4)

        progress_bar = ttk.Progressbar(
            frame, orient="horizontal", length=280, mode="determinate"
        )
        progress_bar.pack(pady=10)

        launch_var = (
            IntVar()
        )  # This variable will hold the state of the checkbox (1 for checked, 0 for unchecked)
        launch_check = Checkbutton(
            frame, text="Launch application after installing", variable=launch_var
        )
        launch_check.pack(pady=10)

        install_button = tk.Button(frame, text="Install")
        finish_button = tk.Button(
            frame, text="Finish", command=root.quit
        )  # Finish button to close the application

        def final_actions():
            if launch_var.get() == 1:  # Check if the checkbox is checked
                executable_path = os.path.join(
                    os.environ["PROGRAMFILES"], "Omega_Verksted", "Omega Verksted.exe"
                )
                os.startfile(
                    executable_path
                )  # Use os.startfile to launch the executable
            root.quit()  # Close the installer

        install_button.config(
            command=lambda: threading.Thread(
                target=download_and_extract,
                args=(
                    "https://github.com/kristiangoystdal/OV_Door/raw/main/Windows/dist/Omega_Verksted.zip",
                    os.path.join(os.environ["PROGRAMFILES"], "Omega_Verksted"),
                    progress_bar,
                    status_label,
                    install_button,
                    finish_button,
                    final_actions,  # Pass the final_actions function to be called after installation
                ),
            ).start()
        )
        install_button.pack(fill="x")

        root.mainloop()
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


def add_to_registry():
    app_name = "Omega Verksted"
    install_path = os.path.join(os.environ["PROGRAMFILES"], "Omega Verksted")
    uninstaller_path = os.path.join(
        install_path, "uninstaller.exe"
    )  # Assuming the uninstaller is named 'uninstaller.exe'

    # Connect to the registry and create a new key under Uninstall
    key = reg.OpenKey(
        reg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
        0,
        reg.KEY_WRITE,
    )
    app_key = reg.CreateKey(key, app_name)

    # Prepare the command that will be run by the uninstaller
    uninstall_command = f'"{uninstaller_path}"'

    # Set values for the application
    reg.SetValueEx(app_key, "DisplayName", 0, reg.REG_SZ, app_name)
    reg.SetValueEx(app_key, "InstallLocation", 0, reg.REG_SZ, install_path)
    reg.SetValueEx(app_key, "UninstallString", 0, reg.REG_SZ, uninstall_command)
    reg.SetValueEx(
        app_key, "Publisher", 0, reg.REG_SZ, "Simulation Edge"
    )  # Optional: Customize as needed

    reg.CloseKey(app_key)
    reg.CloseKey(key)


def remove_from_registry():
    try:
        key = reg.OpenKey(
            reg.HKEY_LOCAL_MACHINE,
            r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
            0,
            reg.KEY_WRITE,
        )
        reg.DeleteKey(key, "Omega Verksted")
        reg.CloseKey(key)
    except WindowsError as e:
        print(f"Failed to remove from registry: {e}")


if __name__ == "__main__":
    run_installer()

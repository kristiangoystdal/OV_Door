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
    url,
    extract_to,
    progress_bar,
    status_label,
    install_button,
    finish_button,
    final_actions,
):
    try:
        status_label.config(text="Starting download...")
        root.update_idletasks()
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        total_length = response.headers.get("content-length")

        if total_length is not None:
            total_length = int(total_length)
        else:
            total_length = 0  # You might consider a different approach here if needed

        downloaded = 0
        start_time = time.time()

        with open("temp.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_length > 0:
                        elapsed_time = time.time() - start_time
                        percent_done = int((downloaded / total_length) * 100)
                        progress_bar["value"] = percent_done
                        status_label.config(
                            text=f"Downloading... {percent_done}% complete"
                        )
                    else:
                        status_label.config(text="Downloading... size unknown")
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
            final_actions,
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
    zip_path,
    extract_to,
    progress_bar,
    status_label,
    install_button,
    finish_button,
    final_actions,
):
    try:
        with zipfile.ZipFile(zip_path) as z:
            total_files = len(z.infolist())
            for i, file_info in enumerate(z.infolist(), start=1):
                try:
                    z.extract(file_info, path=extract_to)
                    if i % 10 == 0 or i == total_files:
                        progress_bar["value"] = 50 + 50 * (i / total_files)
                        status_label.config(
                            text=f"Extracting files... {int(50 + 50 * (i / total_files))}% complete"
                        )
                        root.update_idletasks()
                except PermissionError as e:
                    status_label.config(text="Error: File in use!")
                    messagebox.showerror(
                        "Installation Error",
                        "Please close Omega Verksted or any other program using its files and try again.",
                    )
                    install_button.config(state=tk.NORMAL)
                    return  # Stop further execution and keep the button enabled for retry

        os.remove(zip_path)
        status_label.config(text="Installation completed successfully!")
        add_to_registry()
        install_button.pack_forget()  # Remove the install button
        finish_button.pack(fill="x")  # Show the finish button
        final_actions()  # Call final actions after all operations are done
    except Exception as e:
        status_label.config(text=f"Extraction failed: {e}")
        messagebox.showerror("Installation", f"Extraction failed: {e}")
        install_button.config(state=tk.NORMAL)


def resource_path(relative_path):
    """Get absolute path to resource, works for development and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def run_installer():
    if is_admin():
        global root
        root = tk.Tk()
        root.title("Installer for Omega Verksted")
        root.geometry("350x250")  # Increased size to accommodate checkbox
        icon_path = resource_path("ov_logo.ico")
        root.iconbitmap(icon_path)
        root.resizable(False, False)

        frame = tk.Frame(root)
        frame.pack(pady=20, padx=20)

        status_label = tk.Label(frame, text="", font=("Helvetica", 10))
        status_label.pack(pady=4)

        progress_bar = ttk.Progressbar(
            frame, orient="horizontal", length=280, mode="determinate"
        )
        progress_bar.pack(pady=10)

        launch_var = IntVar(value=1)
        launch_check = Checkbutton(
            frame, text="Launch application after installing", variable=launch_var
        )
        launch_check.pack(pady=10)

        install_button = tk.Button(frame, text="Install")
        finish_button = tk.Button(frame, text="Finish", command=root.quit)

        def final_actions():
            if launch_var.get() == 1:
                executable_path = os.path.join(
                    os.environ["PROGRAMFILES"], "Omega_Verksted", "Omega Verksted.exe"
                )
                os.startfile(executable_path)
            root.quit()

        # Update the start_installation definition to pass final_actions as a parameter
        def start_installation():
            # Disable the install button immediately to prevent multiple presses
            install_button.config(state=tk.DISABLED)

            def on_thread_complete():
                # This function will be called when the thread completes
                root.update_idletasks()  # Update UI tasks if any pending
                # Consider re-enabling the button here if needed, depending on your application logic
                # install_button.config(state=tk.NORMAL)

            threading.Thread(
                target=download_and_extract,
                args=(
                    "https://github.com/kristiangoystdal/OV_Door/raw/main/dist/Omega_Verksted.zip",
                    os.path.join(os.environ["PROGRAMFILES"], "Omega_Verksted"),
                    progress_bar,
                    status_label,
                    install_button,
                    finish_button,
                    final_actions,
                ),
                # Adding a callback to run on the main thread after the thread completes
                daemon=True,  # Optional: makes the thread exit when the main program exits
            ).start()
            # You could use a mechanism here to check when the thread is done if needed, such as a flag or event

        install_button.config(command=start_installation)
        install_button.pack(fill="x")

        root.mainloop()
    else:
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
    reg.SetValueEx(app_key, "Publisher", 0, reg.REG_SZ, "Simulation Edge")
    reg.SetValueEx(app_key, "DisplayIcon", 0, reg.REG_SZ, "ov_logo.ico")

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

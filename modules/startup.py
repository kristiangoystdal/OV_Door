import winreg
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def add_to_startup():
    try:
        exe_path = os.path.abspath(sys.argv[0])
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            winreg.SetValueEx(key, "MyPythonScript", 0, winreg.REG_SZ, exe_path)
        logging.info("Added to startup")
    except PermissionError:
        logging.error(
            "Permission denied: Unable to modify the registry. Please run as administrator."
        )
    except Exception as e:
        logging.error(f"An error occurred while adding to startup: {e}")


def remove_from_startup():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            winreg.DeleteValue(key, "MyPythonScript")
        logging.info("Removed from startup")
    except FileNotFoundError:
        logging.warning("MyPythonScript not found in startup entries.")
    except PermissionError:
        logging.error(
            "Permission denied: Unable to modify the registry. Please run as administrator."
        )
    except Exception as e:
        logging.error(f"An error occurred while removing from startup: {e}")


def check_startup():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        ) as key:
            winreg.QueryValueEx(key, "MyPythonScript")
            return True
    except FileNotFoundError:
        return False
    except PermissionError:
        logging.error(
            "Permission denied: Unable to access the registry. Please run as administrator."
        )
        return False
    except Exception as e:
        logging.error(f"An error occurred while checking startup: {e}")
        return False

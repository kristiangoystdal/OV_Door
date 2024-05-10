import winreg
import os
import sys


def add_to_startup():
    exe_path = os.path.abspath(sys.argv[0])
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        winreg.SetValueEx(key, "MyPythonScript", 0, winreg.REG_SZ, exe_path)
    print("Added to startup")


def remove_from_startup():
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        winreg.DeleteValue(key, "MyPythonScript")
    print("Removed from startup")


def check_startup(*args):
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        ) as key:
            winreg.QueryValueEx(key, "MyPythonScript")
            return True
    except FileNotFoundError:
        return False

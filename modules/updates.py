import os
from win32api import GetFileVersionInfo, LOWORD, HIWORD

def get_version_number(filename):
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{HIWORD(ms)}.{LOWORD(ms)}.{HIWORD(ls)}.{LOWORD(ls)}"
        return version
    except:
        return "No version information available"

# Path to the executable
exe_path = r"C:\Program Files\Omega_Verksted\Omega Verksted.exe"

# Check if the file exists
if os.path.exists(exe_path):
    version = get_version_number(exe_path)
    print(f"Version of {os.path.basename(exe_path)}: {version}")
else:
    print("Executable does not exist.")

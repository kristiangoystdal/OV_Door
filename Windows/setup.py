from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "packages": [],  # List additional packages needed by the script here
    "excludes": [],  # List packages to exclude
    "include_files": [
        ("C:/Users/krisg/Documents/Git/OV_Door/Windows/ov_logo.ico", "ov_logo.ico")
    ],
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Omega Verksted",
    version="1.1.0",
    description="A tool for Omega Verksted's door status",
    options={"build_exe": build_exe_options},
    executables=[Executable("ov_door.py", base=base, icon="ov_logo.ico")],
)

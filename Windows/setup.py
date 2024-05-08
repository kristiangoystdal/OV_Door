from cx_Freeze import setup, Executable
import sys

# Add additional packages as needed
build_exe_options = {
    "packages": [],  # add necessary packages
    "excludes": [],  # exclude unnecessary packages
    "include_files": [
        ("C:/Users/krisg/Documents/Git/OV_Door/Windows/ov_logo.ico", "ov_logo.ico")
    ],  # include additional files
}

# GUI applications require a different base on Windows!
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Omega Verksted",
    version="1.0.0",
    description="A tool for Omega Verksted's door status",
    options={"build_exe": build_exe_options},
    executables=[Executable("ov_door.py", base=base, icon="ov_logo.ico")],
)

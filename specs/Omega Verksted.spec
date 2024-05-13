# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../main.py'],  # Adjust to point to the correct location of main.py
    pathex=['../'],  # Adjust the path to include the parent directory
    binaries=[],
    datas=[
        ('../ov_logo.ico', '.'),  # Include your icon file with the correct path
        # Add any other data files here
    ],
    hiddenimports=[
        'tkinter', 
        'requests',
        'win32api',
        # Add other hidden imports here if needed
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Omega Verksted',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,  # Set to False if you don't want the console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='../version.txt',
    icon='../ov_logo.ico',  # Ensure this path is correct
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Omega Verksted',
)

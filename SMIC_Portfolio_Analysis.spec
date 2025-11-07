# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct, FixedFileInfo
import os
import sys

# Ensure data directory and transaction.csv are included
# Get the absolute path to ensure data is found
base_path = os.path.abspath('.')
data_path = os.path.join(base_path, 'data')
datas = []
if os.path.exists(data_path):
    datas.append((data_path, 'data'))
# Explicitly include transactions.csv
if os.path.exists(os.path.join(data_path, 'transactions.csv')):
    datas.append((os.path.join(data_path, 'transactions.csv'), 'data'))

binaries = []
hiddenimports = ['PySide6.QtWebEngineWidgets', 'plotly.graph_objects', 'plotly.subplots', 'pandas', 'yfinance', 'numpy', 'plotly']

# Collect PySide6 and plotly dependencies
tmp_ret = collect_all('PySide6')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

tmp_ret = collect_all('plotly')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

a = Analysis(
    ['main_app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'torchvision', 'torchaudio', 'tensorflow', 'keras', 'skimage', 'sklearn', 'scipy', 'sympy', 'numba', 'cupy', 'jupyter', 'IPython', 'matplotlib', 'seaborn', 'PIL', 'cv2', 'opencv'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Windows version info
version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0),
        prodvers=(1, 0, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    u'040904B0',
                    [
                        StringStruct(u'CompanyName', u'GCSU Student Managed Investment Committee'),
                        StringStruct(u'FileDescription', u'SMIC Portfolio Analysis Tool'),
                        StringStruct(u'FileVersion', u'1.0.0.0'),
                        StringStruct(u'InternalName', u'SMIC_Portfolio_Analysis'),
                        StringStruct(u'LegalCopyright', u'Copyright (C) 2024-2025 Joel Saucedo, GCSU Student Managed Investment Committee. All rights reserved.'),
                        StringStruct(u'OriginalFilename', u'SMIC_Portfolio_Analysis.exe'),
                        StringStruct(u'ProductName', u'SMIC Portfolio Analysis'),
                        StringStruct(u'ProductVersion', u'1.0.0.0'),
                        StringStruct(u'Publisher', u'Joel Saucedo - GCSU Student Managed Investment Committee Managing Director')
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
    ]
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SMIC_Portfolio_Analysis',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt' if os.name == 'nt' else None,
    icon=None,
)

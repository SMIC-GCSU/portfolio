# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import os

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
)

app = BUNDLE(
    exe,
    name='SMIC Portfolio Analysis.app',
    icon=None,
    bundle_identifier='edu.gcsu.smic.portfolio-analysis',
    version='1.0.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleName': 'SMIC Portfolio Analysis',
        'CFBundleDisplayName': 'SMIC Portfolio Analysis',
        'CFBundleGetInfoString': "SMIC Portfolio Analysis, Version 1.0.0",
        'CFBundleIdentifier': "edu.gcsu.smic.portfolio-analysis",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright (C) 2024-2025 Joel Saucedo, GCSU Student Managed Investment Committee. All rights reserved.",
        'LSApplicationCategoryType': "public.app-category.finance",
        'NSAppleEventsUsageDescription': "This application needs to access Apple Events to function properly.",
    },
)


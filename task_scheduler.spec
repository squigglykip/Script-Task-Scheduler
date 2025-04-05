# -*- mode: python ; coding: utf-8 -*-

import os
import shutil

block_cipher = None

# Get absolute paths
spec_dir = os.path.dirname(SPECPATH)
release_dir = os.path.join(spec_dir, 'release')
build_dir = os.path.join(release_dir, 'build')
dist_dir = os.path.join(release_dir, 'dist')

# Clean up existing directories
if os.path.exists(release_dir):
    shutil.rmtree(release_dir)

# Create directory structure
os.makedirs(build_dir)
os.makedirs(dist_dir)

a = Analysis(
    ['app/gui.py'],
    pathex=[spec_dir],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('app/config.json', '.'),
    ],
    hiddenimports=[
        'schedule',
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'pystray',
        'threading',
        'json',
        'logging',
        'subprocess',
        'datetime',
        'tkinter',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TaskScheduler',
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
    icon='assets/scheduler.ico',
    distpath=dist_dir,
    workpath=build_dir
)
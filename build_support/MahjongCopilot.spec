# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

BASE = Path(__file__).resolve().parent.parent  # project root (spec lives in build_support/)
def p(*parts): 
    return str(BASE.joinpath(*parts))

hiddenimports = []
for pkg in ["mitmproxy", "playwright", "tkinter"]:
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass

# Folders to include (match your screenshot)
data_dirs = ["chrome_ext","libriichi3p","liqi_proto","models","proxinject","resources"]
datas = []
for d in data_dirs:
    full = BASE / d
    if full.exists():
        datas.append((p(d), d))

# Single files to include
for f in ["version"]:
    full = BASE / f
    if full.exists():
        datas.append((p(f), "."))

block_cipher = None

a = Analysis(
    [p("main.py")],
    pathex=[p("")],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    [],
    exclude_binaries=True,
    name="MahjongCopilot",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=p("resources","icon.ico") if (BASE/"resources"/"icon.ico").exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MahjongCopilot",
)
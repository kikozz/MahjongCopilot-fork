# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

BASE = Path(os.getcwd())

def p(*parts):
    return str(BASE.joinpath(*parts))

hiddenimports = []
for pkg in ["mitmproxy", "playwright", "tkinter"]:
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass

# 确保这些目录和文件都会被打进去
datas = []
for d in ["chrome_ext","libriichi3p","liqi_proto","models","proxinject","resources"]:
    if (BASE / d).exists():
        datas.append((p(d), d))

# 单个文件 version
if (BASE / "version").exists():
    datas.append((p("version"), "."))

block_cipher = None

a = Analysis(
    [p("main.py")],
    pathex=[str(BASE)],
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
    console=False,  # 这是 GUI 程序，不要弹黑框
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

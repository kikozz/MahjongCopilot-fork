@echo off
setlocal enabledelayedexpansion
set PY=python

where %PY% >nul 2>nul
if errorlevel 1 (
  echo Python not found. Install Python 3.10+ and rerun.
  exit /b 1
)

if not exist .venv (
  %PY% -m venv .venv
)
set VENV_PY=.venv\Scripts\python.exe
%VENV_PY% -m pip install --upgrade pip wheel setuptools
%VENV_PY% -m pip install -r requirements.txt
%VENV_PY% -m pip install pyinstaller playwright
%VENV_PY% -m playwright install chromium

REM Build with spec (onedir)
%VENV_PY% -m PyInstaller --noconfirm --clean build_support\MahjongCopilot.spec

REM Package to 7z if 7z available
where 7z >nul 2>nul
if %ERRORLEVEL%==0 (
  if exist dist\MahjongCopilot (
    pushd dist
    7z a -t7z -mx=7 MahjongCopilot.windows.7z .\MahjongCopilot\*
    popd
  )
)

echo Done. See dist\MahjongCopilot\ and dist\MahjongCopilot.windows.7z
param(
  [switch]$OneFile
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Ensure Python 3.10+ installed and add to PATH
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Error "Python not found. Install Python 3.10+ and rerun."
}

# Create venv
if (-not (Test-Path .venv)) { python -m venv .venv }
$py = ".\.venv\Scripts\python.exe"
& $py -m pip install --upgrade pip wheel setuptools

# Install deps
& $py -m pip install -r requirements.txt
& $py -m pip install pyinstaller
& $py -m pip install playwright
& $py -m playwright install chromium

# Build
$newArgs = @("--noconfirm","--clean")
if ($OneFile) {
  & $py -m PyInstaller @newArgs --onefile --name MahjongCopilot --icon resources\icon.ico `
    --add-data "chrome_ext;chrome_ext" `
    --add-data "libriichi3p;libriichi3p" `
    --add-data "liqi_proto;liqi_proto" `
    --add-data "models;models" `
    --add-data "proxinject;proxinject" `
    --add-data "resources;resources" `
    main.py
} else {
  & $py -m PyInstaller @newArgs build_support\MahjongCopilot.spec
}

# Optional: pack to .7z shaped like your screenshot root
if (Get-Command 7z -ErrorAction SilentlyContinue) {
  if (Test-Path dist\MahjongCopilot) {
    Push-Location dist
    7z a -t7z -mx=7 MahjongCopilot.windows.7z .\MahjongCopilot\*
    Pop-Location
    Write-Host "Packed dist\MahjongCopilot.windows.7z"
  } else {
    Write-Warning "dist\MahjongCopilot not found."
  }
} else {
  Write-Warning "7z not found. Install 7-Zip to create .7z package."
}

Write-Host "Done. See dist\MahjongCopilot\ (and dist\MahjongCopilot.windows.7z if 7z is installed)."
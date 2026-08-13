# Starts the Task Tracker API (port 8000) and UI (port 5500), then opens the board.
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$VenvPython = Join-Path $Backend "venv\Scripts\python.exe"
$VenvUvicorn = Join-Path $Backend "venv\Scripts\uvicorn.exe"

if (-not (Test-Path (Join-Path $Backend ".env"))) {
    Copy-Item (Join-Path $Backend ".env.example") (Join-Path $Backend ".env")
}

if (-not (Test-Path $VenvUvicorn)) {
    Write-Host "Creating virtual environment and installing dependencies..."
    Push-Location $Backend
    try {
        py -m venv venv
        & $VenvPython -m pip install -r requirements.txt
    }
    finally {
        Pop-Location
    }
}

Write-Host "Starting API at http://localhost:8000 ..."
Start-Process powershell -WorkingDirectory $Backend -ArgumentList @(
    "-NoExit",
    "-Command",
    "& .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"
)

Write-Host "Starting UI at http://localhost:5500 ..."
Start-Process powershell -WorkingDirectory $Frontend -ArgumentList @(
    "-NoExit",
    "-Command",
    "py -m http.server 5500"
)

Start-Sleep -Seconds 2
Start-Process "http://localhost:5500"

Write-Host "Done. Close the two new PowerShell windows to stop the servers, or run scripts\stop.bat."

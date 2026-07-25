# RealEstate Setup Script (Windows PowerShell)
param(
    [string]$EnvFile = ".env"
)

Write-Host "🌾 RealEstate - Setup" -ForegroundColor Green
Write-Host "================================"

# Check Python
try {
    $pyVer = python --version
    Write-Host "✓ Python: $pyVer" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
}

# Activate and install
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create .env if needed
if (-not (Test-Path $EnvFile)) {
    Copy-Item ".env.example" $EnvFile
    Write-Host "✓ Created $EnvFile from .env.example (please edit secrets)" -ForegroundColor Green
} else {
    Write-Host "✓ $EnvFile exists" -ForegroundColor Green
}

# Create directories
New-Item -ItemType Directory -Path "logs", "media\photos", "media\videos" -Force | Out-Null
Write-Host "✓ Directories created" -ForegroundColor Green

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Run: .\venv\Scripts\activate ; python -m backend.main" -ForegroundColor Cyan

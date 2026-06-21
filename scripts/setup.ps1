# =============================================================================
# SkillBridge AI — Local Development Setup (Windows PowerShell)
# =============================================================================

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       SkillBridge AI — Development Setup         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Environment File ────────────────────────────────────────────────────────
if (-not (Test-Path "$ProjectRoot\.env")) {
    Write-Host "→ Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item "$ProjectRoot\.env.example" "$ProjectRoot\.env"
    Write-Host "  ✓ .env created. Update values for your environment." -ForegroundColor Green
} else {
    Write-Host "  ✓ .env already exists." -ForegroundColor Green
}

# ── Backend Setup ───────────────────────────────────────────────────────────
Write-Host ""
Write-Host "→ Setting up backend..." -ForegroundColor Yellow
Set-Location "$ProjectRoot\backend"

if (-not (Test-Path ".venv")) {
    Write-Host "  Creating Python virtual environment..."
    python -m venv .venv
}

Write-Host "  Activating virtual environment..."
& ".venv\Scripts\Activate.ps1"

Write-Host "  Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

Write-Host "  ✓ Backend ready." -ForegroundColor Green

# ── Frontend Setup ──────────────────────────────────────────────────────────
Write-Host ""
Write-Host "→ Setting up frontend..." -ForegroundColor Yellow
Set-Location "$ProjectRoot\frontend"

Write-Host "  Installing npm dependencies..."
npm ci --silent

Write-Host "  ✓ Frontend ready." -ForegroundColor Green

# ── Summary ─────────────────────────────────────────────────────────────────
Set-Location $ProjectRoot
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                  Setup Complete                  ║" -ForegroundColor Cyan
Write-Host "╠══════════════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║                                                  ║" -ForegroundColor Cyan
Write-Host "║  Backend:   cd backend                           ║" -ForegroundColor Cyan
Write-Host "║             .venv\Scripts\Activate.ps1           ║" -ForegroundColor Cyan
Write-Host "║             uvicorn app.main:app --reload        ║" -ForegroundColor Cyan
Write-Host "║                                                  ║" -ForegroundColor Cyan
Write-Host "║  Frontend:  cd frontend && npm run dev           ║" -ForegroundColor Cyan
Write-Host "║                                                  ║" -ForegroundColor Cyan
Write-Host "║  Docker:    docker compose up --build            ║" -ForegroundColor Cyan
Write-Host "║                                                  ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan

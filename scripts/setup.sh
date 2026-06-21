#!/usr/bin/env bash
# =============================================================================
# SkillBridge AI — Local Development Setup (Linux/macOS)
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔══════════════════════════════════════════════════╗"
echo "║       SkillBridge AI — Development Setup         ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Environment File ────────────────────────────────────────────────────────
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "→ Creating .env from .env.example..."
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo "  ✓ .env created. Update values for your environment."
else
    echo "  ✓ .env already exists."
fi

# ── Backend Setup ───────────────────────────────────────────────────────────
echo ""
echo "→ Setting up backend..."
cd "$PROJECT_ROOT/backend"

if [ ! -d ".venv" ]; then
    echo "  Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "  Activating virtual environment..."
source .venv/bin/activate

echo "  Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo "  ✓ Backend ready."

# ── Frontend Setup ──────────────────────────────────────────────────────────
echo ""
echo "→ Setting up frontend..."
cd "$PROJECT_ROOT/frontend"

echo "  Installing npm dependencies..."
npm ci --silent

echo "  ✓ Frontend ready."

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║                  Setup Complete                  ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║                                                  ║"
echo "║  Backend:   cd backend && source .venv/bin/activate  ║"
echo "║             uvicorn app.main:app --reload        ║"
echo "║                                                  ║"
echo "║  Frontend:  cd frontend && npm run dev           ║"
echo "║                                                  ║"
echo "║  Docker:    docker compose up --build            ║"
echo "║                                                  ║"
echo "╚══════════════════════════════════════════════════╝"

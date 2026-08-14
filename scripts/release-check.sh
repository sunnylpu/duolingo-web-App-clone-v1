#!/usr/bin/env bash
set -e

echo "=================================================="
echo "  DUOLINGO CLONE — RELEASE CANDIDATE VERIFICATION"
echo "=================================================="

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "--> [1/5] Running Backend Test Suite (Pytest)..."
cd "$PROJECT_ROOT/backend"
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
python3 -m pytest -v

echo "--> [2/5] Running Deterministic Seed Verification..."
python3 -m seed.verify

echo "--> [3/5] Verifying Production Security & Hardening Tests..."
python3 -m pytest tests/security/ -v

echo "--> [4/5] Running Frontend Typecheck & Production Build..."
cd "$PROJECT_ROOT/frontend"
npm run build

echo "=================================================="
echo "  ✅ RELEASE CHECK PASSED — READY FOR PACKAGING"
echo "=================================================="

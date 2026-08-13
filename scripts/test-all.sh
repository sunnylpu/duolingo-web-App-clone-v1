#!/bin/bash
set -e

echo "=========================================="
echo " Running Duolingo Platform Unified CI Test Suite "
echo "=========================================="

echo ""
echo "[1/4] Running Backend Pytest Unit, Integration & Security Tests with Coverage..."
cd backend
source .venv/bin/activate
python3 -m pytest -v --cov=app
cd ..

echo ""
echo "[2/4] Verifying Seed Data Integrity..."
cd backend
python3 -m seed.verify
cd ..

echo ""
echo "[3/4] Verifying Next.js Production Build..."
cd frontend
npm run build
cd ..

echo ""
echo "=========================================="
echo " ✅ ALL CI TESTS PASSED SUCCESSFULLY! "
echo "=========================================="

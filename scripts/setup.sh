#!/usr/bin/env bash
set -euo pipefail

echo "🌾 RealEstate - Setup"
echo "========================"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "✗ Python3 not found. Install Python 3.10+"
    exit 1
fi
echo "✓ Python: $(python3 --version)"

# Create venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Install
source venv/bin/activate
pip install -r requirements.txt
echo "✓ Dependencies installed"

# .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env from .env.example (edit secrets!)"
fi

# Dirs
mkdir -p logs media/photos media/videos
echo "✓ Directories created"

echo ""
echo "Setup complete!"
echo "Run: source venv/bin/activate && python -m backend.main"

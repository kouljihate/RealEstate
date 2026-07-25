#!/usr/bin/env bash
set -euo pipefail

# RealEstate Deployment Script
# Usage: ./scripts/deploy.sh [production|staging]

ENV=${1:-production}
echo "🚀 Deploying to $ENV"

source venv/bin/activate

# Pull latest
git pull origin main

# Install updates
pip install -r requirements.txt

# Restart service (example with systemd or supervisor)
if command -v systemctl &>/dev/null; then
    sudo systemctl restart realestate
    echo "✓ Service restarted"
elif command -v supervisorctl &>/dev/null; then
    supervisorctl restart realestate
    echo "✓ Supervisor restarted"
else
    echo "⚠ Manual restart required"
fi

# Health check
sleep 2
curl -s http://localhost:8000/health && echo " ✓ Health check passed" || echo " ✗ Health check failed"

echo "✅ Deployment complete"

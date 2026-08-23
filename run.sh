#!/bin/bash
# ==============================================================================
# JobHunter & Career Suite Launcher Script
# Usage:
#   ./run.sh            -> Run Job Hunter & Auto Mailer (Default)
#   ./run.sh network    -> Run Autonomous LinkedIn Networker (Managers & Recruiters)
#   ./run.sh all        -> Run Discovery + Outreach + Networking sequentially
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🚀 JOBHUNTER & CAREER SUITE"
echo "=========================================================="

if [ ! -d "venv" ]; then
    echo "📦 Initializing virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
    ./venv/bin/playwright install chromium
fi

export PYTHONUNBUFFERED=1

MODE="${1:-jobs}"

if [ "$MODE" == "network" ]; then
    echo "🤝 Launching Autonomous LinkedIn Networker Mode..."
    ./venv/bin/python3 linkedin_networker.py
elif [ "$MODE" == "all" ]; then
    echo "🎯 [1/2] Running Autonomous Job Discovery & Auto Mailer..."
    ./venv/bin/python3 auto_pilot.py
    echo ""
    echo "🤝 [2/2] Running Autonomous LinkedIn Networker..."
    ./venv/bin/python3 linkedin_networker.py
else
    echo "🤖 Launching Autonomous Job Discovery & Auto Mailer..."
    ./venv/bin/python3 auto_pilot.py
fi

echo "=========================================================="
echo "✨ Session completed successfully!"
echo "=========================================================="

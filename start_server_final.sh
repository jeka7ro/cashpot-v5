#!/bin/bash
set -Eeuo pipefail

echo "🚀 Starting CASHPOT Gaming System Backend Server..."

# Stop any existing server processes
echo "🔄 Stopping any existing server processes..."
pkill -f "python3 server.py" 2>/dev/null || true
pkill -f "uvicorn.*8002" 2>/dev/null || true
sleep 1

# Set environment variables (allow overriding via existing env)
export MONGO_URL="${MONGO_URL:-mongodb://localhost:27017}"
export DB_NAME="${DB_NAME:-casino_management}"
export JWT_SECRET="${JWT_SECRET:-your-secret-key-here}"

echo "📊 Environment variables set:"
echo "  MONGO_URL: $MONGO_URL"
echo "  DB_NAME: $DB_NAME"
echo "  JWT_SECRET: $JWT_SECRET"

# Move to backend directory (robust to spaces in path)
cd "$(dirname "$0")/backend"

# Ensure Python 3 is available
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ python3 not found. Please install Python 3.11+ and re-run."
  exit 1
fi

# Create virtual environment if missing
if [ ! -d ".venv" ]; then
  echo "🧪 Creating virtual environment in backend/.venv ..."
  python3 -m venv .venv
fi

# Activate virtual environment
# shellcheck disable=SC1091
source .venv/bin/activate

# Upgrade pip and install dependencies
echo "📦 Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start the server
echo "🎯 Starting server on port 8002..."
exec python server.py
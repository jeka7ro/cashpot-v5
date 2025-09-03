#!/bin/bash

echo "🚀 Starting CASHPOT Gaming System Backend Server..."

# Kill any existing server processes
echo "🔄 Stopping any existing server processes..."
pkill -f "python3 server.py" 2>/dev/null || true
sleep 2

# Set environment variables
export MONGO_URL="mongodb://localhost:27017"
export DB_NAME="casino_management"
export JWT_SECRET="your-secret-key-here"

echo "📊 Environment variables set:"
echo "  MONGO_URL: $MONGO_URL"
echo "  DB_NAME: $DB_NAME"
echo "  JWT_SECRET: $JWT_SECRET"

# Start the server
echo "🎯 Starting server on port 8002..."
cd backend
python3 server.py 
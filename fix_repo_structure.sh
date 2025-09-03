#!/bin/bash

# Script to fix repository structure for Render deployment

echo "🔧 Fixing repository structure for Render..."

# Create a temporary directory
mkdir -p /tmp/cashpot-fix
cd /tmp/cashpot-fix

# Clone the repository fresh
git clone https://github.com/jeka7ro/cashpot-v5.git .

# Move all files from subdirectory to root
if [ -d "Downloads/cash-pot v5 copy" ]; then
    echo "Moving files from subdirectory to root..."
    mv "Downloads/cash-pot v5 copy"/* .
    mv "Downloads/cash-pot v5 copy"/.[^.]* . 2>/dev/null || true
    rm -rf Downloads
fi

# Ensure critical files are in root
echo "Ensuring critical files are in root..."
if [ ! -f "requirements.txt" ] && [ -f "backend/requirements.txt" ]; then
    cp backend/requirements.txt .
fi

if [ ! -f "server.py" ] && [ -f "backend/server.py" ]; then
    cp backend/server.py .
fi

if [ ! -f ".env" ] && [ -f "backend/.env" ]; then
    cp backend/.env .
fi

# Update render.yaml
echo "Updating render.yaml..."
cat > backend/render.yaml << 'EOF'
services:
  - type: web
    name: cashpot-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python server.py
    envVars:
      - key: MONGO_URL
        value: mongodb://localhost:27017
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: JWT_ALGORITHM
        value: HS256
      - key: JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      - key: CORS_ORIGINS
        value: '["https://jeka7ro.github.io", "https://jeka7ro.github.io/cashpot-v5"]'
      - key: SECRET_KEY
        generateValue: true
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: "False"
EOF

# Commit and push
echo "Committing changes..."
git add .
git commit -m "Fix repository structure for Render deployment"
git push origin main

echo "✅ Repository structure fixed!"
echo "📁 Files are now in root directory"
echo "🚀 Render should now be able to find requirements.txt and server.py"

# Return to original directory
cd -

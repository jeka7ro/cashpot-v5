#!/usr/bin/env python3
"""
Script automat pentru deployment pe Render fără input
"""

import os
import subprocess
import sys
import json
import time
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🚀" + "=" * 60)
    print("🚀  CASHPOT V5 - AUTO RENDER DEPLOYMENT")
    print("🚀" + "=" * 60)
    print()

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    requirements = {
        'python3': 'python3 --version',
        'node': 'node --version',
        'npm': 'npm --version',
        'git': 'git --version'
    }
    
    for tool, command in requirements.items():
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {tool} is installed")
            else:
                print(f"❌ {tool} is not installed")
                return False
        except FileNotFoundError:
            print(f"❌ {tool} is not installed")
            return False
    
    print("✅ All requirements met!")
    return True

def create_render_yaml():
    """Create render.yaml configuration"""
    print("📝 Creating render.yaml configuration...")
    
    render_config = """services:
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
"""
    
    with open('backend/render.yaml', 'w') as f:
        f.write(render_config)
    
    print("✅ render.yaml created")

def create_requirements_txt():
    """Create requirements.txt for backend"""
    print("📝 Creating requirements.txt...")
    
    requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
pymongo==4.6.0
bcrypt==4.1.2
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
python-dotenv==1.0.0
pydantic==2.5.0
"""
    
    with open('backend/requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ requirements.txt created")

def create_deployment_instructions():
    """Create deployment instructions"""
    print("📝 Creating deployment instructions...")
    
    instructions = """
# 🚀 CASHPOT V5 - Render Deployment Instructions

## ✅ AUTOMATIC STEPS COMPLETED:
- ✅ render.yaml configuration created
- ✅ requirements.txt created
- ✅ All files ready for deployment

## 📋 MANUAL STEPS REQUIRED:

### 1. Deploy to Render
1. Go to: https://render.com/
2. Sign in with your account (jeka7ro@gmail.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository: jeka7ro/cashpot-v5
5. Configure:
   - **Name:** cashpot-backend
   - **Environment:** Python 3
   - **Build Command:** pip install -r requirements.txt
   - **Start Command:** python server.py
   - **Root Directory:** backend

### 2. Environment Variables
Add these environment variables in Render:
- **MONGO_URL:** Your MongoDB Atlas connection string
- **JWT_SECRET_KEY:** (auto-generated)
- **JWT_ALGORITHM:** HS256
- **JWT_ACCESS_TOKEN_EXPIRE_MINUTES:** 30
- **CORS_ORIGINS:** ["https://jeka7ro.github.io", "https://jeka7ro.github.io/cashpot-v5"]
- **SECRET_KEY:** (auto-generated)
- **ENVIRONMENT:** production
- **DEBUG:** False

### 3. MongoDB Atlas Setup
1. Go to: https://cloud.mongodb.com/
2. Create a new cluster (FREE tier)
3. Create database user: cashpot_admin
4. Whitelist IP: 0.0.0.0/0 (all IPs)
5. Get connection string
6. Use it as MONGO_URL in Render

### 4. Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Copy the backend URL
4. Use it as BACKEND_URL secret in GitHub

## 🎉 RESULT:
- **Backend:** https://cashpot-backend.onrender.com (or your custom name)
- **Frontend:** https://jeka7ro.github.io/cashpot-v5

---
**🎰 CASHPOT V5 - Ready for Render deployment! 🚀**
"""
    
    with open('RENDER_DEPLOYMENT_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("✅ RENDER_DEPLOYMENT_INSTRUCTIONS.md created")

def main():
    """Main deployment function"""
    print_header()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Please install missing tools.")
        return
    
    # Create render.yaml
    create_render_yaml()
    
    # Create requirements.txt
    create_requirements_txt()
    
    # Create deployment instructions
    create_deployment_instructions()
    
    print("\n🎉 AUTO RENDER DEPLOYMENT SETUP COMPLETED!")
    print("\n📋 What was done automatically:")
    print("✅ render.yaml configuration created")
    print("✅ requirements.txt created")
    print("✅ Deployment instructions created")
    
    print("\n⚠️  MANUAL STEPS REQUIRED:")
    print("1. Go to https://render.com/")
    print("2. Sign in with jeka7ro@gmail.com")
    print("3. Create new Web Service")
    print("4. Connect GitHub repository: jeka7ro/cashpot-v5")
    print("5. Configure environment variables")
    print("6. Deploy!")
    
    print("\n📁 Files created:")
    print("- backend/render.yaml (Render configuration)")
    print("- backend/requirements.txt (Python dependencies)")
    print("- RENDER_DEPLOYMENT_INSTRUCTIONS.md (complete guide)")
    
    print("\n🔗 Next steps:")
    print("1. Follow instructions in RENDER_DEPLOYMENT_INSTRUCTIONS.md")
    print("2. Deploy backend to Render")
    print("3. Copy backend URL for GitHub secret")

if __name__ == "__main__":
    main()

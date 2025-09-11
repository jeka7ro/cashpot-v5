#!/usr/bin/env python3
"""
Railway Backend Setup - Configure backend for Railway deployment
"""
import os
import json

def main():
    print("🚀 Setting up Railway backend deployment...")
    
    # Create railway.json configuration
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python3 server.py",
            "healthcheckPath": "/health",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open('railway.json', 'w') as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ Created railway.json configuration")
    
    # Create Procfile for Railway
    procfile_content = "web: python3 server.py"
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    print("✅ Created Procfile")
    
    # Update requirements.txt if needed
    requirements = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "motor==3.3.2",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "pymongo==4.6.0",
        "requests==2.31.0",
        "openpyxl==3.1.2",
        "gspread==5.12.4",
        "google-auth==2.23.4",
        "google-auth-oauthlib==1.1.0",
        "google-auth-httplib2==0.1.1"
    ]
    
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(requirements))
    
    print("✅ Updated requirements.txt")
    
    # Create environment variables template
    env_template = """# Railway Environment Variables
# Add these in Railway dashboard under Variables tab

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here-12345-67890
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# MongoDB Configuration (Railway will provide these automatically)
# MONGO_URL=mongodb://localhost:27017 (Railway MongoDB service)
# MONGO_DB_NAME=cashpot_v5

# Google Sheets API (optional)
# GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/credentials.json

# Server Configuration
HOST=0.0.0.0
PORT=8000
"""
    
    with open('railway.env.template', 'w') as f:
        f.write(env_template)
    
    print("✅ Created railway.env.template")
    
    print("\n🎉 Railway backend setup completed!")
    print("\n📋 Next steps:")
    print("1. Go to https://railway.app/")
    print("2. Login with GitHub")
    print("3. Create new project")
    print("4. Deploy from GitHub repo: jeka7ro/cashpot-v5")
    print("5. Add MongoDB service")
    print("6. Add environment variables from railway.env.template")
    print("7. Update frontend BACKEND_URL to Railway URL")

if __name__ == "__main__":
    main()

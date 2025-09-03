#!/usr/bin/env python3
"""
Script to setup production environment variables
This will help configure the application for deployment
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key(length=32):
    """Generate a secure secret key"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Create .env file for production"""
    
    print("🔧 Setting up production environment variables...")
    
    # Get user input for MongoDB Atlas connection
    print("\n📊 MongoDB Atlas Configuration:")
    print("1. Go to https://cloud.mongodb.com/")
    print("2. Create a free cluster")
    print("3. Get your connection string")
    print("4. Create a database user")
    
    mongo_url = input("\nEnter your MongoDB Atlas connection string: ").strip()
    if not mongo_url:
        print("❌ MongoDB URL is required!")
        return False
    
    # Generate JWT secret
    jwt_secret = generate_secret_key(64)
    
    # Create .env file
    env_content = f"""# Production Environment Variables
# MongoDB Atlas Connection
MONGO_URL={mongo_url}
DB_NAME=casino_management

# JWT Configuration
JWT_SECRET_KEY={jwt_secret}
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["https://your-frontend-domain.netlify.app", "https://your-frontend-domain.vercel.app"]

# Security
SECRET_KEY={generate_secret_key(32)}

# Environment
ENVIRONMENT=production
DEBUG=false

# Admin User (will be created on first startup)
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@cashpot.com
ADMIN_PASSWORD=admin123

# API Configuration
API_V1_STR=/api
PROJECT_NAME=CASHPOT Gaming Management System
"""
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with production configuration")
    return True

def create_railway_config():
    """Create Railway deployment configuration"""
    
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "python server.py",
            "healthcheckPath": "/api/health",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open('railway.json', 'w') as f:
        import json
        json.dump(railway_config, f, indent=2)
    
    print("✅ Created railway.json configuration")

def create_render_config():
    """Create Render deployment configuration"""
    
    render_config = """# Render deployment configuration
# Add these environment variables in Render dashboard:

# MongoDB Atlas Connection
MONGO_URL=your_mongodb_atlas_connection_string
DB_NAME=casino_management

# JWT Configuration  
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
CORS_ORIGINS=["https://your-frontend-domain.netlify.app"]

# Security
SECRET_KEY=your_secret_key

# Environment
ENVIRONMENT=production
DEBUG=false

# Admin User
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@cashpot.com
ADMIN_PASSWORD=admin123

# API Configuration
API_V1_STR=/api
PROJECT_NAME=CASHPOT Gaming Management System
"""
    
    with open('render.env', 'w') as f:
        f.write(render_config)
    
    print("✅ Created render.env configuration file")

def main():
    """Main setup function"""
    print("🚀 CASHPOT Production Setup")
    print("=" * 50)
    
    # Create .env file
    if not create_env_file():
        return
    
    # Create deployment configurations
    create_railway_config()
    create_render_config()
    
    print("\n🎉 Production setup completed!")
    print("\n📋 Next steps:")
    print("1. Set up MongoDB Atlas cluster")
    print("2. Update .env file with your MongoDB connection string")
    print("3. Deploy backend to Railway or Render")
    print("4. Deploy frontend to Netlify or Vercel")
    print("5. Update frontend API URLs to point to your backend")
    
    print("\n📁 Files created:")
    print("- .env (production environment variables)")
    print("- railway.json (Railway deployment config)")
    print("- render.env (Render deployment config)")

if __name__ == "__main__":
    main()

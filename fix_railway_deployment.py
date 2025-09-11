#!/usr/bin/env python3
"""
Fix Railway Deployment Issues
"""
import os
import json

def main():
    print("🔧 Fixing Railway deployment issues...")
    
    # Check if server.py exists and is valid
    if not os.path.exists('server.py'):
        print("❌ server.py not found!")
        return
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return
    
    # Fix potential issues in server.py
    with open('server.py', 'r') as f:
        content = f.read()
    
    # Check for common issues
    issues_found = []
    
    # Check if MongoDB connection is configured for Railway
    if 'MONGO_URL' not in content and 'mongodb://localhost' in content:
        issues_found.append("MongoDB connection not configured for Railway")
    
    # Check if port is configured for Railway
    if 'PORT' not in content and '8000' in content:
        issues_found.append("Port not configured for Railway environment")
    
    # Check if CORS is configured for Railway
    if 'allow_origins=["*"]' not in content:
        issues_found.append("CORS not configured for Railway")
    
    if issues_found:
        print("⚠️  Issues found:")
        for issue in issues_found:
            print(f"   - {issue}")
        
        # Create a fixed version
        fixed_content = content
        
        # Add Railway environment variable support
        if 'os.getenv("PORT", "8000")' not in fixed_content:
            fixed_content = fixed_content.replace(
                'uvicorn.run(app, host="0.0.0.0", port=8000)',
                'uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))'
            )
        
        # Add MongoDB environment variable support
        if 'os.getenv("MONGO_URL")' not in fixed_content:
            fixed_content = fixed_content.replace(
                'mongodb://localhost:27017',
                'os.getenv("MONGO_URL", "mongodb://localhost:27017")'
            )
        
        # Write fixed version
        with open('server.py', 'w') as f:
            f.write(fixed_content)
        
        print("✅ Fixed server.py for Railway deployment")
    else:
        print("✅ No issues found in server.py")
    
    # Check requirements.txt
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'motor',
        'python-jose',
        'passlib',
        'python-multipart',
        'python-dotenv',
        'pymongo'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in requirements:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        
        # Add missing packages
        with open('requirements.txt', 'a') as f:
            for package in missing_packages:
                f.write(f'\n{package}')
        
        print("✅ Added missing packages to requirements.txt")
    else:
        print("✅ All required packages present in requirements.txt")
    
    # Create railway.json with proper configuration
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
    
    print("✅ Updated railway.json configuration")
    
    # Create .env template for Railway
    env_template = """# Railway Environment Variables
# Add these in Railway dashboard under Variables tab

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here-12345-67890
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# MongoDB Configuration (Railway will provide these automatically)
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=cashpot_v5

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Google Sheets API (optional)
GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/credentials.json
"""
    
    with open('railway.env.template', 'w') as f:
        f.write(env_template)
    
    print("✅ Updated railway.env.template")
    
    print("\n🎉 Railway deployment fixes completed!")
    print("\n📋 Next steps:")
    print("1. Commit and push these changes")
    print("2. Redeploy on Railway")
    print("3. Add environment variables from railway.env.template")

if __name__ == "__main__":
    main()

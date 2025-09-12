#!/usr/bin/env python3
"""
Railway Error Fix - Diagnose and fix Railway deployment issues
"""
import os
import json

def main():
    print("🔧 Diagnosing Railway deployment error...")
    
    # Check server.py for potential issues
    with open('server.py', 'r') as f:
        content = f.read()
    
    issues_found = []
    
    # Check MongoDB connection configuration
    if 'MONGO_URL' not in content or 'mongodb://localhost' in content:
        issues_found.append("MongoDB connection not properly configured for Railway")
    
    # Check if environment variables are properly handled
    if 'os.getenv("MONGO_URL")' not in content:
        issues_found.append("MONGO_URL environment variable not properly handled")
    
    # Check if port configuration is correct
    if 'os.getenv("PORT", "8000")' not in content:
        issues_found.append("PORT environment variable not properly configured")
    
    # Check if CORS is configured for production
    if 'allow_origins=["*"]' not in content:
        issues_found.append("CORS not configured for production deployment")
    
    if issues_found:
        print("⚠️  Issues found:")
        for issue in issues_found:
            print(f"   - {issue}")
        
        # Fix the issues
        fixed_content = content
        
        # Fix MongoDB connection for Railway
        if 'MONGO_URL' not in fixed_content or 'mongodb://localhost' in fixed_content:
            # Replace hardcoded MongoDB URL with environment variable
            fixed_content = fixed_content.replace(
                'mongodb://localhost:27017',
                'os.getenv("MONGO_URL", "mongodb://localhost:27017")'
            )
            
            # Also fix any other MongoDB connection strings
            fixed_content = fixed_content.replace(
                '"mongodb://localhost:27017"',
                'os.getenv("MONGO_URL", "mongodb://localhost:27017")'
            )
        
        # Ensure port is configured correctly
        if 'os.getenv("PORT", "8000")' not in fixed_content:
            fixed_content = fixed_content.replace(
                'port=8000',
                'port=int(os.getenv("PORT", "8000"))'
            )
        
        # Write the fixed version
        with open('server.py', 'w') as f:
            f.write(fixed_content)
        
        print("✅ Fixed server.py for Railway deployment")
    else:
        print("✅ No issues found in server.py")
    
    # Create a more robust railway.json
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
    
    # Create a more comprehensive environment template
    env_template = """# Railway Environment Variables
# Add these in Railway dashboard under Variables tab

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here-12345-67890
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# MongoDB Configuration (Railway will provide MONGO_URL automatically)
MONGO_DB_NAME=cashpot_v5

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Optional: Google Sheets API
# GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/credentials.json

# Optional: Additional MongoDB settings
# MONGO_MAX_POOL_SIZE=10
# MONGO_MIN_POOL_SIZE=1
"""
    
    with open('railway.env.template', 'w') as f:
        f.write(env_template)
    
    print("✅ Updated railway.env.template")
    
    # Create a simple test script for Railway
    test_script = """#!/usr/bin/env python3
import os
import sys

def test_environment():
    print("🔍 Testing Railway environment...")
    
    # Test environment variables
    port = os.getenv("PORT", "8000")
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    
    print(f"✅ PORT: {port}")
    print(f"✅ MONGO_URL: {mongo_url}")
    
    # Test imports
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        sys.exit(1)
    
    try:
        import motor
        print("✅ Motor imported successfully")
    except ImportError as e:
        print(f"❌ Motor import failed: {e}")
        sys.exit(1)
    
    print("🎉 All tests passed!")

if __name__ == "__main__":
    test_environment()
"""
    
    with open('test_railway.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created test_railway.py for debugging")
    
    print("\n🎉 Railway error fixes completed!")
    print("\n📋 Next steps:")
    print("1. Commit and push these changes")
    print("2. Railway will redeploy automatically")
    print("3. If issues persist, check Railway logs")
    print("4. Run test_railway.py in Railway console for debugging")

if __name__ == "__main__":
    main()

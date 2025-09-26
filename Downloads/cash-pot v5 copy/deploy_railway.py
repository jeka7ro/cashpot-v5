#!/usr/bin/env python3
"""
CASHPOT V5 - Railway Deployment Script
"""

import os
import subprocess
import json
import time

def print_header():
    """Print deployment header"""
    print("🚂" + "=" * 60)
    print("🚂  CASHPOT V5 - RAILWAY DEPLOYMENT")
    print("🚂" + "=" * 60)
    print()

def check_railway_cli():
    """Check if Railway CLI is installed"""
    print("🔍 Checking Railway CLI...")
    
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True, check=True)
        print(f"✅ Railway CLI is installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Railway CLI is not installed")
        print("Please install it from: https://docs.railway.app/develop/cli")
        return False

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment variables...")
    
    # Update .env file with Railway variables
    env_content = """MONGO_URL=mongodb://mongo:szBQQmkgcjGuFGBrAMKtVToeUYrjpY0t@turntable.proxy.rlwy.net:26901
JWT_SECRET_KEY=CashPot2024-SuperSecret-JWT-Key-12345
CORS_ORIGINS=["https://jeka7ro.github.io"]
DB_NAME=cashpot_v5
DEBUG=false
ENVIRONMENT=production
JWT_ALGORITHM=HS256
SECRET_KEY=your-app-secret-key-67890
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment variables configured")

def deploy_to_railway():
    """Deploy to Railway"""
    print("\n🚂 Deploying to Railway...")
    
    try:
        # Login to Railway (if not already logged in)
        print("🔐 Checking Railway authentication...")
        subprocess.run(['railway', 'whoami'], check=True, capture_output=True)
        print("✅ Already authenticated with Railway")
    except subprocess.CalledProcessError:
        print("🔐 Please login to Railway first:")
        print("Run: railway login")
        return False
    
    try:
        # Initialize Railway project (if not already initialized)
        print("📦 Initializing Railway project...")
        subprocess.run(['railway', 'init'], check=True, capture_output=True)
        print("✅ Railway project initialized")
    except subprocess.CalledProcessError:
        print("ℹ️  Railway project already initialized")
    
    try:
        # Set environment variables
        print("🔧 Setting environment variables...")
        env_vars = {
            'MONGO_URL': 'mongodb://mongo:szBQQmkgcjGuFGBrAMKtVToeUYrjpY0t@turntable.proxy.rlwy.net:26901',
            'JWT_SECRET_KEY': 'CashPot2024-SuperSecret-JWT-Key-12345',
            'CORS_ORIGINS': '["https://jeka7ro.github.io"]',
            'DB_NAME': 'cashpot_v5',
            'DEBUG': 'false',
            'ENVIRONMENT': 'production',
            'JWT_ALGORITHM': 'HS256',
            'SECRET_KEY': 'your-app-secret-key-67890'
        }
        
        for key, value in env_vars.items():
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True, capture_output=True)
            print(f"✅ Set {key}")
        
        print("✅ All environment variables set")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting environment variables: {e}")
        return False
    
    try:
        # Deploy to Railway
        print("🚀 Deploying to Railway...")
        result = subprocess.run(['railway', 'up'], check=True, capture_output=True, text=True)
        print("✅ Deployment initiated")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def get_railway_url():
    """Get Railway deployment URL"""
    print("\n🔗 Getting Railway URL...")
    
    try:
        result = subprocess.run(['railway', 'domain'], capture_output=True, text=True, check=True)
        url = result.stdout.strip()
        print(f"✅ Railway URL: {url}")
        return url
    except subprocess.CalledProcessError:
        print("❌ Could not get Railway URL")
        return None

def main():
    """Main deployment function"""
    print_header()
    
    # Check Railway CLI
    if not check_railway_cli():
        return
    
    # Setup environment
    setup_environment()
    
    # Deploy to Railway
    if deploy_to_railway():
        print("\n🎉 Deployment successful!")
        
        # Get Railway URL
        url = get_railway_url()
        if url:
            print(f"\n🌐 Your app is available at: {url}")
            print(f"🔧 Health check: {url}/api/health")
            
            # Update GitHub Pages with new backend URL
            print("\n📝 Next steps:")
            print("1. Update GitHub Pages with the new backend URL")
            print("2. Test the application")
            print("3. Monitor Railway logs if needed")
        else:
            print("\n⚠️  Could not get Railway URL. Check Railway dashboard.")
    else:
        print("\n❌ Deployment failed. Check the errors above.")

if __name__ == "__main__":
    main()

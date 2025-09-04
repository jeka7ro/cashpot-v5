#!/usr/bin/env python3
"""
Railway Setup Script - Configure everything automatically
"""
import os
import json
import subprocess
import time

def run_command(cmd):
    """Run a command and return the output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("🚀 Setting up Railway deployment...")
    
    # Check if Railway CLI is installed
    stdout, stderr, code = run_command("railway --version")
    if code != 0:
        print("❌ Railway CLI not found. Installing...")
        run_command("npm install -g @railway/cli")
    
    # Login to Railway
    print("🔐 Logging into Railway...")
    stdout, stderr, code = run_command("railway login")
    if code != 0:
        print("❌ Failed to login to Railway")
        print("Please run: railway login")
        return
    
    # Create or connect to project
    print("📦 Setting up project...")
    stdout, stderr, code = run_command("railway status")
    if code != 0:
        print("Creating new Railway project...")
        run_command("railway init")
    
    # Add MongoDB service
    print("🗄️ Adding MongoDB service...")
    run_command("railway add mongodb")
    
    # Set environment variables
    print("⚙️ Setting environment variables...")
    
    env_vars = {
        "JWT_SECRET_KEY": "your-super-secret-jwt-key-here-12345-67890",
        "JWT_ALGORITHM": "HS256", 
        "SECRET_KEY": "your-app-secret-key-67890-12345",
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "CORS_ORIGINS": '["https://jeka7ro.github.io"]'
    }
    
    for key, value in env_vars.items():
        print(f"Setting {key}...")
        run_command(f'railway variables set {key}="{value}"')
    
    # Get MongoDB URL
    print("🔗 Getting MongoDB connection string...")
    stdout, stderr, code = run_command("railway variables")
    if "MONGO_URL" in stdout:
        print("✅ MongoDB URL already set")
    else:
        print("⚠️ Please set MONGO_URL manually from Railway dashboard")
        print("1. Go to Railway dashboard")
        print("2. Click on your project")
        print("3. Click on MongoDB service")
        print("4. Copy the connection string")
        print("5. Set MONGO_URL variable")
    
    # Deploy
    print("🚀 Deploying to Railway...")
    run_command("railway up")
    
    print("✅ Setup complete!")
    print("🌐 Your app should be available at: https://cashpot-v5-production.up.railway.app")
    print("🔍 Health check: https://cashpot-v5-production.up.railway.app/health")

if __name__ == "__main__":
    main()

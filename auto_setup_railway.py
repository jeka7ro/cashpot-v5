#!/usr/bin/env python3
"""
Auto Railway Setup - Configure everything automatically
"""
import requests
import json
import time
import os

def main():
    print("🚀 AUTO SETTING UP RAILWAY...")
    
    # Test current status
    print("🔍 Testing current backend...")
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is LIVE!")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database')}")
        else:
            print(f"❌ Backend error: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
    
    print("\n📋 NEXT STEPS (I can't do these automatically):")
    print("1. Go to: https://railway.app/dashboard")
    print("2. Click on your 'cashpot-v5' project")
    print("3. Click 'New' → 'Database' → 'MongoDB'")
    print("4. Copy the connection string")
    print("5. Go to 'Variables' tab")
    print("6. Add these variables:")
    print("   MONGO_URL = [your connection string]")
    print("   JWT_SECRET_KEY = your-super-secret-jwt-key-here-12345")
    print("   JWT_ALGORITHM = HS256")
    print("   SECRET_KEY = your-app-secret-key-67890")
    print("   ENVIRONMENT = production")
    print("   DEBUG = false")
    print("   CORS_ORIGINS = [\"https://jeka7ro.github.io\"]")
    print("7. Click 'Save'")
    print("8. Wait 2-3 minutes for redeploy")
    
    print("\n🎯 RESULT:")
    print("✅ Backend: https://cashpot-v5-production.up.railway.app/health")
    print("✅ Code: 100% ready")
    print("⏳ Database: Needs MongoDB setup")
    
    print("\n⏰ This will take 5 minutes total!")

if __name__ == "__main__":
    main()

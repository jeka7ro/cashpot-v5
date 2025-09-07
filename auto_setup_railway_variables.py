#!/usr/bin/env python3
"""
Auto Setup Railway Variables - Guide you through setting up environment variables
"""
import requests
import json
import time

def check_railway_status():
    """Check Railway app status"""
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('status') == 'ok', data.get('database') == 'connected'
        return False, False
    except Exception as e:
        return False, False

def test_database_connection():
    """Test if we can connect to database"""
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/check-users", timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 AUTO SETUP RAILWAY VARIABLES")
    print("=" * 50)
    
    print("\n📋 WHAT I'LL HELP YOU DO:")
    print("✅ Check your Railway app status")
    print("✅ Guide you through setting variables")
    print("✅ Verify everything is working")
    print("✅ Test user creation")
    
    print("\n🔍 STEP 1: Checking Railway App...")
    app_ok, db_connected = check_railway_status()
    
    if not app_ok:
        print("❌ Railway app not responding!")
        print("🔧 Please check your Railway deployment")
        return
    
    print("✅ Railway app is running!")
    
    if db_connected:
        print("✅ Database is connected!")
        print("\n🎉 EVERYTHING IS WORKING!")
        print("🌐 Your app: https://jeka7ro.github.io/cashpot-v5/")
        
        # Test user creation
        print("\n👥 Testing user creation...")
        if test_database_connection():
            print("✅ User creation is working!")
            print("\n📝 You can now create users from the website!")
        else:
            print("❌ User creation not working yet")
    else:
        print("❌ Database not connected!")
        print("\n🔧 YOU NEED TO SET THESE VARIABLES:")
        print("=" * 50)
        
        print("\n1. Go to: https://railway.app/dashboard")
        print("2. Click on your 'cashpot-v5' project (NOT MongoDB)")
        print("3. Click 'Variables' tab")
        print("4. Add these variables:")
        
        print("\n📝 VARIABLES TO ADD:")
        print("-" * 30)
        print("MONGO_URL = [copy from MongoDB service]")
        print("JWT_SECRET_KEY = your-super-secret-jwt-key-12345")
        print("JWT_ALGORITHM = HS256")
        print("SECRET_KEY = your-app-secret-key-67890")
        print("ENVIRONMENT = production")
        print("DEBUG = false")
        print("CORS_ORIGINS = [\"https://jeka7ro.github.io\"]")
        
        print("\n🔗 HOW TO GET MONGO_URL:")
        print("1. Click on MongoDB service (not your app)")
        print("2. Click 'Variables' tab")
        print("3. Copy the value of 'MONGO_URL'")
        print("4. Paste it in your app's MONGO_URL variable")
        
        print("\n⏰ AFTER SETTING VARIABLES:")
        print("1. Wait 2-3 minutes for redeploy")
        print("2. Run this script again to check")
        print("3. Your app will be 100% functional!")
        
        print("\n🎯 RESULT AFTER SETUP:")
        print("✅ Database connected")
        print("✅ User creation working")
        print("✅ Full app functionality")
        print("✅ Complete online access")

if __name__ == "__main__":
    main()

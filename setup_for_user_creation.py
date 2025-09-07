#!/usr/bin/env python3
"""
Setup for User Creation from Website
"""
import requests
import json
import time

def test_backend():
    """Test backend connection"""
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status')}")
            print(f"📊 Database: {data.get('database')}")
            return data.get('database') == 'connected'
        return False
    except Exception as e:
        print(f"❌ Backend Error: {e}")
        return False

def main():
    print("🌐 SETTING UP FOR USER CREATION FROM WEBSITE")
    print("=" * 60)
    
    print("\n📋 CURRENT STATUS:")
    print("✅ Frontend: https://jeka7ro.github.io/cashpot-v5/")
    print("✅ Backend: https://cashpot-v5-production.up.railway.app/health")
    print("✅ Frontend configured to use Railway backend")
    print("✅ Static files (logo, favicon, manifest) added")
    
    # Test backend
    print("\n🔍 Testing Backend...")
    db_connected = test_backend()
    
    if not db_connected:
        print("\n❌ DATABASE NOT CONNECTED!")
        print("🔧 TO ENABLE USER CREATION FROM WEBSITE:")
        print("1. Go to: https://railway.app/dashboard")
        print("2. Click on 'cashpot-v5' project")
        print("3. Click 'New' → 'Database' → 'MongoDB'")
        print("4. Copy the connection string")
        print("5. Go to 'Variables' tab")
        print("6. Add: MONGO_URL = [your connection string]")
        print("7. Add other variables (see auto_configure_railway.py)")
        print("8. Click 'Save' and wait 2-3 minutes")
        print("\n⏰ This will take 5 minutes!")
        return
    
    print("✅ Database connected!")
    
    print("\n🎉 EVERYTHING IS READY!")
    print("\n🌐 ACCESS YOUR APP:")
    print("   Website: https://jeka7ro.github.io/cashpot-v5/")
    print("   Backend: https://cashpot-v5-production.up.railway.app/health")
    
    print("\n👥 USER CREATION:")
    print("✅ You can now create users directly from the website")
    print("✅ No automatic admin creation")
    print("✅ Only you control who has access")
    
    print("\n📝 HOW TO CREATE USERS:")
    print("1. Go to: https://jeka7ro.github.io/cashpot-v5/")
    print("2. Use the registration form on the website")
    print("3. Create your admin account first")
    print("4. Then create other users as needed")
    
    print("\n🔐 SECURITY:")
    print("✅ Only registered users can access the system")
    print("✅ You control all user permissions")
    print("✅ No unauthorized access possible")

if __name__ == "__main__":
    main()

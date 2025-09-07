#!/usr/bin/env python3
"""
Setup Admin User Online - Configure everything for online access
"""
import requests
import json
import time
import os
from datetime import datetime

def test_backend():
    """Test if backend is accessible"""
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status')}")
            print(f"📊 Database: {data.get('database')}")
            return data.get('database') == 'connected'
        else:
            print(f"❌ Backend Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Not Accessible: {e}")
        return False

def create_admin_user():
    """Create admin user via API"""
    admin_data = {
        "username": "admin",
        "password": "admin123",
        "email": "admin@cashpot.ro",
        "first_name": "Eugeniu",
        "last_name": "Cazmal",
        "role": "admin",
        "phone": "+40712345678"
    }
    
    try:
        print("🔐 Creating admin user...")
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/auth/register",
            json=admin_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Admin user created successfully!")
            return True
        else:
            print(f"❌ Failed to create admin user: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        print("🔑 Testing admin login...")
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"👤 User: {data.get('user', {}).get('username')}")
            print(f"🔑 Token: {data.get('access_token', '')[:20]}...")
            return True
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing login: {e}")
        return False

def main():
    print("🚀 SETTING UP ADMIN USER FOR ONLINE ACCESS...")
    print("=" * 50)
    
    # Test backend
    print("\n1. Testing Backend...")
    db_connected = test_backend()
    
    if not db_connected:
        print("\n❌ DATABASE NOT CONNECTED!")
        print("🔧 SOLUTION:")
        print("1. Go to: https://railway.app/dashboard")
        print("2. Click on 'cashpot-v5' project")
        print("3. Click 'New' → 'Database' → 'MongoDB'")
        print("4. Copy the connection string")
        print("5. Go to 'Variables' tab")
        print("6. Add: MONGO_URL = [your connection string]")
        print("7. Add other variables (see auto_setup_railway.py)")
        print("8. Click 'Save' and wait 2-3 minutes")
        print("\n⏰ This will take 5 minutes!")
        return
    
    print("\n2. Creating Admin User...")
    if create_admin_user():
        print("\n3. Testing Admin Login...")
        if test_admin_login():
            print("\n🎉 SUCCESS! Admin user is ready!")
            print("\n📋 LOGIN CREDENTIALS:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n🌐 ACCESS YOUR APP:")
            print("   Frontend: https://jeka7ro.github.io/cashpot-v5/")
            print("   Backend: https://cashpot-v5-production.up.railway.app/health")
        else:
            print("\n❌ Admin login failed!")
    else:
        print("\n❌ Failed to create admin user!")

if __name__ == "__main__":
    main()

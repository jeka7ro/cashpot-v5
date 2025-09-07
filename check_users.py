#!/usr/bin/env python3
"""
Check Users - See what users are created in your app
"""
import requests
import json

def check_database_status():
    """Check if database is connected"""
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('database') == 'connected'
        return False
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def get_users():
    """Get all users from the app"""
    try:
        # First try to get users without authentication (if any exist)
        response = requests.get("https://cashpot-v5-production.up.railway.app/check-users", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('users', [])
        else:
            print(f"❌ Failed to get users: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return []

def main():
    print("👥 CHECKING USERS IN YOUR APP")
    print("=" * 40)
    
    # Check database status
    print("\n1. Checking Database Status...")
    if not check_database_status():
        print("❌ DATABASE NOT CONNECTED!")
        print("🔧 To see users, you need to:")
        print("1. Go to: https://railway.app/dashboard")
        print("2. Click on 'cashpot-v5' project")
        print("3. Add MongoDB service")
        print("4. Set MONGO_URL variable")
        print("5. Wait for redeploy")
        print("\n⏰ This will take 5 minutes!")
        return
    
    print("✅ Database connected!")
    
    # Get users
    print("\n2. Getting Users...")
    users = get_users()
    
    if not users:
        print("❌ No users found!")
        print("🔧 To create users:")
        print("1. Go to: https://jeka7ro.github.io/cashpot-v5/")
        print("2. Use the registration form")
        print("3. Create your admin account first")
    else:
        print(f"✅ Found {len(users)} users:")
        for i, user in enumerate(users, 1):
            print(f"\n{i}. Username: {user.get('username', 'N/A')}")
            print(f"   Name: {user.get('first_name', '')} {user.get('last_name', '')}")
            print(f"   Email: {user.get('email', 'N/A')}")
            print(f"   Role: {user.get('role', 'N/A')}")
            print(f"   Active: {'Yes' if user.get('is_active', False) else 'No'}")
            print(f"   Created: {user.get('created_at', 'N/A')}")

if __name__ == "__main__":
    main()

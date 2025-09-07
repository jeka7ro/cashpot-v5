#!/usr/bin/env python3
"""
Create Your Users - Manual user creation for your app
"""
import requests
import json
import time

def test_database_connection():
    """Test if database is connected"""
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('database') == 'connected'
        return False
    except:
        return False

def create_user(username, password, email, first_name, last_name, role="admin", phone=""):
    """Create a user via API"""
    user_data = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
        "phone": phone
    }
    
    try:
        print(f"👤 Creating user: {username}...")
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/auth/register",
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ User '{username}' created successfully!")
            return True
        else:
            print(f"❌ Failed to create user '{username}': {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating user '{username}': {e}")
        return False

def test_user_login(username, password):
    """Test user login"""
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        print(f"🔑 Testing login for: {username}...")
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful for '{username}'!")
            print(f"   Role: {data.get('user', {}).get('role')}")
            print(f"   Name: {data.get('user', {}).get('first_name')} {data.get('user', {}).get('last_name')}")
            return True
        else:
            print(f"❌ Login failed for '{username}': {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing login for '{username}': {e}")
        return False

def main():
    print("👥 CREATE YOUR USERS FOR CASH POT APP")
    print("=" * 50)
    
    # Test database connection
    print("\n1. Testing Database Connection...")
    if not test_database_connection():
        print("❌ DATABASE NOT CONNECTED!")
        print("🔧 Please configure MongoDB on Railway first:")
        print("   1. Go to: https://railway.app/dashboard")
        print("   2. Add MongoDB service")
        print("   3. Set MONGO_URL variable")
        print("   4. Wait for redeploy")
        return
    
    print("✅ Database connected!")
    
    # Your users to create
    users_to_create = [
        {
            "username": "eugeniu",
            "password": "your_password_here",
            "email": "eugeniu@cashpot.ro",
            "first_name": "Eugeniu",
            "last_name": "Cazmal",
            "role": "admin",
            "phone": "+40712345678"
        },
        # Add more users here if needed
        # {
        #     "username": "operator1",
        #     "password": "operator123",
        #     "email": "operator1@cashpot.ro",
        #     "first_name": "Operator",
        #     "last_name": "One",
        #     "role": "operator",
        #     "phone": "+40712345679"
        # }
    ]
    
    print(f"\n2. Creating {len(users_to_create)} users...")
    
    success_count = 0
    for user in users_to_create:
        if create_user(**user):
            success_count += 1
        print()  # Empty line for readability
    
    print(f"✅ Successfully created {success_count}/{len(users_to_create)} users!")
    
    # Test logins
    print("\n3. Testing User Logins...")
    for user in users_to_create:
        test_user_login(user["username"], user["password"])
        print()
    
    print("🎉 USER SETUP COMPLETE!")
    print("\n🌐 ACCESS YOUR APP:")
    print("   Frontend: https://jeka7ro.github.io/cashpot-v5/")
    print("   Backend: https://cashpot-v5-production.up.railway.app/health")
    
    print("\n📝 IMPORTANT:")
    print("   - Change passwords after first login")
    print("   - Only you can create new users")
    print("   - No automatic admin creation")

if __name__ == "__main__":
    main()

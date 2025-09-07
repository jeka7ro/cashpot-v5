#!/usr/bin/env python3
"""
Fix Admin Permissions - Update admin user with all permissions
"""
import requests
import json

def login():
    """Login as admin user"""
    login_data = {
        "username": "eugeniu",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def update_admin_permissions(token):
    """Update admin user with all permissions"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # All permissions for admin
    permissions = {
        "modules": {
            "dashboard": True,
            "companies": True,
            "locations": True,
            "providers": True,
            "cabinets": True,
            "game_mixes": True,
            "slot_machines": True,
            "invoices": True,
            "onjn_reports": True,
            "legal_documents": True,
            "metrology": True,
            "jackpots": True,
            "users": True
        },
        "actions": {
            "companies": {"create": True, "read": True, "update": True, "delete": True},
            "locations": {"create": True, "read": True, "update": True, "delete": True},
            "providers": {"create": True, "read": True, "update": True, "delete": True},
            "cabinets": {"create": True, "read": True, "update": True, "delete": True},
            "game_mixes": {"create": True, "read": True, "update": True, "delete": True},
            "slot_machines": {"create": True, "read": True, "update": True, "delete": True},
            "invoices": {"create": True, "read": True, "update": True, "delete": True},
            "onjn_reports": {"create": True, "read": True, "update": True, "delete": True},
            "legal_documents": {"create": True, "read": True, "update": True, "delete": True},
            "metrology": {"create": True, "read": True, "update": True, "delete": True},
            "jackpots": {"create": True, "read": True, "update": True, "delete": True},
            "users": {"create": True, "read": True, "update": True, "delete": True}
        }
    }
    
    update_data = {
        "permissions": permissions
    }
    
    try:
        response = requests.put(
            "https://cashpot-v5-production.up.railway.app/api/users/ea242710-7d88-4a1a-8780-a6b827309301",
            json=update_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Admin permissions updated successfully!")
            return True
        else:
            print(f"❌ Failed to update permissions: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating permissions: {e}")
        return False

def main():
    print("🔧 FIXING ADMIN PERMISSIONS...")
    print("=" * 40)
    
    # Login
    print("1. Logging in as admin...")
    token = login()
    if not token:
        print("❌ Cannot login as admin")
        return
    
    print("✅ Login successful!")
    
    # Update permissions
    print("\n2. Updating admin permissions...")
    if update_admin_permissions(token):
        print("\n🎉 ADMIN PERMISSIONS FIXED!")
        print("✅ All modules should now be visible")
        print("🌐 Go to: https://jeka7ro.github.io/cashpot-v5/")
        print("👤 Login with: eugeniu / admin123")
    else:
        print("\n❌ Failed to update permissions")

if __name__ == "__main__":
    main()

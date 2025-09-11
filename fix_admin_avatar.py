#!/usr/bin/env python3
"""
Script to fix admin user avatar
"""
import os
import base64
import requests
import json

def get_base64_from_file(file_path):
    """Convert image file to base64"""
    try:
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def main():
    # Configuration
    API_BASE = "http://localhost:8000"  # Change to your backend URL
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"
    
    # Avatar file path
    avatar_file = "admin-real-avatar.png"
    
    if not os.path.exists(avatar_file):
        print(f"❌ Avatar file {avatar_file} not found!")
        return
    
    print(f"🔧 Fixing admin avatar with file: {avatar_file}")
    
    # Step 1: Login to get token
    print("🔐 Logging in...")
    login_response = requests.post(f"{API_BASE}/api/auth/login", json={
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Get admin user info
    print("👤 Getting admin user info...")
    me_response = requests.get(f"{API_BASE}/api/auth/me", headers=headers)
    
    if me_response.status_code != 200:
        print(f"❌ Failed to get user info: {me_response.text}")
        return
    
    user_info = me_response.json()
    admin_id = user_info.get("id")
    
    if not admin_id:
        print("❌ No user ID found")
        return
    
    print(f"✅ Admin ID: {admin_id}")
    
    # Step 3: Convert avatar to base64
    print("🖼️ Converting avatar to base64...")
    avatar_base64 = get_base64_from_file(avatar_file)
    
    if not avatar_base64:
        print("❌ Failed to convert avatar to base64")
        return
    
    # Step 4: Upload avatar
    print("📤 Uploading avatar...")
    upload_data = {
        "filename": "admin-avatar.png",
        "mime_type": "image/png",
        "file_data": avatar_base64,
        "entity_type": "users",
        "entity_id": admin_id
    }
    
    upload_response = requests.post(
        f"{API_BASE}/api/attachments",
        headers=headers,
        json=upload_data
    )
    
    if upload_response.status_code == 200:
        print("✅ Admin avatar updated successfully!")
    else:
        print(f"❌ Upload failed: {upload_response.status_code} - {upload_response.text}")
    
    print("🎉 Done!")

if __name__ == "__main__":
    main()

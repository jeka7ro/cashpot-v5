#!/usr/bin/env python3
"""
Script to test if Render can access the files correctly
"""

import requests
import json

def test_github_files():
    """Test if files are accessible from GitHub"""
    print("🔍 Testing GitHub file access...")
    
    base_url = "https://raw.githubusercontent.com/jeka7ro/cashpot-v5/main"
    
    files_to_test = [
        "requirements.txt",
        "server.py",
        ".env"
    ]
    
    for file_name in files_to_test:
        try:
            url = f"{base_url}/{file_name}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {file_name} - Accessible")
                if file_name == "requirements.txt":
                    print(f"   Content preview: {response.text[:100]}...")
            else:
                print(f"❌ {file_name} - Not accessible (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {file_name} - Error: {e}")

def test_render_deployment():
    """Test Render deployment status"""
    print("\n🔍 Testing Render deployment...")
    
    # Common Render URLs to test
    render_urls = [
        "https://cashpot-backend.onrender.com",
        "https://cashpot-backend-v5.onrender.com",
        "https://jeka7ro-cashpot.onrender.com"
    ]
    
    for url in render_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - Online")
            else:
                print(f"⚠️  {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")

def main():
    """Main test function"""
    print("🚀" + "=" * 60)
    print("🚀  CASHPOT V5 - Render Files Test")
    print("🚀" + "=" * 60)
    
    test_github_files()
    test_render_deployment()
    
    print("\n📋 Summary:")
    print("If all files are accessible from GitHub, Render should be able to deploy them.")
    print("If Render deployment fails, check the Render dashboard for specific errors.")

if __name__ == "__main__":
    main()

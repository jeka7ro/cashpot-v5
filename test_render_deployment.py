#!/usr/bin/env python3
"""
Test script to verify Render deployment files are accessible
"""

import requests
import json

def test_github_files():
    """Test if critical files are accessible from GitHub"""
    print("🔍 Testing GitHub file access...")
    
    base_url = "https://raw.githubusercontent.com/jeka7ro/cashpot-v5/main/"
    files_to_check = [
        "Downloads/cash-pot v5 copy/requirements.txt",
        "Downloads/cash-pot v5 copy/server.py",
        "Downloads/cash-pot v5 copy/.env"
    ]
    
    all_accessible = True
    for file_path in files_to_check:
        full_url = base_url + file_path
        try:
            response = requests.get(full_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {file_path} - Accessible")
                if "requirements.txt" in file_path:
                    print(f"   Content preview: {response.text[:100]}...")
            else:
                print(f"❌ {file_path} - Not accessible (Status: {response.status_code})")
                all_accessible = False
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            all_accessible = False
    
    return all_accessible

def test_render_deployment():
    """Test Render deployment URLs"""
    print("\n🔍 Testing Render deployment...")
    
    render_urls = [
        "https://cashpot-backend.onrender.com",
        "https://cashpot-backend-v5.onrender.com",
        "https://jeka7ro-cashpot.onrender.com"
    ]
    
    all_up = True
    for url in render_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - Status: {response.status_code}")
            else:
                print(f"⚠️  {url} - Status: {response.status_code}")
                all_up = False
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} - Error: {e}")
            all_up = False
    
    return all_up

def main():
    print("🚀============================================================")
    print("🚀  CASHPOT V5 - Render Deployment Test")
    print("============================================================\n")
    
    github_accessible = test_github_files()
    render_deployed = test_render_deployment()
    
    print("\n📋 Summary:")
    if github_accessible:
        print("✅ All files are accessible from GitHub")
        print("   Render should be able to deploy them with correct settings")
    else:
        print("❌ Files are NOT accessible from GitHub")
        print("   This is the root cause of deployment failures")
    
    if render_deployed:
        print("✅ Render deployment is up and running")
    else:
        print("❌ Render deployment is not working")
        print("   Check Render dashboard for specific errors")
    
    print("\n🔧 Next Steps:")
    if not github_accessible:
        print("1. Fix GitHub file access issues")
    else:
        print("1. Update Render dashboard settings:")
        print("   - Build Command: pip install -r \"Downloads/cash-pot v5 copy/requirements.txt\"")
        print("   - Start Command: python \"Downloads/cash-pot v5 copy/server.py\"")
        print("   - Root Directory: (leave empty)")
        print("2. Redeploy in Render")

if __name__ == "__main__":
    main()
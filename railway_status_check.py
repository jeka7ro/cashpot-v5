#!/usr/bin/env python3
"""
Railway Status Check - Monitor deployment and get correct URL
"""
import requests
import time
import os

def check_railway_deployment():
    print("🚀 Checking Railway deployment status...")
    
    # Common Railway URL patterns
    possible_urls = [
        "https://cashpot-v5-backend-production.up.railway.app",
        "https://cashpot-v5-backend.up.railway.app", 
        "https://cashpot-v5-production.up.railway.app",
        "https://cashpot-v5.up.railway.app"
    ]
    
    working_url = None
    
    for url in possible_urls:
        try:
            print(f"🔍 Testing: {url}")
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code == 200:
                print(f"✅ Working URL found: {url}")
                working_url = url
                break
            else:
                print(f"❌ Status {response.status_code}: {url}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {url} - {e}")
    
    if working_url:
        print(f"\n🎉 Railway backend is working at: {working_url}")
        print(f"\n📋 Next steps:")
        print(f"1. Update frontend/.env with: REACT_APP_BACKEND_URL={working_url}")
        print(f"2. Commit and push changes")
        print(f"3. GitHub Pages will redeploy automatically")
        
        # Update .env file if found
        env_file = "frontend/.env"
        if os.path.exists(env_file):
            print(f"\n🔧 Updating {env_file}...")
            with open(env_file, 'w') as f:
                f.write(f"REACT_APP_BACKEND_URL={working_url}\n")
                f.write("GENERATE_SOURCEMAP=false\n")
            print(f"✅ Updated {env_file}")
        
        return working_url
    else:
        print("\n⚠️  No working Railway URL found yet.")
        print("Railway deployment might still be in progress.")
        print("Please check Railway dashboard for the correct URL.")
        return None

if __name__ == "__main__":
    check_railway_deployment()

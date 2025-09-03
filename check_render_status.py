#!/usr/bin/env python3
"""
Script to check Render deployment status
"""

import requests
import json
import os
from datetime import datetime

def check_render_service(backend_url):
    """Check if Render service is online"""
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ Render backend: Online")
            return True
        else:
            print(f"⚠️  Render backend: Responding but status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print(f"⏰ Render backend: Timeout (service might be sleeping)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Render backend: Connection failed")
        return False
    except Exception as e:
        print(f"❌ Render backend: Error - {e}")
        return False

def check_github_pages(frontend_url):
    """Check if GitHub Pages is online"""
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ GitHub Pages: Online")
            return True
        else:
            print(f"⚠️  GitHub Pages: Responding but status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print(f"⏰ GitHub Pages: Timeout")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ GitHub Pages: Connection failed")
        return False
    except Exception as e:
        print(f"❌ GitHub Pages: Error - {e}")
        return False

def load_deployment_config():
    """Load deployment configuration if it exists"""
    config_file = "render_deployment_config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def save_deployment_config(config):
    """Save deployment configuration"""
    with open("render_deployment_config.json", 'w') as f:
        json.dump(config, f, indent=2)

def main():
    """Main status check function"""
    print("🔍 CASHPOT Render Deployment Status Check")
    print("=" * 50)
    
    # Load existing config or create new one
    config = load_deployment_config()
    
    if not config:
        print("📝 No deployment configuration found. Let's create one!")
        
        backend_url = input("Enter Render backend URL: ").strip()
        frontend_url = input("Enter GitHub Pages frontend URL (default: https://jeka7ro.github.io/cash-pot-v5-copy): ").strip()
        if not frontend_url:
            frontend_url = "https://jeka7ro.github.io/cash-pot-v5-copy"
        
        config = {
            "backend_url": backend_url,
            "frontend_url": frontend_url,
            "last_updated": datetime.now().isoformat()
        }
        
        save_deployment_config(config)
        print("✅ Configuration saved!")
    else:
        print("📋 Using existing configuration:")
        print(f"   Backend: {config.get('backend_url', 'Not set')}")
        print(f"   Frontend: {config.get('frontend_url', 'Not set')}")
        
        update = input("\nUpdate configuration? (y/n): ").strip().lower()
        if update == 'y':
            backend_url = input(f"Enter backend URL [{config.get('backend_url', '')}]: ").strip()
            frontend_url = input(f"Enter frontend URL [{config.get('frontend_url', '')}]: ").strip()
            
            if backend_url:
                config['backend_url'] = backend_url
            if frontend_url:
                config['frontend_url'] = frontend_url
            
            config['last_updated'] = datetime.now().isoformat()
            save_deployment_config(config)
            print("✅ Configuration updated!")
    
    print(f"\n🚀 Checking services...")
    print("-" * 30)
    
    # Check services
    services_online = 0
    total_services = 0
    
    # Check Render backend
    if config.get('backend_url'):
        total_services += 1
        if check_render_service(config['backend_url']):
            services_online += 1
    
    # Check GitHub Pages frontend
    if config.get('frontend_url'):
        total_services += 1
        if check_github_pages(config['frontend_url']):
            services_online += 1
    
    # Results
    print(f"\n📊 Status Summary: {services_online}/{total_services} services online")
    
    if services_online == total_services:
        print("🎉 All services are online!")
        print("\n🌐 Your CASHPOT application is fully operational!")
        print("👥 Multiple users can access the application")
        print("🗄️  Data is stored in the shared cloud database")
        
        print(f"\n🔗 Quick Links:")
        if config.get('frontend_url'):
            print(f"   Frontend: {config['frontend_url']}")
        if config.get('backend_url'):
            print(f"   Backend: {config['backend_url']}/api")
        
    else:
        print("⚠️  Some services are offline. Please check the issues above.")
        
        print(f"\n🔧 Troubleshooting:")
        print("1. Check if services are running")
        print("2. Verify URLs are correct")
        print("3. Check network connectivity")
        print("4. Review service logs")
        
        if config.get('backend_url'):
            print(f"\n💡 Render Backend Tips:")
            print("- Free tier sleeps after 15min inactivity")
            print("- First request after sleep takes longer")
            print("- Check Render dashboard for logs")
    
    # Additional information
    print(f"\n📋 Additional Information:")
    print(f"   Configuration file: render_deployment_config.json")
    print(f"   Last updated: {config.get('last_updated', 'Unknown')}")
    
    if config.get('backend_url'):
        print(f"\n🧪 Test Commands:")
        print(f"   Health check: curl {config['backend_url']}/api/health")
        print(f"   Test login: curl -X POST {config['backend_url']}/api/auth/login -H 'Content-Type: application/json' -d '{{\"username\":\"admin\",\"password\":\"admin123\"}}'")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script to check deployment status and provide quick access to all services
"""

import requests
import json
import os
from datetime import datetime

def check_service_status(url, service_name):
    """Check if a service is online"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: Online")
            return True
        else:
            print(f"⚠️  {service_name}: Responding but status {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print(f"⏰ {service_name}: Timeout")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {service_name}: Connection failed")
        return False
    except Exception as e:
        print(f"❌ {service_name}: Error - {e}")
        return False

def load_deployment_config():
    """Load deployment configuration if it exists"""
    config_file = "deployment_config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def save_deployment_config(config):
    """Save deployment configuration"""
    with open("deployment_config.json", 'w') as f:
        json.dump(config, f, indent=2)

def main():
    """Main status check function"""
    print("🔍 CASHPOT Deployment Status Check")
    print("=" * 50)
    
    # Load existing config or create new one
    config = load_deployment_config()
    
    if not config:
        print("📝 No deployment configuration found. Let's create one!")
        
        backend_url = input("Enter backend URL: ").strip()
        frontend_url = input("Enter frontend URL: ").strip()
        database_url = input("Enter database URL (optional): ").strip()
        
        config = {
            "backend_url": backend_url,
            "frontend_url": frontend_url,
            "database_url": database_url,
            "last_updated": datetime.now().isoformat()
        }
        
        save_deployment_config(config)
        print("✅ Configuration saved!")
    else:
        print("📋 Using existing configuration:")
        print(f"   Backend: {config.get('backend_url', 'Not set')}")
        print(f"   Frontend: {config.get('frontend_url', 'Not set')}")
        print(f"   Database: {config.get('database_url', 'Not set')}")
        
        update = input("\nUpdate configuration? (y/n): ").strip().lower()
        if update == 'y':
            backend_url = input(f"Enter backend URL [{config.get('backend_url', '')}]: ").strip()
            frontend_url = input(f"Enter frontend URL [{config.get('frontend_url', '')}]: ").strip()
            database_url = input(f"Enter database URL [{config.get('database_url', '')}]: ").strip()
            
            if backend_url:
                config['backend_url'] = backend_url
            if frontend_url:
                config['frontend_url'] = frontend_url
            if database_url:
                config['database_url'] = database_url
            
            config['last_updated'] = datetime.now().isoformat()
            save_deployment_config(config)
            print("✅ Configuration updated!")
    
    print(f"\n🚀 Checking services...")
    print("-" * 30)
    
    # Check services
    services_online = 0
    total_services = 0
    
    # Check backend
    if config.get('backend_url'):
        total_services += 1
        if check_service_status(config['backend_url'], "Backend"):
            services_online += 1
    
    # Check frontend
    if config.get('frontend_url'):
        total_services += 1
        if check_service_status(config['frontend_url'], "Frontend"):
            services_online += 1
    
    # Check database (if URL provided)
    if config.get('database_url'):
        total_services += 1
        if check_service_status(config['database_url'], "Database"):
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
            print(f"   Backend API: {config['backend_url']}/api")
        
    else:
        print("⚠️  Some services are offline. Please check the issues above.")
        
        print(f"\n🔧 Troubleshooting:")
        print("1. Check if services are running")
        print("2. Verify URLs are correct")
        print("3. Check network connectivity")
        print("4. Review service logs")
    
    # Additional information
    print(f"\n📋 Additional Information:")
    print(f"   Configuration file: deployment_config.json")
    print(f"   Last updated: {config.get('last_updated', 'Unknown')}")
    
    if config.get('backend_url'):
        print(f"\n🧪 Test Commands:")
        print(f"   Health check: curl {config['backend_url']}/api/health")
        print(f"   Test login: curl -X POST {config['backend_url']}/api/auth/login -H 'Content-Type: application/json' -d '{{\"username\":\"admin\",\"password\":\"password\"}}'")

if __name__ == "__main__":
    main()
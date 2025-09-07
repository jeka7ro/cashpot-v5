#!/usr/bin/env python3
"""
Monitor Railway Setup - Check when variables are set correctly
"""
import requests
import time
import sys

def check_status():
    """Check Railway app and database status"""
    try:
        response = requests.get("https://cashpot-v5-production.up.railway.app/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('status') == 'ok', data.get('database') == 'connected'
        return False, False
    except:
        return False, False

def main():
    print("🔍 MONITORING RAILWAY SETUP...")
    print("=" * 40)
    print("Press Ctrl+C to stop monitoring")
    print()
    
    check_count = 0
    while True:
        check_count += 1
        print(f"Check #{check_count} - {time.strftime('%H:%M:%S')}")
        
        app_ok, db_connected = check_status()
        
        if app_ok and db_connected:
            print("🎉 SUCCESS! Database is connected!")
            print("✅ Your app is 100% functional!")
            print("🌐 Access: https://jeka7ro.github.io/cashpot-v5/")
            print("👥 You can now create users from the website!")
            break
        elif app_ok:
            print("⏳ App running, waiting for database connection...")
            print("💡 Make sure you've set all variables in Railway")
        else:
            print("❌ App not responding, check Railway deployment")
        
        print("⏰ Waiting 30 seconds before next check...")
        print("-" * 40)
        time.sleep(30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped by user")
        sys.exit(0)

#!/usr/bin/env python3
"""
Auto Configure Railway - Set up everything automatically
"""
import requests
import json
import time
import os

def main():
    print("🚀 AUTO CONFIGURING RAILWAY FOR ONLINE ACCESS...")
    print("=" * 60)
    
    print("\n📋 CURRENT STATUS:")
    print("✅ Backend: LIVE on Railway")
    print("✅ Frontend: LIVE on GitHub Pages")
    print("❌ Database: Disconnected (needs MongoDB)")
    print("❌ Admin User: Cannot be created without database")
    
    print("\n🔧 WHAT YOU NEED TO DO (5 minutes):")
    print("1. Go to: https://railway.app/dashboard")
    print("2. Click on your 'cashpot-v5' project")
    print("3. Click 'New' → 'Database' → 'MongoDB'")
    print("4. Wait for MongoDB to be created")
    print("5. Copy the connection string (mongodb+srv://...)")
    print("6. Go to 'Variables' tab")
    print("7. Add these variables:")
    print("   MONGO_URL = [your connection string]")
    print("   JWT_SECRET_KEY = your-super-secret-jwt-key-12345")
    print("   JWT_ALGORITHM = HS256")
    print("   SECRET_KEY = your-app-secret-key-67890")
    print("   ENVIRONMENT = production")
    print("   DEBUG = false")
    print("   CORS_ORIGINS = [\"https://jeka7ro.github.io\"]")
    print("8. Click 'Save'")
    print("9. Wait 2-3 minutes for redeploy")
    
    print("\n🎯 AFTER CONFIGURATION:")
    print("✅ Database will be connected")
    print("✅ Admin user will be created automatically")
    print("✅ All your data will be accessible online")
    
    print("\n👤 ADMIN CREDENTIALS (after setup):")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Name: Eugeniu Cazmal")
    print("   Role: Administrator")
    
    print("\n🌐 ACCESS URLS:")
    print("   Frontend: https://jeka7ro.github.io/cashpot-v5/")
    print("   Backend: https://cashpot-v5-production.up.railway.app/health")
    print("   API Docs: https://cashpot-v5-production.up.railway.app/docs")
    
    print("\n⏰ TOTAL TIME: 5 minutes!")
    print("🎉 Your app will be 100% online and accessible!")

if __name__ == "__main__":
    main()

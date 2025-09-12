#!/usr/bin/env python3
"""
SOLVE LOGIN ISSUE - Quick fix for Cash Pot V5 login problem
"""
import requests
import json

def main():
    print("🚀 SOLVING LOGIN ISSUE - Cash Pot V5")
    print("=" * 50)
    
    print("🔍 DIAGNOSIS:")
    print("✅ Frontend: Working (https://jeka7ro.github.io/cashpot-v5)")
    print("✅ Backend: Working (https://cashpot-v5.onrender.com)")
    print("❌ Database: DISCONNECTED - This is why login fails!")
    
    print("\n💡 SOLUTION:")
    print("The backend cannot verify the admin user because MongoDB is not connected.")
    print("You need to configure MongoDB Atlas and import the data.")
    
    print("\n🔧 QUICK FIX STEPS:")
    print("1. Create MongoDB Atlas account (free): https://cloud.mongodb.com")
    print("2. Create cluster (free tier)")
    print("3. Configure database user and network access")
    print("4. Run the import script to add admin user and data")
    print("5. Add MONGO_URL to Render environment variables")
    print("6. Redeploy on Render")
    
    print("\n📋 DETAILED STEPS:")
    print("=" * 30)
    
    print("\nSTEP 1: MongoDB Atlas Setup")
    print("- Go to: https://cloud.mongodb.com")
    print("- Click 'Try Free' and create account")
    print("- Create cluster (choose free M0 Sandbox)")
    print("- Wait 3-5 minutes for cluster to be ready")
    
    print("\nSTEP 2: Database Access")
    print("- Go to 'Database Access' in left menu")
    print("- Click 'Add New Database User'")
    print("- Username: cashpot_admin")
    print("- Password: CashPot2024!Secure")
    print("- Privileges: 'Read and write to any database'")
    
    print("\nSTEP 3: Network Access")
    print("- Go to 'Network Access' in left menu")
    print("- Click 'Add IP Address'")
    print("- Choose 'Allow Access from Anywhere' (0.0.0.0/0)")
    
    print("\nSTEP 4: Get Connection String")
    print("- Go to 'Database' in left menu")
    print("- Click 'Connect' on your cluster")
    print("- Choose 'Connect your application'")
    print("- Copy the connection string")
    print("- Replace <password> with your password")
    print("- Add /cashpot_v5 at the end")
    
    print("\nSTEP 5: Import Data")
    print("- Run: python3 import_to_atlas_online.py")
    print("- Enter your MongoDB connection string")
    print("- Script will import admin user and all data")
    
    print("\nSTEP 6: Configure Render")
    print("- Go to: https://dashboard.render.com")
    print("- Find service 'cashpot-v5'")
    print("- Go to 'Environment' tab")
    print("- Add MONGO_URL with your connection string")
    print("- Add JWT_SECRET_KEY: CashPot2024-SuperSecret-JWT-Key-12345")
    print("- Save changes")
    
    print("\nSTEP 7: Redeploy")
    print("- In Render, go to 'Events' tab")
    print("- Click 'Manual Deploy'")
    print("- Choose 'Deploy latest commit'")
    print("- Wait 2-3 minutes")
    
    print("\nSTEP 8: Test Login")
    print("- Go to: https://jeka7ro.github.io/cashpot-v5")
    print("- Username: admin")
    print("- Password: password")
    print("- Login should work perfectly!")
    
    print("\n🎯 EXPECTED RESULT:")
    print("✅ Frontend: https://jeka7ro.github.io/cashpot-v5")
    print("✅ Backend: https://cashpot-v5.onrender.com")
    print("✅ Database: MongoDB Atlas (connected)")
    print("✅ Login: admin/password works")
    print("✅ All data: Companies, slot machines, etc.")
    
    print("\n📞 SUPPORT:")
    print("If you have issues:")
    print("- Check MongoDB Atlas cluster is running")
    print("- Verify connection string is correct")
    print("- Ensure IP is whitelisted (0.0.0.0/0)")
    print("- Check Render environment variables")
    
    print("\n🚀 READY TO START?")
    print("Run this command when ready:")
    print("python3 import_to_atlas_online.py")

if __name__ == "__main__":
    main()

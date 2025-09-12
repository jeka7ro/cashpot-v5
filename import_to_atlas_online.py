#!/usr/bin/env python3
"""
Import to MongoDB Atlas Online - Run this after setting up MongoDB Atlas
"""
import json
import os
import sys
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def import_to_atlas():
    print("🚀 Importing all data to MongoDB Atlas...")
    
    # Get MongoDB Atlas connection string
    mongo_url = input("🔗 Enter your MongoDB Atlas connection string: ").strip()
    
    if not mongo_url:
        print("❌ No connection string provided!")
        return False
    
    # Ensure the connection string has the database name
    if "/cashpot_v5?" not in mongo_url:
        if mongo_url.endswith("/"):
            mongo_url += "cashpot_v5?retryWrites=true&w=majority"
        elif "?" in mongo_url:
            mongo_url = mongo_url.replace("?", "/cashpot_v5?")
        else:
            mongo_url += "/cashpot_v5?retryWrites=true&w=majority"
    
    print(f"📊 Using connection: {mongo_url}")
    
    try:
        # Connect to MongoDB Atlas
        client = AsyncIOMotorClient(mongo_url)
        db = client['cashpot_v5']
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas: {e}")
        print("\n💡 Make sure:")
        print("1. Your connection string is correct")
        print("2. Your IP is whitelisted (0.0.0.0/0)")
        print("3. Your database user has read/write permissions")
        return False
    
    # Import all data
    success_count = 0
    total_imports = 0
    
    # Read all_your_data.json
    if os.path.exists("all_your_data.json"):
        print("\n📥 Importing from all_your_data.json...")
        try:
            with open("all_your_data.json", 'r', encoding='utf-8') as f:
                all_data = json.load(f)
            
            collections_to_import = ['companies', 'locations', 'providers', 'slot_machines', 'game_mixes', 'cabinets', 'invoices', 'jackpots']
            
            for collection_name in collections_to_import:
                if collection_name in all_data and all_data[collection_name]:
                    collection = db[collection_name]
                    
                    # Clear existing data
                    await collection.delete_many({})
                    print(f"🗑️  Cleared existing {collection_name} data")
                    
                    # Insert new data
                    data = all_data[collection_name]
                    for item in data:
                        if 'created_at' not in item:
                            item['created_at'] = datetime.now().isoformat()
                    
                    result = await collection.insert_many(data)
                    print(f"✅ Imported {len(result.inserted_ids)} {collection_name} records")
                    success_count += 1
                
                total_imports += 1
            
        except Exception as e:
            print(f"❌ Error importing from all_your_data.json: {e}")
    
    # Import from individual export files
    export_files = {
        'companies': 'companies_export.json',
        'locations': 'locations_export.json', 
        'providers': 'providers_export.json',
        'slot_machines': 'slot_machines_export.json',
        'game_mixes': 'game_mixes_export.json',
        'cabinets': 'cabinets_export.json',
        'invoices': 'invoices_export.json',
        'jackpots': 'jackpots_export.json'
    }
    
    for collection_name, filename in export_files.items():
        if os.path.exists(filename):
            print(f"\n📥 Importing {collection_name} from {filename}...")
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                collection = db[collection_name]
                await collection.delete_many({})
                
                for item in data:
                    if 'created_at' not in item:
                        item['created_at'] = datetime.now().isoformat()
                
                result = await collection.insert_many(data)
                print(f"✅ Imported {len(result.inserted_ids)} {collection_name} records")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Error importing {collection_name}: {e}")
            
            total_imports += 1
    
    # Create admin user
    print("\n👤 Creating admin user...")
    try:
        users_collection = db['users']
        admin_user = await users_collection.find_one({"username": "admin"})
        
        if not admin_user:
            admin_data = {
                "username": "admin",
                "email": "admin@cashpot.ro",
                "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j7pN7K5r6",  # "password"
                "role": "admin",
                "first_name": "Admin",
                "last_name": "User",
                "phone": "+40 123 456 789",
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "created_by": "system"
            }
            result = await users_collection.insert_one(admin_data)
            print(f"✅ Created admin user with ID: {result.inserted_id}")
        else:
            print("✅ Admin user already exists")
        
        success_count += 1
        total_imports += 1
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    
    # Summary
    print(f"\n🎉 Import completed!")
    print(f"✅ Successfully imported: {success_count}/{total_imports} collections")
    
    if success_count > 0:
        print("\n📋 Summary of imported data:")
        
        collections_to_check = ['companies', 'locations', 'providers', 'slot_machines', 'game_mixes', 'cabinets', 'invoices', 'jackpots', 'users']
        
        for collection_name in collections_to_check:
            try:
                collection = db[collection_name]
                count = await collection.count_documents({})
                print(f"   📊 {collection_name}: {count} records")
            except:
                print(f"   📊 {collection_name}: 0 records")
        
        print(f"\n🌍 Your Cash Pot V5 application is now fully populated!")
        print(f"🔗 Frontend: https://jeka7ro.github.io/cashpot-v5")
        print(f"🔗 Backend: https://cashpot-v5.onrender.com")
        print(f"🔗 Database: MongoDB Atlas (cashpot_v5)")
        
        print(f"\n📋 Next steps:")
        print(f"1. Add MONGO_URL to Render environment variables:")
        print(f"   MONGO_URL={mongo_url}")
        print(f"2. Add JWT_SECRET_KEY to Render environment variables:")
        print(f"   JWT_SECRET_KEY=CashPot2024-SuperSecret-JWT-Key-12345")
        print(f"3. Redeploy on Render")
        print(f"4. Your application will work perfectly!")
        
    else:
        print(f"❌ No data was imported. Check the errors above.")
    
    # Close connection
    client.close()
    return success_count > 0

def main():
    print("🚀 Cash Pot V5 - MongoDB Atlas Import")
    print("=" * 40)
    print("This script will import all your data to MongoDB Atlas")
    print("Make sure you have:")
    print("1. Created a MongoDB Atlas cluster")
    print("2. Created a database user with read/write permissions")
    print("3. Whitelisted your IP (0.0.0.0/0)")
    print()
    
    success = asyncio.run(import_to_atlas())
    
    if success:
        print("\n✅ Import completed successfully!")
        print("🎊 Your Cash Pot V5 application is ready!")
        sys.exit(0)
    else:
        print("\n❌ Import failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

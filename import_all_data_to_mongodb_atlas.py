#!/usr/bin/env python3
"""
Import All Data to MongoDB Atlas - Complete database import script
"""
import json
import os
import sys
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from bson import ObjectId

# Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "cashpot_v5")

async def import_all_data():
    print("🚀 Starting complete data import to MongoDB Atlas...")
    print(f"📊 Database: {DB_NAME}")
    print(f"🔗 Connection: {MONGO_URL}")
    
    # Connect to MongoDB
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("\n💡 Make sure you have:")
        print("1. Created MongoDB Atlas cluster")
        print("2. Added MONGO_URL to Render environment variables")
        print("3. Configured Network Access (0.0.0.0/0)")
        return False
    
    # Import functions for each collection
    async def import_collection(collection_name, data_file, transform_func=None):
        try:
            print(f"\n📥 Importing {collection_name}...")
            
            # Read data file
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Transform data if needed
            if transform_func:
                data = transform_func(data)
            
            # Clear existing data
            collection = db[collection_name]
            await collection.delete_many({})
            print(f"🗑️  Cleared existing {collection_name} data")
            
            # Insert new data
            if isinstance(data, list) and data:
                result = await collection.insert_many(data)
                print(f"✅ Imported {len(result.inserted_ids)} {collection_name} records")
            elif isinstance(data, dict):
                result = await collection.insert_one(data)
                print(f"✅ Imported 1 {collection_name} record")
            else:
                print(f"⚠️  No data found in {collection_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error importing {collection_name}: {e}")
            return False
    
    # Transform functions
    def transform_users(data):
        """Transform users data"""
        for user in data:
            # Ensure required fields
            if 'password' not in user:
                user['password'] = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4j7pN7K5r6'  # "password"
            if 'role' not in user:
                user['role'] = 'user'
            if 'created_at' not in user:
                user['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_companies(data):
        """Transform companies data"""
        for company in data:
            if 'created_at' not in company:
                company['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_locations(data):
        """Transform locations data"""
        for location in data:
            if 'created_at' not in location:
                location['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_providers(data):
        """Transform providers data"""
        for provider in data:
            if 'created_at' not in provider:
                provider['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_slot_machines(data):
        """Transform slot machines data"""
        for machine in data:
            if 'created_at' not in machine:
                machine['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_game_mixes(data):
        """Transform game mixes data"""
        for mix in data:
            if 'created_at' not in mix:
                mix['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_cabinets(data):
        """Transform cabinets data"""
        for cabinet in data:
            if 'created_at' not in cabinet:
                cabinet['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_invoices(data):
        """Transform invoices data"""
        for invoice in data:
            if 'created_at' not in invoice:
                invoice['created_at'] = datetime.now().isoformat()
        return data
    
    def transform_jackpots(data):
        """Transform jackpots data"""
        for jackpot in data:
            if 'created_at' not in jackpot:
                jackpot['created_at'] = datetime.now().isoformat()
        return data
    
    # Import all collections
    success_count = 0
    total_collections = 0
    
    # Define import tasks
    import_tasks = [
        ("companies", "companies_export.json", transform_companies),
        ("locations", "locations_export.json", transform_locations),
        ("providers", "providers_export.json", transform_providers),
        ("slot_machines", "slot_machines_export.json", transform_slot_machines),
        ("game_mixes", "game_mixes_export.json", transform_game_mixes),
        ("cabinets", "cabinets_export.json", transform_cabinets),
        ("invoices", "invoices_export.json", transform_invoices),
        ("jackpots", "jackpots_export.json", transform_jackpots),
    ]
    
    # Import from all_your_data.json if it exists
    if os.path.exists("all_your_data.json"):
        print("\n📥 Importing from all_your_data.json...")
        try:
            with open("all_your_data.json", 'r', encoding='utf-8') as f:
                all_data = json.load(f)
            
            # Import each collection from all_data
            for collection_name in ['companies', 'locations', 'providers', 'slot_machines', 'game_mixes', 'cabinets', 'invoices', 'jackpots']:
                if collection_name in all_data and all_data[collection_name]:
                    collection = db[collection_name]
                    await collection.delete_many({})
                    
                    data = all_data[collection_name]
                    if collection_name == 'companies':
                        data = transform_companies(data)
                    elif collection_name == 'locations':
                        data = transform_locations(data)
                    elif collection_name == 'providers':
                        data = transform_providers(data)
                    elif collection_name == 'slot_machines':
                        data = transform_slot_machines(data)
                    elif collection_name == 'game_mixes':
                        data = transform_game_mixes(data)
                    elif collection_name == 'cabinets':
                        data = transform_cabinets(data)
                    elif collection_name == 'invoices':
                        data = transform_invoices(data)
                    elif collection_name == 'jackpots':
                        data = transform_jackpots(data)
                    
                    result = await collection.insert_many(data)
                    print(f"✅ Imported {len(result.inserted_ids)} {collection_name} records from all_your_data.json")
                    success_count += 1
                    total_collections += 1
            
        except Exception as e:
            print(f"❌ Error importing from all_your_data.json: {e}")
    
    # Import from individual export files
    for collection_name, data_file, transform_func in import_tasks:
        if os.path.exists(data_file):
            total_collections += 1
            success = await import_collection(collection_name, data_file, transform_func)
            if success:
                success_count += 1
    
    # Create admin user if not exists
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
        total_collections += 1
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    
    # Summary
    print(f"\n🎉 Import completed!")
    print(f"✅ Successfully imported: {success_count}/{total_collections} collections")
    
    if success_count == total_collections:
        print("🎊 All data imported successfully!")
        print("\n📋 Summary of imported data:")
        
        # Count records in each collection
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
        print(f"🔗 Database: MongoDB Atlas ({DB_NAME})")
        
    else:
        print(f"⚠️  Some collections failed to import. Check the errors above.")
    
    # Close connection
    client.close()
    return success_count == total_collections

def main():
    print("🚀 Cash Pot V5 - Complete Database Import")
    print("=" * 50)
    
    # Check if we're running on Render or locally
    if os.getenv("RENDER"):
        print("🌐 Running on Render - importing to MongoDB Atlas")
    else:
        print("💻 Running locally - importing to local MongoDB")
    
    # Run the import
    success = asyncio.run(import_all_data())
    
    if success:
        print("\n✅ Import completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Import failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

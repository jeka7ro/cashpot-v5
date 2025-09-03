#!/usr/bin/env python3
"""
Script to import data from JSON files to MongoDB Atlas
This will help migrate data from local MongoDB to cloud
"""

import json
import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def import_collection(collection, filename):
    """Import a collection from JSON file"""
    print(f"Importing {filename}...")
    
    if not os.path.exists(filename):
        print(f"⚠️  File {filename} not found, skipping...")
        return 0
    
    # Read JSON file
    with open(filename, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    if not documents:
        print(f"⚠️  No documents in {filename}, skipping...")
        return 0
    
    # Clear existing collection
    collection.delete_many({})
    print(f"🗑️  Cleared existing data in {collection.name}")
    
    # Insert documents
    try:
        result = collection.insert_many(documents)
        print(f"✅ Imported {len(result.inserted_ids)} documents to {collection.name}")
        return len(result.inserted_ids)
    except Exception as e:
        print(f"❌ Error importing to {collection.name}: {e}")
        return 0

def main():
    """Main import function"""
    print("🚀 Starting data import to MongoDB Atlas...")
    
    # Get MongoDB Atlas connection string from environment
    MONGO_URL = os.environ.get('MONGO_URL')
    DB_NAME = os.environ.get('DB_NAME', 'casino_management')
    
    if not MONGO_URL:
        print("❌ Error: MONGO_URL environment variable not set!")
        print("Please set MONGO_URL to your MongoDB Atlas connection string")
        print("Example: export MONGO_URL='mongodb+srv://username:password@cluster.mongodb.net/'")
        return
    
    # Connect to MongoDB Atlas
    try:
        client = MongoClient(MONGO_URL)
        db = client[DB_NAME]
        # Test connection
        client.admin.command('ping')
        print(f"✅ Connected to MongoDB Atlas: {DB_NAME}")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB Atlas: {e}")
        return
    
    # Check if exports directory exists
    if not os.path.exists('exports'):
        print("❌ Error: exports/ directory not found!")
        print("Please run export_data.py first to create the data files")
        return
    
    # List of collections to import
    collections_to_import = [
        'users',
        'companies', 
        'locations',
        'providers',
        'cabinets',
        'game_mixes',
        'slot_machines',
        'jackpots',
        'invoices',
        'onjn_reports',
        'legal_documents',
        'marketing_campaigns',
        'metrology',
        'comision_dates'
    ]
    
    # Import each collection
    imported_count = 0
    total_documents = 0
    
    for collection_name in collections_to_import:
        try:
            collection = db[collection_name]
            filename = f'exports/{collection_name}.json'
            doc_count = import_collection(collection, filename)
            if doc_count > 0:
                imported_count += 1
                total_documents += doc_count
        except Exception as e:
            print(f"❌ Error importing {collection_name}: {e}")
    
    # Create import summary
    summary = {
        "import_date": datetime.now().isoformat(),
        "database": DB_NAME,
        "collections_imported": imported_count,
        "total_documents": total_documents,
        "collections": collections_to_import
    }
    
    with open('exports/import_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=json_serial)
    
    print(f"\n🎉 Import completed!")
    print(f"📊 Imported {imported_count} collections")
    print(f"📄 Total documents: {total_documents}")
    print(f"📁 Summary saved: exports/import_summary.json")
    
    client.close()

if __name__ == "__main__":
    main()

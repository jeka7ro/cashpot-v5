#!/usr/bin/env python3
"""
Script to backup data from MongoDB Atlas
This will help you create regular backups of your cloud data
"""

import json
import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def backup_collection(collection, filename):
    """Backup a collection to JSON file"""
    print(f"Backing up {collection.name}...")
    
    # Get all documents
    documents = list(collection.find())
    
    # Convert to JSON
    json_data = []
    for doc in documents:
        # Convert ObjectId to string
        doc_str = dumps(doc)
        doc_dict = json.loads(doc_str)
        json_data.append(doc_dict)
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False, default=json_serial)
    
    print(f"✅ Backed up {len(documents)} documents to {filename}")

def main():
    """Main backup function"""
    print("💾 Starting data backup from MongoDB Atlas...")
    
    # Get MongoDB Atlas connection string from environment
    MONGO_URL = os.environ.get('MONGO_URL')
    DB_NAME = os.environ.get('DB_NAME', 'casino_management')
    
    if not MONGO_URL:
        print("❌ Error: MONGO_URL environment variable not set!")
        print("Please set MONGO_URL to your MongoDB Atlas connection string")
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
    
    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f'backups/backup_{timestamp}'
    os.makedirs(backup_dir, exist_ok=True)
    
    # List of collections to backup
    collections_to_backup = [
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
    
    # Backup each collection
    backed_up_count = 0
    total_documents = 0
    
    for collection_name in collections_to_backup:
        try:
            collection = db[collection_name]
            if collection.count_documents({}) > 0:  # Only backup if collection has data
                filename = f'{backup_dir}/{collection_name}.json'
                backup_collection(collection, filename)
                backed_up_count += 1
                total_documents += collection.count_documents({})
            else:
                print(f"⚠️  Collection {collection_name} is empty, skipping...")
        except Exception as e:
            print(f"❌ Error backing up {collection_name}: {e}")
    
    # Create backup summary
    summary = {
        "backup_date": datetime.now().isoformat(),
        "database": DB_NAME,
        "collections_backed_up": backed_up_count,
        "total_documents": total_documents,
        "collections": collections_to_backup,
        "backup_directory": backup_dir
    }
    
    with open(f'{backup_dir}/backup_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=json_serial)
    
    print(f"\n🎉 Backup completed!")
    print(f"📊 Backed up {backed_up_count} collections")
    print(f"📄 Total documents: {total_documents}")
    print(f"📁 Backup saved in: {backup_dir}")
    print(f"📋 Summary: {backup_dir}/backup_summary.json")
    
    client.close()

if __name__ == "__main__":
    main()

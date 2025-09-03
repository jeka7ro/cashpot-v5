#!/usr/bin/env python3
"""
Script to export all data from local MongoDB to JSON files
This will help migrate data to MongoDB Atlas
"""

import json
import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'casino_management')

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def export_collection(collection, filename):
    """Export a collection to JSON file"""
    print(f"Exporting {collection.name}...")
    
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
    
    print(f"✅ Exported {len(documents)} documents to {filename}")

def main():
    """Main export function"""
    print("🚀 Starting data export from local MongoDB...")
    
    # Connect to MongoDB
    try:
        client = MongoClient(MONGO_URL)
        db = client[DB_NAME]
        print(f"✅ Connected to MongoDB: {DB_NAME}")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        return
    
    # Create exports directory
    os.makedirs('exports', exist_ok=True)
    
    # List of collections to export
    collections_to_export = [
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
    
    # Export each collection
    exported_count = 0
    for collection_name in collections_to_export:
        try:
            collection = db[collection_name]
            if collection.count_documents({}) > 0:  # Only export if collection has data
                export_collection(collection, f'exports/{collection_name}.json')
                exported_count += 1
            else:
                print(f"⚠️  Collection {collection_name} is empty, skipping...")
        except Exception as e:
            print(f"❌ Error exporting {collection_name}: {e}")
    
    # Create summary
    summary = {
        "export_date": datetime.now().isoformat(),
        "database": DB_NAME,
        "collections_exported": exported_count,
        "collections": collections_to_export
    }
    
    with open('exports/export_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=json_serial)
    
    print(f"\n🎉 Export completed!")
    print(f"📊 Exported {exported_count} collections")
    print(f"📁 Files saved in: exports/")
    print(f"📋 Summary: exports/export_summary.json")
    
    client.close()

if __name__ == "__main__":
    main()

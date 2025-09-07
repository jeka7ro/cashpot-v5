#!/usr/bin/env python3
"""
Export all data from casino_management database to Railway
"""

import pymongo
import requests
import json
from bson import ObjectId
from datetime import datetime

def login_railway():
    """Login to Railway and get token"""
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = requests.post('https://cashpot-v5-production.up.railway.app/api/auth/login', json=login_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def convert_objectid_to_str(data):
    """Convert ObjectId and datetime to strings"""
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data

def export_and_import_data():
    """Export data from casino_management and import to Railway"""
    
    # Connect to local MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['casino_management']
    
    print('🔍 Exporting data from casino_management database...')
    
    # Login to Railway
    token = login_railway()
    if not token:
        print('❌ Railway login failed')
        return
    
    print('✅ Logged in to Railway')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # Define collections to export (in order of dependencies)
    collections = [
        'companies',
        'providers', 
        'locations',
        'cabinets',
        'game_mixes',
        'slot_machines',
        'invoices',
        'jackpots'
    ]
    
    for collection_name in collections:
        print(f'\\n📊 Processing {collection_name}...')
        
        # Get data from local database
        local_data = list(db[collection_name].find())
        print(f'Found {len(local_data)} {collection_name} locally')
        
        if not local_data:
            print(f'⚠️  No {collection_name} found locally')
            continue
        
        # Convert ObjectId and datetime to strings
        local_data = convert_objectid_to_str(local_data)
        
        # Save to JSON file
        filename = f'{collection_name}_export.json'
        with open(filename, 'w') as f:
            json.dump(local_data, f, indent=2, default=str)
        print(f'✅ Exported to {filename}')
        
        # Import to Railway
        success_count = 0
        for i, item in enumerate(local_data):
            try:
                # Remove _id field for Railway
                item_data = {k: v for k, v in item.items() if k != '_id'}
                
                response = requests.post(
                    f'https://cashpot-v5-production.up.railway.app/api/{collection_name.replace("_", "-")}',
                    json=item_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    success_count += 1
                    print(f'  ✅ {i+1}/{len(local_data)} imported')
                else:
                    print(f'  ❌ {i+1}/{len(local_data)} failed: {response.status_code}')
                    if response.status_code == 400:
                        print(f'     Error: {response.text[:200]}')
                
            except Exception as e:
                print(f'  ❌ {i+1}/{len(local_data)} error: {str(e)}')
        
        print(f'🎉 Imported {success_count}/{len(local_data)} {collection_name}')
    
    client.close()
    print('\\n✅ Export and import completed!')

if __name__ == "__main__":
    export_and_import_data()

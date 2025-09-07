#!/usr/bin/env python3
"""
Export slot machines from local MongoDB to Railway
"""

import pymongo
import requests
import json
from bson import ObjectId
from datetime import datetime

def export_slot_machines():
    """Export slot machines from local to Railway"""
    
    # Connect to local MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['cash_pot']
    
    print('🔍 Exporting slot machines from local database...')
    
    # Get slot machines
    slot_machines = list(db.slot_machines.find())
    print(f'Found {len(slot_machines)} slot machines locally')
    
    if not slot_machines:
        print('❌ No slot machines found locally')
        return
    
    # Convert ObjectId and datetime to strings
    for slot in slot_machines:
        if '_id' in slot:
            slot['_id'] = str(slot['_id'])
        if 'created_at' in slot and slot['created_at']:
            if isinstance(slot['created_at'], datetime):
                slot['created_at'] = slot['created_at'].isoformat()
    
    # Save to JSON file
    with open('slot_machines_export.json', 'w') as f:
        json.dump(slot_machines, f, indent=2, default=str)
    
    print(f'✅ Exported {len(slot_machines)} slot machines to slot_machines_export.json')
    
    # Show details
    for i, slot in enumerate(slot_machines):
        print(f'  {i+1}. {slot.get("name", "N/A")} (ID: {slot.get("id", "N/A")})')
        print(f'     Provider: {slot.get("provider_name", "N/A")}')
        print(f'     Location: {slot.get("location_name", "N/A")}')
        print(f'     Status: {slot.get("status", "N/A")}')
    
    client.close()
    return slot_machines

if __name__ == "__main__":
    export_slot_machines()

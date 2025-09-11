#!/usr/bin/env python3
"""
Import ALL slot machines from Google Sheets (310 slots)
Reads directly from Google Sheets API
"""

import asyncio
import motor.motor_asyncio
import requests
import json
from datetime import datetime
import uuid

# Google Sheets API URL
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1XlGcJxJ6DqL7bd6mVnys_8XamUB9pl1ZKSBd8YLClCU/export?format=csv&gid=0"

async def get_google_sheets_data():
    """Fetch data from Google Sheets"""
    try:
        response = requests.get(GOOGLE_SHEETS_URL)
        response.raise_for_status()
        
        lines = response.text.strip().split('\n')
        headers = lines[0].split(',')
        
        data = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                values = line.split(',')
                if len(values) >= 6:  # Ensure we have all required columns
                    row_data = {
                        'Locație': values[0].strip('"'),
                        'Poziție': values[1].strip('"'),
                        'Nr. serie': values[2].strip('"'),
                        'Producător': values[3].strip('"'),
                        'Tip cabinet': values[4].strip('"'),
                        'Mix': values[5].strip('"')
                    }
                    data.append(row_data)
        
        print(f"📊 Fetched {len(data)} rows from Google Sheets")
        return data
    except Exception as e:
        print(f"❌ Error fetching Google Sheets data: {e}")
        return []

async def get_or_create_entity(db, collection, name_field, entity_data, entity_type):
    """Get existing entity or create new one"""
    existing = await db[collection].find_one({name_field: entity_data[name_field]})
    if existing:
        print(f"✅ Found existing {entity_type}: {entity_data[name_field]}")
        return existing['id']
    else:
        entity_id = str(uuid.uuid4())
        entity_data['id'] = entity_id
        entity_data['created_at'] = datetime.utcnow()
        await db[collection].insert_one(entity_data)
        print(f"➕ Created new {entity_type}: {entity_data[name_field]} (ID: {entity_id})")
        return entity_id

async def import_all_slots():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cashpot_v5
    
    print("🚀 Starting FULL Google Sheets import...")
    
    # Get data from Google Sheets
    slots_data = await get_google_sheets_data()
    if not slots_data:
        print("❌ No data fetched from Google Sheets")
        return
    
    # Clear existing slots
    print("🗑️ Clearing existing slots...")
    await db.slot_machines.delete_many({})
    
    # Create a default company if none exists
    company = await db.companies.find_one({})
    if not company:
        company_id = str(uuid.uuid4())
        company_data = {
            'id': company_id,
            'name': 'Default Company',
            'email': 'admin@company.com',
            'phone': '',
            'address': '',
            'created_at': datetime.utcnow(),
            'is_active': True
        }
        await db.companies.insert_one(company_data)
        print(f"➕ Created default company: {company_id}")
    else:
        company_id = company['id']
        print(f"✅ Using existing company: {company['name']}")
    
    # Process each slot
    slots_created = 0
    for i, slot_data in enumerate(slots_data, 1):
        try:
            # Get or create location
            location_id = await get_or_create_entity(db, 'locations', 'name', {
                'name': slot_data['Locație'],
                'address': f"Address for {slot_data['Locație']}",
                'company_id': company_id,
                'is_active': True
            }, 'location')
            
            # Get or create provider
            provider_id = await get_or_create_entity(db, 'providers', 'name', {
                'name': slot_data['Producător'],
                'email': f"{slot_data['Producător'].lower()}@provider.com",
                'phone': '',
                'is_active': True
            }, 'provider')
            
            # Get or create cabinet
            cabinet_id = await get_or_create_entity(db, 'cabinets', 'name', {
                'name': slot_data['Tip cabinet'],
                'model': slot_data['Tip cabinet'],
                'provider_id': provider_id,
                'is_active': True
            }, 'cabinet')
            
            # Get or create game mix
            game_mix_id = await get_or_create_entity(db, 'game_mixes', 'name', {
                'name': slot_data['Mix'],
                'provider_id': provider_id,
                'is_active': True
            }, 'game mix')
            
            # Create slot machine
            slot_id = str(uuid.uuid4())
            slot = {
                'id': slot_id,
                'serial_number': slot_data['Nr. serie'],
                'provider_id': provider_id,
                'cabinet_id': cabinet_id,
                'game_mix_id': game_mix_id,
                'location_id': location_id,
                'position': slot_data['Poziție'],
                'status': 'active',
                'is_active': True,
                'created_at': datetime.utcnow(),
                'production_year': 2024,
                'ownership_type': 'owned',
                'model': slot_data['Tip cabinet']
            }
            
            await db.slot_machines.insert_one(slot)
            slots_created += 1
            
            if i % 50 == 0:  # Progress every 50 slots
                print(f"📈 Progress: {i}/{len(slots_data)} slots processed...")
            
        except Exception as e:
            print(f"❌ Error creating slot {slot_data.get('Nr. serie', 'Unknown')}: {e}")
    
    print(f"\n✅ Import completed!")
    print(f"📊 Created {slots_created} slot machines")
    
    # Show summary
    total_slots = await db.slot_machines.count_documents({})
    total_locations = await db.locations.count_documents({})
    total_providers = await db.providers.count_documents({})
    total_cabinets = await db.cabinets.count_documents({})
    total_game_mixes = await db.game_mixes.count_documents({})
    
    print(f"\n📈 Database summary:")
    print(f"   🎰 Slot Machines: {total_slots}")
    print(f"   📍 Locations: {total_locations}")
    print(f"   🏢 Providers: {total_providers}")
    print(f"   🏗️ Cabinets: {total_cabinets}")
    print(f"   🎮 Game Mixes: {total_game_mixes}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(import_all_slots())

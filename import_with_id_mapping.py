#!/usr/bin/env python3
"""
Import data with ID mapping to Railway
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

def get_railway_ids(token):
    """Get existing IDs from Railway"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Get companies
    companies = requests.get('https://cashpot-v5-production.up.railway.app/api/companies', headers=headers).json()
    company_map = {company['name']: company['id'] for company in companies}
    
    # Get providers
    providers = requests.get('https://cashpot-v5-production.up.railway.app/api/providers', headers=headers).json()
    provider_map = {provider['name']: provider['id'] for provider in providers}
    
    # Get locations
    locations = requests.get('https://cashpot-v5-production.up.railway.app/api/locations', headers=headers).json()
    location_map = {location['name']: location['id'] for location in locations}
    
    return company_map, provider_map, location_map

def import_data_with_mapping():
    """Import data with ID mapping"""
    
    # Connect to local MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['casino_management']
    
    print('🔍 Importing data with ID mapping...')
    
    # Login to Railway
    token = login_railway()
    if not token:
        print('❌ Railway login failed')
        return
    
    print('✅ Logged in to Railway')
    
    # Get existing IDs from Railway
    company_map, provider_map, location_map = get_railway_ids(token)
    
    print(f'📋 Found {len(company_map)} companies, {len(provider_map)} providers, {len(location_map)} locations on Railway')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # Import cabinets first
    print('\\n📊 Importing cabinets...')
    cabinets = list(db.cabinets.find())
    cabinet_id_map = {}
    
    for cabinet in cabinets:
        cabinet_data = convert_objectid_to_str(cabinet)
        
        # Map provider_id
        provider_name = cabinet_data.get('provider_name', '')
        if provider_name in provider_map:
            cabinet_data['provider_id'] = provider_map[provider_name]
        else:
            print(f'⚠️  Provider {provider_name} not found, skipping cabinet')
            continue
        
        # Map location_id
        location_name = cabinet_data.get('location_name', '')
        if location_name in location_map:
            cabinet_data['location_id'] = location_map[location_name]
        else:
            print(f'⚠️  Location {location_name} not found, skipping cabinet')
            continue
        
        # Remove old fields
        cabinet_data = {k: v for k, v in cabinet_data.items() if k not in ['_id', 'provider_name', 'location_name']}
        
        try:
            response = requests.post(
                'https://cashpot-v5-production.up.railway.app/api/cabinets',
                json=cabinet_data,
                headers=headers
            )
            
            if response.status_code == 200:
                new_cabinet = response.json()
                cabinet_id_map[cabinet['id']] = new_cabinet['id']
                print(f'✅ Cabinet {cabinet_data.get("name", "N/A")} imported')
            else:
                print(f'❌ Cabinet failed: {response.status_code}')
        except Exception as e:
            print(f'❌ Cabinet error: {str(e)}')
    
    print(f'🎉 Imported {len(cabinet_id_map)} cabinets')
    
    # Import game mixes
    print('\\n📊 Importing game mixes...')
    game_mixes = list(db.game_mixes.find())
    game_mix_id_map = {}
    
    for game_mix in game_mixes:
        game_mix_data = convert_objectid_to_str(game_mix)
        
        # Map provider_id
        provider_name = game_mix_data.get('provider_name', '')
        if provider_name in provider_map:
            game_mix_data['provider_id'] = provider_map[provider_name]
        else:
            print(f'⚠️  Provider {provider_name} not found, skipping game mix')
            continue
        
        # Remove old fields
        game_mix_data = {k: v for k, v in game_mix_data.items() if k not in ['_id', 'provider_name']}
        
        try:
            response = requests.post(
                'https://cashpot-v5-production.up.railway.app/api/game-mixes',
                json=game_mix_data,
                headers=headers
            )
            
            if response.status_code == 200:
                new_game_mix = response.json()
                game_mix_id_map[game_mix['id']] = new_game_mix['id']
                print(f'✅ Game mix {game_mix_data.get("name", "N/A")} imported')
            else:
                print(f'❌ Game mix failed: {response.status_code}')
        except Exception as e:
            print(f'❌ Game mix error: {str(e)}')
    
    print(f'🎉 Imported {len(game_mix_id_map)} game mixes')
    
    # Import slot machines
    print('\\n📊 Importing slot machines...')
    slot_machines = list(db.slot_machines.find())
    success_count = 0
    
    for slot in slot_machines:
        slot_data = convert_objectid_to_str(slot)
        
        # Map cabinet_id
        cabinet_id = slot_data.get('cabinet_id')
        if cabinet_id in cabinet_id_map:
            slot_data['cabinet_id'] = cabinet_id_map[cabinet_id]
        else:
            print(f'⚠️  Cabinet {cabinet_id} not found, skipping slot machine')
            continue
        
        # Map game_mix_id
        game_mix_id = slot_data.get('game_mix_id')
        if game_mix_id in game_mix_id_map:
            slot_data['game_mix_id'] = game_mix_id_map[game_mix_id]
        else:
            print(f'⚠️  Game mix {game_mix_id} not found, skipping slot machine')
            continue
        
        # Map provider_id
        provider_name = slot_data.get('provider_name', '')
        if provider_name in provider_map:
            slot_data['provider_id'] = provider_map[provider_name]
        else:
            print(f'⚠️  Provider {provider_name} not found, skipping slot machine')
            continue
        
        # Remove old fields
        slot_data = {k: v for k, v in slot_data.items() if k not in ['_id', 'provider_name']}
        
        try:
            response = requests.post(
                'https://cashpot-v5-production.up.railway.app/api/slot-machines',
                json=slot_data,
                headers=headers
            )
            
            if response.status_code == 200:
                success_count += 1
                print(f'✅ Slot machine {slot_data.get("model", "N/A")} imported')
            else:
                print(f'❌ Slot machine failed: {response.status_code}')
        except Exception as e:
            print(f'❌ Slot machine error: {str(e)}')
    
    print(f'🎉 Imported {success_count}/{len(slot_machines)} slot machines')
    
    client.close()
    print('\\n✅ Import completed!')

if __name__ == "__main__":
    import_data_with_mapping()

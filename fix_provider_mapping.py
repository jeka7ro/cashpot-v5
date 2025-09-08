#!/usr/bin/env python3
"""
Fix provider mapping based on Google Sheet data
"""

import requests
import json
from datetime import datetime

def login_railway():
    """Login to Railway and get token"""
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = requests.post('https://cashpot-v5-production.up.railway.app/api/auth/login', json=login_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def get_entities(token, entity_type):
    """Get all entities of a type"""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://cashpot-v5-production.up.railway.app/api/{entity_type}', headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def update_slot_provider(token, slot_id, provider_id):
    """Update slot machine provider"""
    headers = {'Authorization': f'Bearer {token}'}
    data = {'provider_id': provider_id}
    response = requests.put(f'https://cashpot-v5-production.up.railway.app/api/slot-machines/{slot_id}', json=data, headers=headers)
    return response.status_code == 200

def fix_provider_mapping():
    """Fix provider mapping based on Google Sheet data"""
    
    print('🔍 Fixing provider mapping based on Google Sheet...')
    
    # Login to Railway
    token = login_railway()
    if not token:
        print('❌ Railway login failed')
        return
    
    print('✅ Logged in to Railway')
    
    # Get all providers and slot machines
    providers = get_entities(token, 'providers')
    slot_machines = get_entities(token, 'slot-machines')
    
    print(f'📊 Found {len(providers)} providers and {len(slot_machines)} slot machines')
    
    # Create provider mapping by name
    provider_map = {}
    for provider in providers:
        provider_map[provider['name']] = provider['id']
        print(f'  📋 Provider: {provider["name"]} -> {provider["id"]}')
    
    # Google Sheet mapping: Serial Number -> Provider Name
    google_sheet_mapping = {
        '2522046669': 'Alfastreet',
        '2522046670': 'Alfastreet', 
        '134862': 'EGT',
        '135226': 'EGT',
        '149582': 'EGT',
        '149583': 'EGT',
        '149621': 'EGT',
        '149612': 'EGT',
        '149628': 'EGT',
        '149614': 'EGT',
        '142270': 'EGT',
        '150246': 'EGT',
        '150247': 'EGT',
        '155706': 'EGT',
        '142848': 'EGT',
        '142851': 'EGT',
        '150243': 'EGT',
        '142855': 'EGT',
        '150242': 'EGT'
    }
    
    print(f'\\n🎯 Updating slot machines based on Google Sheet mapping...')
    
    updated_count = 0
    for slot in slot_machines:
        serial_number = slot.get('serial_number')
        if serial_number in google_sheet_mapping:
            correct_provider_name = google_sheet_mapping[serial_number]
            correct_provider_id = provider_map.get(correct_provider_name)
            
            if correct_provider_id and slot.get('provider_id') != correct_provider_id:
                print(f'  🔄 Updating {serial_number}: {slot.get("provider_id")} -> {correct_provider_id} ({correct_provider_name})')
                
                if update_slot_provider(token, slot['id'], correct_provider_id):
                    updated_count += 1
                    print(f'    ✅ Updated successfully')
                else:
                    print(f'    ❌ Failed to update')
            else:
                print(f'  ✅ {serial_number}: Already correct ({correct_provider_name})')
    
    print(f'\\n🎉 Provider mapping fix completed!')
    print(f'✅ Updated {updated_count} slot machines')

if __name__ == "__main__":
    fix_provider_mapping()
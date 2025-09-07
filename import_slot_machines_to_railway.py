#!/usr/bin/env python3
"""
Import slot machines to Railway
"""

import requests
import json

def login_railway():
    """Login to Railway and get token"""
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = requests.post('https://cashpot-v5-production.up.railway.app/api/auth/login', json=login_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def import_slot_machines():
    """Import slot machines to Railway"""
    
    print('🔍 Importing slot machines to Railway...')
    
    # Login
    token = login_railway()
    if not token:
        print('❌ Login failed')
        return
    
    print('✅ Logged in successfully')
    
    # Load slot machines
    try:
        with open('slot_machines_export.json', 'r') as f:
            slot_machines = json.load(f)
    except FileNotFoundError:
        print('❌ slot_machines_export.json not found')
        return
    
    print(f'📋 Found {len(slot_machines)} slot machines to import')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    success_count = 0
    
    for i, slot in enumerate(slot_machines):
        print(f'\\n🎰 Importing slot machine {i+1}/{len(slot_machines)}...')
        print(f'   Model: {slot.get("model", "N/A")}')
        print(f'   Serial: {slot.get("serial_number", "N/A")}')
        
        # Prepare slot data for Railway
        slot_data = {
            'id': slot.get('id'),
            'cabinet_id': slot.get('cabinet_id'),
            'game_mix_id': slot.get('game_mix_id'),
            'provider_id': slot.get('provider_id'),
            'model': slot.get('model'),
            'serial_number': slot.get('serial_number'),
            'denomination': slot.get('denomination'),
            'max_bet': slot.get('max_bet'),
            'rtp': slot.get('rtp'),
            'gaming_places': slot.get('gaming_places'),
            'commission_date': slot.get('commission_date'),
            'invoice_number': slot.get('invoice_number'),
            'status': slot.get('status'),
            'location_id': slot.get('location_id'),
            'production_year': slot.get('production_year'),
            'ownership_type': slot.get('ownership_type'),
            'owner_company_id': slot.get('owner_company_id'),
            'lease_provider_id': slot.get('lease_provider_id'),
            'created_at': slot.get('created_at'),
            'created_by': slot.get('created_by')
        }
        
        # Try to create slot machine
        try:
            response = requests.post(
                'https://cashpot-v5-production.up.railway.app/api/slot_machines',
                json=slot_data,
                headers=headers
            )
            
            if response.status_code == 200:
                print(f'✅ Slot machine imported successfully')
                success_count += 1
            else:
                print(f'❌ Failed to import: {response.status_code}')
                print(f'   Error: {response.text}')
                
        except Exception as e:
            print(f'❌ Error importing slot machine: {str(e)}')
    
    print(f'\\n🎉 Imported {success_count}/{len(slot_machines)} slot machines!')

if __name__ == "__main__":
    import_slot_machines()

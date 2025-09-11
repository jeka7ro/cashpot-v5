#!/usr/bin/env python3
"""
Quick import from Google Sheet
"""

import requests
import pandas as pd

def login_railway():
    login_data = {'username': 'admin_new', 'password': 'admin123'}
    response = requests.post('https://cashpot-v5-production.up.railway.app/api/auth/login', json=login_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def create_entity(token, entity_type, name, data=None):
    headers = {'Authorization': f'Bearer {token}'}
    
    if data is None:
        data = {'name': name, 'status': 'active'}
    
    response = requests.post(
        f'https://cashpot-v5-production.up.railway.app/api/{entity_type}',
        json=data,
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()['id']
    else:
        print(f'❌ Failed to create {entity_type} {name}: {response.status_code}')
        return None

def main():
    print('🚀 Quick import from Google Sheet...')
    
    # Login
    token = login_railway()
    if not token:
        print('❌ Login failed')
        return
    
    print('✅ Logged in')
    
    # Load Google Sheet
    sheet_url = 'https://docs.google.com/spreadsheets/d/1XlGcJxJ6DqL7bd6mVnys_8XamUB9pl1ZKSBd8YLClCU/edit?gid=0#gid=0'
    csv_url = sheet_url.replace('/edit?gid=0#gid=0', '/export?format=csv&gid=0')
    
    try:
        df = pd.read_csv(csv_url)
        print(f'✅ Loaded {len(df)} rows')
    except Exception as e:
        print(f'❌ Error loading sheet: {e}')
        return
    
    # Create mappings
    company_map = {}
    provider_map = {}
    location_map = {}
    cabinet_map = {}
    game_mix_map = {}
    
    # Create company (only Smartflix)
    print('\\n🏢 Creating company...')
    company_data = {
        'name': 'Smartflix',
        'registration_number': '12345678',
        'tax_id': 'RO12345678',
        'address': 'Smartflix Address',
        'city': 'Bucharest',
        'postal_code': '000000',
        'contact_person': 'Eugeniu Cazmal',
        'email': 'admin@smartflix.ro',
        'phone': '123456789',
        'status': 'active'
    }
    company_id = create_entity(token, 'companies', 'Smartflix', company_data)
    if company_id:
        company_map['Smartflix'] = company_id
        print('✅ Company: Smartflix')
    
    # Create providers
    print('\\n🏭 Creating providers...')
    providers = df['Producător'].dropna().unique()
    for provider in providers:
        if provider and provider != 'Producător':
            provider_data = {
                'name': provider,
                'company_name': f'{provider} Company',
                'contact_person': 'Contact Person',
                'email': f'contact@{provider.lower()}.com',
                'phone': '123456789',
                'address': f'{provider} Address',
                'status': 'active'
            }
            provider_id = create_entity(token, 'providers', provider, provider_data)
            if provider_id:
                provider_map[provider] = provider_id
                print(f'✅ Provider: {provider}')
    
    # Create locations
    print('\\n📍 Creating locations...')
    locations = df['Locație'].dropna().unique()
    for location in locations:
        if location and location != 'Locație':
            location_data = {
                'name': location,
                'company_id': company_id,
                'address': f'Address for {location}',
                'city': location,
                'postal_code': '000000',
                'contact_person': 'Eugeniu Cazmal',
                'email': 'admin@smartflix.ro',
                'phone': '123456789',
                'status': 'active'
            }
            location_id = create_entity(token, 'locations', location, location_data)
            if location_id:
                location_map[location] = location_id
                print(f'✅ Location: {location}')
    
    # Create cabinets
    print('\\n🏗️ Creating cabinets...')
    cabinets = df['Tip cabinet'].dropna().unique()
    for cabinet in cabinets:
        if cabinet and cabinet != 'Tip cabinet':
            cabinet_data = {
                'name': cabinet,
                'provider_id': list(provider_map.values())[0] if provider_map else None,
                'location_id': list(location_map.values())[0] if location_map else None,
                'status': 'active',
                'description': f'Cabinet {cabinet}',
                'capacity': 1
            }
            cabinet_id = create_entity(token, 'cabinets', cabinet, cabinet_data)
            if cabinet_id:
                cabinet_map[cabinet] = cabinet_id
                print(f'✅ Cabinet: {cabinet}')
    
    # Create game mixes
    print('\\n🎮 Creating game mixes...')
    game_mixes = df['Mix'].dropna().unique()
    for game_mix in game_mixes:
        if game_mix and game_mix != 'Mix':
            game_mix_data = {
                'name': game_mix,
                'provider_id': list(provider_map.values())[0] if provider_map else None,
                'description': f'Game mix {game_mix}',
                'games': [f'Game {i+1}' for i in range(3)],
                'status': 'active',
                'version': '1.0'
            }
            game_mix_id = create_entity(token, 'game-mixes', game_mix, game_mix_data)
            if game_mix_id:
                game_mix_map[game_mix] = game_mix_id
                print(f'✅ Game Mix: {game_mix}')
    
    # Create slot machines
    print('\\n🎰 Creating slot machines...')
    success_count = 0
    
    for index, row in df.iterrows():
        if index == 0:  # Skip header
            continue
            
        if pd.isna(row['Nr. serie']) or pd.isna(row['Producător']):
            continue
        
        # Skip if missing required fields
        if (pd.isna(row['Producător']) or str(row['Producător']) not in provider_map or
            pd.isna(row['Tip cabinet']) or str(row['Tip cabinet']) not in cabinet_map or
            pd.isna(row['Mix']) or str(row['Mix']) not in game_mix_map):
            continue
        
        # Parse commission date from Google Sheet
        # Set default commission date since Comisie column is not present
        commission_date = '2025-01-01T00:00:00'  # Default
        
        slot_data = {
            'serial_number': str(row['Nr. serie']),
            'model': str(row['Tip cabinet']),
            'denomination': 0.1,
            'max_bet': 100.0,
            'rtp': 95.0,
            'gaming_places': 1,
            'status': 'active',
            'production_year': 2025,
            'ownership_type': 'property',
            'commission_date': commission_date,
            'invoice_number': f'INV-{str(row["Nr. serie"])}',
            'created_by': 'admin',
            'provider_id': provider_map[str(row['Producător'])],
            'cabinet_id': cabinet_map[str(row['Tip cabinet'])],
            'game_mix_id': game_mix_map[str(row['Mix'])]
        }
        
        # Map optional relationships
        if not pd.isna(row['Locație']) and str(row['Locație']) in location_map:
            slot_data['location_id'] = location_map[str(row['Locație'])]
        
        if company_id:
            slot_data['owner_company_id'] = company_id
        
        # Create slot machine
        try:
            response = requests.post(
                'https://cashpot-v5-production.up.railway.app/api/slot-machines',
                json=slot_data,
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                success_count += 1
                if success_count % 20 == 0:
                    print(f'  ✅ Created {success_count} slot machines...')
            else:
                print(f'  ❌ Failed: {row["Nr. serie"]} - {response.status_code}')
                
        except Exception as e:
            print(f'  ❌ Error: {row["Nr. serie"]} - {str(e)}')
    
    print(f'\\n🎉 Import completed!')
    print(f'✅ Created {success_count} slot machines')
    print(f'✅ Created {len(company_map)} companies')
    print(f'✅ Created {len(provider_map)} providers')
    print(f'✅ Created {len(location_map)} locations')
    print(f'✅ Created {len(cabinet_map)} cabinets')
    print(f'✅ Created {len(game_mix_map)} game mixes')

if __name__ == "__main__":
    main()

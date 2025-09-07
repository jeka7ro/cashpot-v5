#!/usr/bin/env python3
"""
Import data from Google Sheet to Railway
"""

import requests
import json
import pandas as pd
from datetime import datetime

def login_railway():
    """Login to Railway and get token"""
    login_data = {'username': 'admin', 'password': 'admin123'}
    response = requests.post('https://cashpot-v5-production.up.railway.app/api/auth/login', json=login_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def create_entity_if_not_exists(token, entity_type, name, data=None):
    """Create entity if it doesn't exist, return ID"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Check if entity exists
    response = requests.get(f'https://cashpot-v5-production.up.railway.app/api/{entity_type}', headers=headers)
    if response.status_code == 200:
        entities = response.json()
        for entity in entities:
            if entity.get('name', '').lower() == name.lower():
                return entity['id']
    
    # Create entity if not exists
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
        print(f'❌ Failed to create {entity_type}: {response.text}')
        return None

def import_google_sheet_data():
    """Import data from Google Sheet"""
    
    print('🔍 Importing data from Google Sheet...')
    
    # Login to Railway
    token = login_railway()
    if not token:
        print('❌ Railway login failed')
        return
    
    print('✅ Logged in to Railway')
    
    # Google Sheet URL
    sheet_url = 'https://docs.google.com/spreadsheets/d/1XlGcJxJ6DqL7bd6mVnys_8XamUB9pl1ZKSBd8YLClCU/edit?gid=0#gid=0'
    
    # Read Google Sheet
    try:
        # Convert to CSV export URL
        csv_url = sheet_url.replace('/edit?gid=0#gid=0', '/export?format=csv&gid=0')
        df = pd.read_csv(csv_url)
        print(f'✅ Loaded Google Sheet with {len(df)} rows')
    except Exception as e:
        print(f'❌ Failed to load Google Sheet: {str(e)}')
        return
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Create mapping dictionaries
    company_map = {}
    provider_map = {}
    location_map = {}
    cabinet_map = {}
    game_mix_map = {}
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print('\\n🏢 Creating companies...')
    companies = df['Firma'].dropna().unique()
    for company in companies:
        if company and company != 'Firma':
            company_id = create_entity_if_not_exists(token, 'companies', company)
            if company_id:
                company_map[company] = company_id
                print(f'✅ Company: {company}')
    
    print('\\n🏭 Creating providers...')
    providers = df['Producător'].dropna().unique()
    for provider in providers:
        if provider and provider != 'Producător':
            provider_id = create_entity_if_not_exists(token, 'providers', provider)
            if provider_id:
                provider_map[provider] = provider_id
                print(f'✅ Provider: {provider}')
    
    print('\\n📍 Creating locations...')
    locations = df['Locație'].dropna().unique()
    for location in locations:
        if location and location != 'Locație':
            # Use first company for location
            company_id = list(company_map.values())[0] if company_map else None
            location_data = {
                'name': location,
                'company_id': company_id,
                'address': f'Address for {location}',
                'city': location,
                'postal_code': '000000',
                'contact_person': 'N/A',
                'status': 'active'
            }
            location_id = create_entity_if_not_exists(token, 'locations', location, location_data)
            if location_id:
                location_map[location] = location_id
                print(f'✅ Location: {location}')
    
    print('\\n🏗️ Creating cabinets...')
    cabinets = df['Tip cabinet'].dropna().unique()
    for cabinet in cabinets:
        if cabinet and cabinet != 'Tip cabinet':
            # Use first provider and location
            provider_id = list(provider_map.values())[0] if provider_map else None
            location_id = list(location_map.values())[0] if location_map else None
            cabinet_data = {
                'name': cabinet,
                'provider_id': provider_id,
                'location_id': location_id,
                'status': 'active'
            }
            cabinet_id = create_entity_if_not_exists(token, 'cabinets', cabinet, cabinet_data)
            if cabinet_id:
                cabinet_map[cabinet] = cabinet_id
                print(f'✅ Cabinet: {cabinet}')
    
    print('\\n🎮 Creating game mixes...')
    game_mixes = df['Mix'].dropna().unique()
    for game_mix in game_mixes:
        if game_mix and game_mix != 'Mix':
            # Use first provider
            provider_id = list(provider_map.values())[0] if provider_map else None
            game_mix_data = {
                'name': game_mix,
                'provider_id': provider_id,
                'description': f'Game mix {game_mix}',
                'games': [f'Game {i+1}' for i in range(3)],
                'status': 'active'
            }
            game_mix_id = create_entity_if_not_exists(token, 'game-mixes', game_mix, game_mix_data)
            if game_mix_id:
                game_mix_map[game_mix] = game_mix_id
                print(f'✅ Game Mix: {game_mix}')
    
    print('\\n🎰 Creating slot machines...')
    success_count = 0
    
    for index, row in df.iterrows():
        if index == 0:  # Skip header
            continue
            
        # Skip rows with empty essential data
        if pd.isna(row['Nr. serie']) or pd.isna(row['Producător']) or pd.isna(row['Tip cabinet']):
            continue
        
        slot_data = {
            'serial_number': str(row['Nr. serie']),
            'model': str(row['Tip cabinet']),  # Use cabinet type as model
            'denomination': 0.1,
            'max_bet': 100.0,
            'rtp': 95.0,
            'gaming_places': 1,
            'status': 'active',
            'production_year': 2025,
            'ownership_type': 'property' if str(row['Proprietate']).lower() == 'smartflix' else 'rent',
            'commission_date': '2025-01-01',
            'invoice_number': f'INV-{str(row["Nr. serie"])}',
            'created_by': 'admin'
        }
        
        # Map relationships
        if not pd.isna(row['Locație']) and str(row['Locație']) in location_map:
            slot_data['location_id'] = location_map[str(row['Locație'])]
        
        if not pd.isna(row['Producător']) and str(row['Producător']) in provider_map:
            slot_data['provider_id'] = provider_map[str(row['Producător'])]
        
        if not pd.isna(row['Tip cabinet']) and str(row['Tip cabinet']) in cabinet_map:
            slot_data['cabinet_id'] = cabinet_map[str(row['Tip cabinet'])]
        
        if not pd.isna(row['Mix']) and str(row['Mix']) in game_mix_map:
            slot_data['game_mix_id'] = game_mix_map[str(row['Mix'])]
        
        if not pd.isna(row['Firma']) and str(row['Firma']) in company_map:
            slot_data['owner_company_id'] = company_map[str(row['Firma'])]
        
        # Create slot machine
        try:
            response = requests.post(
                'https://cashpot-v5-production.up.railway.app/api/slot-machines',
                json=slot_data,
                headers=headers
            )
            
            if response.status_code == 200:
                success_count += 1
                if success_count % 10 == 0:
                    print(f'  ✅ Created {success_count} slot machines...')
            else:
                print(f'  ❌ Failed to create slot machine {row["Nr. serie"]}: {response.status_code}')
                
        except Exception as e:
            print(f'  ❌ Error creating slot machine {row["Nr. serie"]}: {str(e)}')
    
    print(f'\\n🎉 Import completed!')
    print(f'✅ Created {success_count} slot machines')
    print(f'✅ Created {len(company_map)} companies')
    print(f'✅ Created {len(provider_map)} providers')
    print(f'✅ Created {len(location_map)} locations')
    print(f'✅ Created {len(cabinet_map)} cabinets')
    print(f'✅ Created {len(game_mix_map)} game mixes')

if __name__ == "__main__":
    import_google_sheet_data()

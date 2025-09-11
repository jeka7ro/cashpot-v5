#!/usr/bin/env python3
"""
Import slot machines from Google Sheets
Creates missing providers, cabinets, game mixes, and locations as needed
"""

import asyncio
import motor.motor_asyncio
import requests
import json
from datetime import datetime
import uuid

# Google Sheets data from the provided URL
GOOGLE_SHEETS_DATA = [
    {"Locație": "Pitesti", "Poziție": "1001", "Nr. serie": "2522046669", "Producător": "Alfastreet", "Tip cabinet": "Alfastreet Live", "Mix": "Post 1"},
    {"Locație": "Pitesti", "Poziție": "1002", "Nr. serie": "2522046670", "Producător": "Alfastreet", "Tip cabinet": "Alfastreet Live", "Mix": "Post 2"},
    {"Locație": "Pitesti", "Poziție": "1003", "Nr. serie": "134862", "Producător": "EGT", "Tip cabinet": "VIP 27/2x42", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1004", "Nr. serie": "135226", "Producător": "EGT", "Tip cabinet": "VIP 27/2x42", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1005", "Nr. serie": "149582", "Producător": "EGT", "Tip cabinet": "VIP 27/2x42", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1006", "Nr. serie": "149583", "Producător": "EGT", "Tip cabinet": "VIP 27/2x42", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1007", "Nr. serie": "149621", "Producător": "EGT", "Tip cabinet": "P42V Curved ST", "Mix": "Union Collection"},
    {"Locație": "Pitesti", "Poziție": "1008", "Nr. serie": "149612", "Producător": "EGT", "Tip cabinet": "P42V Curved ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1009", "Nr. serie": "149628", "Producător": "EGT", "Tip cabinet": "P42V Curved ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1010", "Nr. serie": "149614", "Producător": "EGT", "Tip cabinet": "P42V Curved ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1011", "Nr. serie": "142270", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Union Collection"},
    {"Locație": "Pitesti", "Poziție": "1012", "Nr. serie": "150246", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1013", "Nr. serie": "150247", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1014", "Nr. serie": "155706", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1015", "Nr. serie": "142848", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1016", "Nr. serie": "142851", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1017", "Nr. serie": "150243", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1018", "Nr. serie": "142855", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1019", "Nr. serie": "150242", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1020", "Nr. serie": "235415", "Producător": "EGT", "Tip cabinet": "G 55\" C VIP", "Mix": "Blue Power HD"},
    {"Locație": "Pitesti", "Poziție": "1021", "Nr. serie": "235423", "Producător": "EGT", "Tip cabinet": "G 55\" C VIP", "Mix": "Blue General HD"},
    {"Locație": "Pitesti", "Poziție": "1022", "Nr. serie": "235414", "Producător": "EGT", "Tip cabinet": "G 55\" C VIP", "Mix": "Blue Power HD"},
    {"Locație": "Pitesti", "Poziție": "1023", "Nr. serie": "235419", "Producător": "EGT", "Tip cabinet": "G 55\" C VIP", "Mix": "Blue General HD"},
    {"Locație": "Pitesti", "Poziție": "1024", "Nr. serie": "299720", "Producător": "EGT", "Tip cabinet": "G 55\" C VIP", "Mix": "Mega Supreme Fruits Selection"},
    {"Locație": "Pitesti", "Poziție": "1025", "Nr. serie": "118857", "Producător": "EGT", "Tip cabinet": "P 32/32 H ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1028", "Nr. serie": "118858", "Producător": "EGT", "Tip cabinet": "P 32/32 H ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1029", "Nr. serie": "235428", "Producător": "EGT", "Tip cabinet": "G 50\" C ST", "Mix": "Blue General HD"},
    {"Locație": "Pitesti", "Poziție": "1030", "Nr. serie": "235430", "Producător": "EGT", "Tip cabinet": "G 50\" C ST", "Mix": "Blue Power HD"},
    {"Locație": "Pitesti", "Poziție": "1034", "Nr. serie": "149589", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1035", "Nr. serie": "149585", "Producător": "EGT", "Tip cabinet": "VIP 27/2x42", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1036", "Nr. serie": "149592", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1037", "Nr. serie": "149588", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1038", "Nr. serie": "149590", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1039", "Nr. serie": "149591", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1040", "Nr. serie": "149593", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1041", "Nr. serie": "149594", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1042", "Nr. serie": "149595", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1043", "Nr. serie": "149596", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1044", "Nr. serie": "149597", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1045", "Nr. serie": "149598", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1046", "Nr. serie": "149599", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1047", "Nr. serie": "149600", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1048", "Nr. serie": "149601", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1049", "Nr. serie": "149602", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1050", "Nr. serie": "149603", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1051", "Nr. serie": "149604", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1052", "Nr. serie": "149605", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1053", "Nr. serie": "149606", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1054", "Nr. serie": "149607", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1055", "Nr. serie": "149608", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1056", "Nr. serie": "149609", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1057", "Nr. serie": "149610", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1058", "Nr. serie": "149611", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1059", "Nr. serie": "149613", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1060", "Nr. serie": "149615", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1061", "Nr. serie": "149616", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1062", "Nr. serie": "149617", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1063", "Nr. serie": "149618", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1064", "Nr. serie": "149619", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1065", "Nr. serie": "149620", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1066", "Nr. serie": "149622", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1067", "Nr. serie": "149623", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1068", "Nr. serie": "149624", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1069", "Nr. serie": "149625", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1070", "Nr. serie": "149626", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1071", "Nr. serie": "149627", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1072", "Nr. serie": "149629", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1073", "Nr. serie": "149630", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1074", "Nr. serie": "149631", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1075", "Nr. serie": "149632", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1076", "Nr. serie": "149633", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1077", "Nr. serie": "149634", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1078", "Nr. serie": "149635", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1079", "Nr. serie": "149636", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1080", "Nr. serie": "149637", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1081", "Nr. serie": "149638", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1082", "Nr. serie": "149639", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Green Collection"},
    {"Locație": "Pitesti", "Poziție": "1083", "Nr. serie": "149640", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Orange Collection"},
    {"Locație": "Pitesti", "Poziție": "1084", "Nr. serie": "149641", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1085", "Nr. serie": "149642", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1086", "Nr. serie": "149643", "Producător": "EGT", "Tip cabinet": "P 27/27 ST", "Mix": "Fruits Collection 2"},
    {"Locație": "Pitesti", "Poziție": "1087", "Nr. serie": "798916", "Producător": "Novomatic", "Tip cabinet": "VIP Eagle III FV880A", "Mix": "Impera 7 HD"},
    {"Locație": "Pitesti", "Poziție": "1088", "Nr. serie": "798915", "Producător": "Novomatic", "Tip cabinet": "VIP Eagle III FV880A", "Mix": "Impera 7 HD"},
    {"Locație": "Pitesti", "Poziție": "1089", "Nr. serie": "200425", "Producător": "EGT", "Tip cabinet": "VIP 27/2x42", "Mix": "Purple Collection"},
    {"Locație": "Pitesti", "Poziție": "1090", "Nr. serie": "200426", "Producător": "EGT", "Tip cabinet": "VIP 27/2x42", "Mix": "Gold Collection HD"},
    {"Locație": "Pitesti", "Poziție": "1097", "Nr. serie": "798918", "Producător": "Novomatic", "Tip cabinet": "VIP Eagle III FV880A", "Mix": "Impera 7 HD"},
    {"Locație": "Pitesti", "Poziție": "1098", "Nr. serie": "798917", "Producător": "Novomatic", "Tip cabinet": "VIP Eagle III FV880A", "Mix": "Impera 7 HD"},
    {"Locație": "Pitesti", "Poziție": "1099", "Nr. serie": "2549887", "Producător": "IGT", "Tip cabinet": "Peakslant 49", "Mix": "Edition Orange"},
    {"Locație": "Pitesti", "Poziție": "1100", "Nr. serie": "2549886", "Producător": "IGT", "Tip cabinet": "Peakslant 49", "Mix": "Edition Azure"},
    {"Locație": "Pitesti", "Poziție": "1101", "Nr. serie": "2548499", "Producător": "IGT", "Tip cabinet": "Peakslant 49", "Mix": "Edition Azure"},
    {"Locație": "Pitesti", "Poziție": "1102", "Nr. serie": "2548500", "Producător": "IGT", "Tip cabinet": "Peakslant 49", "Mix": "Edition Orange"},
    {"Locație": "Pitesti", "Poziție": "1117", "Nr. serie": "190268", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 2"},
    {"Locație": "Pitesti", "Poziție": "1118", "Nr. serie": "190269", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 1"},
    {"Locație": "Pitesti", "Poziție": "1119", "Nr. serie": "190270", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 2"},
    {"Locație": "Pitesti", "Poziție": "1120", "Nr. serie": "190271", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 1"},
    {"Locație": "Pitesti", "Poziție": "1122", "Nr. serie": "190273", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 1"},
    {"Locație": "Pitesti", "Poziție": "1123", "Nr. serie": "190274", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 2"},
    {"Locație": "Pitesti", "Poziție": "1124", "Nr. serie": "9134161533", "Producător": "InterBlock", "Tip cabinet": "Terminal Live", "Mix": "Organic G4"},
    {"Locație": "Pitesti", "Poziție": "1125", "Nr. serie": "9134161532", "Producător": "InterBlock", "Tip cabinet": "Terminal Live", "Mix": "Organic G4"},
    {"Locație": "Pitesti", "Poziție": "1126", "Nr. serie": "9134161534", "Producător": "InterBlock", "Tip cabinet": "Terminal Live", "Mix": "Organic G4"},
    {"Locație": "Pitesti", "Poziție": "1127", "Nr. serie": "9134162900", "Producător": "InterBlock", "Tip cabinet": "Terminal Live", "Mix": "Organic G4"},
    {"Locație": "Pitesti", "Poziție": "1128", "Nr. serie": "100394", "Producător": "Amusnet", "Tip cabinet": "AMS-ST-50", "Mix": "Amusebox"},
    {"Locație": "Pitesti", "Poziție": "1129", "Nr. serie": "100399", "Producător": "Amusnet", "Tip cabinet": "AMS-ST-50", "Mix": "Amusebox"},
    {"Locație": "Pitesti", "Poziție": "1130", "Nr. serie": "100398", "Producător": "Amusnet", "Tip cabinet": "AMS-ST-50", "Mix": "Amusebox"},
    {"Locație": "Pitesti", "Poziție": "1131", "Nr. serie": "100395", "Producător": "Amusnet", "Tip cabinet": "AMS-ST-50", "Mix": "Amusebox"},
    {"Locație": "Pitesti", "Poziție": "1132", "Nr. serie": "100396", "Producător": "Amusnet", "Tip cabinet": "AMS-ST-50", "Mix": "Amusebox"},
    {"Locație": "Pitesti", "Poziție": "1133", "Nr. serie": "100397", "Producător": "Amusnet", "Tip cabinet": "AMS-ST-50", "Mix": "Amusebox"},
    {"Locație": "Valcea", "Poziție": "2001", "Nr. serie": "142850", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Purple Collection"},
    {"Locație": "Valcea", "Poziție": "2005", "Nr. serie": "142847", "Producător": "EGT", "Tip cabinet": "P42V Curved UP", "Mix": "Union Collection"},
    {"Locație": "Valcea", "Poziție": "2009", "Nr. serie": "190281", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 1"},
    {"Locație": "Valcea", "Poziție": "2010", "Nr. serie": "190282", "Producător": "EGT", "Tip cabinet": "G 27/32 ST", "Mix": "Bell Link 2"}
]

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

async def import_slots():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cashpot_v5
    
    print("🚀 Starting Google Sheets import...")
    
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
    for slot_data in GOOGLE_SHEETS_DATA:
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
            print(f"🎰 Created slot: {slot_data['Nr. serie']} at {slot_data['Locație']} position {slot_data['Poziție']}")
            
        except Exception as e:
            print(f"❌ Error creating slot {slot_data['Nr. serie']}: {e}")
    
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
    asyncio.run(import_slots())

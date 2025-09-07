#!/usr/bin/env python3
"""
Export and Import Real Data - Exportează datele locale și le adaugă pe Railway
"""
import asyncio
import requests
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import json

# Local MongoDB connection
LOCAL_MONGO_URL = "mongodb://localhost:27017"
LOCAL_DB_NAME = "cash_pot"

# Railway API
RAILWAY_API = "https://cashpot-v5-production.up.railway.app/api"

def login_railway():
    """Login to Railway"""
    login_data = {
        "username": "eugeniu2",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_API}/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

async def export_local_data():
    """Export data from local MongoDB"""
    print("📤 Exporting data from local MongoDB...")
    
    try:
        client = AsyncIOMotorClient(LOCAL_MONGO_URL)
        db = client[LOCAL_DB_NAME]
        
        # Collections to export
        collections = ['companies', 'locations', 'providers', 'cabinets', 'slot_machines', 'invoices', 'jackpots', 'game_mixes', 'users']
        
        exported_data = {}
        
        for collection_name in collections:
            collection = db[collection_name]
            data = await collection.find({}).to_list(length=None)
            
            # Convert ObjectId to string for JSON serialization
            for item in data:
                if '_id' in item:
                    item['_id'] = str(item['_id'])
                
                # Convert all datetime fields to ISO format
                for key, value in item.items():
                    if isinstance(value, datetime):
                        item[key] = value.isoformat()
            
            exported_data[collection_name] = data
            print(f"✅ Exported {len(data)} {collection_name}")
        
        # Save to JSON file
        with open('exported_data.json', 'w', encoding='utf-8') as f:
            json.dump(exported_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Data saved to exported_data.json")
        return exported_data
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return None
    finally:
        client.close()

def add_company_to_railway(token, company):
    """Add company to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Convert datetime strings back to datetime objects if needed
    company_data = {
        "name": company.get("name", ""),
        "registration_number": company.get("registration_number", ""),
        "tax_id": company.get("tax_id", ""),
        "address": company.get("address", ""),
        "phone": company.get("phone", ""),
        "email": company.get("email", ""),
        "contact_person": company.get("contact_person", ""),
        "status": company.get("status", "active")
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_API}/companies",
            json=company_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Company '{company_data['name']}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add company '{company_data['name']}': {response.status_code}")
            if response.status_code == 400:
                print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error adding company '{company_data['name']}': {e}")
        return None

def add_provider_to_railway(token, provider):
    """Add provider to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    provider_data = {
        "name": provider.get("name", ""),
        "company_name": provider.get("company_name", ""),
        "contact_person": provider.get("contact_person", ""),
        "email": provider.get("email", ""),
        "phone": provider.get("phone", ""),
        "address": provider.get("address", ""),
        "status": provider.get("status", "active")
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_API}/providers",
            json=provider_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Provider '{provider_data['name']}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add provider '{provider_data['name']}': {response.status_code}")
            if response.status_code == 400:
                print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error adding provider '{provider_data['name']}': {e}")
        return None

def add_location_to_railway(token, location):
    """Add location to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    location_data = {
        "name": location.get("name", ""),
        "address": location.get("address", ""),
        "city": location.get("city", ""),
        "county": location.get("county", ""),
        "phone": location.get("phone", ""),
        "company_id": location.get("company_id", ""),
        "postal_code": location.get("postal_code", ""),
        "status": location.get("status", "active")
    }
    
    try:
        response = requests.post(
            f"{RAILWAY_API}/locations",
            json=location_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Location '{location_data['name']}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add location '{location_data['name']}': {response.status_code}")
            if response.status_code == 400:
                print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error adding location '{location_data['name']}': {e}")
        return None

async def main():
    print("🚀 EXPORTING AND IMPORTING REAL DATA...")
    print("=" * 50)
    
    # Export local data
    print("1. Exporting data from local MongoDB...")
    exported_data = await export_local_data()
    
    if not exported_data:
        print("❌ Failed to export local data")
        return
    
    # Login to Railway
    print("\n2. Logging in to Railway...")
    token = login_railway()
    if not token:
        print("❌ Cannot login to Railway")
        return
    
    print("✅ Login successful!")
    
    # Import companies
    print("\n3. Importing companies...")
    company_id_map = {}
    for company in exported_data.get('companies', []):
        new_id = add_company_to_railway(token, company)
        if new_id:
            company_id_map[company.get('id')] = new_id
    
    # Import providers
    print("\n4. Importing providers...")
    provider_id_map = {}
    for provider in exported_data.get('providers', []):
        new_id = add_provider_to_railway(token, provider)
        if new_id:
            provider_id_map[provider.get('id')] = new_id
    
    # Import locations (need to update company_id)
    print("\n5. Importing locations...")
    location_id_map = {}
    for location in exported_data.get('locations', []):
        # Update company_id to new Railway ID
        old_company_id = location.get('company_id')
        if old_company_id in company_id_map:
            location['company_id'] = company_id_map[old_company_id]
        
        new_id = add_location_to_railway(token, location)
        if new_id:
            location_id_map[location.get('id')] = new_id
    
    print("\n🎉 DATA IMPORT COMPLETED!")
    print(f"✅ Companies imported: {len(company_id_map)}")
    print(f"✅ Providers imported: {len(provider_id_map)}")
    print(f"✅ Locations imported: {len(location_id_map)}")
    print("\n🌐 Go to: https://jeka7ro.github.io/cashpot-v5/")
    print("👤 Login with: eugeniu2 / admin123")

if __name__ == "__main__":
    asyncio.run(main())

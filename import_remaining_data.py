#!/usr/bin/env python3
"""
Import Remaining Data - Importează slot machines, invoices și jackpots
"""
import requests
import json

def login_railway():
    """Login to Railway"""
    login_data = {
        "username": "eugeniu2",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/auth/login",
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

def get_railway_data(token, endpoint):
    """Get data from Railway"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(
            f"https://cashpot-v5-production.up.railway.app/api/{endpoint}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get {endpoint}: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting {endpoint}: {e}")
        return []

def add_slot_machine(token, slot_data, company_id_map, provider_id_map, location_id_map):
    """Add slot machine to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Update IDs to Railway IDs
    if slot_data.get('owner_company_id') in company_id_map:
        slot_data['owner_company_id'] = company_id_map[slot_data['owner_company_id']]
    if slot_data.get('provider_id') in provider_id_map:
        slot_data['provider_id'] = provider_id_map[slot_data['provider_id']]
    if slot_data.get('location_id') in location_id_map:
        slot_data['location_id'] = location_id_map[slot_data['location_id']]
    
    slot_machine_data = {
        "model": slot_data.get("model", ""),
        "serial_number": slot_data.get("serial_number", ""),
        "denomination": slot_data.get("denomination", 0.01),
        "max_bet": slot_data.get("max_bet", 100.0),
        "rtp": slot_data.get("rtp", 96.0),
        "gaming_places": slot_data.get("gaming_places", 1),
        "production_year": slot_data.get("production_year", 2023),
        "status": slot_data.get("status", "active"),
        "ownership_type": slot_data.get("ownership_type", "owned"),
        "owner_company_id": slot_data.get("owner_company_id", ""),
        "location_id": slot_data.get("location_id", ""),
        "provider_id": slot_data.get("provider_id", "")
    }
    
    try:
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/slot-machines",
            json=slot_machine_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Slot machine '{slot_machine_data['model']}' (SN: {slot_machine_data['serial_number']}) added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add slot machine '{slot_machine_data['model']}': {response.status_code}")
            if response.status_code == 422:
                print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error adding slot machine '{slot_machine_data['model']}': {e}")
        return None

def add_invoice(token, invoice_data, company_id_map, provider_id_map, location_id_map):
    """Add invoice to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Update IDs to Railway IDs
    if invoice_data.get('company_id') in company_id_map:
        invoice_data['company_id'] = company_id_map[invoice_data['company_id']]
    if invoice_data.get('buyer_id') in company_id_map:
        invoice_data['buyer_id'] = company_id_map[invoice_data['buyer_id']]
    if invoice_data.get('seller_id') in provider_id_map:
        invoice_data['seller_id'] = provider_id_map[invoice_data['seller_id']]
    if invoice_data.get('location_id') in location_id_map:
        invoice_data['location_id'] = location_id_map[invoice_data['location_id']]
    
    invoice_request_data = {
        "invoice_number": invoice_data.get("invoice_number", ""),
        "company_id": invoice_data.get("company_id", ""),
        "location_id": invoice_data.get("location_id", ""),
        "buyer_id": invoice_data.get("buyer_id", ""),
        "seller_id": invoice_data.get("seller_id", ""),
        "transaction_type": invoice_data.get("transaction_type", "buy"),
        "serial_numbers": invoice_data.get("serial_numbers", ""),
        "issue_date": invoice_data.get("issue_date", ""),
        "due_date": invoice_data.get("due_date", ""),
        "amount": invoice_data.get("amount", 0.0),
        "currency": invoice_data.get("currency", "RON"),
        "status": invoice_data.get("status", "pending"),
        "description": invoice_data.get("description", "")
    }
    
    try:
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/invoices",
            json=invoice_request_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Invoice '{invoice_request_data['invoice_number']}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add invoice '{invoice_request_data['invoice_number']}': {response.status_code}")
            if response.status_code == 422:
                print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error adding invoice '{invoice_request_data['invoice_number']}': {e}")
        return None

def add_jackpot(token, jackpot_data, slot_id_map):
    """Add jackpot to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Update slot machine ID to Railway ID
    if jackpot_data.get('cabinet_id') in slot_id_map:
        jackpot_data['cabinet_id'] = slot_id_map[jackpot_data['cabinet_id']]
    
    jackpot_request_data = {
        "cabinet_id": jackpot_data.get("cabinet_id", ""),
        "amount": jackpot_data.get("amount", 0.0),
        "date": jackpot_data.get("date", ""),
        "status": jackpot_data.get("status", "active")
    }
    
    try:
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/jackpots",
            json=jackpot_request_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Jackpot {jackpot_request_data['amount']} RON added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add jackpot: {response.status_code}")
            if response.status_code == 422:
                print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error adding jackpot: {e}")
        return None

def main():
    print("🚀 IMPORTING REMAINING DATA...")
    print("=" * 50)
    
    # Load exported data
    try:
        with open('exported_data.json', 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading exported data: {e}")
        return
    
    # Login to Railway
    print("1. Logging in to Railway...")
    token = login_railway()
    if not token:
        print("❌ Cannot login to Railway")
        return
    
    print("✅ Login successful!")
    
    # Get current Railway data to create ID maps
    print("\n2. Getting current Railway data...")
    companies = get_railway_data(token, "companies")
    providers = get_railway_data(token, "providers")
    locations = get_railway_data(token, "locations")
    
    # Create ID maps (old_id -> new_id)
    company_id_map = {}
    for company in companies:
        for old_company in exported_data.get('companies', []):
            if company['name'] == old_company['name']:
                company_id_map[old_company['id']] = company['id']
                break
    
    provider_id_map = {}
    for provider in providers:
        for old_provider in exported_data.get('providers', []):
            if provider['name'] == old_provider['name']:
                provider_id_map[old_provider['id']] = provider['id']
                break
    
    location_id_map = {}
    for location in locations:
        for old_location in exported_data.get('locations', []):
            if location['name'] == old_location['name']:
                location_id_map[old_location['id']] = location['id']
                break
    
    print(f"✅ Found {len(company_id_map)} company mappings")
    print(f"✅ Found {len(provider_id_map)} provider mappings")
    print(f"✅ Found {len(location_id_map)} location mappings")
    
    # Import slot machines
    print("\n3. Importing slot machines...")
    slot_id_map = {}
    for slot in exported_data.get('slot_machines', []):
        new_id = add_slot_machine(token, slot, company_id_map, provider_id_map, location_id_map)
        if new_id:
            slot_id_map[slot.get('id')] = new_id
    
    # Import invoices
    print("\n4. Importing invoices...")
    for invoice in exported_data.get('invoices', []):
        add_invoice(token, invoice, company_id_map, provider_id_map, location_id_map)
    
    # Import jackpots
    print("\n5. Importing jackpots...")
    for jackpot in exported_data.get('jackpots', []):
        add_jackpot(token, jackpot, slot_id_map)
    
    print("\n🎉 REMAINING DATA IMPORT COMPLETED!")
    print(f"✅ Slot machines imported: {len(slot_id_map)}")
    print(f"✅ Invoices imported: {len(exported_data.get('invoices', []))}")
    print(f"✅ Jackpots imported: {len(exported_data.get('jackpots', []))}")
    print("\n🌐 Go to: https://jeka7ro.github.io/cashpot-v5/")
    print("👤 Login with: eugeniu2 / admin123")

if __name__ == "__main__":
    main()

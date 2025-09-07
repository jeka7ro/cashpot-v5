#!/usr/bin/env python3
"""
Import ALL Your Data to Railway - Importează TOATE datele tale pe Railway
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

def add_company_to_railway(token, company):
    """Add company to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
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
            "https://cashpot-v5-production.up.railway.app/api/companies",
            json=company_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Company '{company_data['name']}' added with ID: {data.get('id')}")
            return data.get('id')
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"⚠️ Company '{company_data['name']}' already exists")
            return None
        else:
            print(f"❌ Failed to add company '{company_data['name']}': {response.status_code}")
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
            "https://cashpot-v5-production.up.railway.app/api/providers",
            json=provider_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Provider '{provider_data['name']}' added with ID: {data.get('id')}")
            return data.get('id')
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"⚠️ Provider '{provider_data['name']}' already exists")
            return None
        else:
            print(f"❌ Failed to add provider '{provider_data['name']}': {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error adding provider '{provider_data['name']}': {e}")
        return None

def add_location_to_railway(token, location, company_id_map):
    """Add location to Railway"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Update company_id to Railway ID
    old_company_id = location.get('company_id')
    if old_company_id in company_id_map:
        location['company_id'] = company_id_map[old_company_id]
    
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
            "https://cashpot-v5-production.up.railway.app/api/locations",
            json=location_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Location '{location_data['name']}' added with ID: {data.get('id')}")
            return data.get('id')
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"⚠️ Location '{location_data['name']}' already exists")
            return None
        else:
            print(f"❌ Failed to add location '{location_data['name']}': {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error adding location '{location_data['name']}': {e}")
        return None

def add_slot_machine_to_railway(token, slot_data, company_id_map, provider_id_map, location_id_map):
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
        "provider_id": slot_data.get("provider_id", ""),
        "cabinet_id": slot_data.get("cabinet_id", ""),
        "game_mix_id": slot_data.get("game_mix_id", "")
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

def add_invoice_to_railway(token, invoice_data, company_id_map, provider_id_map, location_id_map):
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
            return None
    except Exception as e:
        print(f"❌ Error adding invoice '{invoice_request_data['invoice_number']}': {e}")
        return None

def add_jackpot_to_railway(token, jackpot_data, slot_id_map):
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
        "status": jackpot_data.get("status", "active"),
        "serial_number": jackpot_data.get("serial_number", ""),
        "jackpot_type": jackpot_data.get("jackpot_type", "progressive"),
        "jackpot_name": jackpot_data.get("jackpot_name", "Mega Jackpot"),
        "increment_rate": jackpot_data.get("increment_rate", 0.01),
        "description": jackpot_data.get("description", "")
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
            return None
    except Exception as e:
        print(f"❌ Error adding jackpot: {e}")
        return None

def main():
    print("🚀 IMPORTING ALL YOUR DATA TO RAILWAY...")
    print("=" * 60)
    
    # Load all your data
    try:
        with open('all_your_data.json', 'r', encoding='utf-8') as f:
            your_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading your data: {e}")
        return
    
    # Login to Railway
    print("1. Logging in to Railway...")
    token = login_railway()
    if not token:
        print("❌ Cannot login to Railway")
        return
    
    print("✅ Login successful!")
    
    # Import companies
    print("\n2. Importing your companies...")
    company_id_map = {}
    for company in your_data.get('companies', []):
        new_id = add_company_to_railway(token, company)
        if new_id:
            company_id_map[company.get('id')] = new_id
    
    # Import providers
    print("\n3. Importing your providers...")
    provider_id_map = {}
    for provider in your_data.get('providers', []):
        new_id = add_provider_to_railway(token, provider)
        if new_id:
            provider_id_map[provider.get('id')] = new_id
    
    # Import locations
    print("\n4. Importing your locations...")
    location_id_map = {}
    for location in your_data.get('locations', []):
        new_id = add_location_to_railway(token, location, company_id_map)
        if new_id:
            location_id_map[location.get('id')] = new_id
    
    # Import slot machines
    print("\n5. Importing your slot machines...")
    slot_id_map = {}
    for slot in your_data.get('slot_machines', []):
        new_id = add_slot_machine_to_railway(token, slot, company_id_map, provider_id_map, location_id_map)
        if new_id:
            slot_id_map[slot.get('id')] = new_id
    
    # Import invoices
    print("\n6. Importing your invoices...")
    for invoice in your_data.get('invoices', []):
        add_invoice_to_railway(token, invoice, company_id_map, provider_id_map, location_id_map)
    
    # Import jackpots
    print("\n7. Importing your jackpots...")
    for jackpot in your_data.get('jackpots', []):
        add_jackpot_to_railway(token, jackpot, slot_id_map)
    
    print("\n🎉 ALL YOUR DATA IMPORT COMPLETED!")
    print(f"✅ Companies: {len(company_id_map)}")
    print(f"✅ Providers: {len(provider_id_map)}")
    print(f"✅ Locations: {len(location_id_map)}")
    print(f"✅ Slot machines: {len(slot_id_map)}")
    print(f"✅ Invoices: {len(your_data.get('invoices', []))}")
    print(f"✅ Jackpots: {len(your_data.get('jackpots', []))}")
    print("\n🌐 Go to: https://jeka7ro.github.io/cashpot-v5/")
    print("👤 Login with: admin / admin123")

if __name__ == "__main__":
    main()

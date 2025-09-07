#!/usr/bin/env python3
"""
Add Sample Data - Adaugă date de exemplu în aplicația CashPot
"""
import requests
import json
import time

def login():
    """Login as admin user"""
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

def add_company(token, name, registration_number, address, phone, email, tax_id, contact_person):
    """Add a company"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    company_data = {
        "name": name,
        "registration_number": registration_number,
        "address": address,
        "phone": phone,
        "email": email,
        "tax_id": tax_id,
        "contact_person": contact_person,
        "status": "active"
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
            print(f"✅ Company '{name}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add company '{name}': {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error adding company '{name}': {e}")
        return None

def add_location(token, name, address, city, county, phone, company_id, postal_code):
    """Add a location"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    location_data = {
        "name": name,
        "address": address,
        "city": city,
        "county": county,
        "phone": phone,
        "company_id": company_id,
        "postal_code": postal_code,
        "status": "active"
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
            print(f"✅ Location '{name}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add location '{name}': {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error adding location '{name}': {e}")
        return None

def add_provider(token, name, company_name, contact_person, email, phone, address):
    """Add a provider"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    provider_data = {
        "name": name,
        "company_name": company_name,
        "contact_person": contact_person,
        "email": email,
        "phone": phone,
        "address": address,
        "status": "active"
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
            print(f"✅ Provider '{name}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add provider '{name}': {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error adding provider '{name}': {e}")
        return None

def add_cabinet(token, model, serial_number, location_id, provider_id, status="active"):
    """Add a cabinet"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    cabinet_data = {
        "model": model,
        "serial_number": serial_number,
        "location_id": location_id,
        "provider_id": provider_id,
        "status": status,
        "ownership_type": "owned",
        "denomination": 0.01,
        "max_bet": 100,
        "rtp": 96.5,
        "gaming_places": 1,
        "production_year": 2023
    }
    
    try:
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/cabinets",
            json=cabinet_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cabinet '{model}' added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add cabinet '{model}': {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error adding cabinet '{model}': {e}")
        return None

def add_jackpot(token, cabinet_id, amount, date, status="active"):
    """Add a jackpot record"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    jackpot_data = {
        "cabinet_id": cabinet_id,
        "amount": amount,
        "date": date,
        "status": status
    }
    
    try:
        response = requests.post(
            "https://cashpot-v5-production.up.railway.app/api/jackpots",
            json=jackpot_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Jackpot {amount} RON added with ID: {data.get('id')}")
            return data.get('id')
        else:
            print(f"❌ Failed to add jackpot: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error adding jackpot: {e}")
        return None

def main():
    print("🚀 ADDING SAMPLE DATA TO CASHPOT...")
    print("=" * 50)
    
    # Login
    print("1. Logging in as admin...")
    token = login()
    if not token:
        print("❌ Cannot login as admin")
        return
    
    print("✅ Login successful!")
    
    # Add companies
    print("\n2. Adding companies...")
    company1_id = add_company(
        token, 
        "CashPot SRL", 
        "J40/1234/2023", 
        "Str. Popa Savu 78, ap.3, București", 
        "0729030303", 
        "contact@cashpot.ro",
        "RO12345678",
        "Eugeniu Cazmal"
    )
    
    company2_id = add_company(
        token, 
        "Gaming Solutions SRL", 
        "J40/5678/2023", 
        "Bd. Magheru 1, București", 
        "0721234567", 
        "info@gamingsolutions.ro",
        "RO87654321",
        "Maria Popescu"
    )
    
    # Add locations
    print("\n3. Adding locations...")
    location1_id = add_location(
        token, 
        "Cazinoul Central", 
        "Str. Popa Savu 78, ap.3", 
        "București", 
        "București", 
        "0729030303", 
        company1_id,
        "010101"
    )
    
    location2_id = add_location(
        token, 
        "Cazinoul Nord", 
        "Bd. Magheru 1", 
        "București", 
        "București", 
        "0721234567", 
        company2_id,
        "010102"
    )
    
    # Add providers
    print("\n4. Adding providers...")
    provider1_id = add_provider(
        token, 
        "Novomatic", 
        "Novomatic Romania SRL", 
        "Eugeniu Cazmal", 
        "eugeniu@novomatic.ro", 
        "0729030303", 
        "Str. Popa Savu 78, ap.3, București"
    )
    
    provider2_id = add_provider(
        token, 
        "IGT", 
        "IGT Romania SRL", 
        "Maria Popescu", 
        "maria@igt.ro", 
        "0721234567", 
        "Bd. Magheru 1, București"
    )
    
    # Add cabinets
    print("\n5. Adding cabinets...")
    cabinet1_id = add_cabinet(
        token, 
        "Diamond Line 1.2", 
        "DL001234", 
        location1_id, 
        provider1_id
    )
    
    cabinet2_id = add_cabinet(
        token, 
        "Book of Ra", 
        "BOR005678", 
        location1_id, 
        provider1_id
    )
    
    cabinet3_id = add_cabinet(
        token, 
        "Sizzling Hot", 
        "SH009012", 
        location2_id, 
        provider2_id
    )
    
    # Add jackpots
    print("\n6. Adding jackpot records...")
    add_jackpot(token, cabinet1_id, 5000, "2025-09-07", "active")
    add_jackpot(token, cabinet2_id, 7500, "2025-09-06", "active")
    add_jackpot(token, cabinet3_id, 3200, "2025-09-05", "active")
    
    print("\n🎉 SAMPLE DATA ADDED SUCCESSFULLY!")
    print("✅ Companies: 2")
    print("✅ Locations: 2") 
    print("✅ Providers: 2")
    print("✅ Cabinets: 3")
    print("✅ Jackpots: 3")
    print("\n🌐 Go to: https://jeka7ro.github.io/cashpot-v5/")
    print("👤 Login with: eugeniu2 / admin123")

if __name__ == "__main__":
    main()

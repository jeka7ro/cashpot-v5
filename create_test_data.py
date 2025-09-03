import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import uuid

async def create_test_data():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cash_pot
    
    # Create test companies
    company1 = {
        "id": str(uuid.uuid4()),
        "name": "SMARTFLIX",
        "registration_number": "J40/1234/2020",
        "tax_id": "RO12345678",
        "address": "Strada Test 123, Bucuresti",
        "phone": "+40 123 456 789",
        "email": "contact@smartflix.ro",
        "contact_person": "Ion Popescu",
        "status": "active",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    company2 = {
        "id": str(uuid.uuid4()),
        "name": "GAMING CORP",
        "registration_number": "J40/5678/2021",
        "tax_id": "RO87654321",
        "address": "Strada Gaming 456, Cluj",
        "phone": "+40 987 654 321",
        "email": "contact@gamingcorp.ro",
        "contact_person": "Maria Ionescu",
        "status": "active",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    # Create test providers
    provider1 = {
        "id": str(uuid.uuid4()),
        "name": "Amusnet",
        "company_name": "Amusnet Gaming Ltd",
        "contact_person": "John Smith",
        "email": "contact@amusnet.com",
        "phone": "+44 123 456 789",
        "address": "123 Gaming Street, London",
        "status": "active",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    # Create test locations
    location1 = {
        "id": str(uuid.uuid4()),
        "name": "Pitesti",
        "address": "Strada Centrala 1, Pitesti",
        "city": "Pitesti",
        "county": "Arges",
        "country": "Romania",
        "postal_code": "110000",
        "company_id": company1["id"],
        "status": "active",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    # Create test invoices
    invoice1 = {
        "id": str(uuid.uuid4()),
        "invoice_number": "INV-2025-001",
        "company_id": company1["id"],
        "location_id": location1["id"],
        "buyer_id": company1["id"],
        "seller_id": provider1["id"],
        "transaction_type": "buy",
        "serial_numbers": "188681 188682 188683",
        "issue_date": datetime(2025, 8, 1),
        "due_date": datetime(2025, 9, 1),
        "amount": 15000.00,
        "currency": "EUR",
        "status": "paid",
        "description": "Purchase of 3 slot machines",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    invoice2 = {
        "id": str(uuid.uuid4()),
        "invoice_number": "INV-2025-002",
        "company_id": company2["id"],
        "location_id": location1["id"],
        "buyer_id": company2["id"],
        "seller_id": provider1["id"],
        "transaction_type": "rent",
        "serial_numbers": "188684 188685",
        "issue_date": datetime(2025, 8, 15),
        "due_date": datetime(2025, 9, 15),
        "amount": 5000.00,
        "currency": "EUR",
        "status": "pending",
        "description": "Rent of 2 slot machines",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    # Create test slot machines
    slot1 = {
        "id": str(uuid.uuid4()),
        "cabinet_id": str(uuid.uuid4()),
        "game_mix_id": str(uuid.uuid4()),
        "provider_id": provider1["id"],
        "model": "Premium 2000",
        "serial_number": "188681",
        "denomination": 0.10,
        "max_bet": 100.00,
        "rtp": 95.00,
        "gaming_places": 1,
        "commission_date": datetime(2025, 8, 1),
        "invoice_number": "INV-2025-001",
        "status": "active",
        "location_id": location1["id"],
        "production_year": 2025,
        "ownership_type": "property",
        "owner_company_id": company1["id"],
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    slot2 = {
        "id": str(uuid.uuid4()),
        "cabinet_id": str(uuid.uuid4()),
        "game_mix_id": str(uuid.uuid4()),
        "provider_id": provider1["id"],
        "model": "Premium 2000",
        "serial_number": "188684",
        "denomination": 0.10,
        "max_bet": 100.00,
        "rtp": 95.00,
        "gaming_places": 1,
        "commission_date": datetime(2025, 8, 15),
        "invoice_number": "INV-2025-002",
        "status": "active",
        "location_id": location1["id"],
        "production_year": 2025,
        "ownership_type": "rent",
        "lease_provider_id": provider1["id"],
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    # Insert data
    try:
        await db.companies.insert_one(company1)
        await db.companies.insert_one(company2)
        await db.providers.insert_one(provider1)
        await db.locations.insert_one(location1)
        await db.invoices.insert_one(invoice1)
        await db.invoices.insert_one(invoice2)
        await db.slot_machines.insert_one(slot1)
        await db.slot_machines.insert_one(slot2)
        
        print("✅ Test data created successfully!")
        print(f"📄 Created 2 invoices with serial numbers: 188681, 188682, 188683 (buy) and 188684, 188685 (rent)")
        print(f"🎰 Created 2 slot machines with serial numbers: 188681 (property) and 188684 (rent)")
        print(f"🏢 Created 2 companies: SMARTFLIX and GAMING CORP")
        print(f"🏪 Created 1 provider: Amusnet")
        print(f"📍 Created 1 location: Pitesti")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_data()) 
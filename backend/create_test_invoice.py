import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

async def create_test_invoice():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cash_pot
    
    # Get existing companies and providers
    companies = await db.companies.find({}).to_list(10)
    providers = await db.providers.find({}).to_list(10)
    locations = await db.locations.find({}).to_list(10)
    
    if not companies or not providers or not locations:
        print("❌ Need companies, providers, and locations to create test invoice")
        return
    
    # Create test invoice with TEST-PROPERTY-003
    test_invoice = {
        "id": str(uuid.uuid4()),
        "invoice_number": "TEST",
        "company_id": companies[0]["id"],
        "location_id": locations[0]["id"],
        "buyer_id": companies[0]["id"],  # Customer
        "seller_id": providers[0]["id"],  # Provider
        "transaction_type": "rent",  # This should make it Rent (Leased)
        "serial_numbers": "TEST-PROPERTY-003",
        "issue_date": datetime(2025, 8, 6),
        "due_date": datetime(2025, 9, 6),
        "amount": 450.00,
        "currency": "EUR",
        "status": "pending",
        "description": "Rent for TEST-PROPERTY-003",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }
    
    try:
        await db.invoices.insert_one(test_invoice)
        print("✅ Test invoice created successfully!")
        print(f"📄 Invoice: {test_invoice['invoice_number']}")
        print(f"📋 Serial Numbers: {test_invoice['serial_numbers']}")
        print(f"🔄 Transaction Type: {test_invoice['transaction_type']}")
        print(f"🏢 Customer ID: {test_invoice['buyer_id']}")
        print(f"🏪 Provider ID: {test_invoice['seller_id']}")
        print(f"💰 Amount: {test_invoice['amount']}€")
        
    except Exception as e:
        print(f"❌ Error creating test invoice: {e}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_invoice()) 
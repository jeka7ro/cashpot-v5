import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_slots():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cash_pot
    
    # Get all slot machines
    slots = await db.slot_machines.find({}).to_list(10)
    
    print("=== ALL SLOT MACHINES ===")
    for slot in slots:
        print(f"Serial Number: {slot.get('serial_number')}")
        print(f"Commission Date: {slot.get('commission_date')}")
        print(f"Invoice Number: {slot.get('invoice_number')}")
        print(f"Ownership Type: {slot.get('ownership_type')}")
        print(f"Owner Company ID: {slot.get('owner_company_id')}")
        print(f"Lease Provider ID: {slot.get('lease_provider_id')}")
        print("---")
    
    # Check for specific serial number
    slot_with_188681 = await db.slot_machines.find_one({'serial_number': '188681'})
    
    print(f"\n=== SLOT WITH 188681 ===")
    if slot_with_188681:
        print(f"Serial Number: {slot_with_188681.get('serial_number')}")
        print(f"Commission Date: {slot_with_188681.get('commission_date')}")
        print(f"Invoice Number: {slot_with_188681.get('invoice_number')}")
        print(f"Ownership Type: {slot_with_188681.get('ownership_type')}")
        print(f"Owner Company ID: {slot_with_188681.get('owner_company_id')}")
        print(f"Lease Provider ID: {slot_with_188681.get('lease_provider_id')}")
    else:
        print("No slot machine found with serial number 188681")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_slots()) 
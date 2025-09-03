import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_specific_invoice():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cash_pot
    
    # Check for specific serial number
    invoices_with_test = await db.invoices.find({
        'serial_numbers': {'$regex': 'TEST-PROPERTY-003'}
    }).to_list(10)
    
    print(f"=== INVOICES WITH TEST-PROPERTY-003: {len(invoices_with_test)} ===")
    for invoice in invoices_with_test:
        print(f"Invoice: {invoice.get('invoice_number')}")
        print(f"Serial Numbers: {invoice.get('serial_numbers')}")
        print(f"Transaction Type: {invoice.get('transaction_type')}")
        print(f"Buyer ID: {invoice.get('buyer_id')}")
        print(f"Seller ID: {invoice.get('seller_id')}")
        print("---")
    
    # Check all invoices for any TEST serial numbers
    all_invoices = await db.invoices.find({}).to_list(10)
    print(f"\n=== ALL INVOICES WITH 'TEST' ===")
    for invoice in all_invoices:
        if 'TEST' in invoice.get('serial_numbers', ''):
            print(f"Invoice: {invoice.get('invoice_number')}")
            print(f"Serial Numbers: {invoice.get('serial_numbers')}")
            print(f"Transaction Type: {invoice.get('transaction_type')}")
            print(f"Buyer ID: {invoice.get('buyer_id')}")
            print(f"Seller ID: {invoice.get('seller_id')}")
            print("---")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_specific_invoice()) 
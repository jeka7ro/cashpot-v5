import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_invoices():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cash_pot
    
    # Get all invoices
    invoices = await db.invoices.find({}).to_list(10)
    
    print("=== ALL INVOICES ===")
    for invoice in invoices:
        print(f"Invoice: {invoice.get('invoice_number')}")
        print(f"Serial Numbers: {invoice.get('serial_numbers')}")
        print(f"Transaction Type: {invoice.get('transaction_type')}")
        print(f"Buyer ID: {invoice.get('buyer_id')}")
        print(f"Seller ID: {invoice.get('seller_id')}")
        print("---")
    
    # Check for specific serial number
    invoices_with_188681 = await db.invoices.find({
        'serial_numbers': {'$regex': '188681'}
    }).to_list(10)
    
    print(f"\n=== INVOICES WITH 188681: {len(invoices_with_188681)} ===")
    for invoice in invoices_with_188681:
        print(f"Invoice: {invoice.get('invoice_number')}")
        print(f"Serial Numbers: {invoice.get('serial_numbers')}")
        print(f"Transaction Type: {invoice.get('transaction_type')}")
        print(f"Buyer ID: {invoice.get('buyer_id')}")
        print(f"Seller ID: {invoice.get('seller_id')}")
        print("---")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_invoices()) 
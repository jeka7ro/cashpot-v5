import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_date_format():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cash_pot
    
    # Get the test invoice
    invoice = await db.invoices.find_one({'invoice_number': 'TEST'})
    
    if invoice:
        print("=== TEST INVOICE DETAILS ===")
        print(f"Invoice Number: {invoice.get('invoice_number')}")
        print(f"Serial Numbers: {invoice.get('serial_numbers')}")
        print(f"Transaction Type: {invoice.get('transaction_type')}")
        print(f"Issue Date: {invoice.get('issue_date')}")
        print(f"Issue Date Type: {type(invoice.get('issue_date'))}")
        
        # Test date conversion
        issue_date = invoice.get('issue_date')
        if issue_date:
            date_obj = issue_date
            print(f"Date Object: {date_obj}")
            print(f"Date Object Type: {type(date_obj)}")
            
            # Convert to ISO string
            iso_string = date_obj.isoformat()
            print(f"ISO String: {iso_string}")
            
            # Convert to YYYY-MM-DD format
            date_only = date_obj.strftime('%Y-%m-%d')
            print(f"Date Only: {date_only}")
            
            # Test JavaScript Date conversion
            js_date = date_obj.strftime('%Y-%m-%d')
            print(f"JavaScript Date Format: {js_date}")
    else:
        print("❌ Test invoice not found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_date_format()) 
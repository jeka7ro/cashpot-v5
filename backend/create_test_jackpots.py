import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import uuid

async def create_test_jackpots():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.cash_pot

    # Get existing slot machines to link jackpots to them
    slots = await db.slot_machines.find({}).to_list(10)

    if not slots:
        print("❌ Need slot machines to create test jackpots")
        return

    print("📋 Found existing slots:")
    for slot in slots:
        print(f"  - Serial: {slot['serial_number']}")

    # Create test jackpots for existing slots
    jackpot1 = {
        "id": str(uuid.uuid4()),
        "serial_number": "188681",  # Link to first slot
        "jackpot_type": "progressive",
        "jackpot_name": "Mega Jackpot",
        "increment_rate": 0.5,
        "level_1": "1000",
        "level_2": "5000",
        "level_3": "10000",
        "level_4": "25000",
        "level_5": "50000",
        "last_reset_date": datetime.utcnow(),
        "next_reset_date": datetime.utcnow() + timedelta(days=30),
        "status": "active",
        "description": "Progressive jackpot for slot 188681",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }

    jackpot2 = {
        "id": str(uuid.uuid4()),
        "serial_number": "188681",  # Link to first slot (multiple jackpots)
        "jackpot_type": "fixed",
        "jackpot_name": "Fixed Bonus",
        "increment_rate": 0.0,
        "level_1": "500",
        "level_2": "1000",
        "level_3": "2000",
        "level_4": None,
        "level_5": None,
        "last_reset_date": datetime.utcnow(),
        "next_reset_date": None,
        "status": "active",
        "description": "Fixed jackpot for slot 188681",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }

    jackpot3 = {
        "id": str(uuid.uuid4()),
        "serial_number": "188684",  # Link to second slot
        "jackpot_type": "mystery",
        "jackpot_name": "Mystery Prize",
        "increment_rate": 0.3,
        "level_1": "200",
        "level_2": "500",
        "level_3": "1000",
        "level_4": "2500",
        "level_5": None,
        "last_reset_date": datetime.utcnow(),
        "next_reset_date": datetime.utcnow() + timedelta(days=7),
        "status": "active",
        "description": "Mystery jackpot for slot 188684",
        "created_at": datetime.utcnow(),
        "created_by": "admin"
    }

    # Clear existing jackpots first
    await db.jackpots.delete_many({})
    print("🗑️  Cleared existing jackpots")

    # Insert jackpots
    try:
        await db.jackpots.insert_one(jackpot1)
        await db.jackpots.insert_one(jackpot2)
        await db.jackpots.insert_one(jackpot3)

        print("✅ Test jackpots created successfully!")
        print(f"🎰 Slot 188681: 2 jackpots (Progressive + Fixed)")
        print(f"🎰 Slot 188684: 1 jackpot (Mystery)")
        print(f"📊 Total jackpots created: 3")

    except Exception as e:
        print(f"❌ Error creating test jackpots: {e}")

    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_jackpots())

#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== Environment Variables Test ===")
print(f"MONGO_URL: {os.getenv('MONGO_URL', 'NOT SET')}")
print(f"JWT_SECRET_KEY: {'SET' if os.getenv('JWT_SECRET_KEY') else 'NOT SET'}")
print(f"JWT_ALGORITHM: {os.getenv('JWT_ALGORITHM', 'NOT SET')}")
print(f"SECRET_KEY: {'SET' if os.getenv('SECRET_KEY') else 'NOT SET'}")
print(f"ENVIRONMENT: {os.getenv('ENVIRONMENT', 'NOT SET')}")
print(f"DEBUG: {os.getenv('DEBUG', 'NOT SET')}")

print("\n=== Testing Server Import ===")
try:
    import server
    print("✅ Server imports successfully")
except Exception as e:
    print(f"❌ Server import failed: {e}")
    sys.exit(1)

print("\n=== Testing Database Connection ===")
try:
    import asyncio
    from motor.motor_asyncio import AsyncIOMotorClient
    
    async def test_db():
        client = AsyncIOMotorClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
        try:
            await client.admin.command('ping')
            print("✅ Database connection successful")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
        finally:
            client.close()
    
    result = asyncio.run(test_db())
    if not result:
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Database test failed: {e}")
    sys.exit(1)

print("\n✅ All tests passed!")

#!/usr/bin/env python3
import os
import sys

def test_environment():
    print("🔍 Testing Railway environment...")
    
    # Test environment variables
    port = os.getenv("PORT", "8000")
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    
    print(f"✅ PORT: {port}")
    print(f"✅ MONGO_URL: {mongo_url}")
    
    # Test imports
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        sys.exit(1)
    
    try:
        import motor
        print("✅ Motor imported successfully")
    except ImportError as e:
        print(f"❌ Motor import failed: {e}")
        sys.exit(1)
    
    print("🎉 All tests passed!")

if __name__ == "__main__":
    test_environment()

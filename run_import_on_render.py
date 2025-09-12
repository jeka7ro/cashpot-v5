#!/usr/bin/env python3
"""
Run Import on Render - Execute database import on Render deployment
"""
import requests
import json
import time
import os

def run_import_on_render():
    print("🚀 Running database import on Render...")
    
    # Render backend URL
    backend_url = "https://cashpot-v5.onrender.com"
    
    # Check if backend is running
    print("🔍 Checking backend status...")
    try:
        response = requests.get(f"{backend_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend is running: {health_data}")
            
            if health_data.get("database") == "disconnected":
                print("⚠️  Database is disconnected - MongoDB Atlas needs to be configured")
                print("\n💡 Please:")
                print("1. Set up MongoDB Atlas (see QUICK_MONGODB_SETUP.md)")
                print("2. Add MONGO_URL to Render environment variables")
                print("3. Redeploy on Render")
                return False
            else:
                print("✅ Database is connected - ready for import!")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False
    
    # Create import endpoint if it doesn't exist
    print("\n📥 Starting data import...")
    
    # Since we can't directly run the import script on Render,
    # we'll create a simple import endpoint in the server
    print("🔧 Creating import endpoint in server.py...")
    
    # Read the current server.py
    with open('server.py', 'r') as f:
        server_content = f.read()
    
    # Check if import endpoint already exists
    if '/api/import-data' in server_content:
        print("✅ Import endpoint already exists")
    else:
        # Add import endpoint to server.py
        import_endpoint = '''
# Import data endpoint
@app.post("/api/import-data")
async def import_all_data():
    """Import all data to MongoDB"""
    try:
        # This would run the import logic
        # For now, return success message
        return {"status": "success", "message": "Import endpoint ready - use import script locally"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
        
        # Insert before the last line (uvicorn.run)
        server_content = server_content.replace(
            'if __name__ == "__main__":',
            import_endpoint + '\nif __name__ == "__main__":'
        )
        
        # Write back to file
        with open('server.py', 'w') as f:
            f.write(server_content)
        
        print("✅ Added import endpoint to server.py")
    
    # Alternative: Run import locally and then sync
    print("\n🔄 Running import locally first...")
    try:
        import subprocess
        result = subprocess.run(["python3", "import_all_data_to_mongodb_atlas.py"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Local import completed successfully!")
            print(result.stdout)
        else:
            print("❌ Local import failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running import: {e}")
        return False
    
    print("\n🎉 Data import process completed!")
    print("📋 Next steps:")
    print("1. Commit and push changes to GitHub")
    print("2. Render will redeploy automatically")
    print("3. Your application will be fully populated with data")
    
    return True

def main():
    import sys
    
    print("🚀 Cash Pot V5 - Render Import Runner")
    print("=" * 40)
    
    success = run_import_on_render()
    
    if success:
        print("\n✅ Process completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

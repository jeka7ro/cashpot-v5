#!/usr/bin/env python3
"""
Fix Render Database Connection - Configure MongoDB for Render deployment
"""
import os

def main():
    print("🔧 Fixing Render database connection...")
    
    # Check if server.py has proper MongoDB configuration for cloud deployment
    with open('server.py', 'r') as f:
        content = f.read()
    
    issues_found = []
    
    # Check MongoDB connection configuration
    if 'mongodb://localhost' in content:
        issues_found.append("MongoDB still configured for localhost")
    
    if 'MONGO_URL' not in content or 'os.getenv("MONGO_URL")' not in content:
        issues_found.append("MONGO_URL environment variable not properly handled")
    
    if issues_found:
        print("⚠️  Issues found:")
        for issue in issues_found:
            print(f"   - {issue}")
        
        # Fix MongoDB connection for cloud deployment
        fixed_content = content
        
        # Replace any hardcoded localhost MongoDB URLs
        fixed_content = fixed_content.replace(
            'mongodb://localhost:27017',
            'os.getenv("MONGO_URL", "mongodb://localhost:27017")'
        )
        
        # Also fix any other MongoDB connection strings
        fixed_content = fixed_content.replace(
            '"mongodb://localhost:27017"',
            'os.getenv("MONGO_URL", "mongodb://localhost:27017")'
        )
        
        # Write the fixed version
        with open('server.py', 'w') as f:
            f.write(fixed_content)
        
        print("✅ Fixed server.py for cloud deployment")
    else:
        print("✅ No MongoDB connection issues found in server.py")
    
    # Create Render-specific configuration
    render_config = """# Render Environment Variables
# Add these in Render dashboard under Environment tab

# MongoDB Configuration (use MongoDB Atlas for cloud deployment)
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/cashpot_v5?retryWrites=true&w=majority
DB_NAME=cashpot_v5

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here-12345-67890
JWT_ALGORITHM=HS256

# Server Configuration
HOST=0.0.0.0
PORT=10000

# Optional: Google Sheets API
# GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/credentials.json
"""
    
    with open('render.env.template', 'w') as f:
        f.write(render_config)
    
    print("✅ Created render.env.template")
    
    # Create a simple MongoDB Atlas setup guide
    atlas_guide = """# MongoDB Atlas Setup for Render

## 1. Create MongoDB Atlas Account
1. Go to https://cloud.mongodb.com
2. Create a free account
3. Create a new cluster (free tier)

## 2. Configure Database Access
1. Go to "Database Access" in the left menu
2. Add a new database user
3. Create a username and password
4. Set privileges to "Read and write to any database"

## 3. Configure Network Access
1. Go to "Network Access" in the left menu
2. Add IP Address: 0.0.0.0/0 (allow all IPs)
3. Or add Render's IP ranges

## 4. Get Connection String
1. Go to "Clusters" in the left menu
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace <password> with your database user password
6. Replace <dbname> with "cashpot_v5"

## 5. Add to Render Environment Variables
1. Go to your Render service dashboard
2. Go to "Environment" tab
3. Add MONGO_URL with your connection string
4. Add JWT_SECRET_KEY with a secure random string
5. Add DB_NAME=cashpot_v5

## Example MONGO_URL:
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/cashpot_v5?retryWrites=true&w=majority
"""
    
    with open('MONGODB_ATLAS_SETUP.md', 'w') as f:
        f.write(atlas_guide)
    
    print("✅ Created MONGODB_ATLAS_SETUP.md")
    
    print("\n🎉 Render database fixes completed!")
    print("\n📋 Next steps:")
    print("1. Set up MongoDB Atlas (free tier)")
    print("2. Add MONGO_URL to Render environment variables")
    print("3. Add JWT_SECRET_KEY to Render environment variables")
    print("4. Redeploy on Render")
    print("5. Application will work from anywhere!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Deployment script for Render with specific account setup
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def print_header():
    """Print deployment header"""
    print("🚀" + "=" * 60)
    print("🚀  CASHPOT - Deploy to Render (jeka7ro@gmail.com)")
    print("🚀" + "=" * 60)
    print()

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    required_tools = ['python3', 'node', 'npm', 'git']
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"✅ {tool} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {tool} is not installed")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n❌ Missing required tools: {', '.join(missing_tools)}")
        print("Please install them before continuing.")
        return False
    
    print("✅ All requirements met!")
    return True

def setup_mongodb_atlas():
    """Guide user through MongoDB Atlas setup"""
    print("\n📊 MongoDB Atlas Setup")
    print("-" * 30)
    print("1. Go to https://cloud.mongodb.com/")
    print("2. Sign in with your account")
    print("3. Create a new cluster (choose FREE tier)")
    print("4. Create a database user:")
    print("   - Username: cashpot_admin")
    print("   - Password: [generate a strong password]")
    print("5. Whitelist your IP address (or use 0.0.0.0/0 for all IPs)")
    print("6. Get your connection string")
    print("7. Replace <password> with your actual password")
    print("8. Replace <dbname> with 'casino_management'")
    
    connection_string = input("\nEnter your MongoDB Atlas connection string: ").strip()
    
    if not connection_string:
        print("❌ Connection string is required!")
        return None
    
    return connection_string

def export_local_data():
    """Export data from local MongoDB"""
    print("\n📤 Exporting local data...")
    
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Run export script
        result = subprocess.run([sys.executable, 'export_data.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Local data exported successfully!")
            return True
        else:
            print(f"❌ Export failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during export: {e}")
        return False
    finally:
        # Return to root directory
        os.chdir('..')

def import_data_to_atlas(mongo_url):
    """Import data to MongoDB Atlas"""
    print("\n📥 Importing data to MongoDB Atlas...")
    
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Set environment variable
        os.environ['MONGO_URL'] = mongo_url
        
        # Run import script
        result = subprocess.run([sys.executable, 'import_data.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Data imported to MongoDB Atlas successfully!")
            return True
        else:
            print(f"❌ Import failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during import: {e}")
        return False
    finally:
        # Return to root directory
        os.chdir('..')

def get_github_username():
    """Get GitHub username"""
    github_username = input("Enter your GitHub username (default: jeka7ro): ").strip()
    if not github_username:
        github_username = "jeka7ro"
        print(f"✅ Using default GitHub username: {github_username}")
    return github_username

def create_render_deployment_guide(mongo_url, github_username):
    """Create specific deployment guide for Render"""
    
    guide_content = f"""
# 🚀 CASHPOT - Render Deployment Guide
## Account: jeka7ro@gmail.com

## 📊 Backend Deployment (Render)

### 1. Access Render
1. Go to https://render.com/
2. Sign in with: **jeka7ro@gmail.com**
3. Click "New +" → "Web Service"

### 2. Connect Repository
1. Click "Connect a repository"
2. Select your GitHub repository
3. Choose the repository with CASHPOT code

### 3. Configure Service
- **Name**: `cashpot-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python server.py`
- **Plan**: `Free`

### 4. Environment Variables
Add these environment variables in Render dashboard:

```
MONGO_URL={mongo_url}
DB_NAME=casino_management
JWT_SECRET_KEY=your_random_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["https://{github_username}.github.io", "https://{github_username}.github.io/cash-pot-v5-copy"]
SECRET_KEY=your_random_secret_key_here
ENVIRONMENT=production
DEBUG=false
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@cashpot.com
ADMIN_PASSWORD=admin123
API_V1_STR=/api
PROJECT_NAME=CASHPOT Gaming Management System
```

### 5. Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Note the service URL (e.g., https://cashpot-backend.onrender.com)

## 🌐 Frontend Deployment (GitHub Pages)

### 1. Enable GitHub Pages
1. Go to your GitHub repository
2. Click "Settings" tab
3. Scroll to "Pages" section
4. Set source to "GitHub Actions"

### 2. Add Repository Secret
1. Go to "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Name: `BACKEND_URL`
4. Value: Your Render backend URL (from step 5 above)

### 3. Deploy
1. Push your code to main/master branch
2. GitHub Actions will automatically build and deploy
3. Your site will be available at: https://{github_username}.github.io/cash-pot-v5-copy

## 🧪 Testing

### Test Backend
```bash
curl https://your-backend-url.onrender.com/api/health
```

### Test Frontend
Visit: https://{github_username}.github.io/cash-pot-v5-copy

## 🔧 Troubleshooting

### Render Issues
- **Service not starting**: Check Render logs
- **Build failing**: Check build logs in Render dashboard
- **Database connection failed**: Verify MONGO_URL environment variable

### GitHub Pages Issues
- **Build failing**: Check GitHub Actions logs
- **API calls failing**: Verify BACKEND_URL secret is set correctly

## 📞 Support
- Render: https://render.com/docs
- GitHub Pages: https://docs.github.com/en/pages

---
**🎉 Your CASHPOT application will be live at:**
**Frontend**: https://{github_username}.github.io/cash-pot-v5-copy
**Backend**: https://your-backend-url.onrender.com
"""
    
    with open('RENDER_DEPLOYMENT_GUIDE.md', 'w') as f:
        f.write(guide_content)
    
    print("✅ Created RENDER_DEPLOYMENT_GUIDE.md")

def main():
    """Main deployment function"""
    print_header()
    
    # Check requirements
    if not check_requirements():
        return
    
    # Get GitHub username (default: jeka7ro)
    github_username = get_github_username()
    
    # Get MongoDB Atlas connection string
    mongo_url = setup_mongodb_atlas()
    if not mongo_url:
        return
    
    # Export local data
    if not export_local_data():
        print("❌ Failed to export local data. Please check your local MongoDB connection.")
        return
    
    # Import data to MongoDB Atlas
    if not import_data_to_atlas(mongo_url):
        print("❌ Failed to import data to MongoDB Atlas.")
        return
    
    # Create deployment guide
    create_render_deployment_guide(mongo_url, github_username)
    
    # Final instructions
    print("\n🎉 Setup Completed!")
    print("=" * 50)
    print(f"📊 Database: MongoDB Atlas")
    print(f"🔧 Backend: Render (jeka7ro@gmail.com)")
    print(f"🌐 Frontend: GitHub Pages")
    print(f"👤 GitHub Username: {github_username}")
    
    print("\n📋 Next Steps:")
    print("1. Go to https://render.com/ and sign in with jeka7ro@gmail.com")
    print("2. Follow the instructions in RENDER_DEPLOYMENT_GUIDE.md")
    print("3. Deploy backend to Render")
    print("4. Configure GitHub Pages")
    print("5. Test the application")
    
    print(f"\n🔗 Your application will be available at:")
    print(f"   Frontend: https://jeka7ro.github.io/cash-pot-v5-copy")
    print(f"   Backend: https://your-backend-url.onrender.com")
    
    print("\n📁 Files created:")
    print("- RENDER_DEPLOYMENT_GUIDE.md (deployment instructions)")
    print("- backend/exports/ (exported data files)")

if __name__ == "__main__":
    main()

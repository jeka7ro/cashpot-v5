#!/usr/bin/env python3
"""
Setup script for Render backend + GitHub Pages frontend deployment
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🚀" + "=" * 60)
    print("🚀  CASHPOT - Render Backend + GitHub Pages Frontend Setup")
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
    print("2. Create a free account or sign in")
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

def setup_render_backend(mongo_url, github_username):
    """Setup backend for Render deployment"""
    print("\n🔧 Setting up backend for Render deployment...")
    
    # Update render.yaml with correct CORS origins
    render_config = f"""services:
  - type: web
    name: cashpot-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python server.py
    envVars:
      - key: MONGO_URL
        value: {mongo_url}
      - key: DB_NAME
        value: casino_management
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: JWT_ALGORITHM
        value: HS256
      - key: JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      - key: CORS_ORIGINS
        value: '["https://{github_username}.github.io", "https://{github_username}.github.io/cash-pot-v5-copy"]'
      - key: SECRET_KEY
        generateValue: true
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: false
      - key: ADMIN_USERNAME
        value: admin
      - key: ADMIN_EMAIL
        value: admin@cashpot.com
      - key: ADMIN_PASSWORD
        value: admin123
      - key: API_V1_STR
        value: /api
      - key: PROJECT_NAME
        value: CASHPOT Gaming Management System"""
    
    with open('backend/render.yaml', 'w') as f:
        f.write(render_config)
    
    print("✅ Backend configuration updated for Render")
    return True

def setup_github_pages_frontend(github_username):
    """Setup frontend for GitHub Pages"""
    print("\n🔧 Setting up frontend for GitHub Pages...")
    
    # Update GitHub Actions workflow
    workflow_content = f"""name: Deploy to GitHub Pages

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
        
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
        
    - name: Build
      run: |
        cd frontend
        npm run build
      env:
        REACT_APP_BACKEND_URL: ${{{{ secrets.BACKEND_URL }}}}
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
      with:
        github_token: ${{{{ secrets.GITHUB_TOKEN }}}}
        publish_dir: ./frontend/build
        cname: # Add your custom domain here if you have one"""
    
    # Create .github/workflows directory if it doesn't exist
    os.makedirs('.github/workflows', exist_ok=True)
    
    with open('.github/workflows/deploy.yml', 'w') as f:
        f.write(workflow_content)
    
    # Update frontend package.json with homepage
    package_json_path = 'frontend/package.json'
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        package_data['homepage'] = f'https://{github_username}.github.io/cash-pot-v5-copy'
        
        with open(package_json_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        
        print("✅ Frontend package.json updated with GitHub Pages URL")
    
    print("✅ Frontend configuration updated for GitHub Pages")
    return True

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

def create_deployment_instructions(github_username):
    """Create deployment instructions"""
    instructions = f"""
# 🚀 CASHPOT Deployment Instructions - Render + GitHub Pages

## 📊 Backend Deployment (Render)

### 1. Deploy to Render
1. Go to https://render.com/
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: cashpot-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Plan**: Free

### 2. Environment Variables
Add these environment variables in Render dashboard:
- `MONGO_URL`: Your MongoDB Atlas connection string
- `DB_NAME`: casino_management
- `JWT_SECRET_KEY`: [Generate a random string]
- `JWT_ALGORITHM`: HS256
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: 30
- `CORS_ORIGINS`: ["https://{github_username}.github.io", "https://{github_username}.github.io/cash-pot-v5-copy"]
- `SECRET_KEY`: [Generate a random string]
- `ENVIRONMENT`: production
- `DEBUG`: false
- `ADMIN_USERNAME`: admin
- `ADMIN_EMAIL`: admin@cashpot.com
- `ADMIN_PASSWORD`: admin123
- `API_V1_STR`: /api
- `PROJECT_NAME`: CASHPOT Gaming Management System

### 3. Deploy
Click "Create Web Service" and wait for deployment to complete.

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
4. Value: Your Render backend URL (e.g., https://cashpot-backend.onrender.com)

### 3. Deploy
1. Push your code to main/master branch
2. GitHub Actions will automatically build and deploy
3. Your site will be available at: https://{github_username}.github.io/cash-pot-v5-copy

## 🧪 Testing

### 1. Test Backend
```bash
curl https://your-backend-url.onrender.com/api/health
```

### 2. Test Frontend
Visit: https://{github_username}.github.io/cash-pot-v5-copy

### 3. Test Full Application
1. Open frontend URL
2. Try to login with admin/password
3. Test all functionalities

## 🔧 Troubleshooting

### Backend Issues
- Check Render logs for errors
- Verify environment variables are set
- Test MongoDB connection

### Frontend Issues
- Check GitHub Actions logs
- Verify BACKEND_URL secret is set
- Check browser console for errors

### CORS Issues
- Update CORS_ORIGINS in Render with correct frontend URL
- Restart the backend service

## 📞 Support
- Render: https://render.com/docs
- GitHub Pages: https://docs.github.com/en/pages
- MongoDB Atlas: https://docs.atlas.mongodb.com/

---
**🎉 Your CASHPOT application will be live at:**
**Frontend**: https://{github_username}.github.io/cash-pot-v5-copy
**Backend**: https://your-backend-url.onrender.com
"""
    
    with open('RENDER_GITHUB_DEPLOYMENT.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Deployment instructions created: RENDER_GITHUB_DEPLOYMENT.md")

def main():
    """Main setup function"""
    print_header()
    
    # Check requirements
    if not check_requirements():
        return
    
    # Get GitHub username
    github_username = input("Enter your GitHub username: ").strip()
    if not github_username:
        print("❌ GitHub username is required!")
        return
    
    # Get MongoDB Atlas connection string
    mongo_url = setup_mongodb_atlas()
    if not mongo_url:
        return
    
    # Export local data
    if not export_local_data():
        print("❌ Failed to export local data. Please check your local MongoDB connection.")
        return
    
    # Setup backend for Render
    if not setup_render_backend(mongo_url, github_username):
        print("❌ Failed to setup backend for Render.")
        return
    
    # Setup frontend for GitHub Pages
    if not setup_github_pages_frontend(github_username):
        print("❌ Failed to setup frontend for GitHub Pages.")
        return
    
    # Import data to MongoDB Atlas
    if not import_data_to_atlas(mongo_url):
        print("❌ Failed to import data to MongoDB Atlas.")
        return
    
    # Create deployment instructions
    create_deployment_instructions(github_username)
    
    # Final instructions
    print("\n🎉 Setup Completed!")
    print("=" * 50)
    print(f"📊 Database: MongoDB Atlas")
    print(f"🔧 Backend: Render")
    print(f"🌐 Frontend: GitHub Pages")
    print(f"👤 GitHub Username: {github_username}")
    
    print("\n📋 Next Steps:")
    print("1. Deploy backend to Render (follow RENDER_GITHUB_DEPLOYMENT.md)")
    print("2. Add BACKEND_URL secret to GitHub repository")
    print("3. Push code to trigger GitHub Pages deployment")
    print("4. Test the application")
    
    print(f"\n🔗 Your application will be available at:")
    print(f"   Frontend: https://{github_username}.github.io/cash-pot-v5-copy")
    print(f"   Backend: https://your-backend-url.onrender.com")
    
    print("\n📁 Files created/updated:")
    print("- backend/render.yaml (Render configuration)")
    print("- .github/workflows/deploy.yml (GitHub Actions)")
    print("- frontend/package.json (updated homepage)")
    print("- RENDER_GITHUB_DEPLOYMENT.md (deployment guide)")

if __name__ == "__main__":
    main()

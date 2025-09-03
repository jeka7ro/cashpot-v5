#!/usr/bin/env python3
"""
CASHPOT Gaming Management System - Online Deployment Script
This script will help you deploy your application online with shared database
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    """Print deployment header"""
    print("🎰" + "=" * 60)
    print("🎰  CASHPOT Gaming Management System - Online Deployment")
    print("🎰" + "=" * 60)
    print()

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    required_tools = ['python3', 'node', 'npm']
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

def setup_backend_production(mongo_url):
    """Setup backend for production"""
    print("\n🔧 Setting up backend for production...")
    
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Set environment variable
        os.environ['MONGO_URL'] = mongo_url
        
        # Run setup script
        result = subprocess.run([sys.executable, 'setup_production.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Backend production setup completed!")
            return True
        else:
            print(f"❌ Backend setup failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during backend setup: {e}")
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

def setup_frontend_production(backend_url):
    """Setup frontend for production"""
    print("\n🔧 Setting up frontend for production...")
    
    try:
        # Change to frontend directory
        os.chdir('frontend')
        
        # Run setup script
        result = subprocess.run(['node', 'setup_production.js', backend_url], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Frontend production setup completed!")
            return True
        else:
            print(f"❌ Frontend setup failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during frontend setup: {e}")
        return False
    finally:
        # Return to root directory
        os.chdir('..')

def deploy_backend():
    """Guide user through backend deployment"""
    print("\n🚀 Backend Deployment Options")
    print("-" * 30)
    print("Choose your deployment platform:")
    print("1. Railway (Recommended - Easy setup)")
    print("2. Render (Free tier available)")
    print("3. Heroku (Paid)")
    print("4. Manual deployment")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚂 Railway Deployment:")
        print("1. Go to https://railway.app/")
        print("2. Sign up with GitHub")
        print("3. Create new project from GitHub repository")
        print("4. Select your repository")
        print("5. Add environment variables from backend/.env file")
        print("6. Deploy!")
        return "railway"
    elif choice == "2":
        print("\n🎨 Render Deployment:")
        print("1. Go to https://render.com/")
        print("2. Sign up with GitHub")
        print("3. Create new Web Service")
        print("4. Connect your repository")
        print("5. Add environment variables from backend/render.env file")
        print("6. Deploy!")
        return "render"
    elif choice == "3":
        print("\n🟣 Heroku Deployment:")
        print("1. Go to https://heroku.com/")
        print("2. Create new app")
        print("3. Connect GitHub repository")
        print("4. Add environment variables")
        print("5. Deploy!")
        return "heroku"
    else:
        print("\n📋 Manual Deployment:")
        print("1. Set up your own server")
        print("2. Install Python and dependencies")
        print("3. Set environment variables")
        print("4. Run the application")
        return "manual"

def deploy_frontend():
    """Guide user through frontend deployment"""
    print("\n🌐 Frontend Deployment Options")
    print("-" * 30)
    print("Choose your deployment platform:")
    print("1. Netlify (Recommended - Easy setup)")
    print("2. Vercel (Great for React apps)")
    print("3. GitHub Pages")
    print("4. Manual deployment")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🟢 Netlify Deployment:")
        print("1. Go to https://netlify.com/")
        print("2. Sign up with GitHub")
        print("3. Create new site from Git")
        print("4. Select your repository")
        print("5. Set build command: npm install && npm run build")
        print("6. Set publish directory: build")
        print("7. Deploy!")
        return "netlify"
    elif choice == "2":
        print("\n🟡 Vercel Deployment:")
        print("1. Go to https://vercel.com/")
        print("2. Sign up with GitHub")
        print("3. Import your repository")
        print("4. Vercel will auto-detect configuration")
        print("5. Deploy!")
        return "vercel"
    elif choice == "3":
        print("\n📄 GitHub Pages Deployment:")
        print("1. Enable GitHub Pages in repository settings")
        print("2. Set source to GitHub Actions")
        print("3. Create workflow file")
        print("4. Push to trigger deployment")
        return "github-pages"
    else:
        print("\n📋 Manual Deployment:")
        print("1. Build the application: npm run build")
        print("2. Upload build folder to your web server")
        print("3. Configure web server for SPA")
        return "manual"

def main():
    """Main deployment function"""
    print_header()
    
    # Check requirements
    if not check_requirements():
        return
    
    # Get MongoDB Atlas connection string
    mongo_url = setup_mongodb_atlas()
    if not mongo_url:
        return
    
    # Export local data
    if not export_local_data():
        print("❌ Failed to export local data. Please check your local MongoDB connection.")
        return
    
    # Setup backend for production
    if not setup_backend_production(mongo_url):
        print("❌ Failed to setup backend for production.")
        return
    
    # Import data to MongoDB Atlas
    if not import_data_to_atlas(mongo_url):
        print("❌ Failed to import data to MongoDB Atlas.")
        return
    
    # Deploy backend
    backend_platform = deploy_backend()
    
    # Get backend URL
    backend_url = input("\nEnter your deployed backend URL (e.g., https://your-app.railway.app): ").strip()
    if not backend_url:
        print("❌ Backend URL is required!")
        return
    
    # Setup frontend for production
    if not setup_frontend_production(backend_url):
        print("❌ Failed to setup frontend for production.")
        return
    
    # Deploy frontend
    frontend_platform = deploy_frontend()
    
    # Final instructions
    print("\n🎉 Deployment Setup Completed!")
    print("=" * 50)
    print(f"📊 Database: MongoDB Atlas")
    print(f"🔧 Backend: {backend_platform}")
    print(f"🌐 Frontend: {frontend_platform}")
    print(f"🔗 Backend URL: {backend_url}")
    
    print("\n📋 Final Steps:")
    print("1. Deploy your backend to the chosen platform")
    print("2. Deploy your frontend to the chosen platform")
    print("3. Update CORS settings in backend to include your frontend domain")
    print("4. Test the application with multiple users")
    
    print("\n🔐 Security Notes:")
    print("- Change default admin password after first login")
    print("- Use strong passwords for database users")
    print("- Regularly backup your data")
    print("- Monitor your application logs")
    
    print("\n📁 Files created:")
    print("- backend/.env (production environment variables)")
    print("- backend/exports/ (exported data files)")
    print("- backend/railway.json (Railway config)")
    print("- backend/render.env (Render config)")
    print("- frontend/netlify.toml (Netlify config)")
    print("- frontend/vercel.json (Vercel config)")
    print("- frontend/deploy.sh (deployment script)")

if __name__ == "__main__":
    main()

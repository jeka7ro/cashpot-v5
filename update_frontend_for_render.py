#!/usr/bin/env python3
"""
Script to update frontend with Render backend URL
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def update_frontend_backend_url(backend_url):
    """Update frontend with backend URL"""
    print(f"🔧 Updating frontend with backend URL: {backend_url}")
    
    try:
        # Change to frontend directory
        os.chdir('frontend')
        
        # Run the update script
        result = subprocess.run(['node', 'update_backend_url.js', backend_url], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Frontend updated successfully!")
            return True
        else:
            print(f"❌ Frontend update failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating frontend: {e}")
        return False
    finally:
        # Return to root directory
        os.chdir('..')

def create_env_file(backend_url):
    """Create .env file for frontend build"""
    print("🔧 Creating .env file for frontend...")
    
    env_content = f"""REACT_APP_BACKEND_URL={backend_url}
GENERATE_SOURCEMAP=false
"""
    
    env_path = Path('frontend/.env')
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ Created frontend/.env file")

def update_package_json(github_username):
    """Update package.json with GitHub Pages URL"""
    print("🔧 Updating package.json for GitHub Pages...")
    
    package_json_path = Path('frontend/package.json')
    
    if package_json_path.exists():
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        package_data['homepage'] = f'https://{github_username}.github.io/cash-pot-v5-copy'
        
        with open(package_json_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        
        print("✅ Updated package.json with GitHub Pages URL")
    else:
        print("❌ package.json not found!")

def main():
    """Main function"""
    print("🚀 Updating Frontend for Render Backend")
    print("=" * 50)
    
    # Get backend URL
    backend_url = input("Enter your Render backend URL (e.g., https://cashpot-backend.onrender.com): ").strip()
    if not backend_url:
        print("❌ Backend URL is required!")
        return
    
    # Get GitHub username (default: jeka7ro)
    github_username = input("Enter your GitHub username (default: jeka7ro): ").strip()
    if not github_username:
        github_username = "jeka7ro"
        print(f"✅ Using default GitHub username: {github_username}")
    
    # Update frontend
    if not update_frontend_backend_url(backend_url):
        return
    
    # Create .env file
    create_env_file(backend_url)
    
    # Update package.json
    update_package_json(github_username)
    
    print("\n🎉 Frontend updated successfully!")
    print("\n📋 Next steps:")
    print("1. Commit and push your changes to GitHub")
    print("2. GitHub Actions will automatically deploy to GitHub Pages")
    print(f"3. Your app will be available at: https://jeka7ro.github.io/cash-pot-v5-copy")
    
    print("\n📁 Files updated:")
    print("- frontend/src/app.js (backend URL)")
    print("- frontend/.env (environment variables)")
    print("- frontend/package.json (homepage URL)")

if __name__ == "__main__":
    main()

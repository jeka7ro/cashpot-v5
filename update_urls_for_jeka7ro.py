#!/usr/bin/env python3
"""
Script to update all URLs to use jeka7ro as default username
"""

import os
import json
from pathlib import Path

def update_package_json():
    """Update frontend package.json with jeka7ro homepage"""
    print("🔧 Updating frontend package.json...")
    
    package_json_path = Path('frontend/package.json')
    
    if package_json_path.exists():
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        package_data['homepage'] = 'https://jeka7ro.github.io/cash-pot-v5-copy'
        
        with open(package_json_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        
        print("✅ Updated package.json with jeka7ro homepage")
    else:
        print("❌ package.json not found!")

def create_cname_file():
    """Create CNAME file for GitHub Pages"""
    print("🔧 Creating CNAME file for GitHub Pages...")
    
    cname_path = Path('frontend/public/CNAME')
    cname_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(cname_path, 'w') as f:
        f.write('jeka7ro.github.io')
    
    print("✅ Created CNAME file")

def update_env_file():
    """Create .env file with default values"""
    print("🔧 Creating .env file...")
    
    env_content = """REACT_APP_BACKEND_URL=https://your-backend-url.onrender.com
GENERATE_SOURCEMAP=false
"""
    
    env_path = Path('frontend/.env')
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file")

def main():
    """Main function"""
    print("🚀 Updating URLs for jeka7ro")
    print("=" * 40)
    
    update_package_json()
    create_cname_file()
    update_env_file()
    
    print("\n🎉 All URLs updated for jeka7ro!")
    print("\n📋 Summary:")
    print("- Frontend will be available at: https://jeka7ro.github.io/cash-pot-v5-copy")
    print("- Backend URL needs to be updated in .env after deployment")
    print("- CORS is configured for jeka7ro.github.io")
    
    print("\n📁 Files updated:")
    print("- frontend/package.json (homepage)")
    print("- frontend/public/CNAME (GitHub Pages)")
    print("- frontend/.env (environment variables)")

if __name__ == "__main__":
    main()

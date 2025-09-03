#!/usr/bin/env python3
"""
Script to fix GitHub Pages URLs for the correct repository name
"""

import os
import json
from pathlib import Path

def update_package_json():
    """Update frontend package.json with correct repository name"""
    print("🔧 Updating frontend package.json...")
    
    package_json_path = Path('frontend/package.json')
    
    if package_json_path.exists():
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        package_data['homepage'] = 'https://jeka7ro.github.io/cashpot-v5'
        
        with open(package_json_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        
        print("✅ Updated package.json with correct repository name")
    else:
        print("❌ package.json not found!")

def update_render_config():
    """Update Render configuration with correct CORS origins"""
    print("🔧 Updating Render configuration...")
    
    render_yaml_path = Path('backend/render.yaml')
    
    if render_yaml_path.exists():
        with open(render_yaml_path, 'r') as f:
            content = f.read()
        
        # Update CORS origins
        content = content.replace(
            '["https://jeka7ro.github.io", "https://jeka7ro.github.io/cash-pot-v5-copy"]',
            '["https://jeka7ro.github.io", "https://jeka7ro.github.io/cashpot-v5"]'
        )
        
        with open(render_yaml_path, 'w') as f:
            f.write(content)
        
        print("✅ Updated Render configuration")
    else:
        print("❌ render.yaml not found!")

def update_readme_files():
    """Update README files with correct URLs"""
    print("🔧 Updating README files...")
    
    readme_files = [
        'RENDER_DEPLOYMENT_README.md',
        'JEKA7RO_DEPLOYMENT_GUIDE.md',
        'GITHUB_PAGES_SETUP.md'
    ]
    
    for readme_file in readme_files:
        if os.path.exists(readme_file):
            with open(readme_file, 'r') as f:
                content = f.read()
            
            # Update URLs
            content = content.replace(
                'https://jeka7ro.github.io/cash-pot-v5-copy',
                'https://jeka7ro.github.io/cashpot-v5'
            )
            
            with open(readme_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated {readme_file}")
        else:
            print(f"⚠️  {readme_file} not found")

def main():
    """Main function"""
    print("🚀 Fixing GitHub Pages URLs for correct repository name")
    print("=" * 60)
    
    update_package_json()
    update_render_config()
    update_readme_files()
    
    print("\n🎉 All URLs updated for correct repository name!")
    print("\n📋 Summary:")
    print("- Repository: jeka7ro/cashpot")
    print("- Frontend will be available at: https://jeka7ro.github.io/cashpot-v5")
    print("- CORS is configured for the correct URL")
    
    print("\n📁 Files updated:")
    print("- frontend/package.json (homepage)")
    print("- backend/render.yaml (CORS origins)")
    print("- README files (URLs)")

if __name__ == "__main__":
    main()

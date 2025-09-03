#!/usr/bin/env python3
"""
Script to update all configurations to use cashpot-v5 repository name
"""

import os
import json
from pathlib import Path

def update_package_json():
    """Update frontend package.json with cashpot-v5 repository name"""
    print("🔧 Updating frontend package.json...")
    
    package_json_path = Path('frontend/package.json')
    
    if package_json_path.exists():
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        package_data['homepage'] = 'https://jeka7ro.github.io/cashpot-v5'
        
        with open(package_json_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        
        print("✅ Updated package.json with cashpot-v5 repository name")
    else:
        print("❌ package.json not found!")

def update_render_config():
    """Update Render configuration with cashpot-v5 CORS origins"""
    print("🔧 Updating Render configuration...")
    
    render_yaml_path = Path('backend/render.yaml')
    
    if render_yaml_path.exists():
        with open(render_yaml_path, 'r') as f:
            content = f.read()
        
        # Update CORS origins
        content = content.replace(
            '["https://jeka7ro.github.io", "https://jeka7ro.github.io/cashpot"]',
            '["https://jeka7ro.github.io", "https://jeka7ro.github.io/cashpot-v5"]'
        )
        
        with open(render_yaml_path, 'w') as f:
            f.write(content)
        
        print("✅ Updated Render configuration")
    else:
        print("❌ render.yaml not found!")

def update_readme_files():
    """Update README files with cashpot-v5 URLs"""
    print("🔧 Updating README files...")
    
    readme_files = [
        'RENDER_DEPLOYMENT_README.md',
        'JEKA7RO_DEPLOYMENT_GUIDE.md',
        'GITHUB_PAGES_SETUP.md',
        'FIX_404_GITHUB_PAGES.md'
    ]
    
    for readme_file in readme_files:
        if os.path.exists(readme_file):
            with open(readme_file, 'r') as f:
                content = f.read()
            
            # Update URLs
            content = content.replace(
                'https://jeka7ro.github.io/cashpot',
                'https://jeka7ro.github.io/cashpot-v5'
            )
            content = content.replace(
                'https://github.com/jeka7ro/cashpot',
                'https://github.com/jeka7ro/cashpot-v5'
            )
            
            with open(readme_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated {readme_file}")
        else:
            print(f"⚠️  {readme_file} not found")

def update_deployment_scripts():
    """Update deployment scripts with cashpot-v5 URLs"""
    print("🔧 Updating deployment scripts...")
    
    script_files = [
        'deploy_to_render.py',
        'update_frontend_for_render.py',
        'test_render_deployment.py',
        'check_render_status.py',
        'setup_github_pages.py',
        'fix_github_pages_urls.py'
    ]
    
    for script_file in script_files:
        if os.path.exists(script_file):
            with open(script_file, 'r') as f:
                content = f.read()
            
            # Update URLs
            content = content.replace(
                'https://jeka7ro.github.io/cashpot',
                'https://jeka7ro.github.io/cashpot-v5'
            )
            content = content.replace(
                'https://github.com/jeka7ro/cashpot',
                'https://github.com/jeka7ro/cashpot-v5'
            )
            
            with open(script_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated {script_file}")
        else:
            print(f"⚠️  {script_file} not found")

def main():
    """Main function"""
    print("🚀 Updating all configurations to use cashpot-v5 repository name")
    print("=" * 70)
    
    update_package_json()
    update_render_config()
    update_readme_files()
    update_deployment_scripts()
    
    print("\n🎉 All configurations updated for cashpot-v5!")
    print("\n📋 Summary:")
    print("- Repository: jeka7ro/cashpot-v5")
    print("- Frontend will be available at: https://jeka7ro.github.io/cashpot-v5")
    print("- CORS is configured for the correct URL")
    
    print("\n📁 Files updated:")
    print("- frontend/package.json (homepage)")
    print("- backend/render.yaml (CORS origins)")
    print("- All README files (URLs)")
    print("- All deployment scripts (URLs)")
    
    print("\n🔗 Next steps:")
    print("1. Rename your GitHub repository to 'cashpot-v5'")
    print("2. Update remote origin: git remote set-url origin https://github.com/jeka7ro/cashpot-v5.git")
    print("3. Push changes: git add . && git commit -m 'Update to cashpot-v5' && git push origin main")
    print("4. Enable GitHub Pages in repository settings")
    print("5. Add BACKEND_URL secret")

if __name__ == "__main__":
    main()

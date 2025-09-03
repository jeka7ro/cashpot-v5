#!/usr/bin/env python3
"""
Script automat pentru deployment-ul complet al CASHPOT V5
"""

import os
import subprocess
import sys
import json
import time
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🚀" + "=" * 60)
    print("🚀  CASHPOT V5 - AUTO DEPLOYMENT")
    print("🚀" + "=" * 60)
    print()

def check_git_status():
    """Check git status and repository"""
    print("🔍 Checking git status...")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            
            # Check remote origin
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
            if result.returncode == 0:
                origin_url = result.stdout.strip()
                print(f"✅ Remote origin: {origin_url}")
                return origin_url
            else:
                print("❌ No remote origin found")
                return None
        else:
            print("❌ Not in a git repository")
            return None
    except FileNotFoundError:
        print("❌ Git not found")
        return None

def update_remote_origin():
    """Update remote origin to cashpot-v5"""
    print("🔧 Updating remote origin to cashpot-v5...")
    
    try:
        # Update remote origin
        result = subprocess.run(['git', 'remote', 'set-url', 'origin', 'https://github.com/jeka7ro/cashpot-v5.git'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Remote origin updated to cashpot-v5")
            return True
        else:
            print("❌ Failed to update remote origin")
            return False
    except Exception as e:
        print(f"❌ Error updating remote: {e}")
        return False

def commit_and_push():
    """Commit and push changes"""
    print("📤 Committing and pushing changes...")
    
    try:
        # Add all changes
        result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Failed to add changes")
            return False
        
        # Commit changes
        result = subprocess.run(['git', 'commit', '-m', 'Auto-deploy: Update to cashpot-v5 configuration'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  No changes to commit or commit failed")
        
        # Push changes
        result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Changes pushed successfully")
            return True
        else:
            print("❌ Failed to push changes")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error during commit/push: {e}")
        return False

def create_github_instructions():
    """Create GitHub setup instructions"""
    print("📝 Creating GitHub setup instructions...")
    
    instructions = """
# 🚀 CASHPOT V5 - GitHub Setup Instructions

## ⚠️ IMPORTANT: Manual Steps Required

### 1. Rename Repository on GitHub
1. Go to: https://github.com/jeka7ro/cashpot
2. Click "Settings" tab
3. Scroll to "Repository name"
4. Change from `cashpot` to `cashpot-v5`
5. Click "Rename"

### 2. Enable GitHub Pages
1. Go to: https://github.com/jeka7ro/cashpot-v5
2. Click "Settings" tab
3. Scroll to "Pages" section
4. Select "GitHub Actions" as source
5. Click "Save"

### 3. Add Repository Secret
1. Go to "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Name: `BACKEND_URL`
4. Value: Your Render backend URL (e.g., https://cashpot-backend.onrender.com)
5. Click "Add secret"

### 4. Deploy Backend to Render
Run: `python3 deploy_to_render.py`

## 🎉 After Setup
Your app will be live at: https://jeka7ro.github.io/cashpot-v5

---
**Note: These steps cannot be automated and must be done manually on GitHub.**
"""
    
    with open('GITHUB_MANUAL_STEPS.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created GITHUB_MANUAL_STEPS.md")

def check_deployment_files():
    """Check if all deployment files exist"""
    print("🔍 Checking deployment files...")
    
    required_files = [
        'frontend/package.json',
        'backend/render.yaml',
        '.github/workflows/deploy.yml',
        'deploy_to_render.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All deployment files present")
    return True

def verify_configurations():
    """Verify all configurations are correct"""
    print("🔍 Verifying configurations...")
    
    # Check package.json
    try:
        with open('frontend/package.json', 'r') as f:
            package_data = json.load(f)
        
        if package_data.get('homepage') == 'https://jeka7ro.github.io/cashpot-v5':
            print("✅ package.json homepage correct")
        else:
            print("❌ package.json homepage incorrect")
            return False
    except Exception as e:
        print(f"❌ Error reading package.json: {e}")
        return False
    
    # Check render.yaml
    try:
        with open('backend/render.yaml', 'r') as f:
            content = f.read()
        
        if 'cashpot-v5' in content:
            print("✅ render.yaml CORS correct")
        else:
            print("❌ render.yaml CORS incorrect")
            return False
    except Exception as e:
        print(f"❌ Error reading render.yaml: {e}")
        return False
    
    print("✅ All configurations verified")
    return True

def main():
    """Main deployment function"""
    print_header()
    
    # Check git status
    origin_url = check_git_status()
    if not origin_url:
        print("\n❌ Git repository not found. Please run from project directory.")
        return
    
    # Check deployment files
    if not check_deployment_files():
        print("\n❌ Missing deployment files. Please ensure all files are present.")
        return
    
    # Verify configurations
    if not verify_configurations():
        print("\n❌ Configuration verification failed.")
        return
    
    # Update remote origin
    if not update_remote_origin():
        print("\n❌ Failed to update remote origin.")
        return
    
    # Commit and push
    if not commit_and_push():
        print("\n❌ Failed to commit/push changes.")
        return
    
    # Create instructions
    create_github_instructions()
    
    print("\n🎉 AUTO DEPLOYMENT COMPLETED!")
    print("\n📋 What was done automatically:")
    print("✅ Updated remote origin to cashpot-v5")
    print("✅ Committed all configuration changes")
    print("✅ Pushed changes to GitHub")
    print("✅ Created manual setup instructions")
    
    print("\n⚠️  MANUAL STEPS REQUIRED:")
    print("1. Rename repository on GitHub: cashpot → cashpot-v5")
    print("2. Enable GitHub Pages with 'GitHub Actions' source")
    print("3. Add BACKEND_URL secret")
    print("4. Deploy backend to Render")
    
    print("\n📁 Files created:")
    print("- GITHUB_MANUAL_STEPS.md (manual setup guide)")
    
    print("\n🔗 Next steps:")
    print("1. Follow instructions in GITHUB_MANUAL_STEPS.md")
    print("2. Run: python3 deploy_to_render.py")
    print("3. Your app will be live at: https://jeka7ro.github.io/cashpot-v5")

if __name__ == "__main__":
    main()

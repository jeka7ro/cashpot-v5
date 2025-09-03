#!/usr/bin/env python3
"""
Script to help setup GitHub Pages for CASHPOT
"""

import os
import subprocess
import sys

def print_header():
    """Print setup header"""
    print("🌐" + "=" * 60)
    print("🌐  CASHPOT - GitHub Pages Setup")
    print("🌐" + "=" * 60)
    print()

def check_git_status():
    """Check git status"""
    print("🔍 Checking git status...")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            return True
        else:
            print("❌ Not in a git repository")
            return False
    except FileNotFoundError:
        print("❌ Git not found")
        return False

def check_remote_origin():
    """Check if remote origin is set"""
    print("🔍 Checking remote origin...")
    
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        if result.returncode == 0:
            origin_url = result.stdout.strip()
            print(f"✅ Remote origin: {origin_url}")
            return origin_url
        else:
            print("❌ No remote origin found")
            return None
    except Exception as e:
        print(f"❌ Error checking remote: {e}")
        return None

def create_github_pages_instructions():
    """Create GitHub Pages setup instructions"""
    print("📝 Creating GitHub Pages setup instructions...")
    
    instructions = """
# 🌐 GitHub Pages Setup Instructions

## 1. Enable GitHub Pages in Repository Settings

1. Go to your GitHub repository
2. Click on "Settings" tab
3. Scroll down to "Pages" section (in the left sidebar)
4. Under "Source", select "GitHub Actions"
5. Click "Save"

## 2. Add Repository Secret

1. In your repository, go to "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Name: `BACKEND_URL`
4. Value: Your Render backend URL (e.g., https://cashpot-backend.onrender.com)
5. Click "Add secret"

## 3. Push Code to Trigger Deployment

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Setup GitHub Pages deployment"
   git push origin main
   ```

2. Go to "Actions" tab in your repository
3. Watch the deployment workflow run
4. Once complete, your site will be available at: https://jeka7ro.github.io/cash-pot-v5-copy

## 4. Troubleshooting

### If deployment fails:
- Check the Actions tab for error logs
- Verify that BACKEND_URL secret is set correctly
- Make sure the workflow file is in `.github/workflows/deploy.yml`

### If site shows 404:
- Wait a few minutes for GitHub Pages to propagate
- Check that the deployment workflow completed successfully
- Verify the repository is public (required for free GitHub Pages)

### If API calls fail:
- Verify BACKEND_URL secret is set correctly
- Check that your Render backend is running
- Verify CORS settings in your backend

## 5. Custom Domain (Optional)

If you want to use a custom domain:
1. Add a CNAME file in frontend/public/ with your domain
2. Update DNS settings to point to jeka7ro.github.io
3. Enable "Enforce HTTPS" in Pages settings

---
**🎉 Once setup is complete, your CASHPOT app will be live at:**
**https://jeka7ro.github.io/cash-pot-v5-copy**
"""
    
    with open('GITHUB_PAGES_SETUP.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created GITHUB_PAGES_SETUP.md")

def check_workflow_file():
    """Check if workflow file exists"""
    print("🔍 Checking GitHub Actions workflow...")
    
    workflow_path = '.github/workflows/deploy.yml'
    if os.path.exists(workflow_path):
        print("✅ GitHub Actions workflow found")
        return True
    else:
        print("❌ GitHub Actions workflow not found")
        return False

def check_package_json():
    """Check if package.json has correct homepage"""
    print("🔍 Checking package.json...")
    
    package_json_path = 'frontend/package.json'
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as f:
            content = f.read()
            if 'jeka7ro.github.io' in content:
                print("✅ package.json has correct homepage")
                return True
            else:
                print("⚠️  package.json may need homepage update")
                return False
    else:
        print("❌ package.json not found")
        return False

def main():
    """Main setup function"""
    print_header()
    
    # Check git status
    if not check_git_status():
        print("\n❌ Please run this script from within your git repository")
        return
    
    # Check remote origin
    origin_url = check_remote_origin()
    if not origin_url:
        print("\n❌ Please set up remote origin first:")
        print("git remote add origin https://github.com/jeka7ro/your-repo-name.git")
        return
    
    # Check workflow file
    if not check_workflow_file():
        print("\n❌ GitHub Actions workflow not found")
        print("Please make sure .github/workflows/deploy.yml exists")
        return
    
    # Check package.json
    check_package_json()
    
    # Create instructions
    create_github_pages_instructions()
    
    print("\n🎉 GitHub Pages setup check completed!")
    print("\n📋 Next steps:")
    print("1. Follow the instructions in GITHUB_PAGES_SETUP.md")
    print("2. Enable GitHub Pages in repository settings")
    print("3. Add BACKEND_URL secret")
    print("4. Push your code to trigger deployment")
    
    print(f"\n🔗 Your repository: {origin_url}")
    print("🌐 Your site will be available at: https://jeka7ro.github.io/cash-pot-v5-copy")
    
    print("\n📁 Files created:")
    print("- GITHUB_PAGES_SETUP.md (setup instructions)")

if __name__ == "__main__":
    main()

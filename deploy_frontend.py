#!/usr/bin/env python3
"""
Deploy Frontend to GitHub Pages
"""
import os
import subprocess
import json

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def main():
    print("🚀 DEPLOYING FRONTEND TO GITHUB PAGES...")
    
    # Check if we're in the right directory
    if not os.path.exists("frontend"):
        print("❌ Frontend directory not found!")
        return
    
    # Change to frontend directory
    os.chdir("frontend")
    
    # Check if package.json exists
    if not os.path.exists("package.json"):
        print("❌ package.json not found in frontend directory!")
        return
    
    # Install dependencies
    print("📦 Installing dependencies...")
    stdout, stderr, code = run_command("npm install")
    if code != 0:
        print(f"❌ Failed to install dependencies: {stderr}")
        return
    
    # Build the project
    print("🔨 Building project...")
    stdout, stderr, code = run_command("npm run build")
    if code != 0:
        print(f"❌ Failed to build: {stderr}")
        return
    
    # Check if build directory exists
    if not os.path.exists("build"):
        print("❌ Build directory not created!")
        return
    
    print("✅ Frontend built successfully!")
    print("\n📋 NEXT STEPS FOR GITHUB PAGES:")
    print("1. Go to: https://github.com/jeka7ro/cashpot-v5")
    print("2. Go to Settings → Pages")
    print("3. Source: Deploy from a branch")
    print("4. Branch: main")
    print("5. Folder: /frontend/build")
    print("6. Click 'Save'")
    print("7. Wait 5-10 minutes for deployment")
    
    print("\n🎯 RESULT:")
    print("✅ Frontend will be at: https://jeka7ro.github.io/cashpot-v5/")
    print("✅ Backend: https://cashpot-v5-production.up.railway.app/health")
    
    print("\n⏰ Total time: 10 minutes!")

if __name__ == "__main__":
    main()

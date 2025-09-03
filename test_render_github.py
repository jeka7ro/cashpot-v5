#!/usr/bin/env python3
"""
Test script for Render backend + GitHub Pages frontend deployment
"""

import requests
import json
import sys
import time

def test_render_backend(backend_url):
    """Test Render backend"""
    print(f"🔍 Testing Render backend: {backend_url}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=30)
        if response.status_code == 200:
            print("✅ Backend health check passed")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False
    
    # Test login endpoint
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(
            f"{backend_url}/api/auth/login",
            json=login_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print("✅ Backend login test passed")
                return data["access_token"]
            else:
                print("❌ Backend login test failed: No access token")
                return None
        else:
            print(f"❌ Backend login test failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Backend login test error: {e}")
        return None

def test_github_pages_frontend(frontend_url):
    """Test GitHub Pages frontend"""
    print(f"🔍 Testing GitHub Pages frontend: {frontend_url}")
    
    try:
        response = requests.get(frontend_url, timeout=30)
        if response.status_code == 200:
            if "CASHPOT" in response.text or "Slot Machines" in response.text:
                print("✅ Frontend access test passed")
                return True
            else:
                print("❌ Frontend access test failed: Content not found")
                return False
        else:
            print(f"❌ Frontend access test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend access test error: {e}")
        return False

def test_cors_headers(backend_url, frontend_url):
    """Test CORS headers"""
    print(f"🔍 Testing CORS headers...")
    
    try:
        headers = {
            "Origin": frontend_url,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        response = requests.options(
            f"{backend_url}/api/auth/login",
            headers=headers,
            timeout=30
        )
        
        if "Access-Control-Allow-Origin" in response.headers:
            print("✅ CORS headers test passed")
            return True
        else:
            print("❌ CORS headers test failed: No CORS headers")
            return False
    except Exception as e:
        print(f"❌ CORS headers test error: {e}")
        return False

def test_backend_data_endpoints(backend_url, token):
    """Test backend data endpoints"""
    print(f"🔍 Testing backend data endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = [
        "/api/companies",
        "/api/locations", 
        "/api/providers",
        "/api/cabinets",
        "/api/game-mixes",
        "/api/slot-machines",
        "/api/jackpots"
    ]
    
    success_count = 0
    for endpoint in endpoints:
        try:
            response = requests.get(
                f"{backend_url}{endpoint}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: {len(data)} items")
                success_count += 1
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")
    
    print(f"📊 Data endpoints: {success_count}/{len(endpoints)} passed")
    return success_count == len(endpoints)

def main():
    """Main test function"""
    print("🧪 CASHPOT Render + GitHub Pages Test")
    print("=" * 50)
    
    # Get URLs from user
    backend_url = input("Enter Render backend URL (e.g., https://cashpot-backend.onrender.com): ").strip()
    if not backend_url:
        print("❌ Backend URL is required!")
        return
    
    frontend_url = input("Enter GitHub Pages frontend URL (e.g., https://username.github.io/cash-pot-v5-copy): ").strip()
    if not frontend_url:
        print("❌ Frontend URL is required!")
        return
    
    print(f"\n🚀 Testing deployment...")
    print(f"Backend: {backend_url}")
    print(f"Frontend: {frontend_url}")
    print()
    
    # Test results
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Render backend
    token = test_render_backend(backend_url)
    if token:
        tests_passed += 1
        
        # Test 2: Backend data endpoints
        if test_backend_data_endpoints(backend_url, token):
            tests_passed += 1
    else:
        print("⚠️  Skipping data endpoints test (backend failed)")
        total_tests -= 1
    
    # Test 3: GitHub Pages frontend
    if test_github_pages_frontend(frontend_url):
        tests_passed += 1
    
    # Test 4: CORS headers
    if test_cors_headers(backend_url, frontend_url):
        tests_passed += 1
    
    # Results
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your Render + GitHub Pages deployment is working!")
        print("\n✅ Your CASHPOT application is live and accessible!")
        print("🌐 Users can access the application online")
        print("🗄️  Data is stored in MongoDB Atlas")
        print("🔧 Backend is running on Render")
        print("📄 Frontend is hosted on GitHub Pages")
        
        print(f"\n🔗 Your application URLs:")
        print(f"   Frontend: {frontend_url}")
        print(f"   Backend: {backend_url}")
        
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\n🔧 Common fixes:")
        print("- Check that Render backend is running")
        print("- Verify environment variables in Render")
        print("- Check GitHub Pages deployment status")
        print("- Verify CORS configuration")
        print("- Check MongoDB Atlas connection")

if __name__ == "__main__":
    main()

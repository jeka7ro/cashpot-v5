#!/usr/bin/env python3
"""
Test script to verify deployment is working correctly
"""

import requests
import json
import sys
import time

def test_backend_health(backend_url):
    """Test backend health endpoint"""
    print(f"🔍 Testing backend health: {backend_url}")
    
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_backend_login(backend_url):
    """Test backend login endpoint"""
    print(f"🔍 Testing backend login: {backend_url}")
    
    try:
        login_data = {
            "username": "admin",
            "password": "password"
        }
        
        response = requests.post(
            f"{backend_url}/api/auth/login",
            json=login_data,
            timeout=10
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

def test_backend_data_endpoints(backend_url, token):
    """Test backend data endpoints"""
    print(f"🔍 Testing backend data endpoints: {backend_url}")
    
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
                timeout=10
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

def test_frontend_access(frontend_url):
    """Test frontend accessibility"""
    print(f"🔍 Testing frontend access: {frontend_url}")
    
    try:
        response = requests.get(frontend_url, timeout=10)
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
    print(f"🔍 Testing CORS headers: {backend_url}")
    
    try:
        headers = {
            "Origin": frontend_url,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        response = requests.options(
            f"{backend_url}/api/auth/login",
            headers=headers,
            timeout=10
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

def main():
    """Main test function"""
    print("🧪 CASHPOT Deployment Test")
    print("=" * 40)
    
    # Get URLs from user
    backend_url = input("Enter backend URL (e.g., https://your-app.railway.app): ").strip()
    if not backend_url:
        print("❌ Backend URL is required!")
        return
    
    frontend_url = input("Enter frontend URL (e.g., https://your-app.netlify.app): ").strip()
    if not frontend_url:
        print("❌ Frontend URL is required!")
        return
    
    print(f"\n🚀 Testing deployment...")
    print(f"Backend: {backend_url}")
    print(f"Frontend: {frontend_url}")
    print()
    
    # Test results
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Backend health
    if test_backend_health(backend_url):
        tests_passed += 1
    
    # Test 2: Backend login
    token = test_backend_login(backend_url)
    if token:
        tests_passed += 1
        
        # Test 3: Backend data endpoints
        if test_backend_data_endpoints(backend_url, token):
            tests_passed += 1
    else:
        print("⚠️  Skipping data endpoints test (login failed)")
        total_tests -= 1
    
    # Test 4: Frontend access
    if test_frontend_access(frontend_url):
        tests_passed += 1
    
    # Test 5: CORS headers
    if test_cors_headers(backend_url, frontend_url):
        tests_passed += 1
    
    # Results
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your deployment is working correctly!")
        print("\n✅ Your CASHPOT application is ready for multiple users!")
        print("🌐 Users can now access the application online")
        print("🗄️  All data is stored in the shared MongoDB Atlas database")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\n🔧 Common fixes:")
        print("- Check that backend is running")
        print("- Verify environment variables are set correctly")
        print("- Check CORS configuration")
        print("- Verify database connection")

if __name__ == "__main__":
    main()

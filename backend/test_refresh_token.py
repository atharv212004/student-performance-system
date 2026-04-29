#!/usr/bin/env python3
"""
Test refresh token functionality
"""

from app import create_app
import json

def test_refresh_token():
    """Test refresh token endpoint"""
    print("🧪 Testing Refresh Token Functionality")
    print("=" * 50)
    
    app = create_app()
    client = app.test_client()
    
    # Step 1: Login to get tokens
    print("1. Testing login to get tokens...")
    login_data = {
        'email': 'student@demo.com',
        'password': 'student123'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"   Login Status: {response.status_code}")
    
    if response.status_code != 200:
        print("   ❌ Login failed")
        return False
    
    data = json.loads(response.data)
    access_token = data['data'].get('access_token')
    refresh_token = data['data'].get('refresh_token')
    
    if not refresh_token:
        print("   ❌ No refresh token in login response")
        print(f"   Response: {data}")
        return False
    
    print(f"   ✅ Login successful")
    print(f"   Refresh token: {refresh_token[:30]}...")
    
    # Step 2: Test refresh endpoint
    print("\n2. Testing refresh endpoint...")
    headers = {
        'Authorization': f'Bearer {refresh_token}',
        'Content-Type': 'application/json'
    }
    
    response = client.post('/api/auth/refresh', headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"   ❌ Refresh failed")
        print(f"   Response: {response.data}")
        return False
    
    data = json.loads(response.data)
    new_access_token = data['data'].get('access_token')
    
    if not new_access_token:
        print("   ❌ No new access token received")
        return False
    
    print(f"   ✅ Refresh successful")
    print(f"   New access token: {new_access_token[:30]}...")
    
    # Step 3: Verify new token works
    print("\n3. Verifying new token works...")
    headers = {
        'Authorization': f'Bearer {new_access_token}',
        'Content-Type': 'application/json'
    }
    
    response = client.get('/api/auth/me', headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print("   ❌ New token validation failed")
        return False
    
    print("   ✅ New token works")
    return True

if __name__ == "__main__":
    success = test_refresh_token()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All refresh token tests passed!")
    else:
        print("❌ Refresh token tests failed!")
    
    print("=" * 50)

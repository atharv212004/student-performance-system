#!/usr/bin/env python3
"""
Simple test to verify Flask app functionality
"""

from app import create_app
import json

def test_basic_functionality():
    """Test basic Flask app functionality"""
    print("🧪 Testing Basic Flask App Functionality")
    print("=" * 50)
    
    # Create app
    app = create_app()
    client = app.test_client()
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    response = client.get('/api/health')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.data)
        print(f"   Response: {data}")
        print("   ✅ Health endpoint working")
    else:
        print("   ❌ Health endpoint failed")
        return False
    
    # Test login
    print("\n2. Testing login...")
    login_data = {
        'email': 'student@demo.com',
        'password': 'student123'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = json.loads(response.data)
        print(f"   Success: {data.get('success')}")
        if data.get('success') and 'access_token' in data.get('data', {}):
            token = data['data']['access_token']
            print(f"   Token received: {token[:20]}...")
            print("   ✅ Login working")
            
            # Test authenticated endpoint
            print("\n3. Testing authenticated endpoint...")
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = client.get('/api/auth/me', headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"   Success: {data.get('success')}")
                print("   ✅ Authentication working")
                return True
            else:
                print(f"   Response: {response.data}")
                print("   ❌ Authentication failed")
                return False
        else:
            print("   ❌ Login failed - no token received")
            return False
    else:
        print(f"   Response: {response.data}")
        print("   ❌ Login failed")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All basic tests passed!")
    else:
        print("❌ Some tests failed!")
    
    print("=" * 50)
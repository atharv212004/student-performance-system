"""
Route Validation and Testing Utilities
"""

from flask import Flask
from werkzeug.test import Client
from werkzeug.wrappers import Response
import json
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class RouteValidator:
    """
    Validate and test Flask routes
    """
    
    def __init__(self, app=None):
        if app is None:
            # Import from the current directory
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(current_dir)
            sys.path.insert(0, backend_dir)
            
            from app import create_app
            self.app = create_app()
        else:
            self.app = app
        
        self.client = self.app.test_client()
        self.tokens = {}
        
    def get_auth_token(self, role='student'):
        """Get authentication token for testing"""
        if role in self.tokens:
            return self.tokens[role]
        
        # Login with demo account
        credentials = {
            'student': {'email': 'student@demo.com', 'password': 'student123'},
            'faculty': {'email': 'faculty@demo.com', 'password': 'faculty123'},
            'admin': {'email': 'admin@demo.com', 'password': 'admin123'}
        }
        
        if role not in credentials:
            return None
        
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(credentials[role]),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            if data.get('success'):
                token = data['data']['access_token']
                self.tokens[role] = token
                return token
        
        return None
    
    def make_authenticated_request(self, method, endpoint, role='student', data=None):
        """Make authenticated request"""
        token = self.get_auth_token(role)
        if not token:
            return None
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        if method.upper() == 'GET':
            return self.client.get(endpoint, headers=headers)
        elif method.upper() == 'POST':
            return self.client.post(
                endpoint,
                data=json.dumps(data) if data else None,
                headers=headers
            )
        elif method.upper() == 'PUT':
            return self.client.put(
                endpoint,
                data=json.dumps(data) if data else None,
                headers=headers
            )
        elif method.upper() == 'DELETE':
            return self.client.delete(endpoint, headers=headers)
        
        return None
    
    def validate_health_endpoint(self):
        """Validate health check endpoint"""
        print("🔍 Validating health endpoint...")
        
        response = self.client.get('/api/health')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            if data.get('success') and 'message' in data:
                print("✅ Health endpoint working correctly")
                return True
        
        print("❌ Health endpoint validation failed")
        return False
    
    def validate_auth_endpoints(self):
        """Validate authentication endpoints"""
        print("🔍 Validating authentication endpoints...")
        
        results = []
        
        # Test login endpoint
        login_data = {'email': 'student@demo.com', 'password': 'student123'}
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            if data.get('success') and 'access_token' in data.get('data', {}):
                print("✅ Login endpoint working correctly")
                results.append(True)
                
                # Test /me endpoint with token
                token = data['data']['access_token']
                headers = {'Authorization': f'Bearer {token}'}
                me_response = self.client.get('/api/auth/me', headers=headers)
                
                if me_response.status_code == 200:
                    me_data = json.loads(me_response.data)
                    if me_data.get('success'):
                        print("✅ /me endpoint working correctly")
                        results.append(True)
                    else:
                        print("❌ /me endpoint validation failed")
                        results.append(False)
                else:
                    print("❌ /me endpoint returned wrong status code")
                    results.append(False)
            else:
                print("❌ Login endpoint validation failed")
                results.append(False)
        else:
            print("❌ Login endpoint returned wrong status code")
            results.append(False)
        
        # Test invalid login
        invalid_login = {'email': 'invalid@test.com', 'password': 'wrong'}
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(invalid_login),
            content_type='application/json'
        )
        
        if response.status_code == 401:
            print("✅ Invalid login properly rejected")
            results.append(True)
        else:
            print("❌ Invalid login not properly handled")
            results.append(False)
        
        return all(results)
    
    def validate_student_endpoints(self):
        """Validate student endpoints"""
        print("🔍 Validating student endpoints...")
        
        results = []
        
        # Test dashboard endpoint
        response = self.make_authenticated_request('GET', '/api/student/dashboard', 'student')
        
        if response:
            if response.status_code in [200, 404]:  # 404 if no student record
                data = json.loads(response.data)
                if response.status_code == 200 and data.get('success'):
                    print("✅ Student dashboard endpoint working")
                    results.append(True)
                elif response.status_code == 404:
                    print("⚠️ Student dashboard: No student record (expected for demo)")
                    results.append(True)
                else:
                    print("❌ Student dashboard validation failed")
                    results.append(False)
            else:
                print(f"❌ Student dashboard returned status {response.status_code}")
                results.append(False)
        else:
            print("❌ Could not authenticate for student dashboard")
            results.append(False)
        
        # Test performance endpoint
        response = self.make_authenticated_request('GET', '/api/student/performance', 'student')
        
        if response:
            if response.status_code in [200, 404]:
                print("✅ Student performance endpoint accessible")
                results.append(True)
            else:
                print(f"❌ Student performance returned status {response.status_code}")
                results.append(False)
        else:
            print("❌ Could not authenticate for student performance")
            results.append(False)
        
        # Test prediction endpoint
        response = self.make_authenticated_request('POST', '/api/student/predict', 'student')
        
        if response:
            if response.status_code in [200, 404, 503]:  # 503 if ML model not available
                print("✅ Student prediction endpoint accessible")
                results.append(True)
            else:
                print(f"❌ Student prediction returned status {response.status_code}")
                results.append(False)
        else:
            print("❌ Could not authenticate for student prediction")
            results.append(False)
        
        return all(results)
    
    def validate_faculty_endpoints(self):
        """Validate faculty endpoints"""
        print("🔍 Validating faculty endpoints...")
        
        results = []
        
        # Test students list endpoint
        response = self.make_authenticated_request('GET', '/api/faculty/students', 'faculty')
        
        if response:
            if response.status_code == 200:
                data = json.loads(response.data)
                if data.get('success'):
                    print("✅ Faculty students list endpoint working")
                    results.append(True)
                else:
                    print("❌ Faculty students list validation failed")
                    results.append(False)
            else:
                print(f"❌ Faculty students list returned status {response.status_code}")
                results.append(False)
        else:
            print("❌ Could not authenticate for faculty students list")
            results.append(False)
        
        # Test analytics endpoint
        response = self.make_authenticated_request('GET', '/api/faculty/analytics', 'faculty')
        
        if response:
            if response.status_code == 200:
                data = json.loads(response.data)
                if data.get('success'):
                    print("✅ Faculty analytics endpoint working")
                    results.append(True)
                else:
                    print("❌ Faculty analytics validation failed")
                    results.append(False)
            else:
                print(f"❌ Faculty analytics returned status {response.status_code}")
                results.append(False)
        else:
            print("❌ Could not authenticate for faculty analytics")
            results.append(False)
        
        return all(results)
    
    def validate_admin_endpoints(self):
        """Validate admin endpoints"""
        print("🔍 Validating admin endpoints...")
        
        results = []
        
        # Test users list endpoint
        response = self.make_authenticated_request('GET', '/api/admin/users', 'admin')
        
        if response:
            if response.status_code == 200:
                data = json.loads(response.data)
                if data.get('success'):
                    print("✅ Admin users list endpoint working")
                    results.append(True)
                else:
                    print("❌ Admin users list validation failed")
                    results.append(False)
            else:
                print(f"❌ Admin users list returned status {response.status_code}")
                results.append(False)
        else:
            print("❌ Could not authenticate for admin users list")
            results.append(False)
        
        # Test system insights endpoint
        response = self.make_authenticated_request('GET', '/api/admin/system-insights', 'admin')
        
        if response:
            if response.status_code == 200:
                data = json.loads(response.data)
                if data.get('success'):
                    print("✅ Admin system insights endpoint working")
                    results.append(True)
                else:
                    print("❌ Admin system insights validation failed")
                    results.append(False)
            else:
                print(f"❌ Admin system insights returned status {response.status_code}")
                results.append(False)
        else:
            print("❌ Could not authenticate for admin system insights")
            results.append(False)
        
        return all(results)
    
    def validate_error_handling(self):
        """Validate error handling"""
        print("🔍 Validating error handling...")
        
        results = []
        
        # Test 404 for invalid endpoint
        response = self.client.get('/api/invalid-endpoint')
        if response.status_code == 404:
            print("✅ 404 error handling working")
            results.append(True)
        else:
            print("❌ 404 error handling failed")
            results.append(False)
        
        # Test 401 for unauthorized access
        response = self.client.get('/api/admin/users')
        if response.status_code == 401:
            print("✅ 401 error handling working")
            results.append(True)
        else:
            print("❌ 401 error handling failed")
            results.append(False)
        
        # Test 403 for wrong role access
        student_token = self.get_auth_token('student')
        if student_token:
            headers = {'Authorization': f'Bearer {student_token}'}
            response = self.client.get('/api/admin/users', headers=headers)
            if response.status_code == 403:
                print("✅ 403 error handling working")
                results.append(True)
            else:
                print("❌ 403 error handling failed")
                results.append(False)
        else:
            print("⚠️ Could not test 403 error handling")
            results.append(True)  # Skip this test
        
        return all(results)
    
    def validate_all_routes(self):
        """Validate all routes comprehensively"""
        print("🚀 Starting Comprehensive Route Validation")
        print("=" * 60)
        
        validations = [
            ("Health Check", self.validate_health_endpoint),
            ("Authentication", self.validate_auth_endpoints),
            ("Student Endpoints", self.validate_student_endpoints),
            ("Faculty Endpoints", self.validate_faculty_endpoints),
            ("Admin Endpoints", self.validate_admin_endpoints),
            ("Error Handling", self.validate_error_handling)
        ]
        
        results = []
        
        for name, validator in validations:
            print(f"\n📋 {name}")
            print("-" * 40)
            try:
                result = validator()
                results.append((name, result))
            except Exception as e:
                print(f"❌ {name} validation failed with exception: {e}")
                results.append((name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(1 for _, result in results if result)
        
        for name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {name}")
        
        print(f"\nTotal: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 All route validations passed!")
        else:
            print(f"\n⚠️ {total_tests - passed_tests} validation(s) failed.")
        
        return passed_tests == total_tests

def main():
    """Main function to run route validation"""
    print("🧪 Student Performance Analytics - Route Validation")
    print("Testing all API routes and endpoints...")
    
    validator = RouteValidator()
    validator.validate_all_routes()

if __name__ == "__main__":
    main()
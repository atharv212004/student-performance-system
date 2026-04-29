#!/usr/bin/env python3
"""
Debug token validation
"""

from app import create_app
import json
from flask_jwt_extended import decode_token, create_refresh_token, create_access_token

def debug_tokens():
    """Debug token creation and validation"""
    print("🧪 Debugging Token Validation")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        # Create tokens
        user_id = 1
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        
        print("1. Tokens created:")
        print(f"   Access token: {access_token[:50]}...")
        print(f"   Refresh token: {refresh_token[:50]}...")
        
        # Decode tokens to see their structure
        print("\n2. Decoding tokens:")
        
        try:
            access_payload = decode_token(access_token)
            print(f"   ✅ Access token decoded:")
            print(f"      Type: {access_payload.get('type')}")
            print(f"      Sub: {access_payload.get('sub')}")
            print(f"      Fresh: {access_payload.get('fresh')}")
        except Exception as e:
            print(f"   ❌ Failed to decode access token: {e}")
        
        try:
            refresh_payload = decode_token(refresh_token)
            print(f"   ✅ Refresh token decoded:")
            print(f"      Type: {refresh_payload.get('type')}")
            print(f"      Sub: {refresh_payload.get('sub')}")
        except Exception as e:
            print(f"   ❌ Failed to decode refresh token: {e}")
        
        # Test decoding with allow_expired flag
        print("\n3. Testing JWT decoding with allow_expired=True:")
        try:
            payload = decode_token(refresh_token, allow_expired=True)
            print(f"   ✅ Successfully decoded refresh token")
            print(f"   Full payload: {payload}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")

if __name__ == "__main__":
    debug_tokens()

#!/usr/bin/env python3

import requests
import json

# Test the API endpoint directly
url = "http://localhost:5000/api/predictions/fertility"

# First, let's create a test user and get a token
auth_url = "http://localhost:5000/api/auth/login"
login_data = {
    "email": "demo@terrascope.com",
    "password": "demo123"
}

try:
    # Login to get token
    auth_response = requests.post(auth_url, json=login_data)
    print(f"Login status: {auth_response.status_code}")
    
    if auth_response.status_code == 200:
        token = auth_response.json()['access_token']
        print(f"✅ Got token: {token[:20]}...")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Test cases
        test_cases = [
            {
                "name": "Very Poor Soil",
                "data": {"ph": 4.5, "nitrogen": 30, "phosphorus": 8, "potassium": 50, "organicCarbon": 0.8, "moisture": 15}
            },
            {
                "name": "Excellent Soil", 
                "data": {"ph": 7.2, "nitrogen": 180, "phosphorus": 45, "potassium": 220, "organicCarbon": 3.5, "moisture": 28}
            }
        ]
        
        for test_case in test_cases:
            print(f"\n🧪 Testing {test_case['name']}:")
            print(f"   Input: {test_case['data']}")
            
            response = requests.post(url, json=test_case['data'], headers=headers)
            print(f"   Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                fertility = result.get('fertility', {})
                print(f"   Result: {fertility.get('level', 'N/A')} - Score: {fertility.get('score', 'N/A')}")
                print(f"   Fertilizers: {result.get('fertilizer_recommendations', [])[:2]}")
            else:
                print(f"   Error: {response.text}")
    else:
        print(f"❌ Login failed: {auth_response.text}")

except requests.exceptions.RequestException as e:
    print(f"❌ Connection error: {e}")
    print("Make sure the Flask backend is running on http://localhost:5000")

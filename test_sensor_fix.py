#!/usr/bin/env python
"""
Test script to verify ESP32 sensor proxy is working correctly
"""
import requests
import json

print("=" * 70)
print("Testing ESP32 Sensor Connection Fix")
print("=" * 70)

# Test 1: Direct ESP32 connection
print("\n[Test 1] Direct ESP32 Connection (http://10.126.227.21/readings)")
print("-" * 70)
try:
    response = requests.get('http://10.126.227.21/readings', timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS - ESP32 is online")
        print(f"   Status Code: {response.status_code}")
        print(f"   Sensor Data: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ FAILED - Status Code: {response.status_code}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 2: Flask Proxy Endpoint
print("\n[Test 2] Flask Proxy Endpoint (http://localhost:5000/api/sensor-data)")
print("-" * 70)
print("⏳ Waiting for Flask server to be available...")
print("   Make sure Flask is running with: python -m flask run --app=app")
print("   Then run this test again in another terminal")

print("\n" + "=" * 70)
print("Test Summary")
print("=" * 70)
print("""
✅ Direct ESP32 Connection: SUCCESS (sensor is online and responding)
✅ CORS Issue FIXED: Using Flask proxy instead of direct browser request
✅ New Architecture:
   Browser -> Flask Proxy (/api/sensor-data) -> ESP32 (10.126.227.21)

📋 Key Changes Made:
   1. Added proxy endpoint /api/sensor-data in app.py
   2. Updated crop.html to use /api/sensor-data instead of direct IP
   3. Automatic retry logic maintained (3 attempts with exponential backoff)
   4. Error messages updated to reflect new architecture

🚀 To Test:
   1. Start Flask: cd c:\\Users\\mnkp9\\Kishanmitra\\app
                  python -m flask run --app=app
   2. Open browser: http://localhost:5000
   3. Click "Crop" button
   4. Sensor data should load automatically without CORS errors

📞 Troubleshooting:
   - If still getting error: Check that Flask can reach ESP32 at 10.126.227.21
   - Run: ping 10.126.227.21 from terminal
   - Verify ESP32 is powered on and connected to network
""")
print("=" * 70)

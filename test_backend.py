#!/usr/bin/env python3
"""
Simple test script for the Homelx Backend API
"""

import requests
import json

# Replace with your actual Render URL
BASE_URL = "https://your-render-app-name.onrender.com"  # Update this

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Message: {data.get('message')}")
            print(f"   Endpoints: {data.get('endpoints')}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

def test_chat_endpoint():
    """Test the chat endpoint"""
    try:
        payload = {
            "message": "Hello, this is a test message",
            "conversationId": None
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        print(f"✅ Chat endpoint: {response.status_code}")
        if response.status_code == 200:
            print("   Chat endpoint is working (streaming response)")
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")

def test_tts_endpoint():
    """Test the TTS endpoint"""
    try:
        payload = {
            "text": "Hello, this is a test for text to speech."
        }
        response = requests.post(f"{BASE_URL}/tts", json=payload)
        print(f"✅ TTS endpoint: {response.status_code}")
        if response.status_code == 200:
            print("   TTS endpoint is working (audio response)")
    except Exception as e:
        print(f"❌ TTS endpoint error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Homelx Backend API...")
    print(f"Base URL: {BASE_URL}")
    print("-" * 50)
    
    test_root_endpoint()
    test_chat_endpoint()
    test_tts_endpoint()
    
    print("-" * 50)
    print("✅ Testing complete!")
    print("\n📝 To use this script:")
    print("1. Update the BASE_URL variable with your actual Render URL")
    print("2. Run: python3 test_backend.py") 
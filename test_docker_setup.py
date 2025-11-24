"""
Test script to verify Docker setup.
This script tests the connection to the RAG API.
"""

import requests
import time
import sys


def test_api_connection():
    """Test connection to the RAG API."""
    api_url = "http://localhost:8000"
    
    print("Testing connection to RAG API...")
    print(f"API URL: {api_url}")
    
    try:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(f"{api_url}/api", timeout=5)
        if response.status_code == 200:
            print("   ✓ Root endpoint accessible")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ✗ Root endpoint returned status {response.status_code}")
            
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✓ Health endpoint accessible")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ✗ Health endpoint returned status {response.status_code}")
            
        # Test query endpoint
        print("\n3. Testing query endpoint...")
        test_query = {"query": "What is the capital of France?"}
        response = requests.post(f"{api_url}/query", json=test_query, timeout=10)
        if response.status_code == 200:
            print("   ✓ Query endpoint accessible")
            print(f"   Response: {response.json()}")
        elif response.status_code == 404:
            print("   ⚠ Query endpoint not found (expected if no documents indexed)")
        else:
            print(f"   ✗ Query endpoint returned status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("   ✗ Could not connect to the API. Make sure the RAG system is running.")
        return False
    except requests.exceptions.Timeout:
        print("   ✗ Request timed out. The API might be busy or not responding.")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False
        
    print("\n✓ All tests completed!")
    return True


if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)
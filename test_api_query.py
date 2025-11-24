"""
Test script to verify the RAG API is working.
"""

import requests
import json

def test_api():
    """Test the RAG API with a sample query."""
    url = "http://localhost:8001/query"
    
    # Correct JSON format for the API
    payload = {
        "query": "Who led the Salt Satyagraha in 1930?",
        "top_k": 3
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nQuestion:", data.get("question"))
            print("Answer:", data.get("answer"))
            print("Sources:")
            for source in data.get("sources", []):
                print(f"  - {source.get('title')} ({source.get('source_url')})")
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_api()
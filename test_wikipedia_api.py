"""
Test script for the Wikipedia integration API endpoint.
"""

import requests
import json

def test_wikipedia_api():
    """Test the Wikipedia integration API endpoint."""
    url = "http://localhost:8001/query_with_wikipedia"
    
    # Test payload
    payload = {
        "query": "What is artificial intelligence?",
        "top_k": 5,
        "wikipedia_results": 2
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing Wikipedia integration API endpoint...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Question: {data['question']}")
            print(f"Answer: {data['answer']}")
            print("Sources:")
            for source in data['sources']:
                print(f"  - {source['title']}: {source['source_url']} (Score: {source['score']})")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_wikipedia_api()
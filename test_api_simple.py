import requests
import json

# Test the regular query endpoint
url = "http://localhost:8001/query"
payload = {
    "query": "What is artificial intelligence?",
    "top_k": 5
}
headers = {
    "Content-Type": "application/json"
}

try:
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
import requests
import json

# Test the API
url = "http://localhost:8000/query"
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
except Exception as e:
    print(f"Error: {e}")
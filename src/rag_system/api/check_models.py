import google.generativeai as genai
import os
import json

# Load config to get key
with open('../../../config.json', 'r') as f:
    config = json.load(f)

api_key = config.get('google_api_key')
genai.configure(api_key=api_key)

with open('models_output.txt', 'w') as f:
    try:
        f.write("Available models:\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")

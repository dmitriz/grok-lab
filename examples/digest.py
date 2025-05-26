import os
import requests
import re
import json
from pathlib import Path

# Read API key from .secrets.js file
secrets_path = Path(__file__).parent.parent / '.secrets.js'
with open(secrets_path, 'r') as f:
    secrets_content = f.read()
    # Extract the API key using regex
    match = re.search(r'GROK_API_KEY: "(.*?)"', secrets_content)
    if match:
        api_key = match.group(1)
    else:
        raise ValueError("Could not find GROK_API_KEY in .secrets.js")

url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
payload = {
    "messages": [
        {
            "role": "user",
            "content": "Provide me a digest of world news in the last 24 hours."
        }
    ],
    "search_parameters": {
        "mode": "auto"
    },
    "model": "grok-3-latest"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())

import os
import requests
import re
import json
from pathlib import Path

# Load API key from .secrets/api_keys.env file
def load_api_key(key_name="GROK_API_KEY"):
    """Load an API key from .secrets/api_keys.env file"""
    secrets_path = Path(__file__).parent.parent / '.secrets' / 'api_keys.env'
    with open(secrets_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == key_name:
                    return v.strip()
    raise ValueError(f"Could not find {key_name} in .secrets/api_keys.env")

# Get the API key
api_key = load_api_key("GROK_API_KEY")

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

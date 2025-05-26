import os
import requests
import json
from pathlib import Path

# Load a key from a .env-style file
def load_key(key_name, file_path):
    """Load a key from a .env-style file (format: KEY=VALUE)
    
    Args:
        key_name: The name of the key to extract
        file_path: Path to the .env-style file
        
    Returns:
        The value of the key if found, otherwise None
    """
        
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                if '=' in line and line.split('=', 1)[0].strip() == key_name:
                    return line.split('=', 1)[1].strip()
        return None
    except FileNotFoundError:
        return None

# Get the Grok API key
secrets_path = Path(__file__).parent.parent / '.secrets' / 'grok_keys.env'
api_key = load_key(key_name="GROK_API_KEY", file_path=secrets_path)
if not api_key:
    raise ValueError(f"Could not find GROK_API_KEY in {secrets_path}")

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

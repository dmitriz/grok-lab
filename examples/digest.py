"""
Simple News Digest Generator using Grok-3 API
"""

import requests
import json
from pathlib import Path

def load_key(key_name, file_path):
    """Load a key from a .env-style file (format: KEY=VALUE)"""
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line and line.split('=', 1)[0].strip() == key_name:
                    return line.split('=', 1)[1].strip()
        return None
    except FileNotFoundError:
        return None

def get_api_key():
    """Get the Grok API key from the secrets file."""
    secrets_path = Path(__file__).parent.parent / '.secrets' / 'grok_keys.env'
    if not (api_key := load_key(key_name="GROK_API_KEY", file_path=secrets_path)):
        raise ValueError(f"Could not find GROK_API_KEY in {secrets_path}")
    return api_key

def create_request_payload():
    """Create the payload for the API request."""
    return {
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

def call_grok_api(api_key, payload):
    """Call the Grok API with the given payload."""
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response.json()

def main():
    """Main function to execute the digest generation process."""
    # Get API key
    api_key = get_api_key()
    
    # Create payload
    payload = create_request_payload()
    
    # Call API
    try:
        response_json = call_grok_api(api_key, payload)
        print(json.dumps(response_json, indent=2))
    except Exception as e:
        print(f"API call failed: {e}")

if __name__ == "__main__":
    main()

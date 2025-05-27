"""
Optimized News Digest Generator using Grok-3 API with improved connection handling
"""

import requests
import json
from pathlib import Path
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# Disable SSL warnings if needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def create_optimized_session():
    """Create an optimized requests session with connection pooling and retry strategy."""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
        backoff_factor=1
    )
    
    # Configure HTTP adapter with optimized settings
    adapter = HTTPAdapter(
        pool_connections=1,
        pool_maxsize=1,
        max_retries=retry_strategy,
        pool_block=False
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set session-level timeouts and headers
    session.headers.update({
        'Connection': 'keep-alive',
        'User-Agent': 'grok-lab-digest/1.0'
    })
    
    return session

def call_grok_api_optimized(api_key, payload):
    """Call the Grok API with optimized connection handling."""
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    session = create_optimized_session()
    
    try:
        print("Making optimized API request...")
        start_time = time.time()
        response = session.post(
            url, 
            headers=headers, 
            json=payload, 
            timeout=(10, 60),  # (connect timeout, read timeout)
            stream=False
        )
        end_time = time.time()
        
        response.raise_for_status()
        result = response.json()
        print(f"API call completed in {(end_time - start_time) * 1000:.0f}ms")
        return result
        
    finally:
        session.close()

def main():
    """Main function to execute the digest generation process."""
    try:
        print("Starting optimized news digest generation...")
        
        # Get API key
        api_key = get_api_key()
        print("API key loaded successfully")
        
        # Create payload
        payload = create_request_payload()
        print("Request payload created")
        
        # Call API with optimized settings
        response_json = call_grok_api_optimized(api_key, payload)
        print(json.dumps(response_json, indent=2))
        
    except Exception as e:
        print(f"API call failed: {e}")

if __name__ == "__main__":
    main()

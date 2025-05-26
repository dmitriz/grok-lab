"""
Reusable Grok-3 API client module

This module provides a standardized interface for interacting with Grok-3 API,
enabling live chat functionality with multi-message support.
It handles API key management and request formatting according to Grok-3 API specifications.
"""

import requests
import json
from pathlib import Path

# Constants defined at the top of the file for better maintainability
# Default model used by the Grok API
GROK_MODEL = "grok-3-latest"
# API endpoint URL
GROK_API_ENDPOINT = "https://api.x.ai/v1/chat/completions"

def load_key(key_name, file_path):
  """
  Load a key from a .env-style file (format: KEY=VALUE)
  
  Args:
    key_name (str): The name of the key to find in the file
    file_path (Path): Path to the file containing the key
    
  Returns:
    str or None: The key value if found, None otherwise
  """
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
  """
  Get the Grok API key from the secrets file.
  
  Returns:
    str: The API key
    
  Raises:
    ValueError: If the API key is not found in the secrets file
  """
  # Path is relative to the current file location
  secrets_path = Path(__file__).parent / '.secrets' / 'grok_keys.env'
  if not (api_key := load_key(key_name="GROK_API_KEY", file_path=secrets_path)):
    raise ValueError(f"Could not find GROK_API_KEY in {secrets_path}")
  return api_key

def grok_live_response(payload):
  """
  Send a multi-message chat payload to the Grok-3 API and return the live response.
  
  Args:
    payload (dict): The chat payload, must include 'messages'.
                  
  Returns:
    dict: The API response JSON containing the model's response.
    
  Raises:
    ValueError: If payload structure is invalid
    requests.exceptions.RequestException: If API call fails
  """
  # Validate that messages exist
  if "messages" not in payload or not payload["messages"]:
    raise ValueError("Payload must contain non-empty 'messages' field")
  
  # Set required parameters for live mode
  payload["search_parameters"] = {"mode": "on"}
  payload["model"] = GROK_MODEL
  
  # Get API key and prepare request
  api_key = get_api_key()
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
  
  # Make the API call
  response = requests.post(GROK_API_ENDPOINT, headers=headers, json=payload, timeout=30)
  
  # raise_for_status() raises an HTTPError if the response status code is 4XX/5XX
  response.raise_for_status()
  
  return response.json()

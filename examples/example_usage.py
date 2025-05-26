"""
Simple example demonstrating use of the grok_api module
"""

import json
from grok_api import grok_live_response

def main():
  """Simple demonstration of using the Grok API module"""
  # Create a custom chat payload - model is set automatically
  payload = {
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user", 
        "content": "What are the latest advancements in AI research?"
      }
    ]
  }
  
  # Call the API
  try:
    response = grok_live_response(payload)
    print("API Response:")
    print(json.dumps(response, indent=2))
      
  except Exception as e:
    print(f"Error calling Grok API: {e}")

if __name__ == "__main__":
  main()

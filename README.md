# Grok-Lab

A lightweight Python library for interacting with Grok-3 API, providing easy access to Grok-3's live chat capabilities.

## Features

- Simple interface to interact with Grok-3 API
- Support for multi-message chat payloads
- Automatic API key management
- Ensures live mode for reliable responses
- Configurable request parameters

## Installation

```bash
pip install grok-lab
```

## Quick Start

```python
from grok_api import grok_live_response

# Create a chat payload
payload = {
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
  ],
  "model": "grok-3-latest"
}

# Get a response
response = grok_live_response(payload)
print(response["choices"][0]["message"]["content"])
```

## API Key Setup

Store your Grok API key in a file named `grok_keys.env` in the `.secrets` directory with the format:

```env
GROK_API_KEY=your_api_key_here
```

## Testing

Run the unit tests:

```bash
python -m unittest discover -s examples
```

## License

MIT

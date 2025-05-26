# Grok-Lab

A lightweight Python library for interacting with Grok-3 API, providing easy access to Grok-3's live chat capabilities.

## Features

- Simple interface to interact with Grok-3 API
- Support for multi-message chat payloads
- Automatic API key management
- Ensures live mode for reliable responses
- Configurable request parameters
- Multiple implementation options (Python, JavaScript, Shell Script)
- Performance-optimized versions with connection pooling

## Installation

```bash
pip install grok-lab
```

## Quick Start

```python
from grok_api import grok_live_response

# Create a chat payload (model is set automatically)
payload = {
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
  ]
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

## Development

Use the build script to run tests and examples:

```bash
# Run all tests
./build.sh test

# Run example usage
./build.sh example

# Run both tests and example
./build.sh all

# Clean up cache files
./build.sh clean
```

## Testing

Run the unit tests manually:

```bash
python -m unittest grok_api_test.py -v
```

## Performance Comparison

The project includes multiple implementations for performance comparison:

| Implementation | Speed | Use Case |
|---------------|-------|----------|
| `digest_optimized.py` | ~0.9s | **Production** (fastest with connection pooling) |
| `digest.sh` | ~22s | **Development** (simple debugging) |
| `digest.py` | ~24s | **Standard** (basic Python requests) |
| `digest.js` | ~33s | **Integration** (Node.js applications) |

```bash
# Compare all implementations
make digest-performance

# Run specific optimized version
make digest-optimized
```

See [PERFORMANCE_COMPARISON.md](PERFORMANCE_COMPARISON.md) for detailed analysis.

## License

MIT

# Example Scripts

This directory contains example scripts for interacting with the Grok API.

## Setup

Before running these scripts, you need to set up your API keys:

1. Make sure you have a `.secrets/grok_keys.env` file in the project root
2. The file should contain your API key in the following format:

   ```env
   GROK_API_KEY=your-api-key-here
   ```

## Scripts

- `api-key-info.sh` - Get information about your API key
- `hello-waw.sh` - Simple "hello world" chat completion example
- `chat-my.sh` - Chat completion with custom system prompt
- `digest.py` - Python script to generate news digest (already configured to use secrets)

## Security

- **Never commit API keys to git!**
- The `.secrets` directory is excluded from git via `.gitignore`
- All scripts now load API keys from the secrets file instead of having them hardcoded
- If you see any hardcoded keys in the codebase, please remove them immediately

## Usage

Run any script with bash:

```bash
bash api-key-info.sh
bash hello-waw.sh
bash chat-my.sh
python digest.py
```

#!/bin/bash
# Load environment variables from secrets file
source "$(dirname "$0")/../.secrets/grok_keys.env"

# Check if the API key is loaded
if [ -z "$GROK_API_KEY" ]; then
    echo "Error: GROK_API_KEY not found in .secrets/grok_keys.env"
    exit 1
fi

curl https://api.x.ai/v1/api-key \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GROK_API_KEY"
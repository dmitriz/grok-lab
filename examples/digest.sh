#!/bin/bash
# News Digest Generator using Grok-3 API (Shell Script version)

# Load environment variables from secrets file
source "$(dirname "$0")/../.secrets/grok_keys.env"

# Check if the API key is loaded
if [ -z "$GROK_API_KEY" ]; then
    echo "Error: GROK_API_KEY not found in .secrets/grok_keys.env"
    exit 1
fi

# Check if jq is available
if ! command -v jq >/dev/null 2>&1; then
    echo "Error: jq is required but not installed"
    exit 1
fi
if [[ "$(uname)" == "Darwin" ]]; then
  # macOS doesn't support %N in date
  start_time=$(date +%s)
else
  start_time=$(date +%s%N)
fi

curl -s https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -d '{
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
}' | jq '.'

if [[ "$(uname)" == "Darwin" ]]; then
  end_time=$(date +%s)
  duration=$(( (end_time - start_time) * 1000 ))
else
  end_time=$(date +%s%N)
  duration=$(( (end_time - start_time) / 1000000 ))
fi
  },
  "model": "grok-3-latest"
}' | jq '.'

end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))
echo "API call completed in ${duration}ms"

#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
fi

if [ -f "$SCRIPT_DIR/config.ini" ]; then
    PROVIDER_NAME=$(grep "^provider_name" "$SCRIPT_DIR/config.ini" | cut -d'=' -f2 | tr -d ' ')
    PROVIDER_MODEL=$(grep "^provider_model" "$SCRIPT_DIR/config.ini" | cut -d'=' -f2 | tr -d ' ')
    PROVIDER_SERVER=$(grep "^provider_server_address" "$SCRIPT_DIR/config.ini" | cut -d'=' -f2 | tr -d ' ')
    IS_LOCAL=$(grep "^is_local" "$SCRIPT_DIR/config.ini" | cut -d'=' -f2 | tr -d ' ')
fi

if [ -n "$PROVIDER_NAME" ]; then
    echo -e "\033[1;32m[SEEK] Starting with provider: $PROVIDER_NAME\033[0m"
else
    echo -e "\033[1;33m[SEEK] Warning: No provider configured\033[0m"
fi

if [ -n "$PROVIDER_MODEL" ]; then
    echo -e "\033[1;32m[SEEK] Model: $PROVIDER_MODEL\033[0m"
fi

if [ -n "$PROVIDER_SERVER" ]; then
    echo -e "\033[1;32m[SEEK] Server: $PROVIDER_SERVER\033[0m"
fi

if [ "$IS_LOCAL" = "True" ]; then
    echo -e "\033[1;36m[SEEK] Mode: Local\033[0m"
else
    echo -e "\033[1;36m[SEEK] Mode: Cloud\033[0m"
fi

if [ -n "$OPENROUTER_API_KEY" ]; then
    echo -e "\033[1;32m[SEEK] OpenRouter API: Configured\033[0m"
fi

if [ -n "$OPENAI_API_KEY" ]; then
    echo -e "\033[1;32m[SEEK] OpenAI API: Configured\033[0m"
fi

if [ -n "$DEEPSEEK_API_KEY" ]; then
    echo -e "\033[1;32m[SEEK] DeepSeek API: Configured\033[0m"
fi

echo -e "\033[1;34m[SEEK] Initializing SEEK...\033[0m\n"

cd "$SCRIPT_DIR"
python3 cli.py
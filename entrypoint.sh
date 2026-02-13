#!/bin/sh
set -e
# Start Ollama in the background so the app can use localhost:11434
ollama serve &
# Give Ollama a moment to bind
sleep 3
exec "$@"

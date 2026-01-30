#!/usr/bin/env bash
set -euo pipefail

MODEL_LOG_FILE="${MODEL_LOG_FILE:-/var/log/model/server.log}"
MODEL_SERVER_PORT="${MODEL_SERVER_PORT:-8000}"

mkdir -p "$(dirname "$MODEL_LOG_FILE")"

if [ "${ROTATE_MODEL_LOGS:-false}" = "true" ]; then
  : > "$MODEL_LOG_FILE"
fi

# Start the FastAPI model server in the background
python -m uvicorn app:app --host 0.0.0.0 --port "$MODEL_SERVER_PORT" > "$MODEL_LOG_FILE" 2>&1 &

# Start pyworker bootstrap
bootstrap_script=https://raw.githubusercontent.com/vast-ai/pyworker/refs/heads/main/start_server.sh;
curl -L "$bootstrap_script" | bash;

# FirstApp AI PyWorker

This folder contains the Vast Serverless PyWorker wrapper for the FirstApp AI
backend. It forwards serverless requests to the FastAPI backend running inside
the same container and relies on a benchmark input URL to pass readiness checks.

## Required env vars (set in Vast template)

- `PYWORKER_REPO` = Git repo URL for this folder (public).
- `MODEL_SERVER_URL` = `http://127.0.0.1`
- `MODEL_SERVER_PORT` = `8000`
- `MODEL_LOG_FILE` = `/var/log/model/server.log`
- `ROTATE_MODEL_LOGS` = `true`
- `BENCHMARK_INPUT_URL` = public URL to a small sample mp4
- `BENCHMARK_RUNS` = `1`
- `BENCHMARK_CONCURRENCY` = `1`

## On-start script

Paste the contents of `on_start.sh` into the template On-start Script field.

## Notes

- The worker exposes `/process_url`, which forwards JSON to the backend.
- The backend must implement `/process_url` and `/health` (already done).

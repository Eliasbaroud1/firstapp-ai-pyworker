import os
from typing import Dict

from vastai import (
    Worker,
    WorkerConfig,
    HandlerConfig,
    BenchmarkConfig,
    LogActionConfig,
)

MODEL_SERVER_URL = os.getenv("MODEL_SERVER_URL", "http://127.0.0.1")
MODEL_SERVER_PORT = int(os.getenv("MODEL_SERVER_PORT", "8000"))
MODEL_LOG_FILE = os.getenv("MODEL_LOG_FILE", "/var/log/model/server.log")

DEFAULT_WORKLOAD = float(os.getenv("DEFAULT_WORKLOAD", "100.0"))
MAX_QUEUE_TIME = float(os.getenv("MAX_QUEUE_TIME", "1800"))

BENCHMARK_RUNS = int(os.getenv("BENCHMARK_RUNS", "1"))
BENCHMARK_CONCURRENCY = int(os.getenv("BENCHMARK_CONCURRENCY", "1"))
BENCHMARK_INPUT_URL = os.getenv("BENCHMARK_INPUT_URL")


def request_parser(payload: Dict) -> Dict:
    if "input_url" not in payload:
        raise ValueError("input_url is required")
    payload.setdefault("mode", "blur")
    payload.setdefault("blur", 20)
    payload.setdefault("bg_color", "#00ff00")
    payload.setdefault("enhance_audio", False)
    payload.setdefault("output_ttl", int(os.getenv("BENCHMARK_OUTPUT_TTL", "1800")))
    return payload


def workload_calculator(_: Dict) -> float:
    return DEFAULT_WORKLOAD


def benchmark_generator() -> Dict:
    if not BENCHMARK_INPUT_URL:
        raise ValueError("BENCHMARK_INPUT_URL must be set for serverless benchmarks")
    return {
        "input_url": BENCHMARK_INPUT_URL,
        "mode": "blur",
        "blur": 12,
        "bg_color": "#00ff00",
        "enhance_audio": False,
        "output_ttl": int(os.getenv("BENCHMARK_OUTPUT_TTL", "600")),
    }


worker_config = WorkerConfig(
    model_server_url=MODEL_SERVER_URL,
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    handlers=[
        HandlerConfig(
            route="/process_url",
            allow_parallel_requests=False,
            max_queue_time=MAX_QUEUE_TIME,
            workload_calculator=workload_calculator,
            request_parser=request_parser,
            benchmark_config=BenchmarkConfig(
                generator=benchmark_generator,
                runs=BENCHMARK_RUNS,
                concurrency=BENCHMARK_CONCURRENCY,
            ),
        )
    ],
    log_action_config=LogActionConfig(
        on_load=[
            "Application startup complete.",
        ],
        on_error=[
            "Traceback (most recent call last):",
            "RuntimeError:",
        ],
    ),
)


if __name__ == "__main__":
    Worker(worker_config).run()

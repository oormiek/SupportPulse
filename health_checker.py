import time
import requests


def check_url(url):
    """Check an HTTP endpoint and measure response time."""
    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=5)
        elapsed = round((time.perf_counter() - start) * 1000, 2)

        return {
            "ok": response.ok,
            "status": response.status_code,
            "response_time_ms": elapsed,
            "message": response.reason,
        }

    except requests.RequestException as exc:
        elapsed = round((time.perf_counter() - start) * 1000, 2)

        return {
            "ok": False,
            "status": "N/A",
            "response_time_ms": elapsed,
            "message": str(exc),
        }

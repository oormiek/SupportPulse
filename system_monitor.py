import psutil


def get_system_metrics():
    """Return basic local machine health metrics."""
    return {
        "cpu": round(psutil.cpu_percent(interval=0.5), 1),
        "memory": round(psutil.virtual_memory().percent, 1),
        "disk": round(psutil.disk_usage("/").percent, 1),
    }

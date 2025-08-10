import psutil
import redis
import requests

class SimpleMetricsCollector:
    """
    Recolecta métricas REALES del sistema y del cluster de workers,
    leyendo información en vivo de Redis y la API real.
    """
    def __init__(self, redis_host='localhost', redis_port=6379, api_url="http://localhost:8000"):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.api_url = api_url

    def collect_metrics(self):
        # CPU y memoria del host
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()

        # Workers activos y sus IDs vía API real
        try:
            resp = requests.get(f"{self.api_url}/cluster/status/", timeout=2)
            data = resp.json()
            worker_ids = data.get("active_workers", [])
            active_workers = len(worker_ids)
        except Exception:
            worker_ids = []
            active_workers = 0

        # Busy workers, éxito/fallo (todo REAL vía Redis)
        busy_workers = 0
        total_success = 0
        total_fail = 0
        for wid in worker_ids:
            try:
                busy = int(self.r.get(f"worker:{wid}:busy") or 0)
                busy_workers += busy
            except Exception:
                pass
            try:
                total_success += int(self.r.get(f"worker:{wid}:success") or 0)
                total_fail += int(self.r.get(f"worker:{wid}:fail") or 0)
            except Exception:
                pass

        # Tareas en cola (REAL vía Redis)
        try:
            queue_length = self.r.llen("image_tasks")
        except Exception:
            queue_length = -1

        # Cálculo de métricas derivadas
        success_rate = 100.0 * total_success / (total_success + total_fail) if (total_success + total_fail) > 0 else 100.0
        worker_utilization = busy_workers / active_workers if active_workers else 0.0

        return {
            "cpu_usage": cpu,
            "memory_usage": mem.percent,
            "memory_available_gb": mem.available / (1024 ** 3),
            "active_workers": active_workers,
            "busy_workers": busy_workers,
            "worker_utilization": worker_utilization,
            "queue_length": queue_length,
            "success_rate": success_rate
        }

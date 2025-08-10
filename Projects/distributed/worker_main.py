import sys
import os
import threading
import time
import socket
import redis
import json
from datetime import datetime

# Permite que Python encuentre los módulos del proyecto al ejecutarse desde cualquier entorno
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_api.processors import ImageProcessor  # AJUSTA SI ES OTRA RUTA

# Configuración de Redis (host por variable de entorno)
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

worker_id = socket.gethostname()

def heartbeat_loop():
    """
    Heartbeat: Reporta 'vivo' en Redis cada 5s con TTL.
    """
    key = f"worker:{worker_id}:alive"
    pid = os.getpid()
    while True:
        heartbeat_info = {
            "status": "alive",
            "pid": pid,
            "timestamp": datetime.utcnow().isoformat()
        }
        r.set(key, json.dumps(heartbeat_info), ex=10)
        time.sleep(5)

def set_busy(val):
    """
    Marca este worker como ocupado (1) o libre (0), TTL para limpiar si muere.
    """
    r.set(f"worker:{worker_id}:busy", int(val), ex=15)

def incr_success():
    """
    Incrementa el contador de tareas exitosas de este worker.
    """
    r.incr(f"worker:{worker_id}:success")

def incr_fail():
    """
    Incrementa el contador de tareas fallidas de este worker.
    """
    r.incr(f"worker:{worker_id}:fail")

# Lanza heartbeat en background
heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
heartbeat_thread.start()

processor = ImageProcessor(max_workers=1)  # Un worker procesa una tarea a la vez

print(f"👷 Worker {worker_id} iniciado y esperando tareas...")
while True:
    task = r.blpop("image_tasks", timeout=0)  # Espera indefinidamente por nuevas tareas
    if task:
        _, data = task
        task_data = json.loads(data)
        print(f"🔔 Nueva tarea recibida: {task_data}")

        set_busy(1)  # Marca como ocupado
        try:
            result = processor.process_single_image(
                task_data["image_path"], task_data["filters"]
            )
            print(f"✅ Tarea completada: {result['status']}")
            if result.get("status") == "success":
                incr_success()
            else:
                incr_fail()
        except Exception as e:
            print(f"❌ Error procesando tarea: {e}")
            incr_fail()
        set_busy(0)  # Marca como libre

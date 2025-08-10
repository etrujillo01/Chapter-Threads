import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Envia 5 tareas iguales (puedes cambiar el número o usar imágenes diferentes)
for i in range(5):
    task = {
        "image_path": "static/images/sample_4k.jpg",  # Cambia por el nombre real de tus imágenes si tienes varias
        "filters": ["resize", "blur", "brightness"]
    }
    r.rpush("image_tasks", json.dumps(task))
    print(f"🚀 Tarea {i+1} enviada a la cola de Redis")

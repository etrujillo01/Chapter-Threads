#!/usr/bin/env python3
"""
Stress continuo - Mantiene enviando tareas para mantener cola llena usando /api/process/
"""
import requests
import threading
import time
import os
from datetime import datetime

# Calcula la ruta absoluta SIEMPRE desde la raíz del proyecto, no importa dónde ejecutes el script
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(ROOT_DIR, "static", "images", "Clocktower_Panorama_20080622_20mb.jpg")

print("Verificando imagen en:", IMAGE_PATH)
print("¿Existe?", os.path.exists(IMAGE_PATH))

def heavy_task():
    """Envía una imagen pesada al endpoint /api/process/"""
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ Imagen no encontrada: {IMAGE_PATH}")
        return False
    
    with open(IMAGE_PATH, "rb") as img_file:
        files = {'image': img_file}
        data = {'filters': "sharpen,edges,blur,resize,brightness"}
        try:
            response = requests.post(
                "http://localhost:8000/api/process/",
                files=files,
                data=data,
                timeout=15
            )
            if response.status_code == 200:
                print(f"✅ {datetime.now().strftime('%H:%M:%S')}", response.json().get("processed_path", "OK"))
                return True
            else:
                print(f"❌ HTTP {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False

def continuous_load(duration=30, rate=3):
    """
    Envía 'rate' tareas por segundo durante 'duration' segundos
    """
    print(f"🔥 CARGA CONTINUA: {rate} tareas/segundo por {duration} segundos")
    end_time = time.time() + duration

    while time.time() < end_time:
        threads = []
        for _ in range(rate):
            t = threading.Thread(target=heavy_task)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        time.sleep(1)
    print("\n🎯 Carga continua terminada!")

if __name__ == "__main__":
    import sys
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    continuous_load(duration)

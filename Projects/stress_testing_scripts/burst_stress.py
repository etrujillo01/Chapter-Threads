#!/usr/bin/env python3
"""
Burst stress - Envía tareas en paralelo para saturar workers usando /api/process/
"""
import requests
import threading
import time
import os

# Calcula la ruta absoluta SIEMPRE desde la raíz del proyecto, no importa dónde ejecutes el script
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(ROOT_DIR, "static", "images", "Clocktower_Panorama_20080622_20mb.jpg")

print("Verificando imagen en:", IMAGE_PATH)
print("¿Existe?", os.path.exists(IMAGE_PATH))

def rapid_task():
    """Tarea que envía una imagen y filtros al endpoint /api/process/"""
    # IMPORTANTE: IMAGE_PATH debe estar definido antes, como se mostró antes
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
                # Puedes mostrar el path procesado o "OK"
                processed = response.json().get("processed_path") or response.json()
                print("✅", processed)
                return True
            else:
                print(f"❌ HTTP {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False

def burst_attack(count=20):
    print(f"💥 BURST ATTACK: {count} tareas (cada una sube imagen)")
    threads = []
    results = []

    def wrapper():
        results.append(rapid_task())

    for _ in range(count):
        t = threading.Thread(target=wrapper)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    success_count = sum(results)
    failed_count = len(results) - success_count
    print("\n📊 RESULTADOS DEL BURST ATTACK:")
    print(f"✅ Exitosas: {success_count}/{count} ({success_count/count*100:.1f}%)")
    print(f"❌ Fallidas:  {failed_count}/{count} ({failed_count/count*100:.1f}%)")

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    burst_attack(count)

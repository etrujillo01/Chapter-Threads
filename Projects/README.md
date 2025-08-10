# 🖼️ Django Image Server - Session 5 Projects

Servidor Django para servir imágenes 4K y demostrar **operaciones I/O-bound** en contexto de Threading vs Multiprocessing.

## 🎯 Objetivos

Este proyecto demuestra:
- ✅ **I/O-bound operations**: Leer archivos grandes del disco
- ✅ **Threading vs Multiprocessing**: Comparación de rendimiento  
- ✅ **Load testing**: Medición de concurrencia
- ✅ **Real-world scenario**: Servidor web sirviendo contenido estático

## 🚀 Setup Rápido

### 1. Instalar dependencias
```bash
# Desde Chapter-Threads/Projects/
pip install -r requirements.txt
```

### 2. Colocar imagen 4K
Coloca tu imagen 4K en:
```
static/images/sample_4k.jpg
```

### 3. Ejecutar servidor
```bash
python manage.py runserver 8000
```

### 4. Probar endpoints
```bash
# Health check
curl http://localhost:8000/

# Información de imagen (rápido)
curl http://localhost:8000/api/image/info/

# Descargar imagen 4K (I/O-bound)  
curl http://localhost:8000/api/image/4k/ -o downloaded_4k.jpg

# Imagen con procesamiento lento
curl "http://localhost:8000/api/image/slow/?delay=3.0" -o slow_4k.jpg

# Estadísticas del servidor
curl http://localhost:8000/api/stats/
```

## 🧪 Testing de Concurrencia

### Threading vs Multiprocessing Test

Crear archivo `test_concurrency.py`:

```python
import requests
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

BASE_URL = "http://localhost:8000"

def fetch_image():
    """Fetch 4K image - I/O bound operation"""
    start = time.time()
    response = requests.get(f"{BASE_URL}/api/image/4k/")
    elapsed = time.time() - start
    return elapsed, len(response.content)

def test_sequential(num_requests=10):
    """Test secuencial (baseline)"""
    print("🐌 Testing Sequential...")
    start = time.time()
    
    results = []
    for i in range(num_requests):
        elapsed, size = fetch_image()
        results.append(elapsed)
        print(f"Request {i+1}: {elapsed:.2f}s")
    
    total_time = time.time() - start
    print(f"📊 Sequential Total: {total_time:.2f}s")
    return total_time

def test_threading(num_requests=10, max_workers=5):
    """Test con Threading - perfecto para I/O-bound"""
    print(f"🧵 Testing Threading (workers={max_workers})...")
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_image) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    
    total_time = time.time() - start
    print(f"📊 Threading Total: {total_time:.2f}s")
    return total_time

def test_multiprocessing(num_requests=10, max_workers=4):
    """Test con Multiprocessing - menos eficiente para I/O-bound"""
    print(f"🔄 Testing Multiprocessing (workers={max_workers})...")
    start = time.time()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_image) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    
    total_time = time.time() - start
    print(f"📊 Multiprocessing Total: {total_time:.2f}s")
    return total_time

if __name__ == "__main__":
    NUM_REQUESTS = 20
    
    # Tests
    seq_time = test_sequential(NUM_REQUESTS)
    thread_time = test_threading(NUM_REQUESTS, max_workers=10)
    mp_time = test_multiprocessing(NUM_REQUESTS, max_workers=4)
    
    # Comparación
    print(f"\n🏆 RESULTADOS ({NUM_REQUESTS} requests):")
    print(f"Sequential:      {seq_time:.2f}s (baseline)")
    print(f"Threading:       {thread_time:.2f}s ({seq_time/thread_time:.1f}x faster)")
    print(f"Multiprocessing: {mp_time:.2f}s ({seq_time/mp_time:.1f}x faster)")
```

## 📊 Endpoints Disponibles

| Endpoint | Descripción | Uso |
|----------|-------------|-----|
| `GET /` | Health check | Verificar que el servidor funciona |
| `GET /api/image/info/` | Info de imagen | Metadata sin transferir archivo |
| `GET /api/image/4k/` | **Imagen 4K** | **Endpoint principal I/O-bound** |
| `GET /api/image/slow/?delay=N` | Imagen con delay | Simular procesamiento + I/O |
| `GET /api/stats/` | Estadísticas servidor | Monitoreo durante tests |

## 🔍 Análisis Esperado

### ¿Por qué Threading es mejor para este caso?

1. **I/O-bound operations**: Leer archivos del disco
2. **GIL no es problema**: Threads se bloquean en I/O, liberando GIL
3. **Menos overhead**: Crear threads es más rápido que procesos
4. **Shared memory**: Django puede compartir configuración

### ¿Cuándo usar Multiprocessing?

- CPU-bound tasks (resize, filters, compression)
- Operaciones que saturan CPU
- Cuando necesitas verdadero paralelismo

## 🛠️ Troubleshooting

### Imagen no encontrada
```bash
# Verificar que existe
ls -la static/images/sample_4k.jpg

# Descargar imagen de ejemplo (4K sample)
wget https://sample-4k.jpg -O static/images/sample_4k.jpg
```

### Error de dependencias
```bash
pip install Django==4.2.7 psutil==5.9.6 requests
```

### Puerto en uso
```bash
python manage.py runserver 8080  # Cambiar puerto
```

## 📚 Siguientes Pasos

1. **Load testing con wrk**: `wrk -t10 -c100 -d30s http://localhost:8000/api/image/4k/`
2. **Async version**: Implementar con `aiohttp` o Django async views
3. **Caching**: Agregar Redis/Memcached para imágenes  
4. **Monitoring**: Integrar Prometheus + Grafana
5. **Docker**: Containerizar para deployment

---

**¡Perfecto para demostrar por qué Threading domina en operaciones I/O-bound!** 🚀 
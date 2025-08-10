"""
⚖️ SESIÓN 2.4: Guía de Comparación - Threading vs Multiprocessing vs Async

Esta guía completa te ayuda a decidir cuándo usar cada enfoque de concurrencia
basado en el tipo de problema, recursos del sistema y requisitos de rendimiento.

🎯 Objetivos:
- Comparar Threading, Multiprocessing y Async
- Entender cuándo usar cada uno
- Ver ejemplos prácticos de cada enfoque
- Crear una guía de decisión clara
"""

import time
import threading
import multiprocessing as mp
import asyncio
import concurrent.futures
import requests
import math
from typing import List, Dict

# ============================================================================
# 🧪 TAREA DE PRUEBA 1: I/O-bound (Descargas de URLs)
# ============================================================================

def download_url_sync(url: str) -> Dict:
    """Descarga síncrona de URL"""
    try:
        response = requests.get(url, timeout=3)
        return {
            'url': url,
            'status': response.status_code,
            'size': len(response.content),
            'method': 'sync'
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'method': 'sync'
        }

def test_sequential_io(urls: List[str]) -> Dict:
    """Test secuencial para I/O-bound"""
    print("🐌 TEST SECUENCIAL (I/O-bound)")
    start = time.time()
    
    results = []
    for url in urls:
        result = download_url_sync(url)
        results.append(result)
    
    duration = time.time() - start
    print(f"⏱️ Tiempo secuencial: {duration:.2f}s")
    
    return {
        'method': 'sequential',
        'time': duration,
        'results': results
    }

def test_threading_io(urls: List[str]) -> Dict:
    """Test threading para I/O-bound"""
    print("🧵 TEST THREADING (I/O-bound)")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(download_url_sync, urls))
    
    duration = time.time() - start
    print(f"⏱️ Tiempo threading: {duration:.2f}s")
    
    return {
        'method': 'threading',
        'time': duration,
        'results': results
    }

def test_multiprocessing_io(urls: List[str]) -> Dict:
    """Test multiprocessing para I/O-bound (no recomendado)"""
    print("🔥 TEST MULTIPROCESSING (I/O-bound - overhead innecesario)")
    start = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(download_url_sync, urls))
    
    duration = time.time() - start
    print(f"⏱️ Tiempo multiprocessing: {duration:.2f}s")
    
    return {
        'method': 'multiprocessing',
        'time': duration,
        'results': results
    }

async def download_url_async(url: str) -> Dict:
    """Descarga asíncrona de URL"""
    import aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=3) as response:
                content = await response.read()
                return {
                    'url': url,
                    'status': response.status,
                    'size': len(content),
                    'method': 'async'
                }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'method': 'async'
        }

async def test_async_io(urls: List[str]) -> Dict:
    """Test async para I/O-bound"""
    print("⚡ TEST ASYNC (I/O-bound)")
    start = time.time()
    
    tasks = [download_url_async(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    duration = time.time() - start
    print(f"⏱️ Tiempo async: {duration:.2f}s")
    
    return {
        'method': 'async',
        'time': duration,
        'results': results
    }

# ============================================================================
# 🧪 TAREA DE PRUEBA 2: CPU-bound (Cálculo de primos)
# ============================================================================

def is_prime_cpu(n: int) -> bool:
    """Función CPU-intensiva para calcular primos"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def count_primes_in_range(start: int, end: int) -> int:
    """Cuenta primos en un rango"""
    count = 0
    for n in range(start, end + 1):
        if is_prime_cpu(n):
            count += 1
    return count

def test_sequential_cpu(ranges: List[tuple]) -> Dict:
    """Test secuencial para CPU-bound"""
    print("🐌 TEST SECUENCIAL (CPU-bound)")
    start = time.time()
    
    results = []
    for start_range, end_range in ranges:
        count = count_primes_in_range(start_range, end_range)
        results.append(count)
    
    duration = time.time() - start
    total_primes = sum(results)
    print(f"⏱️ Tiempo secuencial: {duration:.2f}s - {total_primes} primos")
    
    return {
        'method': 'sequential',
        'time': duration,
        'primes': total_primes,
        'results': results
    }

def test_threading_cpu(ranges: List[tuple]) -> Dict:
    """Test threading para CPU-bound (limitado por GIL)"""
    print("🧵 TEST THREADING (CPU-bound - limitado por GIL)")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(count_primes_in_range, start_range, end_range) 
                  for start_range, end_range in ranges]
        results = [future.result() for future in futures]
    
    duration = time.time() - start
    total_primes = sum(results)
    print(f"⏱️ Tiempo threading: {duration:.2f}s - {total_primes} primos")
    
    return {
        'method': 'threading',
        'time': duration,
        'primes': total_primes,
        'results': results
    }

def test_multiprocessing_cpu(ranges: List[tuple]) -> Dict:
    """Test multiprocessing para CPU-bound (recomendado)"""
    print("🔥 TEST MULTIPROCESSING (CPU-bound - verdadero paralelismo)")
    start = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = [executor.submit(count_primes_in_range, start_range, end_range) 
                  for start_range, end_range in ranges]
        results = [future.result() for future in futures]
    
    duration = time.time() - start
    total_primes = sum(results)
    print(f"⏱️ Tiempo multiprocessing: {duration:.2f}s - {total_primes} primos")
    
    return {
        'method': 'multiprocessing',
        'time': duration,
        'primes': total_primes,
        'results': results
    }

# ============================================================================
# 📊 COMPARACIONES COMPLETAS
# ============================================================================

def compare_io_bound():
    """Comparar todos los métodos para I/O-bound"""
    print("\n" + "📊" + "="*70)
    print("📊 COMPARACIÓN COMPLETA: I/O-BOUND (Descargas)")
    print("="*70)
    
    # URLs de prueba (simulamos con httpbin)
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1", 
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]
    
    print(f"🎯 Tarea: Descargar {len(urls)} URLs con delay de 1s cada una")
    print(f"⏱️ Tiempo esperado secuencial: ~{len(urls)} segundos")
    print(f"⏱️ Tiempo esperado concurrente: ~1 segundo")
    
    results = {}
    
    # Test secuencial
    try:
        results['sequential'] = test_sequential_io(urls)
    except Exception as e:
        print(f"❌ Error en test secuencial: {e}")
        results['sequential'] = {'method': 'sequential', 'time': float('inf')}
    
    # Test threading
    try:
        results['threading'] = test_threading_io(urls)
    except Exception as e:
        print(f"❌ Error en test threading: {e}")
        results['threading'] = {'method': 'threading', 'time': float('inf')}
    
    # Test multiprocessing
    try:
        results['multiprocessing'] = test_multiprocessing_io(urls)
    except Exception as e:
        print(f"❌ Error en test multiprocessing: {e}")
        results['multiprocessing'] = {'method': 'multiprocessing', 'time': float('inf')}
    
    # Test async (comentado porque requiere aiohttp)
    print("⚡ TEST ASYNC: Requiere 'pip install aiohttp' - omitido")
    
    # Análisis de resultados
    print(f"\n📈 ANÁLISIS I/O-BOUND:")
    seq_time = results['sequential']['time']
    thread_time = results['threading']['time']
    mp_time = results['multiprocessing']['time']
    
    if thread_time < float('inf'):
        thread_speedup = seq_time / thread_time
        print(f"🧵 Threading speedup: {thread_speedup:.1f}x")
        
    if mp_time < float('inf'):
        mp_speedup = seq_time / mp_time
        print(f"🔥 Multiprocessing speedup: {mp_speedup:.1f}x")
    
    print(f"\n💡 CONCLUSIÓN I/O-BOUND:")
    print(f"🥇 GANADOR: Threading/Async (menor overhead)")
    print(f"🥈 Segundo: Multiprocessing (funciona pero overhead innecesario)")
    print(f"🥉 Último: Secuencial (bloquea en cada I/O)")
    
    return results

def compare_cpu_bound():
    """Comparar todos los métodos para CPU-bound"""
    print("\n" + "📊" + "="*70)
    print("📊 COMPARACIÓN COMPLETA: CPU-BOUND (Cálculo de primos)")
    print("="*70)
    
    # Rangos de prueba
    ranges = [
        (10000, 12000),  # ~200 primos cada rango
        (12001, 14000),
        (14001, 16000),
        (16001, 18000)
    ]
    
    print(f"🎯 Tarea: Contar primos en {len(ranges)} rangos")
    print(f"💻 CPU cores disponibles: {mp.cpu_count()}")
    print(f"⏱️ Speedup teórico máximo: ~{mp.cpu_count()}x")
    
    results = {}
    
    # Test secuencial
    results['sequential'] = test_sequential_cpu(ranges)
    
    # Test threading
    results['threading'] = test_threading_cpu(ranges)
    
    # Test multiprocessing  
    results['multiprocessing'] = test_multiprocessing_cpu(ranges)
    
    # Análisis de resultados
    print(f"\n📈 ANÁLISIS CPU-BOUND:")
    seq_time = results['sequential']['time']
    thread_time = results['threading']['time']
    mp_time = results['multiprocessing']['time']
    
    thread_speedup = seq_time / thread_time
    mp_speedup = seq_time / mp_time
    
    print(f"🧵 Threading speedup: {thread_speedup:.1f}x")
    print(f"🔥 Multiprocessing speedup: {mp_speedup:.1f}x")
    
    efficiency = (mp_speedup / mp.cpu_count()) * 100
    print(f"📊 Eficiencia multiprocessing: {efficiency:.1f}%")
    
    print(f"\n💡 CONCLUSIÓN CPU-BOUND:")
    print(f"🥇 GANADOR: Multiprocessing (verdadero paralelismo)")
    print(f"🥈 Segundo: Threading (limitado por GIL, ~1x speedup)")
    print(f"🥉 Último: Secuencial (usa solo 1 core)")
    
    return results

# ============================================================================
# 🎓 GUÍA DE DECISIÓN
# ============================================================================

def decision_guide():
    """Guía completa para decidir qué usar"""
    print("\n" + "🎓" + "="*70)
    print("🎓 GUÍA DE DECISIÓN: ¿QUÉ USAR CUÁNDO?")
    print("="*70)
    
    scenarios = {
        "I/O-bound": {
            "description": "Red, archivos, base de datos",
            "threading": "🥇 EXCELENTE - Ideal para I/O",
            "multiprocessing": "🥈 FUNCIONA - Overhead innecesario", 
            "async": "🥇 EXCELENTE - Muy eficiente para I/O",
            "examples": ["API calls", "File downloads", "Database queries"]
        },
        "CPU-bound": {
            "description": "Cálculos, algoritmos, procesamiento",
            "threading": "🥉 MALO - Limitado por GIL",
            "multiprocessing": "🥇 EXCELENTE - Verdadero paralelismo",
            "async": "🥉 MALO - Un solo thread",
            "examples": ["Image processing", "Mathematical calculations", "Data analysis"]
        },
        "Mixed workload": {
            "description": "Combinación de I/O y CPU",
            "threading": "🥈 BUENO - Para partes I/O",
            "multiprocessing": "🥇 MEJOR - Para partes CPU",
            "async": "🥈 BUENO - Para partes I/O",
            "examples": ["Web scraping + processing", "ETL pipelines"]
        }
    }
    
    for scenario, details in scenarios.items():
        print(f"\n🎯 ESCENARIO: {scenario.upper()}")
        print(f"   📝 {details['description']}")
        print(f"   🧵 Threading: {details['threading']}")
        print(f"   🔥 Multiprocessing: {details['multiprocessing']}")
        print(f"   ⚡ Async: {details['async']}")
        print(f"   💡 Ejemplos: {', '.join(details['examples'])}")

def resource_requirements():
    """Comparar requerimientos de recursos"""
    print("\n" + "💻" + "="*60)
    print("💻 REQUERIMIENTOS DE RECURSOS")
    print("="*60)
    
    resources = {
        "Threading": {
            "memory": "Bajo (memoria compartida)",
            "cpu": "Limitado por GIL para CPU-bound",
            "overhead": "Bajo",
            "scalability": "Buena para I/O, mala para CPU"
        },
        "Multiprocessing": {
            "memory": "Alto (cada proceso tiene su memoria)",
            "cpu": "Excelente (usa todos los cores)",
            "overhead": "Alto (IPC, serialización)",
            "scalability": "Excelente para CPU-bound"
        },
        "Async": {
            "memory": "Muy bajo (un solo thread)",
            "cpu": "Un solo core",
            "overhead": "Muy bajo",
            "scalability": "Excelente para I/O concurrente"
        }
    }
    
    for method, reqs in resources.items():
        print(f"\n🔧 {method}:")
        for resource, description in reqs.items():
            print(f"   {resource.capitalize()}: {description}")

def practical_recommendations():
    """Recomendaciones prácticas"""
    print("\n" + "💡" + "="*60)
    print("💡 RECOMENDACIONES PRÁCTICAS")
    print("="*60)
    
    recommendations = [
        ("🌐 Web APIs", "Threading o Async", "I/O-bound, muchas requests"),
        ("🧮 Procesamiento de datos", "Multiprocessing", "CPU-intensivo"),
        ("📁 Procesamiento de archivos", "Threading", "I/O + algo de CPU"),
        ("🎮 Videojuegos", "Threading", "UI responsiva + lógica"),
        ("🤖 Machine Learning", "Multiprocessing", "Cálculos paralelos"),
        ("🕷️ Web Scraping", "Async > Threading", "Muchas requests HTTP"),
        ("📊 Data Analysis", "Multiprocessing", "Pandas, NumPy paralelo"),
        ("🔄 Background tasks", "Threading", "No bloquear UI principal")
    ]
    
    for use_case, recommendation, reason in recommendations:
        print(f"{use_case:25} → {recommendation:20} ({reason})")

def common_pitfalls():
    """Errores comunes a evitar"""
    print("\n" + "⚠️" + "="*60)
    print("⚠️ ERRORES COMUNES A EVITAR")
    print("="*60)
    
    pitfalls = [
        "🚫 Threading para CPU-bound intensivo",
        "🚫 Multiprocessing para I/O simple", 
        "🚫 Olvidar locks en threading",
        "🚫 No usar context managers (with statements)",
        "🚫 Demasiados threads/procesos (overhead)",
        "🚫 No manejar excepciones en workers",
        "🚫 Mixing async y sync sin cuidado",
        "🚫 No cerrar recursos adecuadamente"
    ]
    
    for pitfall in pitfalls:
        print(f"   {pitfall}")

# ============================================================================
# 🧪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

def run_complete_comparison():
    """Ejecutar comparación completa"""
    print("⚖️ COMPARACIÓN COMPLETA: Threading vs Multiprocessing vs Async")
    print("🎯 Objetivo: Entender cuándo usar cada enfoque")
    
    print(f"\n💻 INFORMACIÓN DEL SISTEMA:")
    print(f"🔢 CPU cores: {mp.cpu_count()}")
    print(f"🧵 Threading disponible: ✅")
    print(f"🔥 Multiprocessing disponible: ✅")
    print(f"⚡ Async disponible: ✅")
    
    # Comparaciones
    io_results = compare_io_bound()
    cpu_results = compare_cpu_bound()
    
    # Guías
    decision_guide()
    resource_requirements()
    practical_recommendations()
    common_pitfalls()
    
    return {
        'io_results': io_results,
        'cpu_results': cpu_results
    }

if __name__ == "__main__":
    print("⚖️ GUÍA COMPLETA: Threading vs Multiprocessing vs Async")
    print("🎯 OBJETIVO: Decidir cuál usar en cada situación")
    
    print("\n🎯 ¿Qué quieres ver?")
    print("1. Comparación completa (I/O + CPU)")
    print("2. Solo comparación I/O-bound")
    print("3. Solo comparación CPU-bound")
    print("4. Solo guías de decisión")
    choice = input("👉 Opción (1-4): ").strip()
    
    if choice == "1":
        # Comparación completa
        run_complete_comparison()
        
    elif choice == "2":
        # Solo I/O
        compare_io_bound()
        decision_guide()
        
    elif choice == "3":
        # Solo CPU
        compare_cpu_bound()
        decision_guide()
        
    else:
        # Solo guías
        decision_guide()
        resource_requirements()
        practical_recommendations()
        common_pitfalls()
    
    print("\n✅ ¡GUÍA DE COMPARACIÓN COMPLETADA!")
    print("🎓 Ahora sabes cuándo usar Threading, Multiprocessing o Async")
    print("🚀 ¡SESIÓN 2 COMPLETADA!")
    print("🎉 Has dominado: Threading → Multiprocessing → IPC → Comparación") 
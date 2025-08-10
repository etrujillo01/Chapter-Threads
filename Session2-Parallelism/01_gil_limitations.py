"""
🔒 SESIÓN 2.1: Limitaciones del GIL (Global Interpreter Lock)

Este módulo demuestra por qué el threading no es efectivo para
operaciones CPU-bound debido al GIL de Python.

🎯 Objetivos:
- Entender qué es el GIL y cómo funciona
- Ver por qué threading no mejora performance para CPU-bound
- Identificar cuándo necesitamos multiprocessing
- Medir diferencias entre I/O-bound vs CPU-bound
"""

import time
import threading
import math
import multiprocessing as mp
import concurrent.futures
from typing import List

# ============================================================================
# 🧮 OPERACIÓN CPU-INTENSIVA: Cálculo de Números Primos
# ============================================================================

def is_prime(n: int) -> bool:
    """Verifica si un número es primo (operación CPU-intensiva)"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Verificar divisores impares hasta sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def find_primes_in_range(start: int, end: int, worker_id: int = 0) -> List[int]:
    """Encuentra números primos en un rango (CPU-intensivo)"""
    print(f"🧮 Worker {worker_id}: Buscando primos entre {start} y {end}")
    start_time = time.time()
    
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    
    duration = time.time() - start_time
    print(f"✅ Worker {worker_id}: Encontrados {len(primes)} primos en {duration:.2f}s")
    
    return primes

# ============================================================================
# 🐌 MÉTODO SECUENCIAL (BASELINE)
# ============================================================================

def find_primes_sequential(ranges: List[tuple]) -> List[int]:
    """🐌 Método secuencial para buscar primos"""
    print("\n" + "🐌" + "="*60)
    print("🐌 BÚSQUEDA SECUENCIAL DE PRIMOS")
    print("="*60)
    
    total_start = time.time()
    all_primes = []
    
    for i, (start, end) in enumerate(ranges):
        primes = find_primes_in_range(start, end, i+1)
        all_primes.extend(primes)
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL SECUENCIAL: {total_time:.2f} segundos")
    print(f"📊 Primos totales encontrados: {len(all_primes)}")
    
    return all_primes, total_time

# ============================================================================
# 🧵 THREADING PARA CPU-BOUND (Limitado por GIL)
# ============================================================================

def threaded_prime_worker(start: int, end: int, worker_id: int, results: List, lock: threading.Lock):
    """Worker thread para buscar primos (limitado por GIL)"""
    primes = find_primes_in_range(start, end, worker_id)
    
    # Usar lock para agregar resultados de forma segura
    with lock:
        results.extend(primes)

def find_primes_threading(ranges: List[tuple]) -> List[int]:
    """🧵 Método threading para buscar primos (INEFECTIVO para CPU-bound)"""
    print("\n" + "🧵" + "="*60)
    print("🧵 BÚSQUEDA CON THREADING (limitado por GIL)")
    print("="*60)
    
    total_start = time.time()
    all_primes = []
    lock = threading.Lock()
    threads = []
    
    # Crear threads
    for i, (start, end) in enumerate(ranges):
        thread = threading.Thread(
            target=threaded_prime_worker,
            args=(start, end, i+1, all_primes, lock)
        )
        threads.append(thread)
        thread.start()
    
    # Esperar que terminen
    for thread in threads:
        thread.join()
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL THREADING: {total_time:.2f} segundos")
    print(f"📊 Primos totales encontrados: {len(all_primes)}")
    
    return all_primes, total_time

# ============================================================================
# 🔄 THREADPOOL PARA CPU-BOUND (También limitado por GIL)
# ============================================================================

def find_primes_threadpool(ranges: List[tuple], max_workers: int = 4) -> List[int]:
    """🔄 Método ThreadPool para buscar primos (INEFECTIVO para CPU-bound)"""
    print("\n" + "🔄" + "="*60)
    print(f"🔄 BÚSQUEDA CON THREADPOOL ({max_workers} workers) - limitado por GIL")
    print("="*60)
    
    total_start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Enviar tareas
        future_to_range = {
            executor.submit(find_primes_in_range, start, end, i+1): (start, end)
            for i, (start, end) in enumerate(ranges)
        }
        
        all_primes = []
        
        # Recoger resultados
        for future in concurrent.futures.as_completed(future_to_range):
            start, end = future_to_range[future]
            try:
                primes = future.result()
                all_primes.extend(primes)
            except Exception as e:
                print(f"❌ Error en rango {start}-{end}: {e}")
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL THREADPOOL: {total_time:.2f} segundos")
    print(f"📊 Primos totales encontrados: {len(all_primes)}")
    
    return all_primes, total_time

# ============================================================================
# 🌐 COMPARACIÓN: I/O-BOUND vs CPU-BOUND
# ============================================================================

def simulate_io_task(task_id: int, delay: float = 1.0) -> dict:
    """Simula tarea I/O-bound (donde threading SÍ funciona)"""
    print(f"🌐 I/O Task {task_id}: Iniciando (delay={delay}s)")
    start_time = time.time()
    
    # Simular I/O con sleep (libera el GIL)
    time.sleep(delay)
    
    duration = time.time() - start_time
    print(f"✅ I/O Task {task_id}: Completada en {duration:.2f}s")
    
    return {
        'task_id': task_id,
        'duration': duration,
        'type': 'io_bound'
    }

def compare_io_vs_cpu_threading():
    """🌐 Comparar threading para I/O-bound vs CPU-bound"""
    print("\n" + "🌐" + "="*60)
    print("🌐 COMPARACIÓN: I/O-bound vs CPU-bound con Threading")
    print("="*60)
    
    # Test 1: I/O-bound (threading es efectivo)
    print("\n🔹 TEST 1: I/O-bound (Threading EFECTIVO)")
    io_tasks = [1.0, 1.0, 1.0, 1.0]  # 4 tareas de 1 segundo cada una
    
    # Secuencial I/O
    start = time.time()
    for i, delay in enumerate(io_tasks):
        simulate_io_task(i+1, delay)
    io_sequential_time = time.time() - start
    print(f"🐌 I/O Secuencial: {io_sequential_time:.2f}s")
    
    # Threading I/O
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(simulate_io_task, i+1, delay) for i, delay in enumerate(io_tasks)]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    io_threading_time = time.time() - start
    print(f"🧵 I/O Threading: {io_threading_time:.2f}s")
    print(f"📈 Mejora I/O: {io_sequential_time/io_threading_time:.1f}x más rápido")
    
    # Test 2: CPU-bound (threading NO es efectivo)
    print(f"\n🔹 TEST 2: CPU-bound (Threading INEFECTIVO)")
    cpu_ranges = [(1000000, 1300000), (1300001, 1600000), (1600001, 1900000), (1900001, 2200000)]
    
    # Secuencial CPU
    _, cpu_sequential_time = find_primes_sequential(cpu_ranges)
    
    # Threading CPU
    _, cpu_threading_time = find_primes_threading(cpu_ranges)
    
    print(f"\n📊 COMPARACIÓN FINAL:")
    print(f"🌐 I/O-bound mejora: {io_sequential_time/io_threading_time:.1f}x")
    print(f"🧮 CPU-bound mejora: {cpu_sequential_time/cpu_threading_time:.1f}x (casi nada)")
    
    return {
        'io_sequential': io_sequential_time,
        'io_threading': io_threading_time,
        'cpu_sequential': cpu_sequential_time,
        'cpu_threading': cpu_threading_time
    }

# ============================================================================
# 🎓 EXPLICACIÓN DEL GIL
# ============================================================================

def explain_gil():
    """🎓 Explicar qué es el GIL y por qué existe"""
    print("\n" + "🎓" + "="*60)
    print("🎓 ¿QUÉ ES EL GIL (Global Interpreter Lock)?")
    print("="*60)
    
    explanations = [
        ("🔒 Definición", "Mutex que protege el acceso a objetos Python"),
        ("🧵 Efecto en Threading", "Solo un thread puede ejecutar código Python a la vez"),
        ("🌐 I/O Operations", "GIL se libera durante operaciones I/O (sleep, read, write)"),
        ("🧮 CPU Operations", "GIL NO se libera durante cálculos intensivos"),
        ("📈 Performance", "Threading útil para I/O, inútil para CPU-bound"),
        ("🏗️ Arquitectura", "Simplifica la implementación de CPython"),
        ("🔄 Context Switching", "Python cambia entre threads cada 5ms aprox"),
        ("💾 Memory Management", "Protege el reference counting de Python"),
    ]
    
    for concept, explanation in explanations:
        print(f"💡 {concept:20}: {explanation}")
    
    print(f"\n🚨 IMPLICACIONES DEL GIL:")
    print(f"✅ Threading FUNCIONA para: I/O, red, archivos, base de datos")
    print(f"❌ Threading NO FUNCIONA para: cálculos, algoritmos, procesamiento")
    print(f"🔄 Solución para CPU-bound: MULTIPROCESSING")
    print(f"⚡ Alternativa moderna: async/await para I/O")
    
    print(f"\n💭 ¿POR QUÉ EXISTE EL GIL?")
    print(f"🎯 Simplifica la gestión de memoria")
    print(f"🎯 Evita corrupción en reference counting")
    print(f"🎯 Hace CPython más simple de implementar")
    print(f"🎯 Compatibilidad con C extensions")

# ============================================================================
# 🧪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

def demonstrate_gil_limitations():
    """Demostración principal de las limitaciones del GIL"""
    print("🔒 DEMOSTRACIÓN: Limitaciones del GIL para CPU-bound")
    print("🎯 Objetivo: Entender por qué threading no mejora CPU-bound tasks")
    
    print("\n⏱️ IMPORTANTE: Esta demo usa rangos MUY GRANDES para mostrar claramente el GIL")
    print(f"⏱️ Optimizado para sistemas con {mp.cpu_count()} cores como el tuyo")
    print("⏱️ Cada test tomará ~5-10 segundos para ser educativo")
    print("⏱️ Para demo rápida, cambiar rangos a (10000, 15000) etc.")
    
    # Configurar rangos para buscar primos
    ranges = [
        (1000000, 1300000),  # Rango 1: ~25000 primos
        (1300001, 1600000),  # Rango 2: ~25000 primos
        (1600001, 1900000),  # Rango 3: ~24000 primos
        (1900001, 2200000),  # Rango 4: ~24000 primos
    ]
    
    print(f"\n🎯 Configuración:")
    print(f"   - Rangos de búsqueda: {len(ranges)}")
    print(f"   - Operación: Encontrar números primos (CPU-intensivo)")
    print(f"   - Objetivo: Comparar secuencial vs threading")
    
    # Ejecutar comparaciones
    sequential_primes, sequential_time = find_primes_sequential(ranges)
    threading_primes, threading_time = find_primes_threading(ranges)
    threadpool_primes, threadpool_time = find_primes_threadpool(ranges)
    
    # Análisis de resultados
    print(f"\n" + "📊" + "="*60)
    print("📊 ANÁLISIS DE RESULTADOS")
    print("="*60)
    print(f"🐌 Secuencial:    {sequential_time:.2f}s - {len(sequential_primes)} primos")
    print(f"🧵 Threading:     {threading_time:.2f}s - {len(threading_primes)} primos")
    print(f"🔄 ThreadPool:    {threadpool_time:.2f}s - {len(threadpool_primes)} primos")
    
    threading_speedup = sequential_time / threading_time
    threadpool_speedup = sequential_time / threadpool_time
    
    print(f"\n🚀 SPEEDUP:")
    print(f"📈 Threading speedup:  {threading_speedup:.2f}x")
    print(f"📈 ThreadPool speedup: {threadpool_speedup:.2f}x")
    
    if threading_speedup < 1.5:
        print(f"\n⚠️ ¡GIL LIMITACIÓN CONFIRMADA!")
        print(f"⚠️ Threading NO mejora performance para CPU-bound")
        print(f"⚠️ Speedup < 1.5x indica limitación del GIL")
    else:
        print(f"\n🤔 Speedup inesperadamente alto")
        print(f"🤔 Puede ser por I/O oculto o variabilidad del sistema")
    
    print(f"\n💡 CONCLUSIÓN:")
    print(f"💡 Para operaciones CPU-bound, necesitamos MULTIPROCESSING")
    print(f"💡 Threading solo es útil para I/O-bound operations")
    
    return {
        'sequential_time': sequential_time,
        'threading_time': threading_time,
        'threadpool_time': threadpool_time,
        'primes_found': len(sequential_primes)
    }

if __name__ == "__main__":
    print("🔒 DEMOSTRACIÓN: Limitaciones del GIL en Python")
    print("🎯 IMPORTANTE: Esto demuestra por qué threading tiene límites")
    
    # Explicar el GIL primero
    explain_gil()
    
    print("\n🎯 ¿Quieres ver la demostración completa? (y/n)")
    choice = input("👉 ").lower().strip()
    
    if choice in ['y', 'yes', 'sí', 's']:
        # Demostración principal
        results = demonstrate_gil_limitations()
        
        print("\n🎯 ¿Quieres ver comparación I/O vs CPU? (y/n)")
        choice2 = input("👉 ").lower().strip()
        
        if choice2 in ['y', 'yes', 'sí', 's']:
            compare_io_vs_cpu_threading()
    else:
        print("\n🔒 Demo rápida del GIL:")
        # Solo explicación
        pass
    
    print("\n🎓 PUNTOS CLAVE:")
    print("🔒 GIL = Global Interpreter Lock")
    print("🧵 Threading útil para I/O-bound")
    print("🧮 Threading inútil para CPU-bound")
    print("🚀 Próximo paso: 02_multiprocessing_basics.py")
    print("🚀 Multiprocessing = Verdadero paralelismo para CPU-bound") 
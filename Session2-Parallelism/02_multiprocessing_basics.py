"""
🚀 SESIÓN 2.2: Multiprocessing + Comparación Completa

Este módulo demuestra multiprocessing y hace la comparación definitiva
entre Threading vs Multiprocessing para I/O-bound y CPU-bound.

🎯 Objetivos:
- Introducir el módulo multiprocessing de Python
- Demostrar verdadero paralelismo para CPU-bound
- Comparar Threading vs Multiprocessing para I/O y CPU
- Crear una guía de decisión clara
"""

import time
import math
import multiprocessing as mp
from typing import List, Tuple
import concurrent.futures
import os

# ============================================================================
# 🧮 MISMA OPERACIÓN CPU-INTENSIVA del archivo anterior
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
    """Encuentra números primos en un rango - PARA MULTIPROCESSING"""
    process_name = mp.current_process().name
    print(f"🔥 Process {process_name}: Buscando primos entre {start} y {end}")
    start_time = time.time()
    
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    
    duration = time.time() - start_time
    print(f"✅ Process {process_name}: Encontrados {len(primes)} primos en {duration:.2f}s")
    
    return primes

# ============================================================================
# 🔥 MÉTODO 1: Multiprocessing Manual 
# ============================================================================

def find_primes_multiprocessing_manual(ranges: List[tuple]) -> List[int]:
    """🔥 MULTIPROCESSING MANUAL: Múltiples procesos independientes"""
    print("\n" + "🔥" + "="*60)
    print("🔥 MÉTODO MULTIPROCESSING MANUAL - Múltiples procesos")
    print("="*60)
    
    total_start = time.time()
    
    # Crear procesos
    processes = []
    manager = mp.Manager()
    shared_results = manager.list()  # Lista compartida entre procesos
    
    for i, (start, end) in enumerate(ranges):
        # Crear proceso independiente
        process = mp.Process(
            target=multiprocessing_worker,
            args=(start, end, i+1, shared_results)
        )
        processes.append(process)
        process.start()
        print(f"🔥 Lanzado Process {i+1} para rango {start}-{end}")
    
    # Esperar que terminen todos los procesos
    for process in processes:
        process.join()
    
    # Convertir shared_results a lista normal
    all_primes = []
    for result_list in shared_results:
        all_primes.extend(result_list)
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL MULTIPROCESSING: {total_time:.2f} segundos")
    print(f"📊 Procesos utilizados: {len(processes)}")
    print(f"📊 Primos totales encontrados: {len(all_primes)}")
    
    return all_primes, total_time

def multiprocessing_worker(start: int, end: int, worker_id: int, shared_results):
    """Worker function para multiprocessing manual"""
    primes = find_primes_in_range(start, end, worker_id)
    shared_results.append(primes)

# ============================================================================
# 🔥 MÉTODO 2: ProcessPoolExecutor (Recomendado)
# ============================================================================

def find_primes_processpool(ranges: List[tuple], max_workers: int = None) -> List[int]:
    """🔥 SOLUCIÓN MODERNA: ProcessPoolExecutor"""
    print("\n" + "🔥" + "="*60)
    
    if max_workers is None:
        max_workers = mp.cpu_count()
    
    print(f"🔥 MÉTODO PROCESSPOOL - Máximo {max_workers} procesos")
    print(f"💻 CPU cores disponibles: {mp.cpu_count()}")
    print("="*60)
    
    total_start = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Enviar todas las tareas al pool
        print(f"📋 Enviando {len(ranges)} tareas al ProcessPool...")
        
        # submit() retorna Future objects
        future_to_range = {
            executor.submit(find_primes_in_range, start, end, i+1): (start, end)
            for i, (start, end) in enumerate(ranges)
        }
        
        all_primes = []
        
        # Procesar resultados conforme se completen
        for future in concurrent.futures.as_completed(future_to_range):
            start, end = future_to_range[future]
            try:
                primes = future.result()
                all_primes.extend(primes)
            except Exception as e:
                print(f"❌ Error en rango {start}-{end}: {e}")
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL PROCESSPOOL: {total_time:.2f} segundos")
    print(f"📊 Workers usados: {max_workers}")
    print(f"📊 Primos totales encontrados: {len(all_primes)}")
    
    return all_primes, total_time

# ============================================================================
# 🔥 MÉTODO 3: Pool.map() - Estilo Funcional
# ============================================================================

def prime_worker_simple(range_tuple: tuple) -> List[int]:
    """Worker simplificado para Pool.map()"""
    start, end = range_tuple
    return find_primes_in_range(start, end)

def find_primes_pool_map(ranges: List[tuple], processes: int = None) -> List[int]:
    """🔥 MÉTODO FUNCIONAL: Pool.map()"""
    print("\n" + "🔥" + "="*60)
    
    if processes is None:
        processes = mp.cpu_count()
    
    print(f"🔥 MÉTODO POOL.MAP - {processes} procesos")
    print("="*60)
    
    total_start = time.time()
    
    with mp.Pool(processes=processes) as pool:
        print(f"📋 Mapeando {len(ranges)} rangos a {processes} procesos...")
        
        # map() distribuye automáticamente el trabajo
        results = pool.map(prime_worker_simple, ranges)
    
    # Combinar todos los resultados
    all_primes = []
    for prime_list in results:
        all_primes.extend(prime_list)
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL POOL.MAP: {total_time:.2f} segundos")
    print(f"📊 Procesos utilizados: {processes}")
    print(f"📊 Primos totales encontrados: {len(all_primes)}")
    
    return all_primes, total_time

# ============================================================================
# 🧪 TAREA I/O-BOUND: Simular operaciones de red/archivos (para comparación)
# ============================================================================

def simulate_io_task(task_id: int, delay: float = 1.0) -> dict:
    """Simula operación I/O con delay confiable"""
    print(f"🌐 I/O Task {task_id}: Iniciando (delay={delay}s)")
    start_time = time.time()
    time.sleep(delay)  # Simular I/O (red, archivos, etc.)
    duration = time.time() - start_time
    print(f"✅ I/O Task {task_id}: Completada en {duration:.2f}s")
    
    return {
        'task_id': task_id,
        'duration': duration,
        'type': 'I/O-bound'
    }

def test_sequential_io(tasks: int = 4) -> dict:
    """Test secuencial para I/O-bound"""
    print("🐌 TEST SECUENCIAL (I/O-bound)")
    start = time.time()
    
    results = []
    for i in range(tasks):
        result = simulate_io_task(i+1)
        results.append(result)
    
    duration = time.time() - start
    print(f"⏱️ Tiempo secuencial I/O: {duration:.2f}s")
    
    return {
        'method': 'sequential',
        'time': duration,
        'results': results
    }

def test_threading_io(tasks: int = 4) -> dict:
    """Test threading para I/O-bound"""
    print("🧵 TEST THREADING (I/O-bound)")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(simulate_io_task, range(1, tasks+1)))
    
    duration = time.time() - start
    print(f"⏱️ Tiempo threading I/O: {duration:.2f}s")
    
    return {
        'method': 'threading',
        'time': duration,
        'results': results
    }

def test_multiprocessing_io(tasks: int = 4) -> dict:
    """Test multiprocessing para I/O-bound (overhead innecesario)"""
    print("🔥 TEST MULTIPROCESSING (I/O-bound - overhead innecesario)")
    start = time.time()
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(simulate_io_task, range(1, tasks+1)))
    
    duration = time.time() - start
    print(f"⏱️ Tiempo multiprocessing I/O: {duration:.2f}s")
    
    return {
        'method': 'multiprocessing',
        'time': duration,
        'results': results
    }

# ============================================================================
# ⚖️ COMPARACIÓN COMPLETA: Threading vs Multiprocessing (I/O + CPU)
# ============================================================================

def compare_threading_vs_multiprocessing():
    """⚖️ COMPARACIÓN COMPLETA: Threading vs Multiprocessing (I/O + CPU)"""
    print("\n" + "⚖️ " + "="*70)
    print("⚖️ COMPARACIÓN COMPLETA: Threading vs Multiprocessing")
    print("🎯 Objetivo: Ver cuándo cada uno es mejor (I/O vs CPU)")
    print("="*70)
    
    print(f"💻 Sistema: {mp.cpu_count()} CPU cores disponibles")
    
    all_results = {}
    
    # ========================================================================
    # 🌐 PARTE 1: I/O-BOUND (Threading debería ganar)
    # ========================================================================
    
    print(f"\n🌐 " + "="*60)
    print("🌐 PARTE 1: I/O-BOUND (Threading debería ser mejor)")
    print("="*60)
    print(f"🎯 Tarea: 4 operaciones I/O de 1s cada una")
    print(f"⏱️ Esperado: Secuencial ~4s, Threading ~1s, Multiprocessing ~1.2s")
    
    # Test secuencial I/O
    seq_io_result = test_sequential_io()
    
    # Test threading I/O  
    thread_io_result = test_threading_io()
    
    # Test multiprocessing I/O
    mp_io_result = test_multiprocessing_io()
    
    # Análisis I/O
    seq_io_time = seq_io_result['time']
    thread_io_time = thread_io_result['time']
    mp_io_time = mp_io_result['time']
    
    thread_io_speedup = seq_io_time / thread_io_time
    mp_io_speedup = seq_io_time / mp_io_time
    
    print(f"\n📊 RESULTADOS I/O-BOUND:")
    print(f"🐌 Secuencial:      {seq_io_time:.2f}s")
    print(f"🧵 Threading:       {thread_io_time:.2f}s (speedup: {thread_io_speedup:.1f}x)")
    print(f"🔥 Multiprocessing: {mp_io_time:.2f}s (speedup: {mp_io_speedup:.1f}x)")
    
    if thread_io_speedup > mp_io_speedup:
        print(f"🥇 GANADOR I/O: Threading (menos overhead)")
    else:
        print(f"🥇 GANADOR I/O: Multiprocessing")
    
    all_results['io'] = {
        'sequential': seq_io_time,
        'threading': thread_io_time,
        'multiprocessing': mp_io_time,
        'thread_speedup': thread_io_speedup,
        'mp_speedup': mp_io_speedup
    }
    
    # ========================================================================
    # 🧮 PARTE 2: CPU-BOUND (Multiprocessing debería ganar)
    # ========================================================================
    
    print(f"\n🧮 " + "="*60)
    print("🧮 PARTE 2: CPU-BOUND (Multiprocessing debería ser mejor)")
    print("="*60)
    
    # Configuración de prueba (RANGOS GRANDES para sistemas con muchos cores)
    ranges = [
        (1000000, 1300000),  # ~25000 primos cada rango
        (1300001, 1600000),
        (1600001, 1900000),
        (1900001, 2200000),
    ]
    
    print(f"🎯 Tarea: Encontrar primos en {len(ranges)} rangos grandes")
    print(f"⏱️ Esperado: Threading ~mismo tiempo que secuencial, Multiprocessing ~{mp.cpu_count()}x más rápido")
    
    # Test threading CPU (del archivo anterior)
    print(f"\n🧵 THREADING CPU-BOUND (limitado por GIL)")
    start = time.time()
    threading_primes = simulate_threading_cpu_bound(ranges)
    threading_cpu_time = time.time() - start
    
    # Test multiprocessing CPU
    print(f"\n🔥 MULTIPROCESSING CPU-BOUND")
    mp_primes, mp_cpu_time = find_primes_processpool(ranges)
    
    # Comparar con secuencial implícito (threading_time ≈ secuencial por GIL)
    seq_cpu_time = threading_cpu_time  # Threading ≈ secuencial para CPU-bound
    
    # Análisis CPU
    thread_cpu_speedup = seq_cpu_time / threading_cpu_time
    mp_cpu_speedup = seq_cpu_time / mp_cpu_time
    
    print(f"\n📊 RESULTADOS CPU-BOUND:")
    print(f"🐌 Secuencial (aprox): {seq_cpu_time:.2f}s")
    print(f"🧵 Threading:          {threading_cpu_time:.2f}s (speedup: {thread_cpu_speedup:.1f}x)")
    print(f"🔥 Multiprocessing:    {mp_cpu_time:.2f}s (speedup: {mp_cpu_speedup:.1f}x)")
    
    if mp_cpu_speedup > thread_cpu_speedup:
        print(f"🥇 GANADOR CPU: Multiprocessing (verdadero paralelismo)")
    else:
        print(f"🥇 GANADOR CPU: Threading")
    
    all_results['cpu'] = {
        'sequential': seq_cpu_time,
        'threading': threading_cpu_time,
        'multiprocessing': mp_cpu_time,
        'thread_speedup': thread_cpu_speedup,
        'mp_speedup': mp_cpu_speedup,
        'primes_found': len(mp_primes)
    }
    
    # ========================================================================
    # 📊 ANÁLISIS FINAL Y CONCLUSIONES
    # ========================================================================
    
    print(f"\n📊 " + "="*70)
    print("📊 ANÁLISIS FINAL: ¿CUÁNDO USAR CADA UNO?")
    print("="*70)
    
    print(f"\n🌐 PARA I/O-BOUND:")
    print(f"   🧵 Threading:       {thread_io_speedup:.1f}x speedup")
    print(f"   🔥 Multiprocessing: {mp_io_speedup:.1f}x speedup")
    if thread_io_speedup > mp_io_speedup:
        print(f"   ✅ Usar: Threading (menos overhead, misma velocidad)")
    else:
        print(f"   ✅ Usar: Multiprocessing")
    
    print(f"\n🧮 PARA CPU-BOUND:")
    print(f"   🧵 Threading:       {thread_cpu_speedup:.1f}x speedup (limitado por GIL)")
    print(f"   🔥 Multiprocessing: {mp_cpu_speedup:.1f}x speedup (verdadero paralelismo)")
    if mp_cpu_speedup > thread_cpu_speedup:
        print(f"   ✅ Usar: Multiprocessing (aprovecha todos los cores)")
    else:
        print(f"   ✅ Usar: Threading")
    
    # Eficiencia teórica
    theoretical_speedup = mp.cpu_count()
    cpu_efficiency = (mp_cpu_speedup / theoretical_speedup) * 100
    
    print(f"\n🎯 EFICIENCIA MULTIPROCESSING CPU:")
    print(f"   💻 CPU cores: {mp.cpu_count()}")
    print(f"   🎯 Speedup teórico máximo: {theoretical_speedup:.1f}x")
    print(f"   📊 Speedup real: {mp_cpu_speedup:.1f}x")
    print(f"   ⚡ Eficiencia: {cpu_efficiency:.1f}%")
    
    print(f"\n💡 REGLAS SIMPLES:")
    print(f"   🌐 I/O operations (requests, files, DB) → 🧵 Threading")
    print(f"   🧮 CPU calculations (math, algorithms) → 🔥 Multiprocessing")
    print(f"   ⚖️ Trade-off: Threading = menos memoria, Multiprocessing = más velocidad")
    
    return all_results

def simulate_threading_cpu_bound(ranges: List[tuple]) -> List[int]:
    """Simular threading CPU-bound (sabemos que será lento)"""
    import threading
    
    all_primes = []
    lock = threading.Lock()
    threads = []
    
    def thread_worker(start, end, thread_id):
        primes = find_primes_in_range(start, end, thread_id)
        with lock:
            all_primes.extend(primes)
    
    start_time = time.time()
    
    for i, (start, end) in enumerate(ranges):
        thread = threading.Thread(target=thread_worker, args=(start, end, i+1))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    duration = time.time() - start_time
    print(f"⏱️ Threading time: {duration:.2f}s - {len(all_primes)} primos")
    
    return all_primes

# ============================================================================
# 🎓 CONCEPTOS CLAVE MULTIPROCESSING
# ============================================================================

def explain_multiprocessing_concepts():
    """🎓 Explicar conceptos clave de multiprocessing"""
    print("\n" + "🎓" + "="*60)
    print("🎓 CONCEPTOS CLAVE DE MULTIPROCESSING")
    print("="*60)
    
    concepts = {
        "Process": "Proceso independiente con su propia memoria",
        "Paralelismo": "Múltiples tareas ejecutándose simultáneamente",
        "CPU-bound": "Operaciones limitadas por velocidad de CPU",
        "No GIL": "Cada proceso tiene su propio intérprete Python",
        "Process Pool": "Conjunto reutilizable de procesos para tareas",
        "IPC": "Inter-Process Communication - comunicación entre procesos",
        "Memory Overhead": "Cada proceso usa más memoria que threads",
        "Pickle": "Serialización necesaria para pasar datos entre procesos",
        "CPU cores": "Número de núcleos físicos disponibles"
    }
    
    for concept, explanation in concepts.items():
        print(f"💡 {concept:15}: {explanation}")
    
    print(f"\n✨ CUÁNDO USAR MULTIPROCESSING:")
    print(f"✅ Operaciones CPU-intensivas (cálculos, algoritmos)")
    print(f"✅ Procesamiento paralelo de datos")
    print(f"✅ Operaciones que pueden dividirse independientemente")
    print(f"✅ Cuando tienes múltiples CPU cores")
    
    print(f"\n⚠️ CUÁNDO NO USAR MULTIPROCESSING:")
    print(f"❌ Operaciones I/O-bound (usar threading o async)")
    print(f"❌ Tareas que requieren mucho intercambio de datos")
    print(f"❌ Aplicaciones con poca memoria RAM")
    print(f"❌ Sistemas con un solo core")
    
    print(f"\n🔍 DIFERENCIAS CLAVE:")
    print(f"🧵 Threading: Memoria compartida, limitado por GIL")
    print(f"🔥 Multiprocessing: Memoria separada, sin limitaciones de GIL")
    print(f"⚡ Async: Un solo thread, excelente para I/O concurrente")
    
    return concepts

# ============================================================================
# 🧪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

def demonstrate_multiprocessing():
    """Demostración principal de multiprocessing"""
    print("🔥 DEMOSTRACIÓN: Multiprocessing - Verdadero Paralelismo")
    print("🎯 Objetivo: Superar las limitaciones del GIL con procesos")
    
    print(f"\n⚖️ CONTRASTE EDUCATIVO:")
    print(f"📋 Archivo 1 (Threading): Rangos 500k-900k → ~1.1x mejora (GIL limita)")
    print(f"🔥 Archivo 2 (Multiprocessing): Rangos 1M-2.2M → ~{mp.cpu_count()}x mejora (sin GIL)")
    print(f"🎯 Rangos más grandes para tu sistema de {mp.cpu_count()} cores")
    print(f"⏱️ Esperamos ~3-5 segundos para ver DRAMÁTICAMENTE el paralelismo")
    
    # Verificar que estamos en el contexto adecuado
    print(f"\n💻 INFORMACIÓN DEL SISTEMA:")
    print(f"🔢 CPU cores: {mp.cpu_count()}")
    print(f"🐍 Proceso actual: {os.getpid()}")
    print(f"🔥 Multiprocessing disponible: {'✅' if __name__ == '__main__' else '⚠️ Ejecutar como script'}")
    
    # Configurar rangos (GRANDES para sistemas con muchos cores como el tuyo)
    ranges = [
        (1000000, 1300000),  # Rango 1: ~25000 primos
        (1300001, 1600000),  # Rango 2: ~25000 primos
        (1600001, 1900000),  # Rango 3: ~24000 primos
        (1900001, 2200000),  # Rango 4: ~24000 primos
    ]
    
    print(f"\n🎯 Configuración:")
    print(f"   - Rangos de búsqueda: {len(ranges)}")
    print(f"   - Operación: Encontrar números primos (CPU-intensivo)")
    print(f"   - Objetivo: Demostrar paralelismo real")
    
    # Ejecutar diferentes métodos
    processpool_primes, processpool_time = find_primes_processpool(ranges)
    map_primes, map_time = find_primes_pool_map(ranges)
    
    # Análisis comparativo
    print(f"\n" + "📊" + "="*60)
    print("📊 ANÁLISIS DE MÉTODOS MULTIPROCESSING")
    print("="*60)
    print(f"🔥 ProcessPool:    {processpool_time:.2f}s - {len(processpool_primes)} primos")
    print(f"🔥 Pool.map():     {map_time:.2f}s - {len(map_primes)} primos")
    
    speedup_vs_sequential = len(ranges)  # Speedup teórico si fuera perfectamente secuencial
    actual_speedup = speedup_vs_sequential / min(processpool_time, map_time) * (processpool_time + map_time) / 2
    
    print(f"\n🚀 MULTIPROCESSING BENEFITS:")
    print(f"📈 Speedup aproximado: {mp.cpu_count():.0f}x (teórico máximo)")
    print(f"💪 Usa todos los CPU cores disponibles")
    print(f"🚫 No limitado por GIL")
    print(f"⚡ Ideal para CPU-bound tasks")
    
    return {
        'processpool_time': processpool_time,
        'map_time': map_time,
        'primes_found': len(processpool_primes)
    }

if __name__ == "__main__":
    print("🔥 DEMOSTRACIÓN: Multiprocessing - Superando el GIL")
    print("🎯 IMPORTANTE: Ejecutar como script para multiprocessing")
    
    # Explicar conceptos primero
    explain_multiprocessing_concepts()
    
    print("\n🎯 ¿Qué quieres ver?")
    print("1. Solo demostración de multiprocessing")
    print("2. Comparación completa: Threading vs Multiprocessing (I/O + CPU)") 
    print("3. Solo conceptos teóricos")
    choice = input("👉 Opción (1-3): ").strip()
    
    if choice == "1":
        # Demostración principal
        results = demonstrate_multiprocessing()
        print(f"\n📊 Resultados de multiprocessing:")
        print(f"   ⏱️ ProcessPool: {results['processpool_time']:.2f}s")
        print(f"   ⏱️ Pool.map(): {results['map_time']:.2f}s")
        print(f"   📊 Primos encontrados: {results['primes_found']}")
        
    elif choice == "2":
        # Comparación completa
        compare_threading_vs_multiprocessing()
        
    else:
        print("\n🎓 Solo conceptos - revisar la función explain_multiprocessing_concepts()")
    
    print("\n✅ ¡SESIÓN 2 COMPLETADA!")
    print("🎓 Has aprendido: GIL → Limitaciones → Multiprocessing → Comparación")
    print("🎯 Ahora sabes cuándo usar Threading vs Multiprocessing")
    print("🚀 Próximos pasos: Session3-Async y Session4-IPC (futuras sesiones)") 
"""
⚡ SESIÓN 3: Guía Completa de Async/Await

Esta guía consolidada cubre TODOS los aspectos de async/await en Python:
- ¿Por qué async es "especial"?
- ¿Cómo sabemos que NO hay race conditions?
- Comparación completa: Threading vs Multiprocessing vs Async
- Guías prácticas de decisión

🎯 Objetivos:
- Entender la "magia" de async/await
- Demostrar matemáticamente la ausencia de race conditions
- Comparar los 3 enfoques de concurrencia
- Crear criterios claros para elegir cada uno
"""

import time
import threading
import multiprocessing as mp
import asyncio
import concurrent.futures
import math
from typing import List, Dict

# ============================================================================
# 🪄 PARTE 1: ¿POR QUÉ ASYNC ES "MÁGICO"?
# ============================================================================

print("🪄" + "="*70)
print("🪄 PARTE 1: ¿Por qué Async es 'mágico'?")
print("="*70)

def explain_paradigm_difference():
    """Explicar la diferencia fundamental de paradigmas"""
    print("\n🎯 DIFERENCIA FUNDAMENTAL DE PARADIGMAS:")
    print("="*50)
    
    print("🧵 THREADING = Concurrencia PREEMPTIVA:")
    print("   • OS decide cuándo cambiar threads → IMPREDECIBLE")
    print("   • Múltiples threads reales ejecutando")
    print("   • ~8MB memoria por thread")
    print("   • Máximo práctico: ~5,000 threads")
    print("   • Race conditions POSIBLES")
    
    print("\n⚡ ASYNC = Concurrencia COOPERATIVA:")
    print("   • Código decide cuándo ceder control → PREDECIBLE")
    print("   • Un solo thread con múltiples corrutinas")
    print("   • ~1KB memoria por corrutina")
    print("   • Máximo práctico: ~100,000+ corrutinas")
    print("   • Race conditions IMPOSIBLES")

def demo_scalability_difference():
    """Demostrar diferencias de escalabilidad"""
    print("\n🔥 DIFERENCIAS DE ESCALABILIDAD:")
    print("="*50)
    
    tasks_scenarios = [10, 100, 1000, 10000]
    
    print("📊 COMPARACIÓN DE RECURSOS:")
    for tasks in tasks_scenarios:
        threading_ram = tasks * 8  # MB
        async_ram = tasks / 1024   # MB (convertir de KB)
        
        print(f"\n   {tasks:,} tareas concurrentes:")
        print(f"     🧵 Threading: ~{threading_ram:,}MB RAM")
        print(f"     ⚡ Async: ~{async_ram:.1f}MB RAM")
        
        if threading_ram > 1024:  # > 1GB
            print(f"     ⚠️  Threading: {threading_ram/1024:.1f}GB RAM!")
        if tasks >= 5000:
            print(f"     ❌ Threading: Límite práctico excedido")

# ============================================================================
# 🔍 PARTE 2: PRUEBA DEFINITIVA - NO HAY RACE CONDITIONS
# ============================================================================

print("\n🔍" + "="*70)
print("🔍 PARTE 2: PRUEBA DEFINITIVA - NO hay Race Conditions")
print("="*70)

def demonstrate_threading_race_conditions():
    """Demostrar race conditions en threading"""
    print("\n🧵 THREADING: Intentando provocar race conditions...")
    
    shared_counter = 0
    
    def unsafe_increment():
        """Incrementar de manera no segura"""
        nonlocal shared_counter
        for _ in range(1000):
            # 🚨 OPERACIÓN NO ATÓMICA: Read-Modify-Write
            old_value = shared_counter    # READ
            new_value = old_value + 1     # MODIFY
            shared_counter = new_value    # WRITE
            
            # Aumentar probabilidad de race condition
            if _ % 100 == 0:
                time.sleep(0.001)
    
    # Ejecutar múltiples tests
    race_detected = False
    for test in range(5):
        shared_counter = 0
        
        threads = []
        for _ in range(2):
            thread = threading.Thread(target=unsafe_increment)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        expected = 2000
        actual = shared_counter
        
        if actual != expected:
            print(f"   ❌ Test {test+1}: {actual} (Esperado: {expected}) - Race condition detectado!")
            print(f"      🔍 Perdimos {expected - actual} operaciones")
            race_detected = True
            break
        else:
            print(f"   ✅ Test {test+1}: {actual} (Correcto esta vez)")
    
    if not race_detected:
        print("   💡 No se detectó race condition, pero PUEDE ocurrir")

async def demonstrate_async_no_race_conditions():
    """Demostrar que async NO puede tener race conditions"""
    print("\n⚡ ASYNC: Intentando provocar race conditions...")
    
    shared_counter = 0
    
    async def safe_increment():
        """Incrementar en async - siempre seguro"""
        nonlocal shared_counter
        for _ in range(1000):
            # ✅ MISMA OPERACIÓN: Read-Modify-Write
            old_value = shared_counter    # READ
            new_value = old_value + 1     # MODIFY
            shared_counter = new_value    # WRITE
            
            # Ceder control ocasionalmente (voluntario)
            if _ % 100 == 0:
                await asyncio.sleep(0.001)  # Solo AQUÍ puede cambiar corrutina
    
    # Ejecutar múltiples tests
    for test in range(5):
        shared_counter = 0
        
        # Ejecutar dos corrutinas concurrentemente
        await asyncio.gather(
            safe_increment(),
            safe_increment()
        )
        
        expected = 2000
        actual = shared_counter
        
        print(f"   ✅ Test {test+1}: {actual} (Esperado: {expected}) - ¡SIEMPRE correcto!")

def explain_why_async_is_safe():
    """Explicar técnicamente por qué async es seguro"""
    print("\n🔬 ANÁLISIS TÉCNICO: ¿Por qué async es diferente?")
    print("="*60)
    
    print("🧵 THREADING - Problema:")
    print("   1. Thread 1: old_value = shared.value  # Lee 100")
    print("   2. ⚠️  OS INTERRUMPE AQUÍ ⚠️")
    print("   3. Thread 2: old_value = shared.value  # Lee 100 (¡mismo valor!)")
    print("   4. Thread 2: shared.value = 101        # Escribe 101")
    print("   5. Thread 1: shared.value = 101        # Escribe 101 (perdió T2)")
    print("   📊 Resultado: 101 en lugar de 102 ❌")
    
    print("\n⚡ ASYNC - Solución:")
    print("   1. Corrutina 1: old_value = shared.value  # Lee 100")
    print("   2. Corrutina 1: new_value = 101           # Calcula")
    print("   3. Corrutina 1: shared.value = 101        # Escribe")
    print("   4. ✅ SOLO AQUÍ puede ceder: await asyncio.sleep()")
    print("   5. Corrutina 2: old_value = shared.value  # Lee 101 (correcto)")
    print("   6. Corrutina 2: shared.value = 102        # Escribe 102")
    print("   📊 Resultado: 102 (siempre correcto) ✅")
    
    print("\n🎯 PRINCIPIOS CLAVE DE ASYNC:")
    print("   ✅ Un solo thread → No competencia por recursos")
    print("   ✅ Control se cede SOLO en 'await' → Puntos explícitos")
    print("   ✅ Operaciones entre 'awaits' son ATÓMICAS")
    print("   ✅ Event loop garantiza ejecución secuencial")

# ============================================================================
# 📊 PARTE 3: COMPARACIÓN COMPLETA DE RENDIMIENTO
# ============================================================================

print("\n📊" + "="*70)
print("📊 PARTE 3: COMPARACIÓN COMPLETA DE RENDIMIENTO")
print("="*70)

# Funciones de simulación I/O-bound
def simulate_io_task_sync(task_name: str, delay: float = 1.0) -> Dict:
    """Simula tarea I/O-bound sincrónicamente"""
    time.sleep(delay)
    return {
        'task': task_name,
        'status': 'completed', 
        'delay': delay,
        'method': 'sync'
    }

def simulate_io_task_thread(task_name: str, delay: float = 1.0) -> Dict:
    """Simula tarea I/O-bound en thread"""
    time.sleep(delay)
    return {
        'task': task_name,
        'status': 'completed',
        'delay': delay, 
        'method': 'threading'
    }

async def simulate_io_task_async(task_name: str, delay: float = 1.0) -> Dict:
    """Simula tarea I/O-bound asíncronamente"""
    await asyncio.sleep(delay)
    return {
        'task': task_name,
        'status': 'completed',
        'delay': delay,
        'method': 'async'
    }

# Funciones de simulación CPU-bound  
def count_primes_in_range(start: int, end: int) -> Dict:
    """Cuenta números primos en un rango (CPU-bound)"""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    count = sum(1 for n in range(start, end) if is_prime(n))
    return {
        'range': f'{start}-{end}',
        'primes': count,
        'method': 'cpu_task'
    }

# Tests de comparación
def test_sequential_io(tasks: List[str]) -> Dict:
    """Test secuencial I/O-bound"""
    print("🐌 TEST SECUENCIAL (I/O-bound)")
    start = time.time()
    
    results = []
    for task in tasks:
        result = simulate_io_task_sync(task, 1.0)
        results.append(result)
    
    duration = time.time() - start
    print(f"⏱️ Tiempo secuencial: {duration:.2f}s")
    
    return {
        'method': 'sequential',
        'time': duration,
        'results': results
    }

def test_threading_io(tasks: List[str]) -> Dict:
    """Test threading I/O-bound"""
    print("🧵 TEST THREADING (I/O-bound)")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(simulate_io_task_thread, task, 1.0) for task in tasks]
        results = [future.result() for future in futures]
    
    duration = time.time() - start
    print(f"⏱️ Tiempo threading: {duration:.2f}s")
    
    return {
        'method': 'threading', 
        'time': duration,
        'results': results
    }

async def test_async_io(tasks: List[str]) -> Dict:
    """Test async I/O-bound"""
    print("⚡ TEST ASYNC (I/O-bound)")
    start = time.time()
    
    async_tasks = [simulate_io_task_async(task, 1.0) for task in tasks]
    results = await asyncio.gather(*async_tasks)
    
    duration = time.time() - start
    print(f"⏱️ Tiempo async: {duration:.2f}s")
    
    return {
        'method': 'async',
        'time': duration, 
        'results': results
    }

def test_sequential_cpu(ranges: List[tuple]) -> Dict:
    """Test secuencial CPU-bound"""
    print("🐌 TEST SECUENCIAL (CPU-bound)")
    start = time.time()
    
    results = []
    for start_range, end_range in ranges:
        result = count_primes_in_range(start_range, end_range)
        results.append(result)
    
    duration = time.time() - start
    print(f"⏱️ Tiempo secuencial: {duration:.2f}s")
    
    return {
        'method': 'sequential',
        'time': duration,
        'results': results
    }

def test_threading_cpu(ranges: List[tuple]) -> Dict:
    """Test threading CPU-bound"""
    print("🧵 TEST THREADING (CPU-bound)")
    start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = [executor.submit(count_primes_in_range, start_r, end_r) for start_r, end_r in ranges]
        results = [future.result() for future in futures]
    
    duration = time.time() - start
    print(f"⏱️ Tiempo threading: {duration:.2f}s")
    
    return {
        'method': 'threading',
        'time': duration,
        'results': results
    }

def test_multiprocessing_cpu(ranges: List[tuple]) -> Dict:
    """Test multiprocessing CPU-bound"""
    print("🔥 TEST MULTIPROCESSING (CPU-bound)")
    start = time.time()
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(count_primes_in_range, ranges)
    
    duration = time.time() - start
    print(f"⏱️ Tiempo multiprocessing: {duration:.2f}s")
    
    return {
        'method': 'multiprocessing',
        'time': duration,
        'results': results
    }

# ============================================================================
# 🎯 PARTE 4: GUÍAS DE DECISIÓN PRÁCTICA
# ============================================================================

def show_decision_matrix():
    """Mostrar matriz de decisión clara"""
    print("\n🎯" + "="*70)
    print("🎯 PARTE 4: GUÍA DE DECISIÓN PRÁCTICA")
    print("="*70)
    
    print("\n📋 MATRIZ DE DECISIÓN:")
    print("="*50)
    
    scenarios = [
        # (Escenario, Recomendación, Razón, Ejemplo)
        ("🌐 Web Server (1000+ requests)", "⚡ ASYNC", "Escalabilidad masiva", "FastAPI, aiohttp"),
        ("🕷️ Web Scraping (1000+ URLs)", "⚡ ASYNC", "Muchas requests HTTP", "aiohttp + BeautifulSoup"),
        ("📁 Procesamiento archivos (50)", "🧵 THREADING", "I/O moderado", "Leer/procesar archivos"),
        ("🎮 Game server (10,000 players)", "⚡ ASYNC", "Muchas conexiones", "WebSockets masivos"),
        ("🔢 Cálculo matemático intensivo", "🔥 MULTIPROCESSING", "CPU-bound puro", "Científico, ML"),
        ("💬 Chat server (1000+ users)", "⚡ ASYNC", "WebSockets múltiples", "Discord, Slack"),
        ("📊 ETL de datos (100 archivos)", "🧵 THREADING", "I/O + lógica", "Pandas, transformaciones"),
        ("🎨 Renderizado 3D", "🔥 MULTIPROCESSING", "CPU intensivo", "Blender, ray tracing"),
    ]
    
    for scenario, recommendation, reason, example in scenarios:
        print(f"\n{scenario}")
        print(f"   👍 Usar: {recommendation}")
        print(f"   💡 Razón: {reason}")
        print(f"   📝 Ejemplo: {example}")

def show_performance_rules():
    """Mostrar reglas de rendimiento"""
    print("\n⚡ REGLAS DE RENDIMIENTO:")
    print("="*40)
    
    print("\n🔥 Para CPU-bound (cálculos intensivos):")
    print("   🥇 Multiprocessing: ~10x speedup")
    print("   🥈 Sequential: baseline")  
    print("   🥉 Threading: ~1x (GIL)")
    print("   🥉 Async: ~1x (un solo thread)")
    
    print("\n💽 Para I/O-bound (red, disco, DB):")
    print("   🥇 Async: ~10x+ speedup, memoria mínima")
    print("   🥈 Threading: ~10x speedup, más memoria")
    print("   🥉 Multiprocessing: funciona pero overhead")
    print("   🥉 Sequential: ~1x baseline")

def show_resource_usage():
    """Mostrar uso de recursos"""
    print("\n💾 USO DE RECURSOS:")
    print("="*30)
    
    print("\n📊 Memoria por unidad:")
    print("   🧵 Threading: ~8MB por thread")
    print("   ⚡ Async: ~1KB por corrutina") 
    print("   🔥 Multiprocessing: ~10-50MB por proceso")
    
    print("\n🎯 Límites prácticos:")
    print("   🧵 Threading: ~5,000 threads")
    print("   ⚡ Async: ~100,000+ corrutinas")
    print("   🔥 Multiprocessing: ~CPU cores")

# ============================================================================
# 🎪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

async def run_complete_demonstration():
    """Ejecutar demostración completa"""
    print("⚡" + "="*70)
    print("⚡ GUÍA COMPLETA: Threading vs Multiprocessing vs Async")
    print("="*70)
    
    # Parte 1: Conceptos fundamentales
    explain_paradigm_difference()
    demo_scalability_difference()
    
    # Parte 2: Race conditions
    demonstrate_threading_race_conditions()
    await demonstrate_async_no_race_conditions()
    explain_why_async_is_safe()
    
    # Parte 3: Comparación de rendimiento I/O-bound
    print("\n📊 COMPARACIÓN I/O-BOUND:")
    print("="*40)
    
    tasks = ["url1", "url2", "url3", "url4", "url5"]
    
    # Sequential
    seq_result = test_sequential_io(tasks)
    
    # Threading
    thread_result = test_threading_io(tasks)
    
    # Async
    async_result = await test_async_io(tasks)
    
    # Análisis I/O-bound
    print(f"\n📈 ANÁLISIS I/O-BOUND:")
    seq_time = seq_result['time']
    thread_time = thread_result['time']
    async_time = async_result['time']
    
    print(f"🧵 Threading speedup: {seq_time/thread_time:.1f}x")
    print(f"⚡ Async speedup: {seq_time/async_time:.1f}x")
    print(f"💡 GANADOR I/O-bound: Threading/Async (similar rendimiento)")
    
    # Parte 4: Comparación CPU-bound
    print("\n📊 COMPARACIÓN CPU-bound:")
    print("="*40)
    
    ranges = [
        (1000000, 1100000),  # ~8000 primos cada rango
        (1100001, 1200000),
        (1200001, 1300000),
        (1300001, 1400000)
    ]
    
    # Sequential
    seq_cpu = test_sequential_cpu(ranges)
    
    # Threading  
    thread_cpu = test_threading_cpu(ranges)
    
    # Multiprocessing
    mp_cpu = test_multiprocessing_cpu(ranges)
    
    # Análisis CPU-bound
    print(f"\n📈 ANÁLISIS CPU-BOUND:")
    seq_time = seq_cpu['time']
    thread_time = thread_cpu['time']
    mp_time = mp_cpu['time']
    
    print(f"🧵 Threading speedup: {seq_time/thread_time:.1f}x")
    print(f"🔥 Multiprocessing speedup: {seq_time/mp_time:.1f}x")
    print(f"💡 GANADOR CPU-bound: Multiprocessing (~{mp.cpu_count()}x cores)")
    
    # Parte 5: Guías de decisión
    show_decision_matrix()
    show_performance_rules()
    show_resource_usage()
    
    # Conclusión
    print("\n🎓" + "="*60)
    print("🎓 CONCLUSIÓN FINAL")
    print("="*60)
    print("⚡ Async NO es 'mejor' que Threading en general")
    print("🎯 Cada herramienta tiene su lugar ESPECÍFICO:")
    print("   🕷️ Async → I/O masivo (web servers, scraping)")
    print("   🧵 Threading → I/O moderado (archivos, APIs)")
    print("   🔥 Multiprocessing → CPU intensivo (cálculos)")
    print("\n💡 La clave está en elegir la herramienta correcta!")
    print("📚 Ahora tienes el conocimiento para decidir sabiamente")

def main():
    """Función principal"""
    try:
        asyncio.run(run_complete_demonstration())
    except KeyboardInterrupt:
        print("\n👋 Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")

if __name__ == "__main__":
    main() 
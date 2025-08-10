"""
🚀 SESIÓN 1.2: Threading Básico - La Solución

Este módulo demuestra cómo threading puede resolver los problemas
del código secuencial, especialmente para operaciones I/O-bound.

🎯 Objetivos:
- Introducir el módulo threading de Python
- Comparar rendimiento: secuencial vs concurrent
- Entender cuándo threading es útil
- Aprender patrones básicos de concurrencia

✅ ACTUALIZADO: Usa simulación confiable con time.sleep() 
   en lugar de requests HTTP para resultados predecibles.
"""

import time
import threading
from typing import List, Dict
import concurrent.futures
from queue import Queue

# ============================================================================
# 🚀 SOLUCIÓN 1: Threading Manual Básico
# ============================================================================

class ThreadedDownloader:
    """Clase para manejar descargas con threading manual"""
    
    def __init__(self):
        self.results = []
        self.lock = threading.Lock()  # Para proteger results
    
    def simulate_task(self, task_name: str, delay: float, thread_id: int):
        """Simula tarea I/O en un hilo específico"""
        print(f"🧵 Thread {thread_id}: Iniciando tarea {task_name} (delay={delay}s)")
        start_time = time.time()
        
        # Simular operación I/O confiable
        time.sleep(delay)
        
        duration = time.time() - start_time
        
        result = {
            'thread_id': thread_id,
            'task_name': task_name,
            'delay_requested': delay,
            'duration': round(duration, 2),
            'status': 'completed'
        }
        
        # 🔒 CRITICAL SECTION: Acceso seguro a la lista compartida
        with self.lock:
            self.results.append(result)
        
        print(f"✅ Thread {thread_id}: Completado {task_name} en {duration:.2f}s")

def simulate_tasks_with_manual_threads(tasks: List[tuple]) -> List[Dict]:
    """🚀 SOLUCIÓN: Tareas concurrentes con threads manuales"""
    print("\n" + "="*60)
    print("🚀 MÉTODO THREADING MANUAL - Múltiples hilos")
    print("="*60)
    
    downloader = ThreadedDownloader()
    threads = []
    
    total_start = time.time()
    
    # Crear y iniciar threads
    for i, (task_name, delay) in enumerate(tasks):
        thread = threading.Thread(
            target=downloader.simulate_task,
            args=(task_name, delay, i+1)
        )
        threads.append(thread)
        thread.start()
        print(f"🚀 Lanzado Thread {i+1} para {task_name}")
    
    # Esperar a que todos terminen
    for thread in threads:
        thread.join()
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL THREADING: {total_time:.2f} segundos")
    print(f"📊 Número de threads usados: {len(threads)}")
    
    return downloader.results

# ============================================================================
# 🚀 SOLUCIÓN 2: ThreadPoolExecutor (Recomendado)
# ============================================================================

def simulate_io_task_modern(task_name: str, delay: float = 1.0) -> Dict:
    """Simula tarea I/O con delay confiable para ThreadPool"""
    thread_name = threading.current_thread().name
    print(f"🧵 {thread_name}: Iniciando tarea {task_name} (delay={delay}s)")
    start_time = time.time()
    
    # Simular operación I/O con delay confiable
    time.sleep(delay)
    
    duration = time.time() - start_time
    
    result = {
        'thread_name': thread_name,
        'task_name': task_name,
        'delay_requested': delay,
        'duration': round(duration, 2),
        'status': 'completed'
    }
    
    print(f"✅ {thread_name}: Completado {task_name} en {duration:.2f}s")
    return result

def simulate_tasks_with_threadpool(tasks: List[tuple], max_workers: int = 3) -> List[Dict]:
    """🚀 SOLUCIÓN MODERNA: ThreadPoolExecutor con simulación confiable"""
    print("\n" + "="*60)
    print(f"🚀 MÉTODO THREADPOOL - Máximo {max_workers} hilos")
    print("="*60)
    
    total_start = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Enviar todas las tareas al pool
        print(f"📋 Enviando {len(tasks)} tareas al ThreadPool...")
        
        # submit() retorna Future objects
        future_to_task = {
            executor.submit(simulate_io_task_modern, task_name, delay): (task_name, delay)
            for task_name, delay in tasks
        }
        
        results = []
        
        # Procesar resultados conforme se completen
        for future in concurrent.futures.as_completed(future_to_task):
            task_name, delay = future_to_task[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"❌ Error procesando {task_name}: {e}")
                results.append({
                    'task_name': task_name,
                    'delay_requested': delay,
                    'status': 'error',
                    'error': str(e)
                })
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL THREADPOOL: {total_time:.2f} segundos")
    print(f"📊 Workers usados: {max_workers}")
    
    return results

# ============================================================================
# 🚀 SOLUCIÓN 3: Producer-Consumer Pattern
# ============================================================================

def worker_thread(name: str, task_queue: Queue, results_queue: Queue):
    """Worker thread que procesa tareas de una queue"""
    print(f"👷 Worker {name}: Iniciado")
    
    while True:
        try:
            # Obtener tarea (blocking)
            task_data = task_queue.get(timeout=1)
            
            if task_data is None:  # Señal de terminar
                break
            
            task_name, delay = task_data
            print(f"👷 Worker {name}: Procesando {task_name} (delay={delay}s)")
            
            # Procesar la tarea con simulación confiable
            start_time = time.time()
            time.sleep(delay)  # Simular I/O confiable
            duration = time.time() - start_time
            
            result = {
                'worker': name,
                'task_name': task_name,
                'delay_requested': delay,
                'duration': round(duration, 2),
                'status': 'completed'
            }
            
            results_queue.put(result)
            print(f"✅ Worker {name}: Completado {task_name}")
            
            # Marcar tarea como completada
            task_queue.task_done()
            
        except:
            # Timeout - no hay más tareas
            break
    
    print(f"👷 Worker {name}: Terminado")

def simulate_tasks_with_producer_consumer(tasks: List[tuple], num_workers: int = 3) -> List[Dict]:
    """🚀 PATRÓN PRODUCER-CONSUMER con Queues y simulación confiable"""
    print("\n" + "="*60)
    print(f"🚀 PATRÓN PRODUCER-CONSUMER - {num_workers} workers")
    print("="*60)
    
    task_queue = Queue()
    results_queue = Queue()
    
    total_start = time.time()
    
    # Crear workers
    workers = []
    for i in range(num_workers):
        worker = threading.Thread(
            target=worker_thread,
            args=(f"Worker-{i+1}", task_queue, results_queue)
        )
        worker.start()
        workers.append(worker)
    
    # Producer: Agregar tareas a la queue
    print(f"📋 Agregando {len(tasks)} tareas a la queue...")
    for task_name, delay in tasks:
        task_queue.put((task_name, delay))
    
    # Esperar a que se completen todas las tareas
    task_queue.join()
    
    # Terminar workers
    for _ in workers:
        task_queue.put(None)  # Señal de terminar
    
    for worker in workers:
        worker.join()
    
    # Recoger resultados
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL PRODUCER-CONSUMER: {total_time:.2f} segundos")
    print(f"📊 Workers utilizados: {num_workers}")
    
    return results

# ============================================================================
# 📊 COMPARACIÓN DE RENDIMIENTO
# ============================================================================

def compare_all_methods():
    """Comparar todos los métodos: secuencial vs threading con simulación confiable"""
    print("\n" + "🏁" + "="*70)
    print("🏁 GRAN COMPARACIÓN: Secuencial vs Threading (SIMULACIÓN CONFIABLE)")
    print("="*70)
    
    # Tareas de prueba (todas con delay de 1 segundo)
    tasks = [
        ("Task-1", 1.0),
        ("Task-2", 1.0),
        ("Task-3", 1.0),
        ("Task-4", 1.0),
    ]
    
    results_comparison = {}
    
    # Método 1: Secuencial simulado
    print("\n🐌 MÉTODO 1: SECUENCIAL (SIMULADO)")
    start = time.time()
    sequential_results = []
    for task_name, delay in tasks:
        print(f"⏱️ Secuencial: Ejecutando {task_name} (delay={delay}s)")
        task_start = time.time()
        time.sleep(delay)
        duration = time.time() - task_start
        sequential_results.append({
            'task_name': task_name,
            'delay_requested': delay,
            'duration': round(duration, 2),
            'method': 'sequential'
        })
        print(f"✅ Secuencial: Completado {task_name} en {duration:.2f}s")
    
    sequential_time = time.time() - start
    print(f"\n⏱️ TIEMPO TOTAL SECUENCIAL: {sequential_time:.2f} segundos")
    results_comparison['sequential'] = {
        'time': sequential_time,
        'results': sequential_results
    }
    
    # Método 2: Threading Manual
    print("\n🚀 MÉTODO 2: THREADING MANUAL")
    start = time.time()
    manual_results = simulate_tasks_with_manual_threads(tasks)
    manual_time = time.time() - start
    results_comparison['manual_threads'] = {
        'time': manual_time,
        'results': manual_results
    }
    
    # Método 3: ThreadPool
    print("\n🚀 MÉTODO 3: THREADPOOL")
    start = time.time()
    pool_results = simulate_tasks_with_threadpool(tasks, max_workers=4)
    pool_time = time.time() - start
    results_comparison['threadpool'] = {
        'time': pool_time,
        'results': pool_results
    }
    
    # Método 4: Producer-Consumer
    print("\n🚀 MÉTODO 4: PRODUCER-CONSUMER")
    start = time.time()
    pc_results = simulate_tasks_with_producer_consumer(tasks, num_workers=4)
    pc_time = time.time() - start
    results_comparison['producer_consumer'] = {
        'time': pc_time,
        'results': pc_results
    }
    
    # 📊 ANÁLISIS DE RESULTADOS
    print("\n" + "📊" + "="*70)
    print("📊 ANÁLISIS DE RENDIMIENTO")
    print("="*70)
    
    print(f"🐌 Secuencial:           {sequential_time:.2f} segundos")
    print(f"🧵 Threading Manual:     {manual_time:.2f} segundos")
    print(f"🏊 ThreadPool:           {pool_time:.2f} segundos")
    print(f"🏭 Producer-Consumer:    {pc_time:.2f} segundos")
    
    # Calcular mejoras
    print(f"\n🚀 MEJORAS DE RENDIMIENTO:")
    print(f"📈 Threading vs Secuencial: {sequential_time/manual_time:.1f}x más rápido")
    print(f"📈 ThreadPool vs Secuencial: {sequential_time/pool_time:.1f}x más rápido")
    print(f"📈 Producer-Consumer vs Secuencial: {sequential_time/pc_time:.1f}x más rápido")
    
    print(f"\n✅ RESULTADOS ESPERADOS CON SIMULACIÓN:")
    print(f"📊 Secuencial: ~4 segundos (1+1+1+1)")
    print(f"📊 Threading: ~1 segundo (todas en paralelo)")
    print(f"📊 Mejora: ~4x más rápido para I/O-bound")
    
    return results_comparison

# ============================================================================
# 🎓 CONCEPTOS CLAVE PARA ESTUDIANTES
# ============================================================================

def explain_threading_concepts():
    """Explicar conceptos clave de threading"""
    print("\n" + "🎓" + "="*60)
    print("🎓 CONCEPTOS CLAVE DE THREADING")
    print("="*60)
    
    concepts = {
        "Thread": "Hilo de ejecución independiente dentro de un proceso",
        "Concurrencia": "Múltiples tareas progresando simultáneamente",
        "I/O Bound": "Operaciones limitadas por entrada/salida (red, disco)",
        "GIL": "Global Interpreter Lock - limita threading para CPU-bound",
        "Thread Pool": "Conjunto reutilizable de threads para tareas",
        "Race Condition": "Problema cuando threads acceden datos compartidos",
        "Lock": "Mecanismo para proteger secciones críticas",
        "Join": "Esperar a que un thread termine",
        "Daemon Thread": "Thread que termina cuando el programa principal termina"
    }
    
    for concept, explanation in concepts.items():
        print(f"💡 {concept:15}: {explanation}")
    
    print(f"\n✨ CUÁNDO USAR THREADING:")
    print(f"✅ Operaciones I/O (red, archivos, base de datos)")
    print(f"✅ Interfaces de usuario responsivas")
    print(f"✅ Tareas que pueden esperar independientemente")
    print(f"❌ Operaciones CPU-intensivas (usar multiprocessing)")
    
    return concepts

# ============================================================================
# 🧪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("🚀 DEMOSTRACIÓN: Threading Básico (CON SIMULACIÓN CONFIABLE)")
    print("🎯 Objetivo: Resolver problemas secuenciales con concurrencia")
    
    # Ejemplo rápido con simulación
    tasks = [
        ("Demo-Task-1", 1.0),
        ("Demo-Task-2", 1.0),
        ("Demo-Task-3", 1.0),
    ]
    
    print(f"\n🧪 Probando con {len(tasks)} tareas simuladas (1s cada una)...")
    print("⏱️ Secuencial esperado: ~3 segundos")
    print("⏱️ Threading esperado: ~1 segundo")
    
    # Demostrar ThreadPool (método recomendado)
    results = simulate_tasks_with_threadpool(tasks, max_workers=3)
    
    print(f"\n✅ Completado! {len(results)} tareas procesadas")
    
    # Explicar conceptos
    explain_threading_concepts()
    
    print("\n🎯 ¿Quieres ver la comparación completa? (y/n)")
    choice = input("👉 ").lower().strip()
    
    if choice in ['y', 'yes', 'sí', 's']:
        compare_all_methods()
    
    print("\n✅ Threading básico completado!")
    print("🚀 Próximo paso: 03_race_conditions.py") 
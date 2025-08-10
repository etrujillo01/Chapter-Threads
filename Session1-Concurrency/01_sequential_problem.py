"""
🐌 SESIÓN 1.1: El Problema del Código Secuencial

Este módulo demuestra por qué el código secuencial puede ser un problema
en operaciones que involucran I/O (red, archivos, base de datos).

🎯 Objetivos:
- Entender el concepto de "blocking operations"
- Medir el impacto del tiempo en operaciones secuenciales
- Identificar oportunidades para optimización
"""

import time
import requests
from typing import List
import json

# ============================================================================
# 🚨 PROBLEMA 1: Descargas Secuenciales (Red)
# ============================================================================

def download_url_sequential(url: str) -> dict:
    """Simula descarga de una URL - OPERACIÓN BLOQUEANTE"""
    print(f"🌐 Iniciando descarga: {url}")
    start_time = time.time()
    
    try:
        # Simulamos descarga lenta
        response = requests.get(url, timeout=10)
        duration = time.time() - start_time
        
        result = {
            'url': url,
            'status': response.status_code,
            'size': len(response.content),
            'duration': round(duration, 2)
        }
        
        print(f"✅ Completado: {url} en {duration:.2f}s")
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Error: {url} - {str(e)}")
        return {
            'url': url,
            'status': 'error',
            'error': str(e),
            'duration': round(duration, 2)
        }

def download_multiple_sequential(urls: List[str]) -> List[dict]:
    """🐌 PROBLEMA: Descargas una por una (BLOQUEANTE)"""
    print("\n" + "="*60)
    print("🐌 MÉTODO SECUENCIAL - Una descarga a la vez")
    print("="*60)
    
    total_start = time.time()
    results = []
    
    for url in urls:
        result = download_url_sequential(url)
        results.append(result)
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL SECUENCIAL: {total_time:.2f} segundos")
    
    return results

# ============================================================================
# 🚨 PROBLEMA 2: Procesamiento Intensivo Secuencial
# ============================================================================

def heavy_computation(n: int) -> dict:
    """Simula una operación computacionalmente intensiva"""
    print(f"🧮 Iniciando cálculo pesado para n={n}")
    start_time = time.time()
    
    # Operación intensiva: calcular suma de cuadrados
    result = sum(i**2 for i in range(n))
    
    duration = time.time() - start_time
    print(f"✅ Cálculo completado para n={n} en {duration:.2f}s")
    
    return {
        'input': n,
        'result': result,
        'duration': round(duration, 3)
    }

def process_multiple_sequential(numbers: List[int]) -> List[dict]:
    """🐌 PROBLEMA: Procesamiento uno por uno"""
    print("\n" + "="*60)
    print("🐌 PROCESAMIENTO SECUENCIAL - Un cálculo a la vez")
    print("="*60)
    
    total_start = time.time()
    results = []
    
    for num in numbers:
        result = heavy_computation(num)
        results.append(result)
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL SECUENCIAL: {total_time:.2f} segundos")
    
    return results

# ============================================================================
# 🚨 PROBLEMA 3: Base de Datos Secuencial (Simulada)
# ============================================================================

def db_query_simulation(query_id: int, delay: float = 0.5) -> dict:
    """Simula una consulta a base de datos lenta"""
    print(f"🗃️ Ejecutando query {query_id}...")
    start_time = time.time()
    
    # Simular delay de red/DB
    time.sleep(delay)
    
    duration = time.time() - start_time
    print(f"✅ Query {query_id} completada en {duration:.2f}s")
    
    return {
        'query_id': query_id,
        'result': f"Resultados para query {query_id}",
        'duration': round(duration, 2)
    }

def execute_queries_sequential(query_count: int) -> List[dict]:
    """🐌 PROBLEMA: Queries una por una"""
    print("\n" + "="*60)
    print("🐌 QUERIES SECUENCIALES - Una consulta a la vez")
    print("="*60)
    
    total_start = time.time()
    results = []
    
    for i in range(1, query_count + 1):
        result = db_query_simulation(i)
        results.append(result)
    
    total_time = time.time() - total_start
    print(f"\n⏱️ TIEMPO TOTAL QUERIES: {total_time:.2f} segundos")
    
    return results

# ============================================================================
# 🧪 DEMOSTRACIÓN PRÁCTICA
# ============================================================================

def demonstrate_sequential_problems():
    """Función principal para demostrar los problemas secuenciales"""
    
    print("🎯 DEMOSTRACIÓN: Problemas del Código Secuencial")
    print("🎯 Objetivo: Entender por qué necesitamos concurrencia")
    print("\n" + "="*70)
    
    # ⏰ PROBLEMA 1: Descargas de Red
    print("\n📡 PROBLEMA 1: Descargas de URLs")
    urls = [
        'https://httpbin.org/delay/1',  # 1 segundo delay
        'https://httpbin.org/delay/1',  # 1 segundo delay  
        'https://httpbin.org/delay/1',  # 1 segundo delay
    ]
    
    # Tiempo esperado: ~3 segundos (1+1+1)
    download_results = download_multiple_sequential(urls)
    
    # ⏰ PROBLEMA 2: Procesamiento Intensivo
    print("\n🧮 PROBLEMA 2: Procesamiento Computacional")
    numbers = [1000000, 1000000, 1000000]  # Números grandes para cálculos
    
    # Tiempo esperado: suma de todos los tiempos individuales
    computation_results = process_multiple_sequential(numbers)
    
    # ⏰ PROBLEMA 3: Queries de Base de Datos
    print("\n🗃️ PROBLEMA 3: Consultas a Base de Datos")
    query_count = 4
    
    # Tiempo esperado: 4 * 0.5 = 2 segundos
    db_results = execute_queries_sequential(query_count)
    
    # 📊 RESUMEN DE PROBLEMAS
    print("\n" + "="*70)
    print("📊 RESUMEN DE PROBLEMAS IDENTIFICADOS:")
    print("="*70)
    print("🚨 1. BLOCKING I/O: Las operaciones de red bloquean el hilo principal")
    print("🚨 2. DESPERDICIO DE CPU: Mientras esperamos red, el CPU está inactivo")
    print("🚨 3. TIEMPO ACUMULATIVO: Cada operación suma su tiempo al total")
    print("🚨 4. MALA EXPERIENCIA: El usuario espera demasiado tiempo")
    print("🚨 5. INEFICIENCIA: No aprovechamos recursos disponibles")
    
    print("\n💡 SOLUCIÓN: ¡Necesitamos CONCURRENCIA!")
    print("💡 Próximo paso: Implementar threading para resolver estos problemas")
    
    return {
        'downloads': download_results,
        'computations': computation_results,
        'db_queries': db_results
    }

# ============================================================================
# 🎯 EJERCICIO PRÁCTICO PARA ESTUDIANTES
# ============================================================================

def simulate_slow_task(task_id: int, delay: float = 2.0) -> dict:
    """Simula una tarea lenta con delay garantizado"""
    print(f"⏱️ Tarea {task_id}: Iniciando (delay={delay}s)")
    start_time = time.time()
    
    # Simular delay confiable
    time.sleep(delay)
    
    duration = time.time() - start_time
    print(f"✅ Tarea {task_id}: Completada en {duration:.2f}s")
    
    return {
        'task_id': task_id,
        'duration': duration
    }

def exercise_with_simulated_delay():
    """Ejercicio alternativo con delay simulado para garantizar tiempos"""
    print("\n" + "🎓" + "="*60)
    print("🎓 EJERCICIO ALTERNATIVO - Delay Simulado")
    print("="*60)
    print("📝 Usando time.sleep() para garantizar delay de 2 segundos")
    
    delays = [2.0, 2.0, 2.0, 2.0, 2.0]  # 5 tareas de 2 segundos
    
    print(f"\n🧪 Probando con {len(delays)} tareas de 2 segundos cada una...")
    print("⏱️ Tiempo esperado: ~10 segundos (2+2+2+2+2)")
    
    start = time.time()
    for i, delay in enumerate(delays):
        simulate_slow_task(i+1, delay)
    total_time = time.time() - start
    
    print(f"\n📊 RESULTADO: {total_time:.2f} segundos")
    print(f"📊 PROMEDIO por tarea: {total_time/len(delays):.2f} segundos")
    print(f"✅ Ahora SÍ vemos el problema secuencial claramente!")
    
    return total_time

def student_exercise():
    """Ejercicio para que los estudiantes midan el impacto"""
    print("\n" + "🎓" + "="*60)
    print("🎓 EJERCICIO PARA ESTUDIANTES")
    print("="*60)
    print("📝 Tarea: Agrega más URLs y mide el tiempo")
    print("📝 Pregunta: ¿Cuánto tiempo tardarían 10 descargas de 2 segundos cada una?")
    print("📝 Respuesta esperada: ~20 segundos (¡Demasiado!)")
    
    # URLs para prueba (puedes cambiar el delay)
    test_urls = [
        'https://httpbin.org/delay/2',  # 2 segundos
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/2',
    ]
    
    print(f"\n⚠️ NOTA: Si httpbin.org/delay no funciona como esperado,")
    print(f"⚠️ el tiempo puede ser menor. Deberían ser ~10 segundos total.")
    
    print(f"\n🧪 Probando con {len(test_urls)} URLs de 2 segundos cada una...")
    print("⏱️ Tiempo esperado: ~10 segundos")
    
    start = time.time()
    results = download_multiple_sequential(test_urls)
    total_time = time.time() - start
    
    print(f"\n📊 RESULTADO: {total_time:.2f} segundos")
    print(f"📊 PROMEDIO por descarga: {total_time/len(test_urls):.2f} segundos")
    
    return results

if __name__ == "__main__":
    # Ejecutar demostración completa
    print("🚀 Ejecutando demostración de problemas secuenciales...")
    
    # Demostración principal
    results = demonstrate_sequential_problems()
    
    # Ejercicio adicional
    print("\n" + "🎯" + "="*60)
    print("🎯 ¿Quieres probar el ejercicio? (y/n)")
    choice = input("👉 ").lower().strip()
    
    if choice in ['y', 'yes', 'sí', 's']:
        print("\n🎯 ¿Qué versión quieres probar?")
        print("1. Con httpbin.org (puede ser inconsistente)")
        print("2. Con delay simulado (tiempos garantizados)")
        option = input("👉 Opción (1 o 2): ").strip()
        
        if option == "2":
            exercise_with_simulated_delay()
        else:
            student_exercise()
    
    print("\n✅ Demostración completada!")
    print("🚀 Próximo paso: 02_basic_threading.py") 
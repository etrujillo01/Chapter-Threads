"""
🏥 Health Monitor - Ejercicio Hands-on

Template para que los estudiantes implementen un monitor de salud distribuido.
Evolución de: threading.Lock → distributed health checking

🎯 OBJETIVOS DEL EJERCICIO:
1. Implementar health checks paralelos con threading
2. Manejar timeouts y errores de red
3. Implementar retry logic y circuit breaker pattern
4. Mostrar estado en tiempo real

⏰ TIEMPO: 10 minutos en la sesión
"""

import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
from datetime import datetime
import json

# 🌐 CONFIGURACIÓN
SERVERS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]

# 📊 ESTADO GLOBAL (Thread-safe con locks)
server_status = {server: {"status": "UNKNOWN", "last_check": None, "response_time": 0} 
                for server in SERVERS}
status_lock = threading.Lock()

# ============================================================================
# 🏥 FUNCIONES BASE (YA IMPLEMENTADAS)
# ============================================================================

def simple_health_check(server: str) -> Tuple[bool, float]:
    """
    🏥 Health check básico a un servidor
    
    Returns:
        (is_healthy, response_time)
    """
    start_time = time.time()
    try:
        response = requests.get(f"{server}/", timeout=2)
        response_time = time.time() - start_time
        return response.status_code == 200, response_time
    except:
        response_time = time.time() - start_time
        return False, response_time

def update_server_status(server: str, is_healthy: bool, response_time: float):
    """🔄 Actualizar estado de servidor (thread-safe)"""
    with status_lock:
        server_status[server] = {
            "status": "UP" if is_healthy else "DOWN",
            "last_check": datetime.now().strftime("%H:%M:%S"),
            "response_time": response_time
        }

def print_status():
    """📊 Mostrar estado actual de todos los servidores"""
    print(f"\n🏥 ESTADO DE SERVIDORES - {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)
    
    with status_lock:
        for server, status in server_status.items():
            status_icon = "🟢" if status["status"] == "UP" else "🔴"
            print(f"{status_icon} {server}: {status['status']} | "
                  f"Last: {status['last_check']} | "
                  f"Time: {status['response_time']:.3f}s")

# ============================================================================
# 🧪 EJERCICIOS PARA IMPLEMENTAR
# ============================================================================

def exercise_1_basic_monitor():
    """
    🧪 EJERCICIO 1: Monitor básico secuencial
    
    TODO: Implementar un loop que:
    1. Verifique cada servidor secuencialmente
    2. Actualice el estado global
    3. Muestre el resultado
    
    ⏰ Tiempo estimado: 2 minutos
    """
    print("\n🧪 EJERCICIO 1: Monitor Básico Secuencial")
    print("=" * 50)
    
    # TODO: Implementar aquí
    # Pista: Usar simple_health_check() y update_server_status()
    
    print("📝 TODO: Implementar monitor secuencial")
    print("💡 Pistas:")
    print("   - for server in SERVERS:")
    print("   - is_healthy, response_time = simple_health_check(server)")
    print("   - update_server_status(server, is_healthy, response_time)")
    print("   - print_status()")
    
    # 🔧 SOLUCIÓN COMENTADA (para referencia del instructor):
    """
    for server in SERVERS:
        print(f"🔍 Checking {server}...")
        is_healthy, response_time = simple_health_check(server)
        update_server_status(server, is_healthy, response_time)
    
    print_status()
    """

def exercise_2_parallel_monitor():
    """
    🧪 EJERCICIO 2: Monitor paralelo con Threading
    
    TODO: Implementar usando ThreadPoolExecutor:
    1. Verificar todos los servidores en paralelo
    2. Usar ThreadPoolExecutor con max_workers=5
    3. Medir diferencia de tiempo vs secuencial
    
    ⏰ Tiempo estimado: 3 minutos
    """
    print("\n🧪 EJERCICIO 2: Monitor Paralelo con Threading")
    print("=" * 50)
    
    start_time = time.time()
    
    # TODO: Implementar aquí
    print("📝 TODO: Implementar monitor paralelo")
    print("💡 Pistas:")
    print("   - from concurrent.futures import ThreadPoolExecutor")
    print("   - with ThreadPoolExecutor(max_workers=5) as executor:")
    print("   - futures = [executor.submit(función, server) for server in SERVERS]")
    print("   - for future in as_completed(futures):")
    
    # 🔧 SOLUCIÓN COMENTADA:
    """
    def check_and_update(server):
        is_healthy, response_time = simple_health_check(server)
        update_server_status(server, is_healthy, response_time)
        return server, is_healthy, response_time
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_and_update, server) for server in SERVERS]
        
        for future in as_completed(futures):
            server, is_healthy, response_time = future.result()
            print(f"✅ {server}: {'UP' if is_healthy else 'DOWN'} ({response_time:.3f}s)")
    
    total_time = time.time() - start_time
    print(f"⏱️ Tiempo total: {total_time:.2f}s")
    print_status()
    """

def exercise_3_retry_logic():
    """
    🧪 EJERCICIO 3: Retry Logic + Circuit Breaker
    
    TODO: Implementar lógica de reintentos:
    1. Si un servidor falla, reintentarlo 3 veces
    2. Esperar 0.5s entre reintentos
    3. Si falla 3 veces seguidas, marcarlo como "CIRCUIT_OPEN"
    
    ⏰ Tiempo estimado: 4 minutos
    """
    print("\n🧪 EJERCICIO 3: Retry Logic + Circuit Breaker")
    print("=" * 50)
    
    # TODO: Implementar aquí
    print("📝 TODO: Implementar retry logic")
    print("💡 Pistas:")
    print("   - for attempt in range(3):")
    print("   - if is_healthy: break")
    print("   - time.sleep(0.5)  # Wait between retries")
    print("   - if not is_healthy after all attempts: 'CIRCUIT_OPEN'")
    
    # 🔧 SOLUCIÓN COMENTADA:
    """
    def health_check_with_retry(server, max_retries=3):
        for attempt in range(max_retries):
            is_healthy, response_time = simple_health_check(server)
            
            if is_healthy:
                return True, response_time, attempt + 1
            
            if attempt < max_retries - 1:  # No sleep on last attempt
                print(f"🔄 {server}: Retry {attempt + 1}/{max_retries}")
                time.sleep(0.5)
        
        return False, response_time, max_retries
    
    for server in SERVERS:
        print(f"🔍 Checking {server} with retry logic...")
        is_healthy, response_time, attempts = health_check_with_retry(server)
        
        if is_healthy:
            update_server_status(server, True, response_time)
            print(f"✅ {server}: UP (attempt {attempts})")
        else:
            # Circuit breaker logic
            server_status[server]["status"] = "CIRCUIT_OPEN"
            print(f"🔴 {server}: CIRCUIT_OPEN after {attempts} attempts")
    
    print_status()
    """

def exercise_4_continuous_monitoring():
    """
    🧪 EJERCICIO 4: Monitoreo Continuo
    
    TODO: Implementar monitoreo que corre cada 5 segundos:
    1. Usar threading para no bloquear
    2. Mostrar estado actualizado en tiempo real
    3. Permitir detener con Ctrl+C
    
    ⏰ Tiempo estimado: 2 minutos (opcional)
    """
    print("\n🧪 EJERCICIO 4: Monitoreo Continuo")
    print("=" * 50)
    
    # TODO: Implementar aquí
    print("📝 TODO: Implementar monitoreo continuo")
    print("💡 Pistas:")
    print("   - def monitor_loop():")
    print("   - while True:")
    print("   - time.sleep(5)")
    print("   - monitor_thread = threading.Thread(target=monitor_loop)")
    print("   - monitor_thread.daemon = True")
    
    # 🔧 SOLUCIÓN COMENTADA:
    """
    def monitor_loop():
        while True:
            print("\\n🔄 Ejecutando health check...")
            
            for server in SERVERS:
                is_healthy, response_time = simple_health_check(server)
                update_server_status(server, is_healthy, response_time)
            
            print_status()
            time.sleep(5)
    
    print("🚀 Iniciando monitoreo continuo (Ctrl+C para detener)...")
    
    monitor_thread = threading.Thread(target=monitor_loop)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n👋 Monitoreo detenido")
    """

# ============================================================================
# 🎓 MENU PARA EL EJERCICIO
# ============================================================================

def hands_on_menu():
    """🎓 Menu para ejercicios hands-on"""
    print("🏥 HEALTH MONITOR - Ejercicios Hands-on")
    print("🎯 Implementa monitoreo distribuido paso a paso")
    print("=" * 60)
    
    while True:
        print(f"\n🧪 ¿Qué ejercicio quieres hacer?")
        print(f"1. 🧪 Monitor básico secuencial")
        print(f"2. ⚡ Monitor paralelo (Threading)")
        print(f"3. 🔄 Retry logic + Circuit breaker")
        print(f"4. 🌊 Monitoreo continuo")
        print(f"5. 📊 Ver estado actual")
        print(f"0. ❌ Salir")
        
        choice = input(f"\n👉 Opción (0-5): ").strip()
        
        if choice == "1":
            exercise_1_basic_monitor()
        elif choice == "2":
            exercise_2_parallel_monitor()
        elif choice == "3":
            exercise_3_retry_logic()
        elif choice == "4":
            exercise_4_continuous_monitoring()
        elif choice == "5":
            print_status()
        elif choice == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

# ============================================================================
# 🏫 SOLUCIONES COMPLETAS (PARA EL INSTRUCTOR)
# ============================================================================

def instructor_solutions():
    """🏫 Soluciones completas para el instructor"""
    print("🏫 SOLUCIONES COMPLETAS - Solo para Instructor")
    print("=" * 60)
    
    # Implementaciones completas aquí...
    # (Las comentadas arriba pero ejecutables)
    
    pass

# ============================================================================
# 🚀 EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("🏥 HEALTH MONITOR - Ejercicio Distribuido")
    print("📋 INSTRUCCIONES:")
    print("   1. Asegúrate de tener servidores corriendo en 8001, 8002, 8003")
    print("   2. Implementa cada ejercicio paso a paso")
    print("   3. Pregunta al instructor si tienes dudas")
    print()
    
    hands_on_menu() 
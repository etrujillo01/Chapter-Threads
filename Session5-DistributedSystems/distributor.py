"""
🌐 Distributor - Load Balancer Simple

Este archivo demuestra cómo distribuir requests entre múltiples servidores.
Evolución de: Queue/Pipe → HTTP requests distribuidos

🎯 Uso en la demo:
1. Levantar 3 servidores Django en puertos 8001, 8002, 8003
2. Ejecutar este distributor para enviar requests balanceados
3. Mostrar cómo se distribuye la carga
"""

import requests
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional
import json

# 🌐 CONFIGURACIÓN DE SERVIDORES
SERVERS = [
    "http://localhost:8001",
    "http://localhost:8002", 
    "http://localhost:8003"
]

# 📊 ESTADÍSTICAS GLOBALES
stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'server_usage': {server: 0 for server in SERVERS}
}

# ============================================================================
# 🔄 ESTRATEGIAS DE LOAD BALANCING
# ============================================================================

class LoadBalancer:
    def __init__(self, servers: List[str]):
        self.servers = servers
        self.current_index = 0
        self.lock = threading.Lock()
    
    def round_robin(self) -> str:
        """🔄 Round Robin: Rotar entre servidores secuencialmente"""
        with self.lock:
            server = self.servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.servers)
            return server
    
    def random_choice(self) -> str:
        """🎲 Random: Elegir servidor al azar"""
        return random.choice(self.servers)
    
    def least_used(self) -> str:
        """📊 Least Used: Servidor con menos requests"""
        return min(self.servers, key=lambda s: stats['server_usage'][s])

# ============================================================================
# 🚀 FUNCIONES DE REQUEST
# ============================================================================

def make_request(server: str, endpoint: str = "/api/image/info/", timeout: int = 5) -> Tuple[str, bool, float, Optional[dict]]:
    """
    🌐 Hacer request HTTP a un servidor específico
    
    Returns:
        (server, success, response_time, response_data)
    """
    start_time = time.time()
    
    try:
        response = requests.get(f"{server}{endpoint}", timeout=timeout)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            stats['successful_requests'] += 1
            stats['server_usage'][server] += 1
            return server, True, response_time, response.json()
        else:
            stats['failed_requests'] += 1
            return server, False, response_time, {"error": f"Status {response.status_code}"}
            
    except requests.RequestException as e:
        response_time = time.time() - start_time
        stats['failed_requests'] += 1
        return server, False, response_time, {"error": str(e)}
    
    finally:
        stats['total_requests'] += 1

def health_check(server: str) -> bool:
    """🏥 Verificar si un servidor está disponible"""
    try:
        response = requests.get(f"{server}/", timeout=2)
        return response.status_code == 200
    except:
        return False

# ============================================================================
# 🎯 DEMOS PARA LA SESIÓN
# ============================================================================

def demo_basic_distribution():
    """🔥 DEMO 1: Distribución básica de requests"""
    print("\n" + "🔥" + "="*60)
    print("🔥 DEMO 1: Distribución Básica de Requests")
    print("="*60)
    
    lb = LoadBalancer(SERVERS)
    
    print("🌐 Enviando 10 requests con Round Robin...")
    
    for i in range(10):
        server = lb.round_robin()
        print(f"📤 Request {i+1} → {server}")
        
        server_result, success, response_time, data = make_request(server)
        
        if success:
            print(f"✅ {server_result}: {response_time:.3f}s - {data.get('status', 'OK')}")
        else:
            print(f"❌ {server_result}: {response_time:.3f}s - {data.get('error', 'Unknown error')}")
        
        time.sleep(0.5)  # Pausa para visualizar mejor

def demo_concurrent_requests():
    """⚡ DEMO 2: Requests concurrentes (Threading distribuido)"""
    print("\n" + "⚡" + "="*60) 
    print("⚡ DEMO 2: Requests Concurrentes - Threading Distribuido")
    print("="*60)
    
    lb = LoadBalancer(SERVERS)
    num_requests = 15
    
    print(f"🚀 Enviando {num_requests} requests concurrentes...")
    start_time = time.time()
    
    # 🧵 Usar ThreadPoolExecutor para concurrencia
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Preparar requests
        futures = []
        for i in range(num_requests):
            server = lb.round_robin()
            future = executor.submit(make_request, server, "/api/image/info/")
            futures.append((i+1, server, future))
        
        # Recoger resultados
        for request_id, server, future in futures:
            server_result, success, response_time, data = future.result()
            status = "✅" if success else "❌"
            print(f"{status} Request {request_id}: {server_result} → {response_time:.3f}s")
    
    total_time = time.time() - start_time
    print(f"\n⏱️ Total: {total_time:.2f}s para {num_requests} requests")
    print(f"🚀 Throughput: {num_requests/total_time:.1f} requests/segundo")

def demo_fault_tolerance():
    """💥 DEMO 3: Tolerancia a fallos"""
    print("\n" + "💥" + "="*60)
    print("💥 DEMO 3: Tolerancia a Fallos") 
    print("="*60)
    
    print("🔍 Verificando estado de servidores...")
    
    active_servers = []
    for server in SERVERS:
        is_healthy = health_check(server)
        status = "🟢 UP" if is_healthy else "🔴 DOWN"
        print(f"   {server}: {status}")
        
        if is_healthy:
            active_servers.append(server)
    
    print(f"\n📊 Servidores activos: {len(active_servers)}/{len(SERVERS)}")
    
    if active_servers:
        print(f"✅ Continuando con servidores disponibles: {active_servers}")
        
        # Hacer requests solo a servidores activos
        lb_healthy = LoadBalancer(active_servers)
        
        for i in range(5):
            server = lb_healthy.round_robin()
            server_result, success, response_time, data = make_request(server)
            status = "✅" if success else "❌"
            print(f"{status} Request {i+1}: {server_result} → {response_time:.3f}s")
            time.sleep(0.3)
    else:
        print("❌ ¡Todos los servidores están down! Sistema no disponible.")

def show_statistics():
    """📊 Mostrar estadísticas finales"""
    print("\n" + "📊" + "="*60)
    print("📊 ESTADÍSTICAS FINALES")
    print("="*60)
    
    print(f"📈 Total requests: {stats['total_requests']}")
    print(f"✅ Exitosos: {stats['successful_requests']}")
    print(f"❌ Fallidos: {stats['failed_requests']}")
    
    if stats['total_requests'] > 0:
        success_rate = (stats['successful_requests'] / stats['total_requests']) * 100
        print(f"🎯 Tasa de éxito: {success_rate:.1f}%")
    
    print(f"\n🌐 Uso por servidor:")
    for server, count in stats['server_usage'].items():
        percentage = (count / max(1, stats['successful_requests'])) * 100
        print(f"   {server}: {count} requests ({percentage:.1f}%)")

# ============================================================================
# 🎓 MENU INTERACTIVO PARA LA DEMO
# ============================================================================

def interactive_demo():
    """🎓 Menu interactivo para la sesión"""
    print("🌐 SISTEMA DISTRIBUIDO - Load Balancer Demo")
    print("🎯 Simula distribución de carga entre múltiples servidores")
    print("=" * 60)
    
    while True:
        print(f"\n🌐 ¿Qué demo quieres ejecutar?")
        print(f"1. 🔥 Distribución básica (Round Robin)")
        print(f"2. ⚡ Requests concurrentes (Threading)")
        print(f"3. 💥 Tolerancia a fallos") 
        print(f"4. 📊 Ver estadísticas")
        print(f"5. 🔄 Reset estadísticas")
        print(f"0. ❌ Salir")
        
        choice = input(f"\n👉 Opción (0-5): ").strip()
        
        if choice == "1":
            demo_basic_distribution()
        elif choice == "2":
            demo_concurrent_requests()
        elif choice == "3":
            demo_fault_tolerance()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            # Reset stats
            global stats
            stats = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'server_usage': {server: 0 for server in SERVERS}
            }
            print("🔄 Estadísticas reseteadas")
        elif choice == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

# ============================================================================
# 🚀 EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("🌐 INICIANDO LOAD BALANCER DISTRIBUIDO")
    print("📋 INSTRUCCIONES:")
    print("   1. Asegúrate de tener servidores corriendo en puertos 8001, 8002, 8003")
    print("   2. Comando: python manage.py runserver PUERTO (desde Projects)")
    print("   3. Ejemplo: python manage.py runserver 8001")
    print()
    
    # Verificar servidores antes de empezar
    print("🔍 Verificando servidores disponibles...")
    available_count = 0
    for server in SERVERS:
        is_healthy = health_check(server)
        status = "🟢" if is_healthy else "🔴"
        print(f"   {server}: {status}")
        if is_healthy:
            available_count += 1
    
    print(f"\n📊 Servidores disponibles: {available_count}/{len(SERVERS)}")
    
    if available_count == 0:
        print("❌ No hay servidores disponibles. Por favor:")
        print("   1. Ve a Chapter-Threads/Projects/")
        print("   2. Ejecuta: python manage.py runserver 8001")
        print("   3. En otra terminal: python manage.py runserver 8002")
        print("   4. En otra terminal: python manage.py runserver 8003")
    else:
        print("✅ Listo para demos!")
        interactive_demo() 
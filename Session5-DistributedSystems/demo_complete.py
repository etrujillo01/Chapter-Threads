"""
🎭 Demo Completo - Session 6: Sistemas Distribuidos

Este script ejecuta toda la sesión de forma automatizada.
Perfecto para instructores que quieren mostrar el flujo completo.

🎯 Uso:
python demo_complete.py  # Ejecuta todos los demos secuencialmente

📋 Incluye:
- Setup automático de servidores
- Demos de load balancing
- Health monitoring
- Cleanup automático
"""

import requests
import time
import threading
import subprocess
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# 🌐 CONFIGURACIÓN
SERVERS = ["http://localhost:8001", "http://localhost:8002", "http://localhost:8003"]
PORTS = [8001, 8002, 8003]
SESSION5_PATH = "../Projects"

# 📊 ESTADO GLOBAL
server_processes = []
demo_stats = {"requests": 0, "successes": 0, "failures": 0}

# ============================================================================
# 🚀 SETUP Y CLEANUP
# ============================================================================

def start_servers():
    """🚀 Iniciar servidores Django automáticamente"""
    print("🚀 INICIANDO SERVIDORES DISTRIBUIDOS")
    print("=" * 50)
    
    for port in PORTS:
        print(f"📡 Iniciando servidor en puerto {port}...")
        
        try:
            process = subprocess.Popen(
                ["python", "manage.py", "runserver", str(port)],
                cwd=SESSION5_PATH,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            server_processes.append(process)
            print(f"✅ Servidor {port}: PID {process.pid}")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error en puerto {port}: {e}")
    
    print(f"\n🌐 {len(server_processes)} servidores iniciados")
    
    # Verificar que están funcionando
    time.sleep(3)
    print("🔍 Verificando servidores...")
    
    for server in SERVERS:
        try:
            response = requests.get(server, timeout=2)
            status = "🟢 UP" if response.status_code == 200 else "🔴 DOWN"
            print(f"   {server}: {status}")
        except:
            print(f"   {server}: 🔴 DOWN")

def cleanup_servers():
    """🧹 Limpiar servidores al final"""
    print(f"\n🧹 LIMPIEZA: Deteniendo {len(server_processes)} servidores...")
    
    for process in server_processes:
        try:
            process.terminate()
        except:
            pass
    
    time.sleep(2)
    
    for process in server_processes:
        try:
            if process.poll() is None:
                process.kill()
        except:
            pass
    
    print("✅ Servidores detenidos")

def signal_handler(signum, frame):
    """📡 Manejar Ctrl+C"""
    print(f"\n📡 Interrupción detectada...")
    cleanup_servers()
    sys.exit(0)

# ============================================================================
# 🎯 DEMOS PRINCIPALES  
# ============================================================================

def demo_1_basic_distribution():
    """🔥 DEMO 1: Distribución básica de requests"""
    print("\n" + "🔥" + "="*60)
    print("🔥 DEMO 1: Distribución Básica - Round Robin")
    print("="*60)
    print("💡 Concepto: Rotar requests entre servidores")
    
    current_server = 0
    
    for i in range(6):
        server = SERVERS[current_server]
        print(f"\n📤 Request {i+1} → {server}")
        
        try:
            start_time = time.time()
            response = requests.get(f"{server}/api/image/info/", timeout=3)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {response_time:.3f}s - {data.get('status', 'OK')}")
                demo_stats['successes'] += 1
            else:
                print(f"❌ {response_time:.3f}s - Status {response.status_code}")
                demo_stats['failures'] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}...")
            demo_stats['failures'] += 1
        
        demo_stats['requests'] += 1
        current_server = (current_server + 1) % len(SERVERS)
        time.sleep(0.5)
    
    print(f"\n📊 Resultado Demo 1:")
    print(f"   Total: {demo_stats['requests']} requests")
    print(f"   Éxito: {demo_stats['successes']} | Fallos: {demo_stats['failures']}")

def demo_2_concurrent_distribution():
    """⚡ DEMO 2: Requests concurrentes con Threading"""
    print("\n" + "⚡" + "="*60)
    print("⚡ DEMO 2: Distribución Concurrente - Threading")
    print("="*60)
    print("💡 Concepto: ThreadPoolExecutor para requests paralelos")
    
    def make_request(server_index):
        server = SERVERS[server_index % len(SERVERS)]
        try:
            start_time = time.time()
            response = requests.get(f"{server}/api/image/info/", timeout=3)
            response_time = time.time() - start_time
            return server, True, response_time
        except:
            return server, False, time.time() - start_time
    
    print(f"🚀 Enviando 10 requests concurrentes...")
    start_total = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(10)]
        
        results = []
        for i, future in enumerate(futures):
            server, success, response_time = future.result()
            status = "✅" if success else "❌"
            print(f"{status} Request {i+1}: {server} → {response_time:.3f}s")
            results.append(success)
            
            if success:
                demo_stats['successes'] += 1
            else:
                demo_stats['failures'] += 1
            demo_stats['requests'] += 1
    
    total_time = time.time() - start_total
    success_rate = sum(results) / len(results) * 100
    
    print(f"\n📊 Resultado Demo 2:")
    print(f"   Tiempo total: {total_time:.2f}s para 10 requests")
    print(f"   Throughput: {10/total_time:.1f} requests/segundo")
    print(f"   Tasa éxito: {success_rate:.0f}%")

def demo_3_fault_tolerance():
    """💥 DEMO 3: Tolerancia a fallos"""
    print("\n" + "💥" + "="*60)
    print("💥 DEMO 3: Tolerancia a Fallos")
    print("="*60)
    print("💡 Concepto: Sistema sigue funcionando aunque fallen servidores")
    
    print("🔍 1. Verificando estado inicial...")
    healthy_servers = []
    
    for server in SERVERS:
        try:
            response = requests.get(server, timeout=2)
            if response.status_code == 200:
                healthy_servers.append(server)
                print(f"   {server}: 🟢 UP")
            else:
                print(f"   {server}: 🔴 DOWN")
        except:
            print(f"   {server}: 🔴 DOWN")
    
    print(f"\n📊 Servidores disponibles: {len(healthy_servers)}/{len(SERVERS)}")
    
    if len(healthy_servers) > 0:
        print(f"✅ Sistema operativo con {len(healthy_servers)} servidor(es)")
        
        print(f"\n🎯 2. Enviando requests solo a servidores activos...")
        for i in range(3):
            server = healthy_servers[i % len(healthy_servers)]
            try:
                start_time = time.time()
                response = requests.get(f"{server}/api/image/info/", timeout=2)
                response_time = time.time() - start_time
                print(f"✅ Request {i+1}: {server} → {response_time:.3f}s")
                demo_stats['successes'] += 1
            except:
                print(f"❌ Request {i+1}: {server} → Falló")
                demo_stats['failures'] += 1
            
            demo_stats['requests'] += 1
            time.sleep(0.3)
    else:
        print("❌ ¡Sistema completamente caído!")
    
    print(f"\n💡 LECCIÓN: Sistema distribuido continúa operando")
    print(f"    aunque fallen algunos componentes")

def demo_4_health_monitoring():
    """🏥 DEMO 4: Health Monitoring automático"""
    print("\n" + "🏥" + "="*60)
    print("🏥 DEMO 4: Health Monitoring Automático")
    print("="*60)
    print("💡 Concepto: Monitoreo continuo del estado del sistema")
    
    def check_health(server):
        try:
            start_time = time.time()
            response = requests.get(server, timeout=1)
            response_time = time.time() - start_time
            return server, response.status_code == 200, response_time
        except:
            return server, False, time.time() - start_time
    
    print("🔄 Ejecutando health check paralelo...")
    
    with ThreadPoolExecutor(max_workers=len(SERVERS)) as executor:
        futures = [executor.submit(check_health, server) for server in SERVERS]
        
        results = []
        for future in futures:
            server, is_healthy, response_time = future.result()
            status = "🟢 UP" if is_healthy else "🔴 DOWN"
            print(f"   {server}: {status} ({response_time:.3f}s)")
            results.append(is_healthy)
    
    healthy_count = sum(results)
    health_percentage = (healthy_count / len(SERVERS)) * 100
    
    print(f"\n📊 Estado del Sistema:")
    print(f"   Salud general: {health_percentage:.0f}%")
    print(f"   Servidores UP: {healthy_count}/{len(SERVERS)}")
    
    if health_percentage >= 66:
        print(f"✅ Sistema SALUDABLE")
    elif health_percentage >= 33:
        print(f"⚠️ Sistema DEGRADADO")
    else:
        print(f"❌ Sistema EN RIESGO")

# ============================================================================
# 🎓 RESUMEN Y LECCIONES
# ============================================================================

def show_final_summary():
    """📊 Mostrar resumen final de la sesión"""
    print("\n" + "🎓" + "="*60)
    print("🎓 RESUMEN FINAL - Sistemas Distribuidos")
    print("="*60)
    
    print(f"📊 ESTADÍSTICAS TOTALES:")
    print(f"   Total requests: {demo_stats['requests']}")
    print(f"   Exitosos: {demo_stats['successes']}")
    print(f"   Fallidos: {demo_stats['failures']}")
    
    if demo_stats['requests'] > 0:
        success_rate = (demo_stats['successes'] / demo_stats['requests']) * 100
        print(f"   Tasa de éxito: {success_rate:.1f}%")
    
    print(f"\n🌟 CONCEPTOS APRENDIDOS:")
    print(f"✅ Load Balancing: Distribución de carga")
    print(f"✅ Threading: Para requests HTTP paralelos")
    print(f"✅ Fault Tolerance: Resistencia a fallos")
    print(f"✅ Health Monitoring: Supervisión automática")
    
    print(f"\n🔄 EVOLUCIÓN DE CONCEPTOS:")
    print(f"   Queue            → HTTP requests")
    print(f"   Pipe             → REST APIs")
    print(f"   Shared Memory    → Distributed databases")
    print(f"   threading.Lock   → Distributed locks")
    
    print(f"\n🚀 SIGUIENTES PASOS:")
    print(f"   - Message Queues (Redis/RabbitMQ)")
    print(f"   - Container Orchestration (Docker/K8s)")
    print(f"   - Microservices Architecture")
    print(f"   - Distributed Monitoring (Prometheus)")

# ============================================================================
# 🎭 EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    """🎭 Demo completo de la sesión"""
    print("🎭 DEMO COMPLETO: Session 6 - Sistemas Distribuidos")
    print("🎯 Duración estimada: 45 minutos")
    print("📋 Prerequisito: Projects funcionando")
    print("=" * 70)
    
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # 1. Setup automático
        start_servers()
        
        input("\n⏸️ Presiona ENTER para continuar con Demo 1...")
        
        # 2. Demos secuenciales
        demo_1_basic_distribution()
        
        input("\n⏸️ Presiona ENTER para continuar con Demo 2...")
        demo_2_concurrent_distribution()
        
        input("\n⏸️ Presiona ENTER para continuar con Demo 3...")
        demo_3_fault_tolerance()
        
        input("\n⏸️ Presiona ENTER para continuar con Demo 4...")
        demo_4_health_monitoring()
        
        # 3. Resumen final
        show_final_summary()
        
        print(f"\n🎉 ¡DEMO COMPLETO FINALIZADO!")
        print(f"💡 Los estudiantes ahora pueden trabajar en health_monitor.py")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Demo interrumpido por el usuario")
    
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
    
    finally:
        cleanup_servers()

if __name__ == "__main__":
    main() 
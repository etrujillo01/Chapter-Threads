"""
🚀 Start Servers - Script auxiliar para demos

Levanta múltiples servidores Django automáticamente.
Útil para preparar la demo rápidamente.

🎯 Uso:
python start_servers.py  # Levanta 3 servidores en puertos 8001, 8002, 8003
"""

import subprocess
import time
import os
import signal
import sys
from pathlib import Path

# 📋 CONFIGURACIÓN
PORTS = [8001, 8002, 8003]
SESSION5_PATH = "../Projects"

# 📊 PROCESOS ACTIVOS
processes = []

def start_django_server(port: int):
    """🚀 Iniciar servidor Django en un puerto específico"""
    print(f"🚀 Iniciando servidor en puerto {port}...")
    
    try:
        # Cambiar al directorio de Projects
        cmd = [
            "python", "manage.py", "runserver", str(port)
        ]
        
        process = subprocess.Popen(
            cmd,
            cwd=SESSION5_PATH,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        processes.append(process)
        print(f"✅ Servidor {port}: PID {process.pid}")
        return process
        
    except Exception as e:
        print(f"❌ Error iniciando servidor {port}: {e}")
        return None

def check_session5_exists():
    """🔍 Verificar que existe Projects"""
    session5_full_path = Path(__file__).parent / SESSION5_PATH
    
    if not session5_full_path.exists():
        print(f"❌ No se encuentra {SESSION5_PATH}")
        print(f"   Ruta buscada: {session5_full_path.absolute()}")
        print(f"   Por favor ejecuta desde Session5-DistributedSystems/")
        return False
    
    manage_py = session5_full_path / "manage.py"
    if not manage_py.exists():
        print(f"❌ No se encuentra manage.py en {session5_full_path}")
        return False
    
    print(f"✅ Projects encontrado: {session5_full_path.absolute()}")
    return True

def stop_all_servers():
    """🛑 Detener todos los servidores"""
    print(f"\n🛑 Deteniendo {len(processes)} servidores...")
    
    for process in processes:
        try:
            process.terminate()
            print(f"🛑 Detenido PID {process.pid}")
        except:
            pass
    
    # Esperar que terminen
    time.sleep(2)
    
    # Force kill si es necesario
    for process in processes:
        try:
            if process.poll() is None:  # Still running
                process.kill()
                print(f"💀 Force killed PID {process.pid}")
        except:
            pass

def signal_handler(signum, frame):
    """📡 Manejar Ctrl+C"""
    print(f"\n📡 Señal recibida: {signum}")
    stop_all_servers()
    sys.exit(0)

def main():
    """🎯 Función principal"""
    print("🚀 START SERVERS - Helper para Demo Distribuido")
    print("=" * 60)
    
    # Verificar pre-requisitos
    if not check_session5_exists():
        return
    
    # Configurar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Iniciar servidores
    print(f"\n🚀 Iniciando {len(PORTS)} servidores Django...")
    
    for port in PORTS:
        process = start_django_server(port)
        if process:
            time.sleep(1)  # Esperar entre inicios
    
    print(f"\n✅ {len(processes)} servidores iniciados!")
    print(f"🌐 URLs disponibles:")
    for port in PORTS:
        print(f"   http://localhost:{port}/")
    
    print(f"\n🎯 Ahora puedes ejecutar:")
    print(f"   python distributor.py")
    print(f"   python health_monitor.py")
    
    print(f"\n⏰ Servidores corriendo... (Ctrl+C para detener)")
    
    # Mantener vivo
    try:
        while True:
            time.sleep(1)
            
            # Verificar que los procesos siguen vivos
            alive_count = 0
            for process in processes:
                if process.poll() is None:
                    alive_count += 1
            
            if alive_count == 0:
                print("❌ Todos los servidores han terminado")
                break
                
    except KeyboardInterrupt:
        pass
    finally:
        stop_all_servers()

if __name__ == "__main__":
    main() 
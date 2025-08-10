"""
⚠️ DEMOSTRACIÓN SIMPLE: ¿Qué ves al imprimir estos objetos?

Este archivo muestra de manera simple qué pasa cuando imprimes:
- Threads
- Objetos async sin await  
- Objetos de IPC
"""

import threading
import asyncio
import time
from multiprocessing import Queue, Pipe, Array, Value, Manager

# ============================================================================
# 🧵 ¿QUÉ PASA AL IMPRIMIR UN THREAD?
# ============================================================================

def demo_thread_objects():
    """Demostrar qué se ve al imprimir Thread objects"""
    print("🧵" + "="*60)
    print("🧵 ¿QUÉ PASA AL IMPRIMIR UN THREAD?")
    print("="*60)
    
    def dummy_work():
        time.sleep(0.5)
        return "trabajo completado"
    
    # Crear thread
    thread = threading.Thread(target=dummy_work)
    
    print("📊 Estados del Thread:")
    print(f"   🔍 Antes de start(): {thread}")
    print(f"   🔍 Tipo: {type(thread)}")
    print(f"   🔍 ¿Está vivo? {thread.is_alive()}")
    print(f"   🔍 Name: {thread.name}")
    
    # Iniciar
    thread.start()
    print(f"\n   🔍 Después de start(): {thread}")
    print(f"   🔍 ¿Está vivo? {thread.is_alive()}")
    
    # Esperar
    thread.join()
    print(f"\n   🔍 Después de join(): {thread}")
    print(f"   🔍 ¿Está vivo? {thread.is_alive()}")
    
    print("\n💡 OBSERVACIONES:")
    print("   ❌ NO ves el resultado del trabajo")
    print("   ❌ Solo ves metadata: <Thread(name, state)>")
    print("   ✅ Estados: initial → started → stopped")

# ============================================================================
# ⚡ ¿QUÉ PASA CON ASYNC SIN AWAIT?
# ============================================================================

async def demo_async_objects():
    """Demostrar objetos async sin await"""
    print("\n⚡" + "="*60)
    print("⚡ ¿QUÉ PASA CON ASYNC SIN AWAIT?")
    print("="*60)
    
    async def async_worker():
        await asyncio.sleep(0.5)
        return "¡Resultado asíncrono!"
    
    print("📊 Comparación:")
    
    # Sin await - crea corrutina pero no ejecuta
    coroutine_obj = async_worker()
    print(f"   🔍 Sin await: {coroutine_obj}")
    print(f"   🔍 Tipo: {type(coroutine_obj)}")
    print("   ❌ ¡Es <coroutine object>, NO el resultado!")
    
    # Cerrar para evitar warnings
    coroutine_obj.close()
    
    # Con await - ejecuta y devuelve resultado
    result = await async_worker()
    print(f"\n   🔍 Con await: {result}")
    print(f"   🔍 Tipo: {type(result)}")
    print("   ✅ ¡Ahora SÍ es el resultado!")
    
    print("\n💡 OBSERVACIONES:")
    print("   ❌ Sin await: <coroutine object at 0x...>")
    print("   ✅ Con await: resultado real")

# ============================================================================
# 🔄 ¿QUÉ PASA AL IMPRIMIR OBJETOS IPC?
# ============================================================================

def demo_ipc_objects():
    """Demostrar objetos IPC vs su contenido"""
    print("\n🔄" + "="*60)
    print("🔄 ¿QUÉ PASA AL IMPRIMIR OBJETOS IPC?")
    print("="*60)
    
    print("📊 OBJETOS vs CONTENIDO:")
    
    # Queue
    queue = Queue()
    print(f"\n🔄 QUEUE:")
    print(f"   🔍 Objeto: {queue}")
    print(f"   🔍 Tipo: {type(queue)}")
    print("   💡 Es el 'contenedor', no los datos")
    
    # Pipe  
    parent_conn, child_conn = Pipe()
    print(f"\n📞 PIPE:")
    print(f"   🔍 Parent: {parent_conn}")
    print(f"   🔍 Child: {child_conn}")
    print("   💡 Son 'conexiones', no mensajes")
    
    # Shared Memory
    shared_array = Array('i', [10, 20, 30])
    shared_value = Value('i', 42)
    print(f"\n💾 SHARED MEMORY:")
    print(f"   🔍 Array object: {shared_array}")
    print(f"   🔍 Value object: {shared_value}")
    print(f"   ✅ Array CONTENT: {list(shared_array[:])}")
    print(f"   ✅ Value CONTENT: {shared_value.value}")
    
    # Manager
    manager = Manager()
    shared_list = manager.list([1, 2, 3])
    shared_dict = manager.dict({'key': 'value'})
    print(f"\n🗂️ MANAGER:")
    print(f"   🔍 Manager: {manager}")
    print(f"   🔍 List object: {shared_list}")
    print(f"   🔍 Dict object: {shared_dict}")
    print(f"   ✅ List CONTENT: {list(shared_list)}")
    print(f"   ✅ Dict CONTENT: {dict(shared_dict)}")
    
    print("\n💡 OBSERVACIONES:")
    print("   ❌ Objetos IPC son 'wrappers'")
    print("   ✅ Para datos: .value, [:], list(), dict()")
    
    # Cleanup
    parent_conn.close()
    child_conn.close()
    manager.shutdown()

# ============================================================================
# 🎯 COMPARACIÓN LADO A LADO
# ============================================================================

def demo_objects_vs_results():
    """Mostrar la diferencia entre objetos y resultados"""
    print("\n🎯" + "="*60)
    print("🎯 OBJETOS vs RESULTADOS - COMPARACIÓN")
    print("="*60)
    
    print("📦 LO QUE VES AL IMPRIMIR:")
    print("-"*35)
    
    # Thread
    thread = threading.Thread(target=lambda: time.sleep(0.1))
    print(f"Thread:        {thread}")
    
    # Queue
    queue = Queue()
    print(f"Queue:         {queue}")
    
    # Shared Memory
    shared_val = Value('i', 123)
    print(f"Value object:  {shared_val}")
    print(f"Value CONTENT: {shared_val.value}")
    
    # Array
    shared_arr = Array('i', [1, 2, 3])
    print(f"Array object:  {shared_arr}")
    print(f"Array CONTENT: {list(shared_arr[:])}")
    
    print("\n🔑 LA CLAVE:")
    print("   📦 Objects = Herramientas/Contenedores")
    print("   📊 Content = Datos reales que necesitas")
    print("   🎯 Debes saber CÓMO acceder al contenido")

# ============================================================================
# 🚫 ERRORES TÍPICOS
# ============================================================================

def demo_common_errors():
    """Mostrar errores comunes y malentendidos"""
    print("\n🚫" + "="*60)
    print("🚫 ERRORES COMUNES")
    print("="*60)
    
    print("❌ ERROR 1: Esperar resultado directo")
    print("   BAD:  result = threading.Thread(target=func)")
    print("   GOOD: Usar Queue para obtener resultado")
    
    print("\n❌ ERROR 2: Imprimir objeto en lugar de contenido")
    print("   BAD:  print(shared_array)     # <SynchronizedArray...>")
    print("   GOOD: print(shared_array[:])  # [1, 2, 3]")
    
    print("\n❌ ERROR 3: Async sin await")
    print("   BAD:  result = async_func()   # <coroutine object>")
    print("   GOOD: result = await async_func()  # resultado real")
    
    print("\n❌ ERROR 4: Confundir wrapper con contenido")
    print("   BAD:  Pensar que el objeto ES el dato")
    print("   GOOD: Entender que el objeto CONTIENE el dato")
    
    print("\n✅ REGLA DE ORO:")
    print("   🎯 Objects ≠ Results")
    print("   🎯 Siempre pregúntate: ¿Es el objeto o su contenido?")

# ============================================================================
# 🎪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

def main():
    """Ejecutar todas las demostraciones"""
    print("⚠️" + "="*70)
    print("⚠️ ¿QUÉ VES AL IMPRIMIR ESTOS OBJETOS?")
    print("="*70)
    
    # Threading
    demo_thread_objects()
    
    # IPC Objects
    demo_ipc_objects()
    
    # Comparación
    demo_objects_vs_results()
    
    # Errores comunes
    demo_common_errors()
    
    print("\n🎓" + "="*60)
    print("🎓 LECCIÓN APRENDIDA")
    print("="*60)
    print("💡 PRINCIPAL:")
    print("   🎯 Al imprimir objetos NO ves resultados")
    print("   🎯 Ves metadata, referencias, o wrappers")
    print("   🎯 Para datos reales necesitas métodos específicos")
    print("\n🔑 MÉTODOS PARA ACCEDER A DATOS:")
    print("   📊 Shared Array: array[:]")
    print("   📊 Shared Value: value.value")
    print("   📊 Manager List: list(shared_list)")
    print("   📊 Async: await coroutine()")
    print("\n✅ ¡Ahora sabes qué esperar!")

if __name__ == "__main__":
    # Ejecutar demos síncronas
    main()
    
    # Ejecutar demo async
    print("\n⚡ EJECUTANDO DEMO ASYNC...")
    asyncio.run(demo_async_objects()) 
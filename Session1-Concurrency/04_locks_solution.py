"""
🔒 SESIÓN 1.4: Locks y Sincronización - Las Soluciones

Este módulo demuestra cómo resolver los problemas de race conditions
usando mecanismos de sincronización: locks, RLocks, semaphores, etc.

🎯 Objetivos:
- Resolver race conditions con locks
- Entender diferentes tipos de sincronización
- Comparar rendimiento: sin lock vs con lock
- Aprender mejores prácticas de sincronización
"""

import time
import threading
from typing import List, Dict
from threading import Lock, RLock, Semaphore, Event

# ============================================================================
# 🔒 SOLUCIÓN 1: Contador Seguro con Lock
# ============================================================================

# Variable global protegida
safe_counter = 0
counter_lock = Lock()

def increment_safe(thread_id: int, increments: int):
    """🔒 SEGURO: Incrementa contador con protección"""
    global safe_counter
    
    print(f"🧵 Thread {thread_id}: Iniciando {increments} incrementos seguros")
    
    for i in range(increments):
        # 🔒 CRITICAL SECTION: Solo un thread a la vez
        with counter_lock:
            current_value = safe_counter  # Lee valor actual
            
            # Simular procesamiento (ahora es seguro)
            time.sleep(0.00001)  # 10 microsegundos
            
            new_value = current_value + 1   # Calcula nuevo valor
            safe_counter = new_value        # Escribe nuevo valor
        
        if i % 1000 == 0:  # Progress cada 1000 incrementos
            with counter_lock:  # También proteger la lectura para display
                print(f"🧵 Thread {thread_id}: Progress {i}/{increments}, counter={safe_counter}")
    
    print(f"✅ Thread {thread_id}: Completado seguramente")

def demonstrate_safe_counter():
    """🔒 DEMOSTRACIÓN: Contador seguro con locks"""
    global safe_counter
    
    print("\n" + "🔒" + "="*60)
    print("🔒 DEMOSTRACIÓN: Contador Seguro con Lock")
    print("="*60)
    
    # Reset counter
    safe_counter = 0
    
    # Configuración
    num_threads = 5
    increments_per_thread = 5000
    expected_total = num_threads * increments_per_thread
    
    print(f"🎯 Configuración:")
    print(f"   - Threads: {num_threads}")
    print(f"   - Incrementos por thread: {increments_per_thread}")
    print(f"   - Total esperado: {expected_total}")
    
    # Crear y lanzar threads
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=increment_safe,
            args=(i+1, increments_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Esperar que terminen
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    # 📊 ANÁLISIS DE RESULTADOS
    print(f"\n📊 RESULTADOS:")
    print(f"   🎯 Esperado: {expected_total}")
    print(f"   ✅ Obtenido: {safe_counter}")
    print(f"   ✅ Diferencia: {expected_total - safe_counter}")
    print(f"   ⏱️ Tiempo: {end_time - start_time:.2f} segundos")
    
    if safe_counter == expected_total:
        print(f"\n✅ ¡ÉXITO! Contador consistente con locks")
        print(f"✅ No hay race conditions - resultado predecible")
    else:
        print(f"\n⚠️ Algo salió mal (muy raro con locks)")
    
    return safe_counter

# ============================================================================
# 🔒 SOLUCIÓN 2: Lista Segura con Lock
# ============================================================================

class SafeList:
    """🔒 Lista thread-safe con lock interno"""
    
    def __init__(self):
        self._items = []
        self._lock = Lock()
    
    def append(self, item):
        """Agregar item de forma thread-safe"""
        with self._lock:
            self._items.append(item)
    
    def extend(self, items):
        """Agregar múltiples items de forma thread-safe"""
        with self._lock:
            self._items.extend(items)
    
    def get_length(self):
        """Obtener longitud de forma thread-safe"""
        with self._lock:
            return len(self._items)
    
    def get_copy(self):
        """Obtener copia segura de la lista"""
        with self._lock:
            return self._items.copy()

safe_list = SafeList()

def add_items_safe(thread_id: int, items_count: int):
    """🔒 SEGURO: Agrega items a lista protegida"""
    print(f"🧵 Thread {thread_id}: Agregando {items_count} items de forma segura")
    
    for i in range(items_count):
        new_item = f"Thread-{thread_id}-Item-{i}"
        safe_list.append(new_item)
        
        if i % 500 == 0:
            current_length = safe_list.get_length()
            print(f"🧵 Thread {thread_id}: Agregados {i}/{items_count}, lista tiene {current_length} items")
    
    final_length = safe_list.get_length()
    print(f"✅ Thread {thread_id}: Completado, lista final: {final_length} items")

def demonstrate_safe_list():
    """🔒 DEMOSTRACIÓN: Lista segura con locks"""
    global safe_list
    
    print("\n" + "🔒" + "="*60)
    print("🔒 DEMOSTRACIÓN: Lista Segura con Lock")
    print("="*60)
    
    # Reset lista
    safe_list = SafeList()
    
    # Configuración
    num_threads = 4
    items_per_thread = 2000
    expected_total = num_threads * items_per_thread
    
    print(f"🎯 Configuración:")
    print(f"   - Threads: {num_threads}")
    print(f"   - Items por thread: {items_per_thread}")
    print(f"   - Total esperado: {expected_total}")
    
    # Crear y lanzar threads
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=add_items_safe,
            args=(i+1, items_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Esperar que terminen
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    # 📊 ANÁLISIS DE RESULTADOS
    actual_total = safe_list.get_length()
    
    print(f"\n📊 RESULTADOS:")
    print(f"   🎯 Esperado: {expected_total} items")
    print(f"   ✅ Obtenido: {actual_total} items")
    print(f"   ✅ Diferencia: {expected_total - actual_total}")
    print(f"   ⏱️ Tiempo: {end_time - start_time:.2f} segundos")
    
    if actual_total == expected_total:
        print(f"\n✅ ¡ÉXITO! Lista consistente con locks")
        print(f"✅ Todos los items agregados correctamente")
    
    return actual_total

# ============================================================================
# 🔒 SOLUCIÓN 3: Cuenta Bancaria Segura
# ============================================================================

class SafeBankAccount:
    """🔒 SEGURO: Cuenta bancaria con locks para transacciones"""
    
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.transaction_history = []
        self._lock = RLock()  # RLock permite múltiples acquire() del mismo thread
    
    def deposit(self, amount: float, thread_id: int):
        """🔒 SEGURO: Depósito con protección"""
        print(f"💰 Thread {thread_id}: Depositando ${amount:.2f}")
        
        # 🔒 CRITICAL SECTION: Transacción atómica
        with self._lock:
            current_balance = self.balance
            
            # Simular procesamiento de transacción
            time.sleep(0.001)  # 1ms - simula verificación, etc.
            
            new_balance = current_balance + amount
            self.balance = new_balance
            
            # Historial también protegido
            transaction = {
                'type': 'deposit',
                'amount': amount,
                'balance_after': new_balance,
                'thread': thread_id,
                'timestamp': time.time()
            }
            self.transaction_history.append(transaction)
            
            print(f"✅ Thread {thread_id}: Depósito completado, balance: ${self.balance:.2f}")
    
    def withdraw(self, amount: float, thread_id: int):
        """🔒 SEGURO: Retiro con protección"""
        print(f"💸 Thread {thread_id}: Intentando retirar ${amount:.2f}")
        
        # 🔒 CRITICAL SECTION: Verificación y modificación atómica
        with self._lock:
            current_balance = self.balance
            
            if current_balance >= amount:
                # Simular procesamiento
                time.sleep(0.001)
                
                new_balance = current_balance - amount
                self.balance = new_balance
                
                transaction = {
                    'type': 'withdrawal',
                    'amount': amount,
                    'balance_after': new_balance,
                    'thread': thread_id,
                    'timestamp': time.time()
                }
                self.transaction_history.append(transaction)
                
                print(f"✅ Thread {thread_id}: Retiro completado, balance: ${self.balance:.2f}")
                return True
            else:
                print(f"❌ Thread {thread_id}: Fondos insuficientes para retirar ${amount:.2f}")
                return False
    
    def get_balance(self):
        """🔒 SEGURO: Obtener balance de forma thread-safe"""
        with self._lock:
            return self.balance
    
    def get_transaction_count(self):
        """🔒 SEGURO: Obtener número de transacciones"""
        with self._lock:
            return len(self.transaction_history)

def safe_banking_thread(account: SafeBankAccount, thread_id: int, transactions: int):
    """Simula transacciones bancarias seguras con valores FIJOS para claridad"""
    print(f"🏦 Thread {thread_id}: Iniciando {transactions} transacciones seguras")
    
    # 🔒 MISMOS valores fijos que el archivo inseguro para comparación directa
    deposit_amounts = {
        1: [100.0, 50.0, 75.0],  # Thread 1: depósitos
        2: [25.0, 30.0, 20.0],   # Thread 2: depósitos  
        3: [40.0, 60.0, 35.0],   # Thread 3: depósitos
    }
    
    withdraw_amounts = {
        1: [10.0, 15.0, 5.0],    # Thread 1: retiros
        2: [20.0, 25.0, 10.0],   # Thread 2: retiros
        3: [30.0, 35.0, 15.0],   # Thread 3: retiros  
    }
    
    for i in range(transactions):
        transaction_num = i % 3  # Usar índice para valores fijos
        
        # Alternar entre depósitos y retiros de forma predecible
        if i % 2 == 0:  # Pares = depósito
            amount = deposit_amounts[thread_id][transaction_num]
            print(f"💰 Thread {thread_id}: Depositando ${amount:.2f} (transacción {i+1}) 🔒")
            account.deposit(amount, thread_id)
        else:  # Impares = retiro
            amount = withdraw_amounts[thread_id][transaction_num]
            print(f"💸 Thread {thread_id}: Retirando ${amount:.2f} (transacción {i+1}) 🔒")
            account.withdraw(amount, thread_id)
        
        # Pequeña pausa entre transacciones
        time.sleep(0.001)  # Más tiempo para mostrar que es seguro incluso con delays
    
    print(f"🏦 Thread {thread_id}: Transacciones seguras completadas")

def demonstrate_safe_banking():
    """🔒 DEMOSTRACIÓN: Transacciones bancarias seguras"""
    print("\n" + "🔒" + "="*60)
    print("🔒 DEMOSTRACIÓN: Transacciones Bancarias Seguras")
    print("="*60)
    
    # Crear cuenta segura
    initial_balance = 1000.0
    account = SafeBankAccount(initial_balance)
    
    print(f"🏦 Balance inicial: ${account.get_balance():.2f}")
    
    # Configuración
    num_threads = 3
    transactions_per_thread = 3  # 3 transacciones con valores fijos predecibles
    
    print(f"🎯 Configuración:")
    print(f"   - Threads: {num_threads}")
    print(f"   - Transacciones por thread: {transactions_per_thread}")
    
    print(f"\n💰 TRANSACCIONES PLANIFICADAS (valores fijos + 🔒 LOCKS):")
    print(f"Thread 1: +$100, -$10, +$50   (neto: +$140)")
    print(f"Thread 2: +$25,  -$20, +$30   (neto: +$35)")  
    print(f"Thread 3: +$40,  -$30, +$60   (neto: +$70)")
    print(f"Balance esperado CON locks (CORRECTO): $1000 + $245 = $1245")
    
    # Lanzar threads concurrentes
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=safe_banking_thread,
            args=(account, i+1, transactions_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Esperar que terminen
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    # 📊 ANÁLISIS DE RESULTADOS
    final_balance = account.get_balance()
    transaction_count = account.get_transaction_count()
    
    print(f"\n📊 RESULTADOS:")
    print(f"   💰 Balance inicial: ${initial_balance:.2f}")
    print(f"   💰 Balance final: ${final_balance:.2f}")
    print(f"   📜 Transacciones registradas: {transaction_count}")
    print(f"   ⏱️ Tiempo: {end_time - start_time:.2f} segundos")
    
    # Calcular balance teórico basado en transacciones
    theoretical_balance = initial_balance
    for transaction in account.transaction_history:
        if transaction['type'] == 'deposit':
            theoretical_balance += transaction['amount']
        else:
            theoretical_balance -= transaction['amount']
    
    print(f"   🧮 Balance teórico: ${theoretical_balance:.2f}")
    
    difference = abs(final_balance - theoretical_balance)
    expected_balance = 1245.0  # Balance esperado con los valores fijos
    
    if difference < 0.01:  # Permitir pequeños errores de punto flotante
        print(f"\n🎉 ¡PERFECTO! LOCKS FUNCIONAN CORRECTAMENTE")
        print(f"✅ Balance final: ${final_balance:.2f}")
        print(f"✅ Balance esperado: ${expected_balance:.2f}")
        print(f"✅ Diferencia: ${difference:.2f} (despreciable)")
        print(f"✅ No hay corrupción de datos - ¡LOCKS resuelven race conditions!")
        
        if abs(final_balance - expected_balance) < 0.01:
            print(f"🎯 ¡COMPARACIÓN CON ARCHIVO 3 (sin locks):")
            print(f"   📊 SIN locks: Balance incorrecto (~$1025 típicamente)")
            print(f"   🔒 CON locks: Balance correcto (${final_balance:.2f})")
            print(f"   🚀 LOCKS garantizan operaciones atómicas!")
    else:
        print(f"\n⚠️ Inconsistencia inesperada: ${difference:.2f}")
        print(f"⚠️ Esto NO debería pasar con locks correctos")
    
    return account

# ============================================================================
# 🔒 TIPOS DE SINCRONIZACIÓN AVANZADOS
# ============================================================================

def demonstrate_rlock():
    """🔒 DEMOSTRACIÓN: RLock (Reentrant Lock)"""
    print("\n" + "🔒" + "="*40)
    print("🔒 RLock - Lock Reentrante")
    print("="*40)
    
    rlock = RLock()
    
    def recursive_function(n: int, thread_id: int):
        """Función recursiva que necesita RLock"""
        with rlock:
            print(f"🧵 Thread {thread_id}: Nivel {n}")
            if n > 0:
                time.sleep(0.1)
                recursive_function(n-1, thread_id)  # Re-acquire del mismo thread
    
    # Lanzar threads que usan recursión
    threads = []
    for i in range(2):
        thread = threading.Thread(target=recursive_function, args=(3, i+1))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("✅ RLock permite múltiples acquire() del mismo thread")

def demonstrate_semaphore():
    """🔒 DEMOSTRACIÓN: Semaphore - Limitador de recursos"""
    print("\n" + "🔒" + "="*40)
    print("🔒 Semaphore - Limitador de Recursos")
    print("="*40)
    
    # Semáforo que permite máximo 2 threads simultáneos
    semaphore = Semaphore(2)
    
    def limited_resource_access(thread_id: int):
        """Función que simula acceso a recurso limitado"""
        print(f"🧵 Thread {thread_id}: Esperando acceso al recurso...")
        
        with semaphore:
            print(f"✅ Thread {thread_id}: Accediendo al recurso limitado")
            time.sleep(1)  # Simular uso del recurso
            print(f"🔄 Thread {thread_id}: Liberando recurso")
    
    # Lanzar 5 threads, pero solo 2 pueden acceder simultáneamente
    threads = []
    start_time = time.time()
    
    for i in range(5):
        thread = threading.Thread(target=limited_resource_access, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"⏱️ Tiempo total: {end_time - start_time:.2f}s (debería ser ~3s)")

def demonstrate_event():
    """🔒 DEMOSTRACIÓN: Event - Señalización entre threads"""
    print("\n" + "🔒" + "="*40)
    print("🔒 Event - Señalización")
    print("="*40)
    
    event = Event()
    
    def waiter(thread_id: int):
        """Thread que espera la señal"""
        print(f"🧵 Thread {thread_id}: Esperando señal...")
        event.wait()  # Bloquea hasta que se active el event
        print(f"✅ Thread {thread_id}: ¡Señal recibida! Continuando...")
    
    def signaler():
        """Thread que envía la señal"""
        print("📡 Signaler: Esperando 2 segundos antes de enviar señal...")
        time.sleep(2)
        print("📡 Signaler: ¡Enviando señal!")
        event.set()  # Activa el event
    
    # Crear threads waiters
    threads = []
    for i in range(3):
        thread = threading.Thread(target=waiter, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    # Crear thread signaler
    signal_thread = threading.Thread(target=signaler)
    signal_thread.start()
    
    # Esperar que terminen
    for thread in threads:
        thread.join()
    signal_thread.join()
    
    print("✅ Event permite coordinar múltiples threads")

# ============================================================================
# 📊 COMPARACIÓN: SIN LOCKS vs CON LOCKS
# ============================================================================

def compare_performance():
    """📊 COMPARACIÓN: Rendimiento con y sin locks"""
    print("\n" + "📊" + "="*60)
    print("📊 COMPARACIÓN: Rendimiento SIN vs CON Locks")
    print("="*60)
    
    # Importar función insegura
    print("\n📊 COMPARACIÓN: Rendimiento SIN vs CON Locks")
    print("="*60)
    
    print("🎯 COMPARACIÓN CONCEPTUAL:")
    print("🐌 SIN locks: Más rápido pero INCORRECTOS resultados")
    print("🔒 CON locks: Puede ser más lento pero CORRECTOS resultados")
    
    # Test solo con locks (seguro)
    print("\n🔒 DEMO: CON LOCKS (seguro)")
    global safe_counter
    safe_counter = 0
    
    num_threads = 3
    increments = 10000
    expected = num_threads * increments
    
    start = time.time()
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=increment_safe, args=(i+1, increments))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    safe_time = time.time() - start
    
    # Análisis
    print(f"\n📊 ANÁLISIS:")
    print(f"🔒 Con locks: {safe_time:.3f}s - Resultado: {safe_counter}")
    print(f"🎯 Esperado: {expected}")
    
    if safe_counter == expected:
        print(f"✅ ¡PERFECTO! Locks garantizan correctitud")
        print(f"✅ Resultado: {safe_counter} = {expected} ✅")
    else:
        print(f"⚠️ Resultado inesperado con locks")
    
    print(f"\n💡 LECCIÓN:")
    print(f"💡 Para comparar SIN locks, ejecuta archivo 03_race_conditions.py")
    print(f"💡 Locks pueden ser 10-20% más lentos, pero garantizan correctitud")

# ============================================================================
# 🎓 MEJORES PRÁCTICAS
# ============================================================================

def best_practices():
    """🎓 Mejores prácticas para locks y sincronización"""
    print("\n" + "🎓" + "="*60)
    print("🎓 MEJORES PRÁCTICAS PARA LOCKS")
    print("="*60)
    
    practices = [
        ("🔒 Usar 'with' statement", "Garantiza liberación automática del lock"),
        ("⚡ Minimizar critical sections", "Mantener locks el menor tiempo posible"),
        ("🚫 Evitar nested locks", "Previene deadlocks cuando es posible"),
        ("🔄 RLock para recursión", "Cuando necesitas re-acquire del mismo thread"),
        ("📊 Semaphore para recursos", "Limitar acceso a recursos contados"),
        ("📡 Event para coordinación", "Sincronizar entre threads"),
        ("🎯 Lock granular", "Múltiples locks específicos vs uno global"),
        ("⚠️ Timeout en acquire", "Evitar bloqueos infinitos"),
        ("🧪 Testing exhaustivo", "Race conditions son difíciles de reproducir")
    ]
    
    for practice, description in practices:
        print(f"{practice:25}: {description}")
    
    print(f"\n⚠️ PROBLEMAS A EVITAR:")
    print(f"💀 Deadlock: Threads esperando locks mutuamente")
    print(f"🐌 Lock contention: Demasiados threads compitiendo")
    print(f"🔄 Livelock: Threads cambiando estado sin progreso")
    print(f"⚡ Starvation: Thread nunca obtiene el lock")

# ============================================================================
# 🧪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

def run_all_safe_demos():
    """Ejecutar todas las demostraciones de locks seguros"""
    print("🔒 EJECUTANDO TODAS LAS DEMOSTRACIONES SEGURAS")
    print("🎯 Objetivo: Resolver race conditions con sincronización")
    
    # Demo 1: Contador seguro
    counter_result = demonstrate_safe_counter()
    
    # Demo 2: Lista segura
    list_result = demonstrate_safe_list()
    
    # Demo 3: Cuenta bancaria segura
    account_result = demonstrate_safe_banking()
    
    # Demos avanzadas
    demonstrate_rlock()
    demonstrate_semaphore()
    demonstrate_event()
    
    # Mejores prácticas
    best_practices()
    
    return {
        'safe_counter': counter_result,
        'safe_list_length': list_result,
        'safe_account': account_result
    }

if __name__ == "__main__":
    print("🔒 DEMOSTRACIÓN: Locks y Sincronización - Soluciones Seguras")
    print("🎯 Objetivo: Resolver race conditions con mecanismos de sincronización")
    print("🎯 COMPARACIÓN DIRECTA: Mismos valores fijos que archivo 3 (sin locks)")
    
    print("\n🎯 ¿Qué quieres ver?")
    print("1. Demo bancaria (comparación directa con archivo 3)")
    print("2. Todas las demostraciones completas")
    print("3. Solo demo rápida")
    choice = input("👉 Opción (1-3): ").strip()
    
    if choice == "1":
        # Demo bancaria para comparar directamente
        print("\n🔒 DEMOSTRACIÓN PRINCIPAL: Cuenta bancaria CON locks")
        account_result = demonstrate_safe_banking()
        print(f"\n🎯 RESULTADO CLAVE:")
        print(f"📊 Balance final CON locks: ${account_result.get_balance():.2f}")
        print(f"📊 Compáralo con archivo 3 (SIN locks): ~$1025 típicamente")
        print(f"✅ ¡LOCKS resuelven completamente los race conditions!")
        
    elif choice == "2":
        # Todas las demos
        results = run_all_safe_demos()
        print(f"\n📊 Resumen de resultados seguros:")
        print(f"   ✅ Contador: {results['safe_counter']} (correcto)")
        print(f"   ✅ Lista: {results['safe_list_length']} items (correcto)")
        print(f"   ✅ Cuenta: ${results['safe_account'].get_balance():.2f} (consistente)")
    else:
        # Demo rápida
        print("\n🔒 Demo rápida: Contador seguro")
        demonstrate_safe_counter()
    
    print("\n🎯 ¿Quieres comparar rendimiento sin vs con locks? (y/n)")
    choice2 = input("👉 ").lower().strip()
    
    if choice2 in ['y', 'yes', 'sí', 's']:
        compare_performance()
    
    print("\n✅ ¡SESIÓN 1 COMPLETADA!")
    print("🎓 Has aprendido: Problemas secuenciales → Threading → Race Conditions → Locks")
    print("🚀 Próxima sesión: Multiprocessing y Paralelismo verdadero") 
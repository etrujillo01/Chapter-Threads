"""
⚠️ SESIÓN 1.3: Race Conditions - Los Peligros de la Concurrencia

Este módulo demuestra los problemas que surgen cuando múltiples threads
acceden a recursos compartidos sin sincronización adecuada.

🎯 Objetivos:
- Entender qué son las race conditions
- Ver ejemplos prácticos de data corruption
- Identificar problemas de concurrencia
- Preparar para soluciones con locks
"""

import time
import threading
from typing import List

# ============================================================================
# ⚠️ PROBLEMA 1: Contador Global Sin Protección
# ============================================================================

# Variable global compartida (¡PELIGRO!)
unsafe_counter = 0

def increment_unsafe(thread_id: int, increments: int):
    """⚠️ PELIGROSO: Incrementa contador sin protección"""
    global unsafe_counter
    
    print(f"🧵 Thread {thread_id}: Iniciando {increments} incrementos")
    
    for i in range(increments):
        # ⚠️ RACE CONDITION: Multiple threads leyendo/escribiendo la misma variable
        current_value = unsafe_counter  # Lee valor actual
        
        # Simular algo de procesamiento (hace el problema más visible)
        time.sleep(0.00001)  # 10 microsegundos
        
        new_value = current_value + 1   # Calcula nuevo valor
        unsafe_counter = new_value      # Escribe nuevo valor
        
        if i % 1000 == 0:  # Progress cada 1000 incrementos
            print(f"🧵 Thread {thread_id}: Progress {i}/{increments}, counter={unsafe_counter}")
    
    print(f"✅ Thread {thread_id}: Completado")

def demonstrate_race_condition():
    """⚠️ DEMOSTRACIÓN: Race condition en acción"""
    global unsafe_counter
    
    print("\n" + "⚠️ " + "="*60)
    print("⚠️ DEMOSTRACIÓN: Race Condition - Contador Inseguro")
    print("="*60)
    
    # Reset counter
    unsafe_counter = 0
    
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
            target=increment_unsafe,
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
    print(f"   💥 Obtenido: {unsafe_counter}")
    print(f"   ❌ Diferencia: {expected_total - unsafe_counter}")
    print(f"   ⏱️ Tiempo: {end_time - start_time:.2f} segundos")
    
    if unsafe_counter != expected_total:
        print(f"\n⚠️ ¡RACE CONDITION DETECTADA!")
        print(f"⚠️ Se perdieron {expected_total - unsafe_counter} incrementos")
        print(f"⚠️ Esto ocurre cuando threads interfieren entre sí")
    else:
        print(f"\n🤔 No se detectó race condition en esta ejecución")
        print(f"🤔 (Puede ocurrir por casualidad - ejecuta varias veces)")
    
    return unsafe_counter

# ============================================================================
# ⚠️ PROBLEMA 2: Lista Compartida Sin Protección
# ============================================================================

# ⚠️ Variable global compartida (PELIGROSA)
shared_list = []

def add_items_unsafe(thread_id: int, items_count: int):
    global shared_list
    
    for i in range(items_count):
        # ⚠️ RACE CONDITION: "Read-Copy-Replace" EXTREMADAMENTE peligroso
        
        # STEP 1: Read current list (snapshot)
        current_snapshot = shared_list[:]  # Create copy
        current_length = len(current_snapshot)
        
        # STEP 2: Vulnerability window - otros threads pueden modificar shared_list
        time.sleep(0.0001)  # Critical section sin protección
        
        # STEP 3: Modify the copy (basado en snapshot "stale")
        new_item = f"Thread-{thread_id}-Item-{i}"
        current_snapshot.append(new_item)
        
        # STEP 4: Replace entire list with modified copy (DANGEROUS!)
        # ¡Si otro thread modificó shared_list, esos cambios se pierden!
        shared_list = current_snapshot  # 💥 DESTRUCTIVE WRITE
        
        if i % 500 == 0:
            print(f"🧵 Thread {thread_id}: Agregados {i}/{items_count}, lista tiene {len(shared_list)} items")
    
    print(f"✅ Thread {thread_id}: Completado, lista final: {len(shared_list)} items")

def demonstrate_list_race_condition():
    """⚠️ DEMOSTRACIÓN: Race condition con lista compartida"""
    global shared_list
    
    print("\n" + "⚠️ " + "="*60)
    print("⚠️ DEMOSTRACIÓN: Race Condition - Lista Compartida")
    print("="*60)
    
    # Reset lista
    shared_list = []
    
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
            target=add_items_unsafe,
            args=(i+1, items_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Esperar que terminen
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    # 📊 ANÁLISIS DE RESULTADOS
    actual_total = len(shared_list)
    
    print(f"\n📊 RESULTADOS:")
    print(f"   🎯 Esperado: {expected_total} items")
    print(f"   💥 Obtenido: {actual_total} items")
    print(f"   ❌ Diferencia: {expected_total - actual_total}")
    print(f"   ⏱️ Tiempo: {end_time - start_time:.2f} segundos")
    
    if actual_total != expected_total:
        print(f"\n⚠️ ¡RACE CONDITION EN LISTA DETECTADA!")
        print(f"⚠️ Posible corrupción de datos o items perdidos")
    
    return actual_total

# ============================================================================
# ⚠️ PROBLEMA 3: Cuenta Bancaria Insegura
# ============================================================================

class UnsafeBankAccount:
    """⚠️ PELIGROSO: Cuenta bancaria sin protección para transacciones"""
    
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.transaction_history = []
    
    def deposit(self, amount: float, thread_id: int):
        """⚠️ PELIGROSO: Depósito sin protección"""
        print(f"💰 Thread {thread_id}: Depositando ${amount}")
        
        # ⚠️ RACE CONDITION: Lectura y escritura no atómica
        current_balance = self.balance
        
        # Simular procesamiento de transacción
        time.sleep(0.001)  # 1ms - simula verificación, etc.
        
        new_balance = current_balance + amount
        self.balance = new_balance
        
        # ⚠️ RACE CONDITION: Lista también sin protección
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
        """⚠️ PELIGROSO: Retiro sin protección"""
        print(f"💸 Thread {thread_id}: Retirando ${amount}")
        
        # ⚠️ RACE CONDITION: Verificación y modificación no atómica
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
        else:
            print(f"❌ Thread {thread_id}: Fondos insuficientes para retirar ${amount}")

def banking_thread(account: UnsafeBankAccount, thread_id: int, transactions: int):
    """Simula transacciones bancarias concurrentes con valores FIJOS para claridad"""
    print(f"🏦 Thread {thread_id}: Iniciando {transactions} transacciones")
    
    # Valores fijos predecibles por thread
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
            print(f"💰 Thread {thread_id}: Depositando ${amount:.2f} (transacción {i+1})")
            account.deposit(amount, thread_id)
        else:  # Impares = retiro
            amount = withdraw_amounts[thread_id][transaction_num]
            print(f"💸 Thread {thread_id}: Retirando ${amount:.2f} (transacción {i+1})")
            account.withdraw(amount, thread_id)
        
        # Pequeña pausa entre transacciones
        time.sleep(0.001)  # Más tiempo para hacer race condition más visible
    
    print(f"🏦 Thread {thread_id}: Transacciones completadas")

def demonstrate_banking_race_condition():
    """⚠️ DEMOSTRACIÓN: Race condition en transacciones bancarias"""
    print("\n" + "⚠️ " + "="*60)
    print("⚠️ DEMOSTRACIÓN: Race Condition - Transacciones Bancarias")
    print("="*60)
    
    # Crear cuenta
    initial_balance = 1000.0
    account = UnsafeBankAccount(initial_balance)
    
    print(f"🏦 Balance inicial: ${account.balance:.2f}")
    
    # Configuración
    num_threads = 3
    transactions_per_thread = 3  # 3 transacciones con valores fijos predecibles
    
    print(f"🎯 Configuración:")
    print(f"   - Threads: {num_threads}")
    print(f"   - Transacciones por thread: {transactions_per_thread}")
    
    print(f"\n💰 TRANSACCIONES PLANIFICADAS (valores fijos):")
    print(f"Thread 1: +$100, -$10, +$50   (neto: +$140)")
    print(f"Thread 2: +$25,  -$20, +$30   (neto: +$35)")  
    print(f"Thread 3: +$40,  -$30, +$60   (neto: +$70)")
    print(f"Balance esperado SIN race conditions: $1000 + $245 = $1245")
    
    # Lanzar threads concurrentes
    threads = []
    start_time = time.time()
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=banking_thread,
            args=(account, i+1, transactions_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Esperar que terminen
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    
    # 📊 ANÁLISIS DE RESULTADOS
    print(f"\n📊 RESULTADOS:")
    print(f"   💰 Balance inicial: ${initial_balance:.2f}")
    print(f"   💰 Balance final: ${account.balance:.2f}")
    print(f"   📜 Transacciones registradas: {len(account.transaction_history)}")
    print(f"   ⏱️ Tiempo: {end_time - start_time:.2f} segundos")
    
    # Calcular balance teórico basado en transacciones
    theoretical_balance = initial_balance
    for transaction in account.transaction_history:
        if transaction['type'] == 'deposit':
            theoretical_balance += transaction['amount']
        else:
            theoretical_balance -= transaction['amount']
    
    print(f"   🧮 Balance teórico: ${theoretical_balance:.2f}")
    
    difference = abs(account.balance - theoretical_balance)
    if difference > 0.01:  # Permitir pequeños errores de punto flotante
        print(f"\n⚠️ ¡INCONSISTENCIA DETECTADA!")
        print(f"⚠️ Diferencia: ${difference:.2f}")
        print(f"⚠️ Posible corrupción por race conditions")
    else:
        print(f"\n✅ Balance consistente (por casualidad)")
    
    return account

# ============================================================================
# 🎓 CONCEPTOS Y CAUSAS DE RACE CONDITIONS
# ============================================================================

def explain_race_conditions():
    """Explicar qué son las race conditions y por qué ocurren"""
    print("\n" + "🎓" + "="*60)
    print("🎓 ENTENDIENDO LAS RACE CONDITIONS")
    print("="*60)
    
    explanations = [
        ("¿Qué es una Race Condition?", 
         "Cuando el resultado depende del timing impredecible de threads"),
        
        ("¿Por qué ocurren?", 
         "Operaciones no-atómicas en recursos compartidos"),
        
        ("Read-Modify-Write", 
         "Secuencia vulnerable: leer → modificar → escribir"),
        
        ("Context Switching", 
         "El OS puede cambiar de thread en cualquier momento"),
        
        ("Visibilidad de Memoria", 
         "Cambios de un thread pueden no ser visibles inmediatamente"),
        
        ("Lost Updates", 
         "Modificaciones se pierden cuando threads sobrescriben"),
        
        ("Data Corruption", 
         "Estructuras de datos quedan en estado inconsistente"),
        
        ("Non-Deterministic", 
         "Resultado diferente en cada ejecución")
    ]
    
    for concept, explanation in explanations:
        print(f"💡 {concept:20}: {explanation}")
    
    print(f"\n🚨 SIGNOS DE RACE CONDITIONS:")
    print(f"❌ Resultados diferentes en cada ejecución")
    print(f"❌ Datos 'perdidos' o incorrectos")
    print(f"❌ Inconsistencias en estructuras de datos")
    print(f"❌ Comportamiento impredecible")
    print(f"❌ Errores que aparecen/desaparecen")
    
    print(f"\n💡 PRÓXIMA SOLUCIÓN: ¡LOCKS y SINCRONIZACIÓN!")

# ============================================================================
# 🧪 EJECUTAR TODAS LAS DEMOSTRACIONES
# ============================================================================

def run_all_race_condition_demos():
    """Ejecutar todas las demostraciones de race conditions"""
    print("⚠️ EJECUTANDO TODAS LAS DEMOSTRACIONES DE RACE CONDITIONS")
    print("🎯 Objetivo: Ver problemas antes de aprender soluciones")
    
    # Demo 1: Contador
    counter_result = demonstrate_race_condition()
    
    # Demo 2: Lista
    list_result = demonstrate_list_race_condition()
    
    # Demo 3: Cuenta bancaria
    account_result = demonstrate_banking_race_condition()
    
    # Explicación
    explain_race_conditions()
    
    return {
        'counter': counter_result,
        'list_length': list_result,
        'account': account_result
    }

if __name__ == "__main__":
    print("⚠️ DEMOSTRACIÓN: Race Conditions y Problemas de Concurrencia")
    print("🎯 IMPORTANTE: Estos son ejemplos de lo que NO debes hacer")
    
    print("\n🤔 ¿Quieres ver todas las demostraciones? (y/n)")
    choice = input("👉 ").lower().strip()
    
    if choice in ['y', 'yes', 'sí', 's']:
        results = run_all_race_condition_demos()
        print(f"\n📊 Resumen de problemas encontrados:")
        print(f"   - Contador: {results['counter']} (puede estar incorrecto)")
        print(f"   - Lista: {results['list_length']} items (puede estar incorrecto)")
        print(f"   - Cuenta: ${results['account'].balance:.2f} (puede estar inconsistente)")
    else:
        # Solo una demo rápida
        print("\n⚠️ Demo rápida: Contador inseguro")
        demonstrate_race_condition()
    
    print("\n⚠️ Estos problemas son REALES en aplicaciones de producción")
    print("💡 La solución: Sincronización con LOCKS")
    print("🚀 Próximo paso: 04_locks_solution.py") 
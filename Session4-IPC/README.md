# 🔄 SESIÓN 4: Comunicación entre procesos (IPC)

## 📋 Descripción
Esta sesión cubre Inter-Process Communication (IPC) y métodos avanzados de comunicación entre procesos en Python.

## 🎯 Contenido

### **🔧 Métodos de IPC Cubiertos:**
1. **🔄 Queue** - Comunicación segura Producer-Consumer
2. **📞 Pipe** - Comunicación bidireccional entre 2 procesos  
3. **💾 Shared Memory** - Memoria compartida de alta performance
4. **🚦 Event** - Sincronización y coordinación entre procesos
5. **🗂️ Manager** - Objetos compartidos inteligentes (listas, dicts)

### **📊 Comparación de Métodos:**

| **Método** | **Facilidad** | **Velocidad** | **Uso Principal** |
|------------|---------------|---------------|-------------------|
| **🔄 Queue** | 🟢 Fácil | 🟡 Media | Producer-Consumer |
| **📞 Pipe** | 🟡 Media | 🟢 Rápida | 2 procesos directos |
| **💾 Shared Memory** | 🔴 Complejo | 🟢 MUY Rápida | Arrays grandes |
| **🚦 Event** | 🟢 Fácil | 🟢 Rápida | Sincronización |
| **🗂️ Manager** | 🟢 MUY Fácil | 🟡 Media | Objetos complejos |

---

## 💡 **DIFERENCIAS CLAVE: Shared Memory vs Manager**

### **🎯 ¿SON LO MISMO? ¡NO!**

Ambos comparten memoria, pero son **fundamentalmente diferentes**:

### **💾 SHARED MEMORY = Pizarra Compartida**
- **🔧 Concepto**: Memoria RAW compartida directamente
- **⚡ Velocidad**: **MUY Rápida** - acceso directo sin serialización
- **🧠 Facilidad**: **Complejo** - necesitas manejar locks manualmente
- **📦 Tipos**: Solo **tipos básicos** (int, float, arrays)
- **🔒 Sincronización**: **Manual** - tienes que usar locks

```python
# Ejemplo Shared Memory
shared_array = Array('i', [0, 0, 0])      # Solo enteros
shared_value = Value('d', 3.14)           # Solo double

with lock:                                 # Lock manual
    shared_array[0] = 42                   # Acceso directo a memoria
```

### **🗂️ MANAGER = Secretaria Inteligente**
- **🎯 Concepto**: Objetos de alto nivel compartidos
- **🟡 Velocidad**: **Media** - serialización en cada acceso
- **😊 Facilidad**: **MUY Fácil** - como objetos normales de Python
- **📦 Tipos**: **Cualquier objeto** Python (listas, dicts, objetos personalizados)
- **✅ Sincronización**: **Automática** - thread-safe incluido

```python
# Ejemplo Manager
shared_list = manager.list([1, "texto", {'key': 'value'}])
shared_dict = manager.dict({'config': 'value'})

shared_list.append({'nuevo': 'objeto'})   # ¡Como lista normal!
```

### **📊 Comparación Rápida:**

| **Aspecto** | **💾 Shared Memory** | **🗂️ Manager** |
|-------------|----------------------|----------------|
| **⚡ Velocidad** | **MUY Rápida** | **Media** |
| **🧠 Facilidad** | **Complejo** | **MUY Fácil** |
| **🔒 Sincronización** | **Manual (locks)** | **Automática** |
| **📦 Tipos** | **Básicos solamente** | **Cualquier objeto** |
| **🔧 Acceso** | **Directo a memoria** | **Proxy objects** |

### **🎯 Cuándo usar cada uno:**

#### **💾 USA SHARED MEMORY cuando:**
- ✅ Necesitas **velocidad máxima**
- ✅ Tienes **datos simples** (números, arrays)
- ✅ **Acceso muy frecuente** a los mismos datos
- ✅ No te importa la **complejidad adicional**

**📝 Ejemplos**: Procesamiento de imágenes, cálculos matemáticos, simulaciones

#### **🗂️ USA MANAGER cuando:**
- ✅ Quieres **simplicidad** y facilidad de uso
- ✅ Tienes **objetos complejos** (listas, diccionarios)
- ✅ Estás **prototipando** rápidamente
- ✅ La velocidad **no es crítica**

**📝 Ejemplos**: Colectar resultados, configuración compartida, estados complejos

---

## 📦 **TIPOS DE DATOS EN IPC**

### **✅ DATOS QUE SÍ se pueden enviar:**

#### **🟢 Tipos Básicos:**
```python
queue.put("texto string")
queue.put(42)               # enteros
queue.put(3.14159)          # floats  
queue.put(True)             # booleanos
queue.put(None)             # None
```

#### **🟢 Estructuras de Datos:**
```python
queue.put([1, 2, 3, 4])                    # listas
queue.put({"key": "value", "num": 42})     # diccionarios
queue.put((1, "tuple", 3.14))              # tuplas
queue.put({1, 2, 3})                       # sets
```

#### **🟢 Objetos Complejos:**
```python
import datetime
queue.put(datetime.datetime.now())         # objetos datetime

# Objetos personalizados (serializables)
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

queue.put(Task("mi_tarea", "high"))        # objetos personalizados
```

#### **🟢 Estructuras Anidadas:**
```python
complex_data = {
    'metadata': {
        'created': datetime.datetime.now(),
        'priority': 'high'
    },
    'tasks': [
        {'id': 1, 'action': 'process_file'},
        {'id': 2, 'action': 'send_email'}
    ],
    'numbers': [1, 2, 3, 4, 5]
}
queue.put(complex_data)                    # estructuras complejas
```

### **❌ DATOS QUE NO se pueden enviar:**

#### **🔴 Funciones y Métodos:**
```python
def mi_funcion():
    return "hello"

queue.put(mi_funcion)                      # ❌ Error!
queue.put(lambda x: x * 2)                # ❌ Error!
```

#### **🔴 Objetos con Estado Externo:**
```python
# Archivos abiertos
with open("file.txt") as f:
    queue.put(f)                           # ❌ Error!

# Conexiones de red
import socket
s = socket.socket()
queue.put(s)                               # ❌ Error!

# Threads o procesos
import threading
t = threading.Thread(target=some_func)
queue.put(t)                               # ❌ Error!
```

#### **🔴 Objetos No Serializables:**
```python
# Generadores
def my_generator():
    yield 1
    yield 2

queue.put(my_generator())                  # ❌ Error!

# Objetos con __slots__ complejos
class ComplexObject:
    __slots__ = ['_internal_state']
    def __init__(self):
        self._internal_state = SomeUnpicklableObject()

queue.put(ComplexObject())                 # ❌ Puede fallar!
```

---

## 🔧 **CÓMO FUNCIONA INTERNAMENTE:**

```python
import pickle

# PASO 1: queue.put() serializa datos
original_data = {"task": "process_file", "id": 123}
serialized = pickle.dumps(original_data)  # bytes

# PASO 2: Los bytes se envían entre procesos

# PASO 3: queue.get() deserializa datos  
received_data = pickle.loads(serialized)  # dict otra vez

# ✅ Mismo contenido, diferente objeto en memoria
print(original_data == received_data)     # True
print(id(original_data) == id(received_data))  # False
```

---

## 💡 **CONSEJOS PRÁCTICOS:**

### **✅ MEJORES PRÁCTICAS:**
- **Usa diccionarios** para estructurar tus datos
- **Incluye metadatos** (timestamps, IDs, prioridades)
- **Serializa datos simples** cuando sea posible
- **Envía señales de control** (None para "terminé")

### **⚠️ EVITA:**
- **Objetos muy grandes** (usa Shared Memory instead)
- **Funciones** (envía nombres de función como strings)
- **Estados complejos** (simplifica antes de enviar)
- **Referencias circulares** (pueden causar problemas)

### **🎯 EJEMPLO TÍPICO:**
```python
# ✅ BUEN diseño de mensaje
task = {
    'type': 'process_image',
    'input_file': '/path/to/image.jpg',
    'operations': ['resize', 'compress'],
    'params': {'width': 800, 'quality': 85},
    'priority': 'normal',
    'created_at': time.time(),
    'worker_id': os.getpid()
}
queue.put(task)
```

---

## 📁 Archivos

- `01_process_communication.py` - Demostración completa de todos los métodos IPC
- `objects_vs_results_demo.py` - ¿Qué ves al imprimir threads, async y objetos IPC?

## 🚀 Ejecución

```bash
# Demostración completa de IPC
python 01_process_communication.py

# Ver qué pasa al imprimir objetos (threads, async, IPC)
python objects_vs_results_demo.py
```

## 🚀 Estado
✅ **Completado** - Todos los métodos IPC principales implementados y documentados.

---

## 🎯 **ARCHIVO EDUCATIVO ADICIONAL:**

### **`objects_vs_results_demo.py`** 
Este archivo resuelve una **confusión muy común**: ¿Por qué al imprimir ciertos objetos no veo lo que espero?

**🔍 Demuestra:**
- **🧵 Threads**: Estados (initial → started → stopped), no resultados
- **⚡ Async**: Diferencia entre `<coroutine object>` y resultado real
- **🔄 IPC Objects**: Wrappers vs contenido real
- **🚫 Errores comunes** y cómo evitarlos

**💡 Aprendes:**
- `Objects ≠ Results` (regla de oro)
- Cómo acceder al contenido real (`array[:]`, `value.value`, `await`)
- Por qué necesitas métodos específicos para cada tipo

**🎓 Ideal para:** Principiantes que se confunden al ver `<Thread object>` o `<coroutine object>` en lugar de sus datos.

---
**Nota**: Este contenido corresponde a la **Sesión 4** del temario de 7 sesiones.
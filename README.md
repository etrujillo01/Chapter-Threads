# 🧵 Chapter-Threads: Concurrencia y Paralelismo en Python

## 📋 Descripción General

Este capítulo cubre **concurrencia y paralelismo en Python** con un enfoque práctico y progresivo. Los estudiantes aprenderán desde los problemas de la ejecución secuencial hasta las soluciones avanzadas de multiprocessing.

**⏱️ Duración Principal**: 1.5 horas (2 sesiones de 45 minutos)  
**⏱️ Duración Completa**: 4+ horas (4 sesiones disponibles + futuras)  
**🎯 Nivel**: Intermedio a Avanzado  
**🔧 Lenguaje**: Python 3.7+

## 🎯 Objetivos del Capítulo

Al completar este capítulo, los estudiantes podrán:

1. **Distinguir I/O-bound vs CPU-bound** operaciones (concepto fundamental)
2. **Identificar problemas** de rendimiento en código secuencial
3. **Implementar concurrencia** con threading para I/O-bound
4. **Resolver race conditions** con sincronización
5. **Entender verdadero vs falso paralelismo** y el rol del GIL
6. **Lograr paralelismo real** con multiprocessing para CPU-bound
7. **Decidir cuándo usar** cada enfoque según el tipo de operación

## 📚 Estructura del Capítulo

### 🧵 Sesión 1: Hilos y Concurrencia (45 min)
**Enfoque**: Threading, race conditions y sincronización

| Archivo | Duración | Concepto |
|---------|----------|----------|
| `01_sequential_problem.py` | 10 min | 🐌 Problemas del código secuencial |
| `02_basic_threading.py` | 15 min | 🧵 Threading básico y ThreadPool |
| `03_race_conditions.py` | 10 min | ⚠️ Race conditions y sus peligros |
| `04_locks_solution.py` | 10 min | 🔒 Locks y sincronización |

### 🔥 Sesión 2: Multiprocesamiento y Paralelismo (45 min)
**Enfoque**: Multiprocessing y verdadero paralelismo

| Archivo | Duración | Concepto |
|---------|----------|----------|
| `01_gil_limitations.py` | 20 min | 🔒 Limitaciones del GIL para CPU-bound |
| `02_multiprocessing_basics.py` | 25 min | 🚀 Multiprocessing + Comparación completa |

**Nota**: El archivo 2 incluye comparación I/O-bound vs CPU-bound para evitar redundancia.

### 📋 Sesiones Futuras (Separadas por tema)

| Sesión | Enfoque | Estado |
|---------|---------|---------|
| **Session3-Async/** | ⚡ async/await y asyncio | ✅ **Completado** |
| **Session4-IPC/** | 🔄 Comunicación entre procesos | ✅ **Completado** |
| **Projects/** | 🚀 Proyectos prácticos | ✅ Completo |
| **Session5-DistributedSystems/** | 🌐 Sistemas distribuidos | ✅ **Completado** |

**Nota**: Las **sesiones 1-2 son el núcleo** del temario (obligatorio). Las **sesiones 3-4 son extensiones** avanzadas (opcional).

## 🚀 Inicio Rápido

### Pre-requisitos
```bash
# Instalar dependencias
pip install requests

# Opcional para ejemplos async
pip install aiohttp
```

### Ejecutar por sesiones
```bash
# Sesión 1: Concurrencia
cd Chapter-Threads/Session1-Concurrency/
python 01_sequential_problem.py
python 02_basic_threading.py
python 03_race_conditions.py
python 04_locks_solution.py

# Sesión 2: Paralelismo
cd ../Session2-Parallelism/
python 01_gil_limitations.py
python 02_multiprocessing_basics.py

# Sesión 3: Async/Await (Opcional - Avanzado)
cd ../Session3-Async/
python async_complete_guide.py

# Sesión 4: IPC - Comunicación entre Procesos (Opcional - Avanzado)
cd ../Session4-IPC/
python 01_process_communication.py
python objects_vs_results_demo.py
```

## 📊 Progresión del Aprendizaje

```
🐌 Secuencial         → 🧵 Threading        → 🔒 Sincronización
    ↓                       ↓                     ↓
Bloqueos en I/O      Concurrencia         Race Conditions
Uso de 1 core        mejor para I/O       Necesita Locks
                          ↓                     ↓
                    🔥 Multiprocessing  → ⚖️ Decisión
                          ↓                     ↓
                    Verdadero           Cuándo usar
                    Paralelismo         cada uno
```

## 💡 Conceptos Clave

### 🧵 Concurrencia vs Paralelismo

#### **Definiciones básicas:**
- **Concurrencia**: Múltiples tareas progresando **alternativamente**
- **Paralelismo**: Múltiples tareas ejecutándose **simultáneamente**

#### **🔍 VERDADERO vs FALSO Paralelismo:**

**✅ VERDADERO PARALELISMO (Multiprocessing):**
```
CPU Core 1: Process 1 ████████████████ (trabajando)
CPU Core 2: Process 2 ████████████████ (trabajando)  
CPU Core 3: Process 3 ████████████████ (trabajando)
CPU Core 4: Process 4 ████████████████ (trabajando)
↑ LITERALMENTE AL MISMO TIEMPO
```

**❌ FALSO PARALELISMO (Threading con GIL):**
```
1 CPU Core: Thread 1████░░░░████░░░░ (alternando)
           Thread 2 ░░░░████░░░░████ (alternando)
           Thread 3 ░░░░░░░░████░░░░ (alternando)
↑ PARECE simultáneo, pero es SECUENCIAL disfrazado
```

#### **🎯 La diferencia clave:**
- **Threading**: "4 personas, 1 calculadora" → Se turnan
- **Multiprocessing**: "4 personas, 4 calculadoras" → Trabajan juntas

## 🎯 I/O-bound vs CPU-bound - CONCEPTOS FUNDAMENTALES

### **🌐 I/O-bound (Input/Output bound)**
**Operaciones limitadas por entrada/salida, NO por velocidad de CPU**

#### **✅ Características:**
```python
# Ejemplos típicos I/O-bound:
requests.get("https://api.com")    # ⏳ Espera respuesta de red
file.read()                       # ⏳ Espera lectura de disco
time.sleep(2)                     # ⏳ Espera tiempo
database.query("SELECT * FROM")   # ⏳ Espera consulta DB
input("Escribe algo: ")           # ⏳ Espera usuario
```

#### **🧠 Patrón mental I/O-bound:**
```
Tu programa: "Voy a hacer una request HTTP"
             ⏳ Esperando... esperando... esperando...
Red:         "Aquí está la respuesta"
Tu programa: "¡Perfecto! Continúo trabajando"

💡 El CPU está LIBRE durante la espera → Threading funciona genial
```

### **🧮 CPU-bound (CPU bound)**
**Operaciones limitadas por velocidad de procesamiento, NO por I/O**

#### **✅ Características:**
```python
# Ejemplos típicos CPU-bound:
for i in range(10000000):         # 🔥 Cálculo intensivo
    math.sqrt(i)                  # 🔥 Operación matemática

[x**2 for x in range(100000)]     # 🔥 Procesamiento de datos
sum(range(10000000))              # 🔥 Agregación numérica
is_prime(982451653)               # 🔥 Algoritmo complejo
image.resize((1000, 1000))        # 🔥 Procesamiento imagen
```

#### **🧠 Patrón mental CPU-bound:**
```
Tu programa: "Voy a calcular si 982451653 es primo"
CPU:         🔥🔥🔥 Trabajando al 100%... calculando... calculando...
Tu programa: "¡Listo! Es primo"

💡 El CPU está OCUPADO todo el tiempo → Threading NO ayuda (GIL)
```

### **🔍 ¿Cómo identificar el tipo?**

#### **🌐 Es I/O-bound si:**
- ✅ Hace requests HTTP/API
- ✅ Lee/escribe archivos
- ✅ Consulta bases de datos  
- ✅ Espera input del usuario
- ✅ Usa `time.sleep()`
- ✅ **CPU usage < 50%** durante ejecución

#### **🧮 Es CPU-bound si:**
- ✅ Loops matemáticos intensivos
- ✅ Procesamiento de imágenes/video
- ✅ Cálculos científicos
- ✅ Algoritmos complejos (ordenamiento, búsqueda)
- ✅ Machine learning training
- ✅ **CPU usage ~100%** durante ejecución

### **⚖️ ¿Por qué importa esta distinción?**

```python
# 🌐 I/O-bound: Threading ES efectivo
def download_file(url):
    response = requests.get(url)  # ⏳ CPU libre durante request
    # 💡 Mientras Thread 1 espera, Thread 2 puede trabajar
    
# 🧮 CPU-bound: Threading NO es efectivo  
def calculate_primes(n):
    for i in range(2, n):         # 🔥 CPU ocupado 100%
        if is_prime(i): ...       # 🔒 GIL bloquea otros threads
```

### 🔒 Global Interpreter Lock (GIL) - CONCEPTO CLAVE
- **Problema**: Solo 1 thread ejecuta Python bytecode a la vez
- **Impacto**: Limita paralelismo para CPU-bound
- **Solución**: Multiprocessing para CPU-bound

#### 📊 Visualización del GIL:
```
❌ Lo que CREEMOS que pasa con 4 threads:
Thread 1: ████████████████████████████ (100% del tiempo)
Thread 2: ████████████████████████████ (100% del tiempo)  
Thread 3: ████████████████████████████ (100% del tiempo)
Thread 4: ████████████████████████████ (100% del tiempo)

✅ Lo que REALMENTE pasa (GIL alternando):
Thread 1: ████░░░░████░░░░████░░░░████ (25% del tiempo)
Thread 2: ░░░░████░░░░████░░░░████░░░░ (25% del tiempo)
Thread 3: ░░░░░░░░░░░░████░░░░░░░░████ (25% del tiempo)  
Thread 4: ░░░░░░░░░░░░░░░░████░░░░░░░░ (25% del tiempo)
Resultado: ❌ FALSO PARALELISMO → Sin mejora real para CPU-bound
```

#### 🔓 Cuándo el GIL se libera vs se mantiene:
```python
# ✅ GIL SE LIBERA (Threading funciona):
time.sleep(1.0)           # I/O operation
requests.get("http://")   # Network I/O
file.read()              # File I/O
numpy.sqrt(array)        # C extensions

# ❌ GIL SE MANTIENE (Threading no funciona):
for i in range(1000000): # Pure Python loops
    math.sqrt(i)         # Python calculations
    if i % 2 == 0:       # Python comparisons
        list.append(i)   # Python data structures
```

#### 🔬 **¿Por qué Multiprocessing NO tiene limitaciones de GIL?**

```
🧵 THREADING (Falso Paralelismo):
┌────────────────────────────────┐
│       📦 1 Proceso Python      │
│   ┌────────────────────────┐   │
│   │      🔒 1 GIL          │   │
│   │  ┌───┬───┬───┬───┐     │   │
│   │  │T1 │T2 │T3 │T4 │     │   │
│   │  └─┬─┴─┬─┴─┬─┴─┬─┘     │   │
│   │    └───┼───┼───┘       │   │
│   │        └───┼───────────│   │
│   │            └───────────│   │
│   └────────────────────────┘   │
│          ↓ Se turnan           │
│       💻 1 CPU Core            │
└────────────────────────────────┘
   ⏱️ ~4s ❌ Falso paralelismo

🔥 MULTIPROCESSING (Verdadero Paralelismo):
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│📦 Proc1│ │📦 Proc2│ │📦 Proc3│ │📦 Proc4│
│🔒 GIL1 │ │🔒 GIL2 │ │🔒 GIL3 │ │🔒 GIL4 │
│🧵 T1   │ │🧵 T2   │ │🧵 T3   │ │🧵 T4   │
└───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    ↓          ↓          ↓          ↓
💻 Core1   💻 Core2   💻 Core3   💻 Core4
   ⏱️ ~1s ✅ Verdadero paralelismo

🔑 CLAVE: Cada proceso = Su propio GIL = Sin competencia
```

**💡 Explicación clave:**
- **🧵 Threading**: Todos los threads comparten 1 GIL → Se turnan para ejecutar
- **🔥 Multiprocessing**: Cada proceso tiene su propio GIL → Ejecutan independientemente  
- **🔑 Resultado**: Sin competencia entre procesos = Verdadero paralelismo para CPU-bound

### 🎯 Cuándo usar qué:

| Tipo de Tarea | Threading | Multiprocessing |
|---------------|-----------|-----------------|
| **I/O-bound** | 🥇 Excelente | 🥈 Funciona (overhead) |
| **CPU-bound** | 🥉 Malo (GIL) | 🥇 Excelente |
| **Mixto** | 🥈 Bueno | 🥇 Mejor |

## 📈 Resultados de Performance Esperados

### Para I/O-bound (4 requests de 1s cada uno):
```
🐌 Secuencial:      ~4.0s  (bloquea en cada I/O)
🧵 Threading:       ~1.0s  (concurrencia efectiva)
🔥 Multiprocessing: ~1.2s  (overhead innecesario)

💡 Threading mejora: 4.0x → ¡EXCELENTE para I/O!
💡 Multiprocessing: 3.3x → Funciona pero con overhead
```

### Para CPU-bound (números primos 500k-900k):
```
🐌 Secuencial:      ~5-8s  (usa 1 core, tiempo perceptible)
🧵 Threading:       ~5-8s  (GIL limita, mismo tiempo)
🔥 Multiprocessing: ~1-2s  (verdadero paralelismo)

💡 Threading mejora: 1.1x → ❌ FALSO PARALELISMO (GIL limita)
💡 Multiprocessing: 4.0x → ✅ VERDADERO PARALELISMO (sin GIL)
```

### 🧮 Ejemplo CPU-bound específico (cálculo de primos):
```python
# Rangos educativos que toman tiempo perceptible:
ranges = [
    (500000, 600000),  # ~8000 primos
    (600001, 700000),  # ~7500 primos  
    (700001, 800000),  # ~7500 primos
    (800001, 900000),  # ~7500 primos
]

# Operación CPU-intensiva:
def is_prime(n):
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:  # ← Código Python puro (GIL retenido)
            return False
    return True
```

## 🎓 Casos de Uso Reales

### 🥇 Usa Threading para:
- 🌐 **APIs y web scraping** (muchas requests HTTP)
- 📁 **Procesamiento de archivos** (leer/escribir archivos)
- 🎮 **Interfaces gráficas** (UI responsiva)
- 🔄 **Background tasks** (no bloquear hilo principal)

### 🥇 Usa Multiprocessing para:
- 🧮 **Procesamiento de imágenes** (PIL, OpenCV)
- 📊 **Análisis de datos** (Pandas, NumPy paralelo)
- 🤖 **Machine Learning** (entrenamiento distribuido)
- 🔢 **Cálculos matemáticos** (simulaciones, algoritmos)

### ⚡ Para operaciones Async:
*Contenido disponible en **Session3-Async/** ✅*
- 🕷️ Web scraping masivo (1000+ URLs concurrentes)
- 🌐 APIs de alta concurrencia (WebSocket servers)
- 🔄 Streaming de datos
- 📊 **Archivo disponible**: `async_complete_guide.py` - Guía consolidada completa

### 🔄 Para comunicación entre procesos:
*Contenido disponible en **Session4-IPC/** ✅*
- 🔄 Queue (Producer-Consumer patterns)  
- 📞 Pipe (Comunicación bidireccional)
- 💾 Shared Memory (Alta performance)
- 🗂️ Manager (Objetos compartidos inteligentes)
- 🚦 Event (Sincronización entre procesos)
- 📊 **Archivos disponibles**: `01_process_communication.py`, `objects_vs_results_demo.py`

## 🎓 ¿Por qué Números Primos como Ejemplo?

### **Ejemplo perfecto para demostrar limitaciones del GIL:**

#### ✅ **Características CPU-intensivas (perfecto ejemplo CPU-bound):**
- **Loops intensivos**: `for i in range(3, sqrt(n), 2)` 🔥
- **Operaciones matemáticas**: División, módulo, comparaciones 🔥
- **Código Python puro**: Sin I/O, sin C extensions 🔥
- **CPU al 100%**: Sin esperas, sin time.sleep() 🔥
- **Escalable**: Rangos ajustables para tiempos educativos

#### 📊 **Progresión educativa de rangos:**
```python
# 🚀 Demo rápida (clase):
ranges = [(10000, 15000), ...]  # ~0.01s → Resultados confusos

# 📚 Demo educativa (aprendizaje):  
ranges = [(100000, 150000), ...]  # ~0.16s → Mejor, pero rápido

# 🎯 Demo perfecta (comprensión):
ranges = [(500000, 600000), ...]  # ~5-8s → ¡Contraste dramático!
```

#### 💡 **Lección clave visual:**
```
I/O-bound:  🌐────🌐────🌐────🌐  (Threading: 4x mejora)
CPU-bound:  🧮■■■■🧮■■■■🧮■■■■🧮■■■■  (Threading: 1x mejora)
           ↑ GIL bloquea paralelismo real
```

## ⚠️ Errores Comunes a Evitar

1. **🚫 Threading para CPU-bound intensivo**
   ```python
   # ❌ Malo: GIL limita el paralelismo
   threads = [Thread(target=heavy_calculation) for _ in range(4)]
   
   # ✅ Bueno: Usar multiprocessing
   with ProcessPoolExecutor() as executor:
       futures = [executor.submit(heavy_calculation) for _ in range(4)]
   ```

2. **🚫 Race conditions sin locks**
   ```python
   # ❌ Malo: Race condition
   counter = 0
   def increment():
       global counter
       counter += 1  # No thread-safe
   
   # ✅ Bueno: Con lock
   lock = Lock()
   def increment():
       global counter
       with lock:
           counter += 1  # Thread-safe
   ```

3. **🚫 Demasiados workers**
   ```python
   # ❌ Malo: Overhead supera beneficios
   ThreadPoolExecutor(max_workers=1000)
   
   # ✅ Bueno: Basado en cores/tarea
   ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4))
   ```

## 🧪 Ejercicios Adicionales

### Ejercicio 1: Benchmark Personal y Rangos Educativos
```python
# 🎯 IMPORTANTE: Ajustar rangos para resultados educativos

# ❌ Rangos muy pequeños (confusos):
ranges = [(1000, 2000), ...]  # 0.01s → No se ve el GIL

# ✅ Rangos educativos (claros):
ranges = [(500000, 600000), ...]  # 5-8s → GIL obvio

# Mide el performance en tu sistema específico:
# ¿Cómo varía según tu número de CPU cores?
# ¿A partir de qué rango se ve claramente el GIL?
```

### Ejercicio 2: Aplicación Real
```python
# Crea un scraper que:
# 1. Descarga 100 páginas web (Threading/Async)
# 2. Procesa el contenido (Multiprocessing)
# 3. Guarda en base de datos (Threading)
```

### Ejercicio 3: Sistema de Monitoreo
```python
# Implementa un sistema que:
# 1. Monitorea archivos (Threading)
# 2. Procesa cambios (Multiprocessing)
# 3. Envía notificaciones (Async)
```

## 📚 Recursos Adicionales

### Documentación Oficial
- [threading — Thread-based parallelism](https://docs.python.org/3/library/threading.html)
- [multiprocessing — Process-based parallelism](https://docs.python.org/3/library/multiprocessing.html)
- [concurrent.futures — Launching parallel tasks](https://docs.python.org/3/library/concurrent.futures.html)

### Artículos Recomendados
- [Understanding the Python GIL](https://realpython.com/python-gil/)
- [Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency/)
- [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)

### Librerías Avanzadas
- `asyncio` - Async/await nativo
- `uvloop` - Event loop más rápido
- `joblib` - Paralelización simple para NumPy
- `dask` - Paralelización para big data

## 🎉 Al Completar Este Capítulo

Habrás dominado:

### 🎯 **Sesiones Principales (1-2):**
✅ **I/O-bound vs CPU-bound** (distinción fundamental)  
✅ **Diferencias entre concurrencia y paralelismo**  
✅ **VERDADERO vs FALSO paralelismo** (concepto clave)  
✅ **Cuándo y cómo usar threading efectivamente**  
✅ **Cómo evitar y resolver race conditions**  
✅ **Por qué el GIL limita threading para CPU-bound**  
✅ **Implementación de verdadero paralelismo con multiprocessing**  
✅ **Guía de decisión para cada caso de uso**

### ⚡ **Sesión Adicional 3 - Async/Await:**
✅ **Diferencias entre concurrencia preemptiva vs cooperativa**  
✅ **Por qué async NO puede tener race conditions**  
✅ **Escalabilidad masiva** (1000+ corrutinas vs 5000 threads max)  
✅ **Cuándo usar Async vs Threading vs Multiprocessing**  
✅ **Event loop y puntos de cedencia explícitos**

### 🔄 **Sesión Adicional 4 - IPC:**
✅ **5 métodos de comunicación entre procesos**  
✅ **Queue** (Producer-Consumer), **Pipe** (Bidireccional)  
✅ **Shared Memory** (Alta performance) vs **Manager** (Facilidad)  
✅ **Event** (Sincronización) y **coordinación** entre procesos  
✅ **Objects vs Results** - Diferencia entre contenedores y contenido  

## 📚 Archivos Educativos Especiales

### 🎯 **`objects_vs_results_demo.py`** (Session4-IPC)
Archivo **único y educativo** que resuelve confusiones comunes:
- ¿Por qué `print(thread)` muestra `<Thread object>` y no mi resultado?
- ¿Qué es `<coroutine object>` cuando olvido `await`?
- ¿Por qué `print(shared_array)` muestra wrapper y no `[1,2,3]`?

**💡 Regla de oro**: `Objects ≠ Results` - Aprende a acceder al contenido real.

### ⚡ **`async_complete_guide.py`** (Session3-Async)  
Guía **consolidada** que unifica TODO sobre async:
- 🪄 Por qué async es "mágico"
- 🔍 Prueba matemática: NO race conditions
- 📊 Comparación completa: Threading vs Multiprocessing vs Async
- 🎯 Guías de decisión práctica

## 🚀 Próximos Pasos

Después de dominar este capítulo, puedes continuar con:

- **Distributed computing** con `celery` o `dask`
- **GPU computing** con `numba` o `cupy`
- **Reactive programming** con `RxPY`
- **Microservices** con patrones async

---

**🎯 ¡Comienza tu journey hacia la programación concurrente y paralela!**

```bash
cd Session1-Concurrency/
python 01_sequential_problem.py
``` 
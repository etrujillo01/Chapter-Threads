# 🌐 Session 6: Introducción a Sistemas Distribuidos con Python

**Duración: 45 minutos** | **Nivel: Intermedio** | **Prerequisitos: Sessions 1-5**

## 🎯 **Objetivos de la Sesión**

Al finalizar esta sesión, los estudiantes podrán:

1. ✅ **Entender la evolución**: Threading/Multiprocessing → Sistemas Distribuidos
2. ✅ **Implementar load balancing**: Distribución de requests entre servidores
3. ✅ **Manejar fallos distribuidos**: Health checks, retries, circuit breakers
4. ✅ **Aplicar threading**: Para operaciones de red concurrentes
5. ✅ **Comparar escalabilidad**: 1 servidor vs múltiples servidores

---

## 📋 **Estructura de la Sesión (45 min)**

### **🎯 Minutos 0-5: Conexión con Conocimiento Previo**
> *"Hemos visto concurrencia EN una máquina... ¿Qué pasa cuando necesitamos MÚLTIPLES máquinas?"*

**Evolución de Conceptos:**
```python
# Lo que ya sabemos:
queue = Queue()          # Memoria compartida (Session 1-2)
pipe1, pipe2 = Pipe()    # IPC local (Session 4)

# Lo nuevo:
requests.post("http://server1:8000/api/task")  # Comunicación por red
```

### **📚 Minutos 5-15: Conceptos Fundamentales**

#### **🔄 Cambios Clave:**
| Local (Sessions 1-5) | Distribuido (Session 6) |
|-----------------------|-------------------------|
| Memoria compartida | Solo comunicación por red |
| Fallos = proceso crash | Fallos parciales (una máquina) |
| Tiempo sincronizado | Cada máquina su reloj |
| Threading.Lock | Distributed locks |

#### **💡 3 Desafíos Nuevos:**
1. **🌐 Sin memoria compartida** → Todo por HTTP/gRPC
2. **💥 Fallos parciales** → Una máquina puede morir, otras siguen
3. **🕰️ Sin tiempo global** → Difícil coordinar eventos

### **🛠️ Minutos 15-30: Demo Práctica Progresiva**

#### **Demo 1: Del Monolito al Distribuido (15 min)**

**Setup:**
```bash
# Terminal 1-3: Múltiples servidores
python manage.py runserver 8001
python manage.py runserver 8002  
python manage.py runserver 8003

# Terminal 4: Load balancer
python distributor.py
```

**Progresión:**
1. **1 servidor** → `curl http://localhost:8001/api/image/4k/`
2. **3 servidores** → Manual round-robin
3. **Load balancer** → Automático + estadísticas

### **👨‍💻 Minutos 30-40: Ejercicio Hands-on**

#### **🏥 Health Monitor Distribuido**

**Objetivo:** Implementar monitor que detecta servidores caídos

**4 Ejercicios Progresivos:**
```python
# 1. Monitor secuencial (2 min)
for server in servers:
    check_health(server)

# 2. Monitor paralelo con threading (3 min)  
with ThreadPoolExecutor(max_workers=5):
    # TODO: Implementar

# 3. Retry logic + Circuit breaker (4 min)
if failed_3_times:
    status = "CIRCUIT_OPEN"

# 4. Monitoreo continuo (1 min - opcional)
```

### **🎓 Minutos 40-45: Wrap-up y Siguientes Pasos**

#### **📊 Comparación Final:**
```
Threading          →  Microservicios
Queue             →  Message Broker (Redis) 
multiprocessing   →  Container orchestration
Shared Memory     →  Distributed database
```

---

## 🚀 **Setup Rápido para Instructores**

### **1. Pre-requisitos**
```bash
# Verificar que Projects funciona
cd ../Projects
python manage.py runserver 8000
# Probar: curl http://localhost:8000/

# Instalar dependencias adicionales
cd ../Session5-DistributedSystems  
pip install -r requirements.txt
```

### **2. Preparación Demo (30 segundos)**
```bash
# Opción A: Manual (para demo paso a paso)
python manage.py runserver 8001 &
python manage.py runserver 8002 &
python manage.py runserver 8003 &

# Opción B: Automático (más rápido)
python start_servers.py
```

### **3. Verificación**
```bash
python distributor.py  # Debería mostrar 3 servidores UP
```

---

## 📊 **Material Incluido**

### **🎯 Para Demos:**
- **`distributor.py`**: Load balancer interactivo con 3 demos
  - Demo 1: Distribución básica (Round Robin)
  - Demo 2: Requests concurrentes (Threading)  
  - Demo 3: Tolerancia a fallos
- **`start_servers.py`**: Helper para levantar servidores automáticamente

### **🧪 Para Ejercicios:**
- **`health_monitor.py`**: Template con 4 ejercicios progresivos
  - TODOs claros con pistas
  - Soluciones comentadas para instructor
  - Menu interactivo

### **📋 Apoyo:**
- **`requirements.txt`**: Dependencias adicionales
- **`README.md`**: Este archivo con instrucciones completas

---

## 🎭 **Guía de Ejecución para Instructores**

### **📝 Minuto a Minuto:**

**0-5: Intro**
```
👋 "Hemos visto Threading, Multiprocessing, Async, IPC..."
🤔 "¿Qué pasa cuando necesito 100 servidores?"
📊 Mostrar evolución: 1 máquina → N máquinas
```

**5-15: Teoría**
```
🌐 "Sin memoria compartida = todo por red"
💥 "Fallos parciales = nueva realidad"  
🕰️ "Sin tiempo global = orden difícil"
```

**15-30: Demo**
```
🚀 "Vamos a distribuir nuestro servidor de imágenes 4K"
📺 Ejecutar distributor.py en vivo
💥 "¿Qué pasa si mato un servidor?" (Ctrl+C en terminal)
```

**30-40: Hands-on**
```
👨‍💻 "Ahora ustedes: implementen health monitor"
🧪 "4 ejercicios, empiecen por el 1"
🤝 Ayudar con threading en ejercicio 2
```

**40-45: Cierre**
```
🎓 "Threading les ayudó aquí también!"
🚀 "Próximo: Message queues (Redis), Containers (Docker)"
```

### **🎪 Tips de Engagement:**

1. **Preguntas constantes**: 
   - "¿Qué creen que pasa si...?"
   - "¿Cómo harían esto con threading?"

2. **Demos interactivas**:
   - Matar servidor durante demo
   - Mostrar estadísticas en tiempo real

3. **Conexiones explícitas**:
   - "Esto es como ThreadPoolExecutor, pero por red"
   - "Queue vs HTTP requests"

---

## 🔍 **Conceptos Clave a Enfatizar**

### **🧵 Threading Sigue Siendo Relevante**
```python
# Para requests HTTP paralelos
with ThreadPoolExecutor(max_workers=10):
    futures = [executor.submit(make_request, server) for server in servers]
```

### **🌐 Nuevos Patrones**
```python
# Load balancing
server = load_balancer.round_robin()

# Health checking  
if not health_check(server):
    servers.remove(server)

# Circuit breaker
if failed_count > 3:
    circuit_open = True
```

### **📊 Escalabilidad**
```
1 servidor:   100 requests/segundo
3 servidores: ¿300 requests/segundo?
```

---

## 🚀 **Siguientes Sesiones (Preview)**

### **Session 7: Message Queues**
```python
# Redis/RabbitMQ para comunicación asíncrona
import redis
redis_client.lpush("tasks", json.dumps(task))
```

### **Session 8: Container Orchestration**  
```yaml
# Docker + Kubernetes básico
apiVersion: v1
kind: Service
metadata:
  name: image-server
spec:
  replicas: 3
```

### **Session 9: Monitoring Distribuido**
```python
# Prometheus + Grafana
from prometheus_client import Counter
request_count = Counter('requests_total')
```

---

## 🛠️ **Troubleshooting**

### **❌ Problema: Servidores no inician**
```bash
# Verificar puerto libre
lsof -i :8001

# Verificar desde Projects
cd ../Projects
python manage.py check
```

### **❌ Problema: ImportError requests**
```bash
pip install requests==2.31.0
```

### **❌ Problema: distributor.py no encuentra servidores**
```bash
# Verificar manualmente
curl http://localhost:8001/
curl http://localhost:8002/  
curl http://localhost:8003/
```

---

## 📚 **Recursos Adicionales**

### **📖 Para Estudiantes:**
- [Distributed Systems for Fun and Profit](http://book.mixu.net/distsys/)
- [CAP Theorem Explained](https://www.educative.io/blog/what-is-cap-theorem)

### **🎓 Para Instructores:**
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [Microservices Patterns](https://microservices.io/patterns/)

---

**🎯 ¡Material completo listo para usar! Solo ejecuta `python start_servers.py` y `python distributor.py` para empezar.** 🚀 
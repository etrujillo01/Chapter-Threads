# 🔥 DÍA 1 - MARTES: Threading + Image Processing

**Objetivo**: Convertir servidor estático → pipeline de procesamiento con threading

**Tiempo**: 45min seguimiento + 1h autónoma = 1.75h total

---

## 🎯 **OBJETIVO DEL DÍA**

Implementar un **pipeline de procesamiento de imágenes** usando **threading** para aplicar múltiples filtros en paralelo.

### **Antes vs Después:**
```
ANTES: GET /api/image/4k/ → imagen estática
DESPUÉS: POST /api/process/ → imagen + 3 filtros aplicados en paralelo
```

### **🖼️ IMÁGENES REALES DISPONIBLES:**
```
static/images/sample_4k.jpg      ← 368KB imagen 4K real
static/images/misurina-sunset.jpg ← 368KB imagen paisaje real
```
**El sistema alterna entre estas 2 imágenes reales para testing de performance.**

---

## ⏰ **AGENDA DEL DÍA**

### **📚 45min - SEGUIMIENTO EN CLASE:**

#### **Minutos 0-10: Setup + Review**
- ✅ Review Session 5 (sistemas distribuidos)
- ✅ Explicar objetivo del proyecto semanal
- ✅ Setup inicial del pipeline

#### **Minutos 10-25: Implementación básica**
- ✅ Instalar dependencias: `pip install Pillow`
- ✅ Implementar primer filtro (resize)  
- ✅ Probar ThreadPoolExecutor básico

#### **Minutos 25-40: Threading en acción**
- ✅ Completar filtros blur y brightness
- ✅ Implementar procesamiento en lote
- ✅ Test de performance

#### **Minutos 40-45: Q&A y siguiente paso**
- ✅ Resolver dudas
- ✅ Explicar tareas autónomas
- ✅ Preview DÍA 2

### **🚀 1h - TRABAJO AUTÓNOMO:**
- ✅ Completar implementación de filtros
- ✅ Crear endpoints de API
- ✅ Testing exhaustivo
- ✅ Documentar resultados

---

## 🛠️ **TAREAS ESPECÍFICAS**

### **📋 CHECKLIST - SEGUIMIENTO (45 min):**

#### **1. Setup inicial (10 min)**
```bash
# Instalar dependencias
pip install Pillow opencv-python

# Verificar instalación
python -c "from PIL import Image; print('PIL OK')"
```

#### **2. Implementar resize filter (10 min)**
Completar en `image_api/filters.py`:
```python
@staticmethod
def resize_filter(image_data: Any, size: Tuple[int, int] = (800, 600)) -> Any:
    # TODO: Descommentar cuando PIL esté instalado
    # return image_data.resize(size, Image.Resampling.LANCZOS)
```

#### **3. Threading básico (15 min)**
Completar en `image_api/processors.py`:
```python
def process_batch_threading(self, image_paths: List[str], filters: List[str]):
    # TODO: Implementar ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
        # ... código aquí
```

#### **4. Test inicial (10 min)**
```python
# Ejecutar test de performance
python image_api/processors.py
```

### **📋 CHECKLIST - AUTÓNOMO (1h):**

#### **1. Completar filtros (20 min)**
En `image_api/filters.py`:
- ✅ Implementar `blur_filter()` con PIL
- ✅ Implementar `brightness_filter()` con PIL  
- ✅ Testear cada filtro individualmente

#### **2. API endpoints (20 min)**
En `image_api/views.py`:
- ✅ Crear endpoint `POST /api/process/`
- ✅ Manejar upload de archivos
- ✅ Integrar con `ImageProcessor`
- ✅ Retornar resultados JSON

#### **3. Testing completo (15 min)**
- ✅ Probar con imagen real
- ✅ Comparar sequential vs threading
- ✅ Medir speedup obtenido

#### **4. Documentación (5 min)**
- ✅ Actualizar README con nuevos endpoints
- ✅ Documentar resultados de performance

---

## 🧪 **DEMOS Y TESTING**

### **🔬 Test 1: Filtros individuales**
```python
from image_api.filters import ImageFilters
from PIL import Image

# Cargar imagen
img = Image.open('static/images/sample_4k.jpg')

# Probar filtros
resized = ImageFilters.resize_filter(img)
blurred = ImageFilters.blur_filter(img)
bright = ImageFilters.brightness_filter(img)
```

### **🔬 Test 2: Threading performance**
```python
from image_api.processors import test_threading_performance

# Comparar sequential vs threading
test_threading_performance()

# Esperado: 2-4x speedup
```

### **🔬 Test 3: API endpoint**
```bash
# Upload y procesar imagen
curl -X POST \
  -F "image=@static/images/sample_4k.jpg" \
  -F "filters=resize,blur,brightness" \
  http://localhost:8000/api/process/

# Respuesta esperada:
{
  "status": "success",
  "processing_time": 1.2,
  "filters_applied": ["resize", "blur", "brightness"],
  "output_files": ["processed_1.jpg", "processed_2.jpg", "processed_3.jpg"],
  "speedup": "3.2x vs sequential"
}
```

---

## 📊 **MÉTRICAS DE ÉXITO**

### **Funcionalidad:**
- ✅ 3 filtros funcionando (resize, blur, brightness)
- ✅ ThreadPoolExecutor procesando en paralelo
- ✅ API endpoint recibiendo imágenes
- ✅ Resultados guardados en `static/processed/`

### **Performance:**
- ✅ **Speedup mínimo**: 2x vs sequential
- ✅ **Tiempo de respuesta**: <3 segundos para imagen 4K
- ✅ **Concurrencia**: Múltiples requests simultáneos

### **Calidad de código:**
- ✅ Manejo de errores
- ✅ Logging apropiado
- ✅ Código documentado
- ✅ Tests unitarios básicos

---

## 🚨 **TROUBLESHOOTING COMÚN**

### **❌ Error: PIL no instalado**
```bash
pip install Pillow
# Si falla: pip install --upgrade pip
```

### **❌ Error: Threading no mejora performance**
- Verificar que estés usando I/O-bound tasks
- Revisar que ThreadPoolExecutor tenga >1 worker
- Asegurar que no hay locks innecesarios

### **❌ Error: Imagen no se carga**
```python
# Verificar formato soportado
from PIL import Image
supported = Image.registered_extensions()
print(supported)  # ['.jpg', '.png', ...]
```

### **❌ Error: Out of memory**
- Redimensionar imágenes grandes antes de procesar
- Usar menos workers concurrentes
- Procesar en chunks más pequeños

---

## 🎯 **CRITERIOS DE EVALUACIÓN**

### **Básico (suficiente):**
- ✅ 2 filtros funcionando
- ✅ Threading con speedup >1.5x
- ✅ API endpoint básico

### **Intermedio (bien):**
- ✅ 3 filtros funcionando
- ✅ Speedup >2.5x
- ✅ Manejo de errores
- ✅ Tests automatizados

### **Avanzado (excelente):**
- ✅ 3+ filtros funcionando
- ✅ Speedup >3x
- ✅ Multiple concurrent requests
- ✅ Progress tracking
- ✅ Resource monitoring

---

## 🚀 **PREVIEW DÍA 2**

**Próximo objetivo**: Migrar filtros pesados a **multiprocessing**

**Por qué**: Threading es perfecto para I/O, pero para filtros CPU-intensivos (edge detection, complex transformations) necesitamos multiprocessing.

**Preparación**: Los filtros `sharpen` y `edges` en `filters.py` están listos para DÍA 2.

---

## 📝 **ENTREGA DEL DÍA**

Al final del DÍA 1, debes tener:

1. **Código funcionando**:
   - `image_api/processors.py` - Threading implementation
   - `image_api/filters.py` - 3 filtros básicos
   - `image_api/views.py` - API endpoint

2. **Demo funcionando**:
   ```bash
   curl -X POST -F "image=@test.jpg" http://localhost:8000/api/process/
   ```

3. **Reporte de performance**:
   - Sequential time: X.X seconds
   - Threading time: X.X seconds  
   - Speedup: X.Xx
   - Efficiency: XX%

**🎯 ¡Listo para convertir tu servidor estático en un pipeline de procesamiento concurrente!** 🚀 
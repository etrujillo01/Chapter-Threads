"""
🖼️ Image Processors - DÍA 1 y 2: Threading + Multiprocessing + Image Processing

Base para que los estudiantes implementen procesamiento de imágenes con threading (Día 1) y multiprocessing (Día 2).
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from pathlib import Path
from typing import List, Dict, Any
import logging
import os

from PIL import Image
from image_api.filters import ImageFilters  # Cambia la ruta si es necesario
import uuid


logger = logging.getLogger(__name__)

# ===========================================================
# 🔥 Worker para multiprocessing - NIVEL DE MÓDULO
# ===========================================================
import uuid  # Al inicio del archivo si no lo tienes ya

import uuid  # <-- Esto va al inicio del archivo donde está el worker, si no lo tienes aún

def worker_process_mp(img_path, filters):
    """
    Worker independiente para multiprocessing (debe estar a nivel de módulo)
    """
    from image_api.filters import ImageFilters, FilterFactory
    from PIL import Image
    import os

    try:
        # VALIDACIÓN DE FILTROS
        for filter_name in filters:
            if filter_name not in FilterFactory.AVAILABLE_FILTERS:
                return {
                    "original_path": img_path,
                    "error": f"Filtro '{filter_name}' no está disponible",
                    "status": "error"
                }

        img = Image.open(img_path)
        for filter_name in filters:
            if filter_name == "sharpen":
                img = ImageFilters.heavy_sharpen_filter(img)
            elif filter_name == "edges":
                img = ImageFilters.edge_detection_filter(img)

        # GENERA UN NOMBRE ÚNICO PARA CADA ARCHIVO PROCESADO
        unique_id = uuid.uuid4().hex[:8]
        processed_path = os.path.join(
            "static", "processed", f"{Path(img_path).stem}_{unique_id}_mp_filtered.jpg"
        )
        os.makedirs(os.path.dirname(processed_path), exist_ok=True)
        img.save(processed_path)
        return {
            "original_path": img_path,
            "processed_path": processed_path,
            "filters_applied": filters,
            "status": "success (multiprocessing)"
        }
    except Exception as e:
        return {
            "original_path": img_path,
            "error": str(e),
            "status": "error"
        }

# ===========================================================
# 🎯 ImageProcessor
# ===========================================================

class ImageProcessor:
    """
    🎯 Procesador de imágenes con soporte para threading y multiprocessing

    DÍA 1: Implementar threading básico
    DÍA 2: Multiprocessing para filtros pesados
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.processed_count = 0
        self.processing_lock = threading.Lock()

    # =====================================================================
    # 🔥 DÍA 1: THREADING
    # =====================================================================

    
    import uuid  # <- AGREGA ESTE IMPORT AL INICIO

    def process_single_image(self, image_path: str, filters: List[str]) -> Dict[str, Any]:
        start_time = time.time()
        thread_id = threading.get_ident()
        processed_path = None
        file_size = 0

        logger.info(
            f"🧵 Thread {thread_id}: Procesando {image_path} con filtros {filters}"
        )

        try:
            # VALIDACIÓN DE FILTROS
            from image_api.filters import FilterFactory
            for filter_name in filters:
                if filter_name not in FilterFactory.AVAILABLE_FILTERS:
                    logger.error(f"❌ Filtro '{filter_name}' no está disponible")
                    return {
                        "original_path": image_path,
                        "error": f"Filtro '{filter_name}' no está disponible",
                        "status": "error"
                    }

            if not Path(image_path).exists():
                logger.warning(f"⚠️ Imagen no encontrada: {image_path}")
                image_path = os.path.join("static", "images", "sample_4k.jpg")

            img = Image.open(image_path)
            file_size = os.path.getsize(image_path)

            for filter_name in filters:
                if filter_name == "resize":
                    img = ImageFilters.resize_filter(img)
                elif filter_name == "blur":
                    img = ImageFilters.blur_filter(img)
                elif filter_name == "brightness":
                    img = ImageFilters.brightness_filter(img)

            # GENERA UN NOMBRE ÚNICO PARA CADA ARCHIVO PROCESADO
            unique_id = uuid.uuid4().hex[:8]
            processed_path = os.path.join(
                "static", "processed", f"{Path(image_path).stem}_{unique_id}_filtered.jpg"
            )
            os.makedirs(os.path.dirname(processed_path), exist_ok=True)
            img.save(processed_path)

            with self.processing_lock:
                self.processed_count += 1

        except Exception as e:
            logger.error(f"❌ Error procesando {image_path}: {e}")
            file_size = 0
            processed_path = None

        processing_time = time.time() - start_time

        return {
            "original_path": image_path,
            "processed_path": processed_path,
            "filters_applied": filters,
            "processing_time": processing_time,
            "file_size": file_size,
            "thread_id": str(thread_id),
            "status": "success" if processed_path else "error",
        }


    def process_batch_threading(self, image_paths: List[str], filters: List[str]) -> List[Dict[str, Any]]:
        """
        🚀 Procesar múltiples imágenes en paralelo con ThreadPoolExecutor (threading)
        """
        logger.info(f"🚀 Iniciando procesamiento en lote: {len(image_paths)} imágenes")
        results = []
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_image = {
                executor.submit(self.process_single_image, img_path, filters): img_path
                for img_path in image_paths
            }

            for future in as_completed(future_to_image):
                image_path = future_to_image[future]
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"✅ Completado: {image_path}")
                except Exception as e:
                    logger.error(f"❌ Error procesando {image_path}: {e}")
                    results.append(
                        {
                            "original_path": image_path,
                            "error": str(e),
                            "thread_id": str(threading.get_ident()),
                        }
                    )

        total_time = time.time() - start_time
        logger.info(
            f"🎯 Lote completado: {len(results)} resultados en {total_time:.2f}s"
        )

        return results

    # =====================================================================
    # 🔥 DÍA 2: MULTIPROCESSING
    # =====================================================================

    def process_batch_multiprocessing(self, image_paths: List[str], filters: List[str]) -> List[Dict[str, Any]]:
        """
        🚀 Procesar múltiples imágenes en paralelo con ProcessPoolExecutor (multiprocessing)
        Solo para filtros pesados (Día 2)
        """
        import copy
        results = []
        start_time = time.time()

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(worker_process_mp, img_path, copy.deepcopy(filters)): img_path
                for img_path in image_paths
            }
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f"❌ Error en multiprocessing: {e}")

        total_time = time.time() - start_time
        logger.info(f"🎯 Lote multiprocessing completado: {len(results)} resultados en {total_time:.2f}s")
        return results

    def get_stats(self) -> Dict[str, Any]:
        """📊 Estadísticas del procesador"""
        return {
            "total_processed": self.processed_count,
            "max_workers": self.max_workers,
            "active_threads": threading.active_count(),
        }


# =====================================================================
# 🧪 FUNCIONES DE TESTING PARA DÍA 1 Y 2
# =====================================================================

def test_threading_performance():
    """
    🧪 Test de performance threading vs secuencial

    TODO DÍA 1: Los estudiantes ejecutan esto para comparar
    """
    import time

    test_images = [f"test_image_{i}.jpg" for i in range(10)]
    test_filters = ["resize", "blur", "brightness"]

    processor = ImageProcessor(max_workers=4)

    print("🧪 Testing Threading vs Sequential...")

    # Test secuencial
    start = time.time()
    sequential_results = []
    for img in test_images:
        result = processor.process_single_image(img, test_filters)
        sequential_results.append(result)
    sequential_time = time.time() - start

    # Test threading
    start = time.time()
    threaded_results = processor.process_batch_threading(test_images, test_filters)
    threaded_time = time.time() - start

    # Resultados
    speedup = sequential_time / threaded_time if threaded_time > 0 else 1
    print(f"📊 RESULTADOS:")
    print(f"   Sequential: {sequential_time:.2f}s")
    print(f"   Threading:  {threaded_time:.2f}s")
    print(f"   Speedup:    {speedup:.1f}x")
    print(f"   Efficiency: {speedup/processor.max_workers*100:.1f}%")

def test_multiprocessing_performance():
    """
    🧪 Test de performance multiprocessing (Día 2)
    """
    import time

    test_images = [f"test_image_{i}.jpg" for i in range(6)]
    test_filters = ["sharpen", "edges"]

    processor = ImageProcessor(max_workers=4)

    print("🧪 Testing Multiprocessing...")

    # Test multiprocessing
    start = time.time()
    mp_results = processor.process_batch_multiprocessing(test_images, test_filters)
    mp_time = time.time() - start

    print(f"📊 RESULTADOS MP:")
    print(f"   Multiprocessing:  {mp_time:.2f}s")
    print(f"   Procesados: {len(mp_results)}")

if __name__ == "__main__":
    # Para testing rápido
    test_threading_performance()
    test_multiprocessing_performance()

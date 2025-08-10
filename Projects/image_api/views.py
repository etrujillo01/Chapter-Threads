"""
🖼️ Image API Views

Views para servir imágenes 4K y demostrar operaciones I/O-bound.
Perfecto para testing con Threading vs Multiprocessing.
"""

import os
import time
import logging
from pathlib import Path

from django.http import HttpResponse, JsonResponse, Http404
from django.conf import settings
from django.views.decorators.http import require_http_methods,require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import redis


logger = logging.getLogger(__name__)


# ============================================================================
# 🏠 HEALTH CHECK ENDPOINT
# ============================================================================


@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse(
        {
            "status": "healthy",
            "service": "Django Image Server",
            "version": "1.0.0",
            "endpoints": {
                "health": "/",
                "4k_image": "/api/image/4k/",
                "image_info": "/api/image/info/",
                "slow_image": "/api/image/slow/",
            },
        }
    )


# ============================================================================
# 🖼️ IMAGE SERVING ENDPOINTS
# ============================================================================


@require_http_methods(["GET"])
def serve_4k_image(request):
    """
    🖼️ Endpoint principal: Sirve imagen 4K

    Este endpoint demuestra una operación I/O-bound típica:
    - Lee archivo grande del disco (4K image)
    - Envía respuesta HTTP
    - Perfecto para testing con concurrencia
    """
    start_time = time.time()

    # Path de la imagen 4K
    image_path = Path(settings.STATICFILES_DIRS[0]) / "images" / "sample_4k.jpg"

    logger.info(f"📸 Sirviendo imagen 4K: {image_path}")

    # Verificar que existe la imagen
    if not image_path.exists():
        logger.error(f"❌ Imagen no encontrada: {image_path}")
        return JsonResponse(
            {
                "error": "Imagen 4K no encontrada",
                "message": "Por favor coloca tu imagen 4K en: static/images/sample_4k.jpg",
                "expected_path": str(image_path),
            },
            status=404,
        )

    try:
        # 📖 I/O OPERATION: Leer archivo del disco
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Calcular estadísticas
        file_size_mb = len(image_data) / (1024 * 1024)
        processing_time = time.time() - start_time

        logger.info(
            f"✅ Imagen servida: {file_size_mb:.2f}MB en {processing_time:.3f}s"
        )

        # Crear respuesta HTTP con la imagen
        response = HttpResponse(image_data, content_type="image/jpeg")
        response["Content-Length"] = len(image_data)
        response["X-File-Size-MB"] = f"{file_size_mb:.2f}"
        response["X-Processing-Time"] = f"{processing_time:.3f}"
        response["X-IO-Type"] = "I/O-bound"

        return response

    except Exception as e:
        logger.error(f"❌ Error sirviendo imagen: {e}")
        return JsonResponse(
            {"error": "Error al servir imagen", "message": str(e)}, status=500
        )


@require_http_methods(["GET"])
def get_image_info(request):
    """
    📊 Endpoint de información: Datos sobre la imagen sin enviarla

    Útil para:
    - Verificar que la imagen existe
    - Obtener metadata sin transferir datos
    - Testing rápido
    """
    image_path = Path(settings.STATICFILES_DIRS[0]) / "images" / "sample_4k.jpg"

    if not image_path.exists():
        return JsonResponse(
            {
                "error": "Imagen no encontrada",
                "expected_path": str(image_path),
                "instructions": "Coloca tu imagen 4K en static/images/sample_4k.jpg",
            },
            status=404,
        )

    try:
        # Obtener estadísticas del archivo
        stat_info = image_path.stat()
        file_size_bytes = stat_info.st_size
        file_size_mb = file_size_bytes / (1024 * 1024)

        return JsonResponse(
            {
                "status": "found",
                "filename": image_path.name,
                "path": str(image_path),
                "size_bytes": file_size_bytes,
                "size_mb": round(file_size_mb, 2),
                "is_4k_size": file_size_mb > 5,  # Rough estimate for 4K image
                "endpoints": {
                    "download": "/api/image/4k/",
                    "slow_version": "/api/image/slow/",
                },
            }
        )

    except Exception as e:
        return JsonResponse(
            {"error": "Error accediendo imagen", "message": str(e)}, status=500
        )


@require_http_methods(["GET"])
def serve_slow_image(request):
    """
    🐌 Endpoint "lento": Simula procesamiento + I/O

    Útil para:
    - Demostrar diferencias dramáticas con threading
    - Simular operaciones más complejas
    - Testing de timeouts
    """
    start_time = time.time()

    # Simular procesamiento (podría ser resize, filters, etc.)
    delay = float(request.GET.get("delay", 2.0))
    logger.info(f"🐌 Simulando procesamiento por {delay}s...")
    time.sleep(delay)

    # Luego servir la imagen normalmente
    image_path = Path(settings.STATICFILES_DIRS[0]) / "images" / "sample_4k.jpg"

    if not image_path.exists():
        return JsonResponse(
            {
                "error": "Imagen no encontrada para procesamiento lento",
                "expected_path": str(image_path),
            },
            status=404,
        )

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        total_time = time.time() - start_time
        file_size_mb = len(image_data) / (1024 * 1024)

        logger.info(f"🐌 Imagen 'procesada' y servida: {total_time:.2f}s total")

        response = HttpResponse(image_data, content_type="image/jpeg")
        response["X-Processing-Time"] = f"{total_time:.3f}"
        response["X-Simulated-Delay"] = f"{delay:.1f}"
        response["X-File-Size-MB"] = f"{file_size_mb:.2f}"
        response["X-IO-Type"] = "I/O-bound + Processing"

        return response

    except Exception as e:
        return JsonResponse(
            {"error": "Error en procesamiento lento", "message": str(e)}, status=500
        )


# ============================================================================
# 📊 STATISTICS ENDPOINT
# ============================================================================


@require_http_methods(["GET"])
def get_server_stats(request):
    """
    📊 Estadísticas del servidor

    Útil para monitoring durante load testing
    """
    import psutil
    import threading
    import multiprocessing

    # Información del sistema
    cpu_count = multiprocessing.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()

    # Información de threading (aproximada)
    active_threads = threading.active_count()

    return JsonResponse(
        {
            "system": {
                "cpu_cores": cpu_count,
                "cpu_usage_percent": cpu_percent,
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_used_percent": memory.percent,
                "active_threads": active_threads,
            },
            "recommendations": {
                "threading": "Perfecto para este servidor (I/O-bound)",
                "multiprocessing": f"Máximo recomendado: {cpu_count} workers",
                "async": "Excelente para alta concurrencia",
            },
        }
    )


# ============================================================================
# 🚀 PROJECT DAY 1: BATCH PROCESSING ENDPOINTS
# ============================================================================

import json
from django.views.decorators.csrf import csrf_exempt
from .processors import ImageProcessor
from .filters import FilterFactory


@csrf_exempt
@require_http_methods(["POST"])
def process_batch_sequential(request):
    """
    🐌 Procesamiento secuencial (LENTO) - para comparar con threading

    Demo de Day 1: Procesa múltiples filtros secuencialmente
    """
    try:
        data = json.loads(request.body)
        filters = data.get("filters", ["resize", "blur", "brightness"])
        count = data.get("count", 5)

        start_time = time.time()

        # Procesamiento SECUENCIAL usando imágenes REALES
        processor = ImageProcessor()
        results = []

        # Usar imágenes reales de static/images/
        available_images = [
            "static/images/sample_4k.jpg",
            "static/images/misurina-sunset.jpg",
        ]

        for i in range(count):
            # Alternar entre las imágenes disponibles
            image_path = available_images[i % len(available_images)]
            result = processor.process_single_image(image_path, filters)
            results.append(result)

        total_time = time.time() - start_time

        return JsonResponse(
            {
                "method": "sequential",
                "processed_count": len(results),
                "filters_used": filters,
                "total_time": round(total_time, 3),
                "avg_time_per_image": round(total_time / count, 3),
                "performance": "🐌 LENTO - sin concurrencia",
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def process_batch_threading(request):
    """
    🚀 Procesamiento con THREADING (RÁPIDO) - objetivo Day 1

    Demo de Day 1: Muestra el speedup con threading
    """
    try:
        data = json.loads(request.body)
        filters = data.get("filters", ["resize", "blur", "brightness"])
        count = data.get("count", 5)

        start_time = time.time()

        # Procesamiento con THREADING usando imágenes REALES
        processor = ImageProcessor()

        # Usar imágenes reales de static/images/
        available_images = [
            "static/images/sample_4k.jpg",
            "static/images/misurina-sunset.jpg",
        ]

        # Generar lista de imágenes reales para procesar
        real_images = [
            available_images[i % len(available_images)] for i in range(count)
        ]
        results = processor.process_batch_threading(real_images, filters)

        total_time = time.time() - start_time

        return JsonResponse(
            {
                "method": "threading",
                "processed_count": len(results),
                "filters_used": filters,
                "total_time": round(total_time, 3),
                "avg_time_per_image": round(total_time / count, 3),
                "speedup_estimate": "🚀 2-3x más rápido que secuencial",
                "performance": "⚡ RÁPIDO - con threading",
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def compare_performance(request):
    """
    📊 DEMO PRINCIPAL Day 1: Compara secuencial vs threading

    Este es el endpoint estrella para mostrar el speedup
    """
    try:
        data = json.loads(request.body)
        filters = data.get("filters", ["resize", "blur", "brightness"])
        count = data.get("count", 5)

        processor = ImageProcessor()

        # Usar imágenes reales para ambos tests
        available_images = [
            "static/images/sample_4k.jpg",
            "static/images/misurina-sunset.jpg",
        ]

        # Test SECUENCIAL con imágenes REALES
        start_seq = time.time()
        results_seq = []
        for i in range(count):
            image_path = available_images[i % len(available_images)]
            result = processor.process_single_image(image_path, filters)
            results_seq.append(result)
        time_sequential = time.time() - start_seq

        # Test THREADING con imágenes REALES
        start_thr = time.time()
        real_images = [
            available_images[i % len(available_images)] for i in range(count)
        ]
        results_threading = processor.process_batch_threading(real_images, filters)
        time_threading = time.time() - start_thr

        # Calcular speedup
        speedup = round(time_sequential / time_threading, 2)

        return JsonResponse(
            {
                "comparison": {
                    "sequential": {
                        "time": round(time_sequential, 3),
                        "method": "🐌 Uno por uno",
                        "processed": len(results_seq),
                    },
                    "threading": {
                        "time": round(time_threading, 3),
                        "method": "🚀 Paralelo",
                        "processed": len(results_threading),
                    },
                },
                "results": {
                    "speedup": f"{speedup}x",
                    "improvement": f"{((speedup-1)*100):.1f}% más rápido",
                    "recommendation": "🎯 Threading es perfecto para I/O-bound operations",
                },
                "filters_tested": filters,
                "images_processed": count,
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def process_image_view(request):
    """
    Endpoint POST para subir y procesar una imagen con filtros.
    Form data:
        - image: archivo imagen
        - filters: string "resize,blur,brightness"
    """
    image_file = request.FILES.get("image")
    filters_str = request.POST.get("filters", "")

    if not image_file:
        return Response(
            {"error": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST
        )

    filters = [f.strip() for f in filters_str.split(",") if f.strip()]
    if not filters:
        filters = ["resize"]

    import os

    temp_dir = os.path.join("static", "uploaded")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, image_file.name)
    with open(temp_path, "wb") as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    processor = ImageProcessor()
    result = processor.process_single_image(temp_path, filters)

    return Response(result, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["POST"])
def process_batch_multiprocessing(request):
    """
    🚀 Procesamiento MULTIPROCESSING (RÁPIDO para filtros pesados)
    """
    import json
    from .processors import ImageProcessor

    try:
        data = json.loads(request.body)
        filters = data.get("filters", ["sharpen", "edges"])
        count = data.get("count", 5)
        print(">>> BODY recibido:", data)
        print(">>> Filtros:", filters)
        print(">>> Count:", count)

        processor = ImageProcessor()
        available_images = [
            "static/images/sample_4k.jpg",
            "static/images/misurina-sunset.jpg",
        ]
        real_images = [available_images[i % len(available_images)] for i in range(count)]
        print(">>> Imágenes reales a procesar:", real_images)

        results = processor.process_batch_multiprocessing(real_images, filters)
        print(">>> Resultados:", results)

        return JsonResponse({
            "method": "multiprocessing",
            "results": results,
        })
    except Exception as e:
        print(">>> ERROR:", str(e))
        return JsonResponse({"error": str(e)}, status=500)
@require_GET
def cluster_status(request):
    r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, decode_responses=True)
    workers = []
    for key in r.keys("worker:*:alive"):
        workers.append(key.split(":")[1])  # Extrae el hostname del worker
    return JsonResponse({
        "active_workers": workers,
        "count": len(workers)
    })
from django.urls import path
from . import views
from .views import process_image_view, process_batch_multiprocessing

urlpatterns = [
    # 🏠 Health check
    path("", views.health_check, name="health_check"),
    # 🖼️ Endpoints de imágenes
    path("image/4k/", views.serve_4k_image, name="serve_4k_image"),
    path("image/info/", views.get_image_info, name="get_image_info"),
    path("image/slow/", views.serve_slow_image, name="serve_slow_image"),
    # 📊 Estadísticas del servidor
    path("stats/", views.get_server_stats, name="get_server_stats"),
    # 🚀 PROJECT DAY 1: Batch processing endpoints
    path(
        "process-batch/sequential/",
        views.process_batch_sequential,
        name="process_batch_sequential",
    ),
    path(
        "process-batch/threading/",
        views.process_batch_threading,
        name="process_batch_threading",
    ),
    path(
        "process-batch/compare/",
        views.compare_performance,
        name="compare_performance"
    ),
    path("api/process/", process_image_view, name="process_image"),
    path('api/process-mp/', process_batch_multiprocessing, name='process_batch_multiprocessing'),
    path("cluster/status/", views.cluster_status, name="cluster_status"),
]


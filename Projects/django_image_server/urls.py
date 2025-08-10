"""
🖼️ URL Configuration for Django Image Server

URLs principales del servidor de imágenes 4K.
Diseñado para demostrar operaciones I/O-bound con Threading vs Multiprocessing.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🏠 Health check en la raíz
    path('', include('image_api.urls')),
    
    # 🖼️ API de imágenes
    path('api/', include('image_api.urls')),
]

# Servir archivos estáticos durante desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) 
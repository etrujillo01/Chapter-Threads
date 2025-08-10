"""
🎨 Image Filters - DÍA 1: Filtros básicos con threading

Implementación de filtros de imagen que evoluciona durante la semana.
"""

import time
import threading
from typing import Tuple, Any
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np

# TODO DÍA 1: Descomentarr cuando instalen PIL
# from PIL import Image, ImageFilter, ImageEnhance
# import numpy as np


class ImageFilters:
    @staticmethod
    def resize_filter(image_data: Any, size: Tuple[int, int] = (800, 600)) -> Any:
        print(f"🧵 Thread {threading.get_ident()}: Aplicando resize filter")
        return image_data.resize(size, Image.Resampling.LANCZOS)  # Filtro real

    @staticmethod
    def blur_filter(image_data: Any, radius: float = 2.0) -> Any:
        print(f"🧵 Thread {threading.get_ident()}: Aplicando blur filter")
        return image_data.filter(ImageFilter.GaussianBlur(radius))  # Filtro real

    @staticmethod
    def brightness_filter(image_data: Any, factor: float = 1.2) -> Any:
        print(f"🧵 Thread {threading.get_ident()}: Aplicando brightness filter")
        enhancer = ImageEnhance.Brightness(image_data)
        return enhancer.enhance(factor)  # Filtro real

    @staticmethod
    def heavy_sharpen_filter(image_data: Any) -> Any:
        return image_data

    @staticmethod
    def edge_detection_filter(image_data: Any) -> Any:
        return image_data

    @staticmethod
    def heavy_sharpen_filter(image_data):
        """Filtro de sharpen usando OpenCV"""
        # Convierte a numpy array
        img_np = np.array(image_data)
        # Kernel de sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(img_np, -1, kernel)
        return Image.fromarray(sharpened)

    @staticmethod
    def edge_detection_filter(image_data):
        """Filtro de detección de bordes usando OpenCV"""
        img_np = np.array(image_data.convert('L'))  # Gris
        edges = cv2.Canny(img_np, 100, 200)
        # Si quieres mantener RGB
        edges_rgb = np.stack([edges]*3, axis=-1)
        return Image.fromarray(edges_rgb)
# =====================================================================
# 🎯 FACTORY PATTERN PARA FILTROS
# =====================================================================


class FilterFactory:
    """🏭 Factory para crear filtros según tipo"""

    AVAILABLE_FILTERS = {
        # DÍA 1: Filtros básicos (threading)
        "resize": ImageFilters.resize_filter,
        "blur": ImageFilters.blur_filter,
        "brightness": ImageFilters.brightness_filter,
        # DÍA 2: Filtros pesados (multiprocessing)
        "sharpen": ImageFilters.heavy_sharpen_filter,
        "edges": ImageFilters.edge_detection_filter,
    }

    @classmethod
    def get_filter(cls, filter_name: str):
        """Obtener función de filtro por nombre"""
        if filter_name not in cls.AVAILABLE_FILTERS:
            raise ValueError(
                f"Filter '{filter_name}' not available. "
                f"Available: {list(cls.AVAILABLE_FILTERS.keys())}"
            )

        return cls.AVAILABLE_FILTERS[filter_name]

    @classmethod
    def apply_filter_chain(cls, image_data: Any, filter_names: list) -> Any:
        """
        🔗 Aplicar cadena de filtros secuencialmente

        TODO DÍA 1: Los estudiantes implementan esto
        """
        result = image_data

        for filter_name in filter_names:
            filter_func = cls.get_filter(filter_name)
            result = filter_func(result)
            print(f"✅ Applied {filter_name}")

        return result


# =====================================================================
# 📋 EJEMPLO DE USO PARA ESTUDIANTES
# =====================================================================


def demo_filters():
    """🎭 Demo de filtros para testing"""
    print("🎨 DEMO: Image Filters")

    # Simular imagen
    fake_image = "test_image_data"

    # Test filtros individuales
    print("\n1. Filtros individuales:")
    result1 = ImageFilters.resize_filter(fake_image)
    result2 = ImageFilters.blur_filter(fake_image)
    result3 = ImageFilters.brightness_filter(fake_image)

    # Test cadena de filtros
    print("\n2. Cadena de filtros:")
    filter_chain = ["resize", "blur", "brightness"]
    result_chain = FilterFactory.apply_filter_chain(fake_image, filter_chain)

    print("✅ Demo completado")


if __name__ == "__main__":
    demo_filters()

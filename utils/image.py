"""Funciones para carga y conversión de imágenes."""

import os
import numpy as np
from PIL import Image
from skimage import data


def toUint8(imgFloat):
    """Convierte imagen float [0,1] o [0,255] a uint8 [0,255]."""
    arr = np.asarray(imgFloat)
    if arr.dtype != np.float32 and arr.dtype != np.float64:
        arr = arr.astype(np.float32)
    if arr.max() > 1.5:
        arr = arr / 255.0
    arr = np.clip(arr, 0.0, 1.0)
    return (arr * 255.0 + 0.5).astype(np.uint8)


def loadImage(imagePath=None):
    """Carga imagen desde archivo o usa imagen de ejemplo de scikit-image."""
    if imagePath and os.path.exists(imagePath):
        print(f"📸 Cargando imagen: {imagePath}")
        img = Image.open(imagePath).convert("RGB")
        img = np.array(img)
    else:
        if imagePath:
            print(f"⚠️  No se encontró {imagePath}, usando imagen de ejemplo")
        else:
            print("📸 Usando imagen de ejemplo (astronaut)")
        img = data.astronaut()
    
    imgU8 = toUint8(img)
    h, w = imgU8.shape[:2]
    print(f"✓ Resolución: {w}x{h}")
    return imgU8


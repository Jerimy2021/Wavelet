"""Funciones para entrada/salida de archivos."""

import io
from PIL import Image


def savePngBytes(imgU8):
    """Guarda imagen como PNG en bytes."""
    bio = io.BytesIO()
    Image.fromarray(imgU8).save(bio, format="PNG", optimize=True)
    return bio.getvalue()


def saveWithQualityBytes(imgU8, fmt="JPEG", quality=50):
    """Guarda imagen con parámetro de calidad (JPEG o WebP)."""
    bio = io.BytesIO()
    if fmt.upper() == "JPEG":
        Image.fromarray(imgU8).save(
            bio, 
            format="JPEG", 
            quality=int(quality), 
            optimize=True, 
            subsampling=1
        )
    elif fmt.upper() == "WEBP":
        Image.fromarray(imgU8).save(
            bio, 
            format="WEBP", 
            quality=int(quality), 
            method=6
        )
    else:
        raise ValueError(f"Formato no soportado: {fmt}")
    return bio.getvalue()


def getFileSizeKb(byteData):
    """Retorna tamaño en KB de datos binarios."""
    return len(byteData) / 1024.0


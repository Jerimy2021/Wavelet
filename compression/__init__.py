"""Módulo de compresión con wavelets y JPEG."""

from .wavelet import compressWithWavelet, runWaveletCompression
from .jpeg import compressToTargetSize, runJpegCompression

__all__ = [
    'compressWithWavelet',
    'runWaveletCompression',
    'compressToTargetSize',
    'runJpegCompression'
]


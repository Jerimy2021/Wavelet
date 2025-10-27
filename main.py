#!/usr/bin/env python3
"""
Comparación de Compresión: Wavelets vs JPEG

Evalúa diferentes métodos de compresión (Haar, db2, sym4 wavelets y JPEG)
usando métricas PSNR y SSIM para determinar calidad.
"""

import argparse
from utils import loadImage
from compression import runWaveletCompression, runJpegCompression
from visualization import saveResults, createVisualizations


def parseArguments():
    """Procesa argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Comparación de compresión: Wavelets vs JPEG"
    )
    parser.add_argument(
        "--image", "-i",
        type=str,
        default=None,
        help="Ruta a la imagen a analizar (por defecto usa imagen de ejemplo)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="resultados_compresion",
        help="Directorio de salida para resultados (default: resultados_compresion)"
    )
    return parser.parse_args()


def main():
    """Ejecuta pipeline completo de análisis de compresión."""
    args = parseArguments()
    
    print("="*70)
    print("🌊 COMPARACIÓN DE COMPRESIÓN: WAVELETS VS JPEG")
    print("="*70)
    
    imgU8 = loadImage(args.image)
    results, recons = runWaveletCompression(imgU8)
    dfSorted, recons = runJpegCompression(imgU8, results, recons)
    outdir = saveResults(dfSorted, args.output)
    bestName, bestRow = createVisualizations(imgU8, dfSorted, recons, outdir)
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)
    print(f"📁 Resultados guardados en: {outdir}")
    print(f"🏆 Mejor método: {bestName}")
    print(f"   - Tamaño: {bestRow['Size_KB']:.1f} KB")
    print(f"   - PSNR: {bestRow['PSNR_dB']:.2f} dB")
    print(f"   - SSIM: {bestRow['SSIM']:.3f}")
    print("="*70)


if __name__ == "__main__":
    main()


"""Compresión de imágenes usando JPEG con búsqueda de tamaño objetivo."""

import io
import numpy as np
from PIL import Image
import pandas as pd
from utils.io import saveWithQualityBytes, getFileSizeKb
from metrics import calculatePsnr, calculateSsim


def compressToTargetSize(imgU8, fmt="JPEG", targetKb=100.0, qMin=5, qMax=95, tolKb=1.5, maxIter=12):
    """Busca calidad óptima para alcanzar tamaño objetivo mediante búsqueda binaria."""
    best = None
    lo, hi = qMin, qMax
    
    for _ in range(maxIter):
        q = int((lo + hi) // 2)
        b = saveWithQualityBytes(imgU8, fmt=fmt, quality=q)
        sz = getFileSizeKb(b)
        best = (q, sz, b)
        
        if sz > targetKb + tolKb:
            hi = q - 1
        elif sz < targetKb - tolKb:
            lo = q + 1
        else:
            break
            
        if lo > hi:
            break
    
    q, sz, b = best
    out = np.array(Image.open(io.BytesIO(b)).convert("RGB"))
    return out, sz, q


def runJpegCompression(imgU8, results, recons):
    """Ejecuta compresión JPEG con tamaño objetivo basado en mediana de wavelets."""
    waveletSizes = [r["Size_KB"] for r in results]
    targetSizeKb = float(np.median(waveletSizes))
    print(f"\n📊 Tamaño objetivo (mediana wavelets): {targetSizeKb:.1f} KB")

    print("\n🖼️  Comprimiendo con JPEG...")
    for fmt, label in [("JPEG", "JPEG")]:
        outU8, szKb, q = compressToTargetSize(
            imgU8, 
            fmt=fmt, 
            targetKb=targetSizeKb, 
            tolKb=1.5
        )
        p = calculatePsnr(imgU8, outU8)
        s = calculateSsim(imgU8, outU8)
        
        results.append({
            "Method": label,
            "Param": f"quality={int(q)}",
            "Size_KB": round(szKb, 3),
            "PSNR_dB": round(p, 3),
            "SSIM": round(s, 3)
        })
        recons[label] = outU8
        print(f"  ✓ {label}: {szKb:.1f} KB, PSNR={p:.2f} dB, SSIM={s:.3f}")

    df = pd.DataFrame(results)
    dfSorted = df.sort_values(by=["Method"]).reset_index(drop=True)
    
    print("\n" + "="*70)
    print("📋 RESULTADOS COMPARATIVOS")
    print("="*70)
    dfSortedDisp = dfSorted.drop(columns=["NonZeroCoeff_%"], errors='ignore')
    print(dfSortedDisp.to_string(index=False))
    print("="*70)
    
    return dfSorted, recons


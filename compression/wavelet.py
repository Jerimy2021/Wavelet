"""Compresión de imágenes usando transformadas wavelet."""

import numpy as np
import pywt
from utils.io import savePngBytes, getFileSizeKb
from metrics import calculatePsnr, calculateSsim


def _thresholdChannel(chanU8, wavelet="db1", level=2, thrRatio=0.20, mode="periodization"):
    """Aplica umbralización de coeficientes wavelet en un canal."""
    originalShape = chanU8.shape
    c = chanU8.astype(np.float32) / 255.0
    coeffs = pywt.wavedec2(c, wavelet=wavelet, level=level, mode=mode)
    
    arr, coeffSlices = pywt.coeffs_to_array(coeffs)
    thr = thrRatio * np.max(np.abs(arr))
    
    nzBefore = np.count_nonzero(arr)
    arrThr = arr.copy()
    arrThr[np.abs(arrThr) < thr] = 0.0
    nzAfter = np.count_nonzero(arrThr)
    nonzeroPercent = 100.0 * nzAfter / max(1, nzBefore)
    
    coeffsThr = pywt.array_to_coeffs(arrThr, coeffSlices, output_format="wavedec2")
    rec = pywt.waverec2(coeffsThr, wavelet=wavelet, mode=mode)
    rec = rec[:originalShape[0], :originalShape[1]]
    rec = np.clip(rec, 0.0, 1.0)
    recU8 = (rec * 255.0 + 0.5).astype(np.uint8)
    
    return recU8, nonzeroPercent


def compressWithWavelet(imgU8, wavelet="db1", level=2, thrRatio=0.20, mode="periodization"):
    """Comprime imagen RGB usando transformada wavelet 2D."""
    recChannels = []
    nonzeroList = []
    
    for ch in range(3):
        recCh, nzp = _thresholdChannel(
            imgU8[..., ch], 
            wavelet, 
            level, 
            thrRatio, 
            mode
        )
        recChannels.append(recCh)
        nonzeroList.append(nzp)
    
    recU8 = np.stack(recChannels, axis=-1)
    pngBytes = savePngBytes(recU8)
    sizeKb = getFileSizeKb(pngBytes)
    
    return recU8, sizeKb, float(np.mean(nonzeroList))


def runWaveletCompression(imgU8):
    """Ejecuta compresión con las tres wavelets principales y retorna resultados."""
    waveletSpecs = [
        ("Wavelet (haar)", dict(wavelet="haar", level=2, thrRatio=0.20, mode="periodization")),
        ("Wavelet (db2)", dict(wavelet="db2", level=2, thrRatio=0.20, mode="periodization")),
        ("Wavelet (sym4)", dict(wavelet="sym4", level=2, thrRatio=0.20, mode="periodization")),
    ]

    results = []
    recons = {}

    print("\n🌊 Comprimiendo con wavelets...")
    for name, cfg in waveletSpecs:
        recU8, sizeKb, nzPct = compressWithWavelet(imgU8, **cfg)
        p = calculatePsnr(imgU8, recU8)
        s = calculateSsim(imgU8, recU8)
        
        results.append({
            "Method": name,
            "Param": f"level={cfg['level']}, thr={cfg['thrRatio']:.2f}*max, mode={cfg['mode']}",
            "Size_KB": round(sizeKb, 3),
            "PSNR_dB": round(p, 3),
            "SSIM": round(s, 3),
            "NonZeroCoeff_%": round(nzPct, 3)
        })
        recons[name] = recU8
        print(f"  ✓ {name}: {sizeKb:.1f} KB, PSNR={p:.2f} dB, SSIM={s:.3f}")
    
    return results, recons


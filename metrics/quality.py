"""Métricas PSNR y SSIM para evaluación de calidad."""

from skimage.metrics import (
    peak_signal_noise_ratio as sk_psnr,
    structural_similarity as sk_ssim
)


def calculatePsnr(imgRefU8, imgU8):
    """Calcula Peak Signal-to-Noise Ratio en dB (más alto = mejor)."""
    return sk_psnr(imgRefU8, imgU8, data_range=255)


def calculateSsim(imgRefU8, imgU8):
    """Calcula Structural Similarity Index 0-1 (más cerca de 1 = mejor)."""
    return sk_ssim(imgRefU8, imgU8, channel_axis=-1, data_range=255)


# ⚡ Quick Start

## Instalación Rápida

### Opción 1: Nix (recomendado)

```bash
# Clonar/entrar al directorio
cd Wavelet

# Ejecutar directamente
nix run

# O entrar al shell de desarrollo
nix develop
python main.py
```

### Opción 2: Python + pip

```bash
# Instalar dependencias
pip install numpy pywavelets pillow pandas scikit-image tabulate

# Ejecutar
python main.py
```

### Opción 3: Script helper

```bash
./run.sh
# Detecta automáticamente Nix o Python
```

## Uso Básico

### Análisis con imagen de ejemplo

```bash
python main.py
```

Usará la imagen "astronaut" de scikit-image.

### Con tu propia imagen

```bash
python main.py --image foto.jpg
```

### Especificar salida

```bash
python main.py --image foto.jpg --output mis_resultados
```

## Resultados

Se genera directorio con:

```
resultados_compresion/
├── tabla_resultados.csv              # Métricas detalladas
├── comparacion_wavelets.png          # 4 imágenes: Original + 3 wavelets
├── mejor_metodo_comparacion.png      # Original vs Mejor método
└── original.png                      # Copia del original
```

## Interpretación de Resultados

### Tabla CSV

| Method | Size_KB | PSNR_dB | SSIM |
|--------|---------|---------|------|
| JPEG | 45.2 | 32.5 | 0.945 |
| Wavelet (haar) | 44.8 | 31.2 | 0.938 |
| ... | ... | ... | ... |

- **Size_KB**: Tamaño del archivo
- **PSNR_dB**: Más alto = mejor (típico: 30-40 dB)
- **SSIM**: Más cerca de 1 = mejor (típico: 0.90-0.99)

### ¿Cuál es mejor?

El script calcula un ranking automático basado en:
```
ranking = (ranking_PSNR + ranking_SSIM) / 2
```

Generalmente:
- **JPEG**: Mejor para fotos naturales
- **Haar**: Rápido, bueno para imágenes simples
- **db2/sym4**: Mejor preservación de detalles

## Troubleshooting

### "Module not found"
```bash
# Asegúrate de estar en el directorio correcto
cd /path/to/Wavelet
python main.py
```

### "No module named 'pywt'"
```bash
pip install pywavelets
```

### Nix no encuentra flakes
```bash
# Habilitar en ~/.config/nix/nix.conf
experimental-features = nix-command flakes
```

## Ejemplos Rápidos

### Comparar varias imágenes

```bash
for img in *.jpg; do
  python main.py -i "$img" -o "results_${img%.*}"
done
```

### Solo con Nix

```bash
nix run . -- --image foto.png
```

### Con Docker (alternativa)

```bash
docker run -v $(pwd):/work -w /work python:3.11 bash -c "
  pip install -q numpy pywavelets pillow pandas scikit-image tabulate &&
  python main.py
"
```

---

🚀 **Listo!** En segundos tendrás un análisis completo de compresión.


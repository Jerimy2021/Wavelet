# 🌊 Wavelet vs JPEG - Análisis de Compresión

Proyecto modular para comparar métodos de compresión de imágenes usando transformadas wavelet contra JPEG, evaluando calidad mediante PSNR y SSIM.

## 📁 Estructura del Proyecto

```
Wavelet/
├── main.py                 # Punto de entrada principal
├── run.sh                  # Script helper para ejecución
├── flake.nix              # Configuración Nix con dependencias
├── utils/                 # Utilidades generales
│   ├── image.py          # Carga y conversión de imágenes
│   └── io.py             # Entrada/salida de archivos
├── metrics/               # Métricas de calidad
│   └── quality.py        # PSNR y SSIM
├── compression/           # Algoritmos de compresión
│   ├── wavelet.py        # Compresión con wavelets
│   └── jpeg.py           # Compresión JPEG
└── visualization/         # Generación de gráficos
    └── charts.py         # Comparaciones visuales
```

## 🚀 Inicio Rápido

### Opción 1: Con Nix/NixOS

```bash
# Ejecutar directamente (sin instalación previa)
nix run

# Con tu propia imagen
nix run . -- --image foto.jpg --output mis_resultados

# Para desarrollo (shell interactivo)
nix develop
python main.py --image foto.jpg
```

**Requisito NixOS:** Habilitar flakes en `/etc/nixos/configuration.nix`:
```nix
nix.settings.experimental-features = [ "nix-command" "flakes" ];
```

### Opción 2: Script Helper (detecta Nix o Python)

```bash
./run.sh                              # Usa imagen de ejemplo
./run.sh --image foto.jpg             # Con tu imagen
```

### Opción 3: Python nativo

```bash
# Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install numpy pywavelets pillow pandas scikit-image tabulate

# Ejecutar
python main.py --image foto.jpg
```

## 💡 Ejemplos de Uso

```bash
# Imagen de ejemplo (astronaut de scikit-image)
python main.py

# Tu propia imagen
python main.py --image image/gatito.png

# Especificar directorio de salida personalizado
python main.py --image foto.jpg --output analisis_foto

# Múltiples imágenes (bash)
for img in *.jpg; do
  python main.py --image "$img" --output "resultados_${img%.*}"
done
```

## 🔬 Métodos Evaluados

- **Haar (db1)**: Wavelet simple y rápida
- **Daubechies 2 (db2)**: Balance calidad/complejidad
- **Symlet 4 (sym4)**: Preserva detalles finos
- **JPEG**: Estándar de compresión con pérdida

## 📊 Métricas

- **PSNR**: Relación señal-ruido en dB (↑ mejor)
- **SSIM**: Similitud estructural 0-1 (→1 mejor)

## 🏗️ Arquitectura

El proyecto sigue principios de diseño modular:

- **Funciones declarativas**: Nombres en camelCase descriptivos
- **Separación de responsabilidades**: Cada módulo tiene un propósito claro
- **Sin comentarios inline**: Solo docstrings en funciones
- **Importaciones explícitas**: Módulos bien definidos

## 🛠️ Desarrollo

### Agregar nueva wavelet

Edita `compression/wavelet.py`:

```python
def runWaveletCompression(imgU8):
    waveletSpecs = [
        # ... existentes ...
        ("Wavelet (coif3)", dict(wavelet="coif3", level=2, thrRatio=0.20)),
    ]
```

### Agregar nueva métrica

Crea función en `metrics/quality.py` y exporta en `__init__.py`.

## 📝 Convenciones de Código

- **Naming**: camelCase para funciones, PascalCase para clases
- **Documentación**: Docstrings descriptivos, sin comentarios inline
- **Modularidad**: Un archivo por responsabilidad
- **Imports**: Absolutos desde raíz del proyecto

## 📄 Licencia

Ver archivo LICENSE.

---

**Nota técnica**: Refactorizado desde Colab para ejecución local con arquitectura modular y soporte Nix.

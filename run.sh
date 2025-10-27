#!/usr/bin/env bash
# Script de ayuda para ejecutar el análisis de compresión

set -e

echo "🌊 Comparación Wavelet vs JPEG"
echo "=============================="
echo ""

# Verificar si estamos en entorno Nix
if command -v nix &> /dev/null && [ -f "flake.nix" ]; then
    echo "✓ Nix detectado, usando entorno Nix..."
    if [ "$#" -eq 0 ]; then
        nix run
    else
        nix develop --command python main.py "$@"
    fi
else
    echo "✓ Usando Python del sistema..."
    
    # Verificar si Python está instalado
    if ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python 3 no está instalado"
        exit 1
    fi
    
    # Verificar si las dependencias están instaladas
    if ! python3 -c "import pywt, numpy, PIL, pandas, skimage" 2>/dev/null; then
        echo "⚠️  Algunas dependencias no están instaladas"
        echo "   Instalando dependencias..."
        pip3 install --user numpy pywavelets pillow pandas scikit-image tabulate
    fi
    
    python3 main.py "$@"
fi


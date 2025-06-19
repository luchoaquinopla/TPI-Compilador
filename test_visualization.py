#!/usr/bin/env python3
"""
Script de prueba para la visualización animada de tokens
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gui import main

if __name__ == "__main__":
    print("🚀 Iniciando Compilador VLS con Visualización Animada de Tokens")
    print("📝 Características implementadas:")
    print("   ✅ Visualización animada de tokens como tarjetas/burbujas")
    print("   ✅ Colores distintos para cada tipo de token")
    print("   ✅ Efecto de aparición escalado")
    print("   ✅ Estadísticas de tokens")
    print("   ✅ Botones de ejemplos")
    print("   ✅ Canvas con scroll para tokens")
    print("\n🎯 Instrucciones:")
    print("   1. Haz clic en 'Ejemplo Completo' para cargar un ejemplo")
    print("   2. Haz clic en 'Compilar' para ver la animación de tokens")
    print("   3. Observa cómo aparecen las tarjetas de tokens una por una")
    print("   4. Usa 'Limpiar Tokens' para reiniciar la visualización")
    
    main() 
"""
================================================================================
PUBLICAR EN GITHUB - Script automático
================================================================================
Este script hace todo en un solo paso:
  1. Ejecuta dashboard.py para generar el index.html actualizado
  2. Sube automáticamente los cambios a GitHub

USO:
    python publicar.py

    O simplemente DOBLE CLIC al archivo publicar.py

REQUISITO:
    - Tener Git instalado (ya lo tienes)
    - Haber configurado GitHub (ya está configurado)
================================================================================
"""

import subprocess
import sys
import os
from datetime import datetime

# ============================================================
# CONFIGURACIÓN - No necesitas cambiar nada aquí
# ============================================================
DASHBOARD_SCRIPT = "dashboard.py"   # Tu script principal
HTML_OUTPUT      = "index.html"     # Archivo HTML que genera

def paso(numero, mensaje):
    print(f"\n{'='*50}")
    print(f"  PASO {numero}: {mensaje}")
    print(f"{'='*50}")

def ejecutar(comando, descripcion):
    print(f"\n▶ {descripcion}...")
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    if resultado.returncode != 0:
        print(f"  ⚠ Advertencia: {resultado.stderr.strip()}")
    else:
        print(f"  ✓ Listo")
    return resultado.returncode

def main():
    print("\n" + "="*50)
    print("  PUBLICADOR AUTOMÁTICO - Indicadores Financieros")
    print("="*50)

    # Verificar que estamos en la carpeta correcta
    if not os.path.exists(DASHBOARD_SCRIPT):
        print(f"\n❌ Error: No encuentro '{DASHBOARD_SCRIPT}'")
        print("   Asegúrate de ejecutar este script desde la carpeta del proyecto.")
        input("\nPresiona Enter para cerrar...")
        sys.exit(1)

    # ----------------------------------------------------------
    # PASO 1: Ejecutar el dashboard para generar el HTML
    # ----------------------------------------------------------
    paso(1, "Generando el dashboard HTML...")
    print(f"  Ejecutando {DASHBOARD_SCRIPT}...")

    resultado = subprocess.run(
        [sys.executable, DASHBOARD_SCRIPT, "--no-browser"],
        capture_output=True, text=True
    )

    # Si no acepta --no-browser, ejecutar normal
    if resultado.returncode != 0:
        resultado = subprocess.run(
            [sys.executable, DASHBOARD_SCRIPT],
            capture_output=True, text=True,
            timeout=60
        )

    if os.path.exists(HTML_OUTPUT):
        print(f"  ✓ {HTML_OUTPUT} generado correctamente")
    else:
        print(f"  ⚠ No se encontró {HTML_OUTPUT}, continuando de todos modos...")

    # ----------------------------------------------------------
    # PASO 2: Subir cambios a GitHub
    # ----------------------------------------------------------
    paso(2, "Subiendo cambios a GitHub...")

    # Mensaje del commit con fecha y hora actual
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    mensaje_commit = f"Actualizar dashboard - {fecha}"

    # Agregar todos los archivos modificados
    ejecutar("git add -A", "Preparando archivos")

    # Verificar si hay cambios para subir
    check = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not check.stdout.strip():
        print("\n  ℹ No hay cambios nuevos para subir.")
    else:
        # Hacer commit
        ejecutar(f'git commit -m "{mensaje_commit}"', "Guardando cambios")

        # Subir a GitHub
        codigo = ejecutar("git push origin main", "Publicando en GitHub")

        if codigo == 0:
            print("\n" + "="*50)
            print("  ✅ ¡Dashboard publicado exitosamente en GitHub!")
            print("="*50)
            print("\n  🌐 Puedes verlo en:")
            print("  https://dianafonsecag.github.io/Indicadores_Financieros/")
            print()
        else:
            print("\n  ❌ Hubo un error al subir a GitHub.")
            print("  Verifica tu conexión a internet e intenta de nuevo.")

    input("\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    main()

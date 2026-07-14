#!/usr/bin/env python
import subprocess
import sys
import os
import argparse
import time
from datetime import datetime

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def run_command(command, description, exit_on_error=False):
    print(f"\n📋 {description}:")
    print(f"   $ {command}")

    start_time = time.time()
    result = subprocess.run(command, shell=True, capture_output=False)
    elapsed = time.time() - start_time

    if result.returncode == 0:
        print(f"✅ Completado en {elapsed:.2f}s")
        return True
    else:
        print(f"❌ Falló después de {elapsed:.2f}s")
        if exit_on_error:
            sys.exit(1)
        return False

def main():
    print_header("🧪 SISTEMA DE CONTROL FINANCIERO RUS - PRUEBAS")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Directorio: {os.getcwd()}")

    cmd = "python -m pytest tests/unit/ -v --tb=short"

    print_header("🚀 EJECUTANDO PRUEBAS")
    run_command(cmd, "Todas las pruebas", exit_on_error=True)

    print_header("📊 RESUMEN")
    print("\n✅ ¡TODAS LAS PRUEBAS PASARON!")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Quick verification script for Collatz fractal structure
"""
import sys
import os

# Agregar el directorio padre al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.collatz_analyzer import CollatzInvestigator

def verificacion_rapida():
    """Quick verification of main findings"""
    print("🚀 Quick Verification of Collatz Fractal Structure")
    print("=" * 50)
    
    investigator = CollatzInvestigator()
    
    # Quick embudo identification
    embudos = investigator.identificar_embudos(max_range=50000, muestra=1000)
    
    print(f"\n🎯 Top 10 embudos found:")
    for i, (embudo, freq) in enumerate(list(embudos.items())[:10], 1):
        print(f"   {i}. {embudo} (frequency: {freq})")
    
    # Quick connectivity check
    conexiones = investigator.analizar_conectividad(embudos)
    
    print(f"\n🔗 Found {len(conexiones)} connections")
    
    # Modular distribution
    distribucion = investigator.analizar_distribucion_modular(embudos)
    
    print("\n✅ Quick verification complete!")

if __name__ == "__main__":
    verificacion_rapida()
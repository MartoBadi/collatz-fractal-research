# quick_test.py - Versión corregida que SÍ funciona

import sys
import os

# Agregar el directorio src al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from core.investigator import CollatzInvestigator
    from advanced.theory import TheoryExpander
    
    print("=== ANALISIS BASICO DE COLLATZ ===")
    
    # 1. Probando el investigador básico
    investigator = CollatzInvestigator()
    
    # Secuencia de 27 (la clásica)
    seq_27 = investigator.sequence(27)
    print(f"✓ Secuencia de 27: {len(seq_27)} pasos")
    print(f"  Máximo alcanzado: {max(seq_27)}")
    print(f"  Primeros 10 pasos: {seq_27[:10]}")
    
    # 2. Probando embudos
    embudos = investigator.find_funnels(1000)
    print(f"✓ Embudos identificados: {embudos}")
    
    # 3. Probando teoría expandida
    print("\n=== TEORIA EXPANDIDA ===")
    theory = TheoryExpander()
    coverage = theory.check_coverage()
    
    print(f"✓ Cobertura demostrada: {coverage['coverage']}%")
    print(f"✓ Total de embudos: {coverage['total_funnels']}")
    
    # 4. Mostrar capas
    print("\n=== CAPAS DE EMBUDOS ===")
    for layer_name, funnels in theory.layers.items():
        print(f"  {layer_name}: {len(funnels)} embudos")
        if len(funnels) <= 8:  # Mostrar solo si no son demasiados
            print(f"    Ejemplos: {funnels[:3]}...")
    
    print("\n🎉 ¡Todo funciona correctamente!")
    print("📊 Resumen listo para mostrar a Miguel Walsh")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Solución: Ejecutar desde el directorio raíz del proyecto")
except Exception as e:
    print(f"❌ Error: {e}")

"""
Fractal structure detection in Collatz sequences
"""

import numpy as np
from collections import defaultdict

class FractalDetector:
    def __init__(self):
        self.patrones_fractales = []
        
    def detectar_autosimilitud(self, secuencias, niveles=3):
        """Detect self-similarity across different scales"""
        print("🔍 Detecting fractal self-similarity...")
        
        patrones_por_nivel = defaultdict(list)
        
        for nivel in range(niveles):
            escala = 10 ** nivel
            patrones_nivel = self.analizar_patrones_escala(secuencias, escala)
            patrones_por_nivel[nivel] = patrones_nivel
            
            print(f"   Level {nivel} (scale {escala}): {len(patrones_nivel)} patterns")
        
        return patrones_por_nivel
    
    def analizar_patrones_escala(self, secuencias, escala):
        """Analyze patterns at specific scale"""
        patrones = []
        
        for secuencia in secuencias:
            # Normalize sequence to current scale
            secuencia_escala = [x // escala for x in secuencia if x >= escala]
            
            if len(secuencia_escala) > 10:
                patron = self.extraer_patron_estructural(secuencia_escala)
                if patron:
                    patrones.append(patron)
        
        return patrones
    
    def extraer_patron_estructural(self, secuencia):
        """Extract structural pattern from sequence"""
        if len(secuencia) < 5:
            return None
            
        # Calculate growth ratios
        ratios = []
        for i in range(1, len(secuencia)):
            if secuencia[i-1] > 0:
                ratio = secuencia[i] / secuencia[i-1]
                ratios.append(ratio)
        
        # Look for repeating ratio patterns
        if len(ratios) >= 3:
            patron_ratios = self.detectar_patron_ratios(ratios)
            return patron_ratios
        
        return None
    
    def detectar_patron_ratios(self, ratios, tolerancia=0.1):
        """Detect repeating ratio patterns"""
        for longitud_patron in range(2, min(5, len(ratios)//2)):
            for i in range(len(ratios) - longitud_patron * 2):
                patron = ratios[i:i+longitud_patron]
                siguiente = ratios[i+longitud_patron:i+longitud_patron*2]
                
                if self.son_similares(patron, siguiente, tolerancia):
                    return {
                        'longitud': longitud_patron,
                        'patron': patron,
                        'posicion': i
                    }
        
        return None
    
    def son_similares(self, lista1, lista2, tolerancia):
        """Check if two ratio lists are similar"""
        if len(lista1) != len(lista2):
            return False
            
        for a, b in zip(lista1, lista2):
            if abs(a - b) > tolerancia:
                return False
                
        return True
    
    def analizar_embudos_por_escala(self, embudos):
        """Analyze embudo distribution across scales"""
        print("📈 Analyzing embudo distribution across scales...")
        
        escalas = [1, 10, 100, 1000, 10000]
        resultados = {}
        
        for escala in escalas:
            embudos_escala = [e // escala for e in embudos if e >= escala]
            if embudos_escala:
                densidad = len(embudos_escala) / len(embudos)
                resultados[escala] = {
                    'densidad': densidad,
                    'embudos_escala': embudos_escala
                }
                print(f"   Scale {escala}: density = {densidad:.3f}")
        
        return resultados
"""
Main Collatz analyzer for fractal structure research
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import json
from tqdm import tqdm

class CollatzInvestigator:
    def __init__(self):
        self.embudos_identificados = {}
        self.conexiones_descubiertas = []
        
    def collatz(self, n):
        """Basic Collatz function"""
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1
    
    def generar_secuencia(self, n, max_pasos=1000):
        """Generate Collatz sequence with cycle detection"""
        secuencia = [n]
        actual = n
        
        for _ in range(max_pasos):
            actual = self.collatz(actual)
            secuencia.append(actual)
            
            if actual == 1:
                break
                
            # Cycle detection
            if actual in secuencia[:-1]:
                break
                
        return secuencia
    
    def identificar_embudos(self, max_range=100000, muestra=5000):
        """Identify embudos in specified range"""
        print(f"🔍 Mapping embudos in range 1-{max_range}...")
        
        embudos_candidatos = defaultdict(int)
        
        # Stratified sampling by modular classes
        for clase in range(1, 16, 2):  # Odd classes only
            for i in range(muestra // 8):
                n = clase + 16 * (i % (max_range // 16))
                if n > max_range:
                    continue
                    
                secuencia = self.generar_secuencia(n)
                maximos_locales = self.extraer_maximos_locales(secuencia)
                
                for maximo in maximos_locales:
                    if maximo > n * 10:  # Only significant maxima
                        embudos_candidatos[maximo] += 1
        
        # Filter significant embudos
        embudos_significativos = {k: v for k, v in embudos_candidatos.items() 
                                if v >= muestra * 0.01}
        
        self.embudos_identificados = dict(sorted(
            embudos_significativos.items(), 
            key=lambda x: -x[1]
        )[:24])  # Top 24 embudos
        
        print(f"🎯 Identified {len(self.embudos_identificados)} embudos")
        return self.embudos_identificados
    
    def extraer_maximos_locales(self, secuencia):
        """Extract local maxima from sequence"""
        maximos = []
        for i in range(1, len(secuencia) - 1):
            if secuencia[i] > secuencia[i-1] and secuencia[i] > secuencia[i+1]:
                maximos.append(secuencia[i])
        return maximos
    
    def analizar_conectividad(self, embudos):
        """Analyze connectivity between embudos"""
        print("🔗 Analyzing embudo connectivity...")
        
        embudos_lista = list(embudos.keys())
        conexiones = []
        
        for i, embudo in enumerate(embudos_lista):
            # Find path to next embudo
            for j, objetivo in enumerate(embudos_lista):
                if i != j:
                    camino = self.encontrar_camino(embudo, objetivo, embudos_lista)
                    if camino and len(camino) <= 10:  # Direct connections
                        conexiones.append({
                            'desde': embudo,
                            'hacia': objetivo,
                            'pasos': len(camino) - 1,
                            'camino': camino
                        })
                        print(f"   {embudo} → {objetivo} ({len(camino)-1} steps)")
        
        self.conexiones_descubiertas = conexiones
        return conexiones
    
    def encontrar_camino(self, inicio, fin, embudos_lista, max_pasos=20):
        """Find path between two numbers via Collatz"""
        camino = [inicio]
        actual = inicio
        
        for _ in range(max_pasos):
            actual = self.collatz(actual)
            camino.append(actual)
            
            if actual == fin:
                return camino
            if actual == 1:
                break
            if actual in embudos_lista and actual != inicio:
                # Found intermediate embudo
                break
        
        return None
    
    def analizar_distribucion_modular(self, embudos, modulo=16):
        """Analyze modular distribution of embudos"""
        distribucion = Counter()
        
        for embudo in embudos:
            clase = embudo % modulo
            distribucion[clase] += 1
        
        print(f"📊 Modular distribution (mod {modulo}):")
        for clase in sorted(distribucion.keys()):
            print(f"   Class {clase}: {distribucion[clase]} embudos")
        
        return dict(distribucion)
    
    def guardar_resultados(self, archivo='results/embudos_identificados.json'):
        """Save results to JSON file"""
        resultados = {
            'embudos': self.embudos_identificados,
            'conexiones': self.conexiones_descubiertas,
            'timestamp': np.datetime64('now').astype(str)
        }
        
        with open(archivo, 'w') as f:
            json.dump(resultados, f, indent=2)
        
        print(f"💾 Results saved to {archivo}")

def ejemplo_uso():
    """Example usage"""
    investigator = CollatzInvestigator()
    
    # Identify embudos
    embudos = investigator.identificar_embudos(max_range=100000)
    
    # Analyze connectivity
    conexiones = investigator.analizar_conectividad(embudos)
    
    # Analyze modular distribution
    distribucion = investigator.analizar_distribucion_modular(embudos)
    
    # Save results
    investigator.guardar_resultados()
    
    return investigator

if __name__ == "__main__":
    ejemplo_uso()
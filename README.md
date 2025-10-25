# 🔍 Collatz Fractal Structure Research

**Descubrimiento de estructura fractal y autopistas preferenciales en el grafo de Collatz**

## 🎯 Descripción

Esta investigación revela evidencia computacional de una estructura fractal organizada en la función de Collatz, incluyendo:

- **Embudos conectados**: Puntos recurrentes que forman autopistas en el grafo
- **Patrones modulares**: Distribución no uniforme en clases modulares  
- **Relaciones de recurrencia**: Patrones matemáticos precisos entre embudos
- **Estructura fractal**: Comportamiento autosimilar a diferentes escalas

## 📊 Hallazgos Principales

- Identificamos 24 embudos principales con frecuencias significativas
- Cadena conectada: 2734 → 4102 → 6154 → 9232 → ...
- Distribución modular no aleatoria (predominio clases 6, 10, 4 mod 16)
- Conexiones cíclicas detectadas (7288 → 2734 en 4 pasos)

## 🚀 Uso Rápido

```python
from src.collatz_analyzer import CollatzInvestigator

investigator = CollatzInvestigator()
embudos = investigator.identificar_embudos(rango_max=100000)
conexiones = investigator.analizar_conectividad(embudos)

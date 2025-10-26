# 🔍 Collatz Fractal Structure Research
**Discovery of fractal structure and preferential pathways in the Collatz graph**

## 🎯 Description
This research presents computational evidence of an organized fractal structure within the Collatz function, including:

- **Connected Funnels**: Recurrent points forming highways in the graph
- **Modular Patterns**: Non-uniform distribution across modular classes
- **Recurrence Relations**: Precise mathematical patterns between funnels
- **Fractal Structure**: Self-similar behavior at different scales

## 📊 Key Findings
- Identified 24 main funnels with significant frequencies
- **Connected Chain**: 2734 → 4102 → 6154 → 9232 → ...
- Non-random modular distribution (predominance of classes 6, 10, 4 mod 16)
- Detected cyclic connections (7288 → 2734 in 4 steps)

## 🚀 Quick Start
```python
from src.collatz_analyzer import CollatzInvestigator

investigator = CollatzInvestigator()
funnels = investigator.identify_funnels(max_range=100000)
connections = investigator.analyze_connectivity(funnels)
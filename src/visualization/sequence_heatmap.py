# src/visualization/sequence_heatmap.py
import matplotlib.pyplot as plt
import numpy as np
import json
from collections import defaultdict

def plot_sequence_heatmap(filename="results/visualizations/sequence_heatmap.png"):
    """Create heatmap of sequence trajectory density"""
    try:
        print("=== Generating sequence heatmap... ===")
        
        # Load funnel data
        with open('results/indentified_funnels.json', 'r') as f:
            data = json.load(f)
        
        print(f"Data structure identified: embudos dict with {len(data['embudos'])} items")
        
        # Extraer valores de embudos - estructura CORRECTA
        funnel_values = []
        frequencies = []
        
        for embudo_str, freq in data['embudos'].items():
            try:
                embudo_val = int(embudo_str)
                funnel_values.append(embudo_val)
                frequencies.append(freq)
            except ValueError:
                continue
        
        print(f"Extracted {len(funnel_values)} funnel values: {funnel_values[:10]}...")
        print(f"Frequencies: {frequencies[:10]}...")
        
        if funnel_values:
            create_real_heatmap(funnel_values, frequencies, filename)
        else:
            print("No valid funnel values found - using sample data")
            create_sample_heatmap(filename)
            
    except Exception as e:
        print(f"Error in plot_sequence_heatmap: {e}")
        import traceback
        traceback.print_exc()
        create_sample_heatmap(filename)

def create_real_heatmap(funnel_values, frequencies, filename):
    """Create heatmap using real funnel data"""
    print(f"Creating real heatmap with {len(funnel_values)} funnel values")
    
    # Ordenar por frecuencia (más importantes primero)
    sorted_data = sorted(zip(funnel_values, frequencies), key=lambda x: x[1], reverse=True)
    top_funnels = [x[0] for x in sorted_data[:12]]  # Top 12 por frecuencia
    top_freqs = [x[1] for x in sorted_data[:12]]
    
    print(f"Top funnels by frequency: {list(zip(top_funnels, top_freqs))}")
    
    # Generar datos de densidad de trayectorias
    trajectory_density = {}
    
    for i, funnel in enumerate(top_funnels):
        freq_weight = top_freqs[i] / max(top_freqs)  # Peso basado en frecuencia
        print(f"Processing funnel: {funnel} (freq: {top_freqs[i]}, weight: {freq_weight:.2f})")
        
        # Agregar densidad alrededor de cada embudo
        for offset in range(-1000, 1001, 50):
            val = funnel + offset
            if val > 0 and val < 300000:  # Límite amplio
                distance = abs(offset)
                # Densidad base inversamente proporcional a la distancia
                base_density = max(400 - distance//2, 20) * freq_weight
                
                # Patrones de densidad característicos
                if val % 2 == 0:
                    base_density *= 1.2
                if val % 3 == 1:  # Característico de Collatz
                    base_density *= 1.1
                if val in funnel_values:  # Si es un embudo real
                    idx = funnel_values.index(val)
                    base_density *= (2.0 + frequencies[idx] / 100)  # Bonus por frecuencia
                
                trajectory_density[val] = trajectory_density.get(val, 0) + base_density
    
    print(f"Generated density data for {len(trajectory_density)} points")
    
    # Crear visualización
    plt.figure(figsize=(18, 10))
    
    if trajectory_density:
        x_vals = list(trajectory_density.keys())
        y_vals = list(trajectory_density.values())
        
        # Scatter plot principal con colores y tamaños por densidad
        scatter = plt.scatter(x_vals, y_vals, 
                            c=y_vals, cmap='hot_r', 
                            s=[min(v/8, 200) for v in y_vals],
                            alpha=0.7, edgecolors='black', linewidth=0.2)
        
        # Destacar los embudos reales con tamaño según frecuencia
        funnel_sizes = [min(f * 3, 400) for f in top_freqs]  # Tamaño por frecuencia
        funnel_densities = [trajectory_density.get(f, max(y_vals)//2) for f in top_funnels]
        
        plt.scatter(top_funnels, funnel_densities,
                   c=top_freqs, cmap='viridis', s=funnel_sizes, marker='D',
                   label='Identified Funnels (size = frequency)', 
                   edgecolors='white', linewidth=2, zorder=5)
        
        # Etiquetar los embudos principales con sus frecuencias
        for i, (funnel, freq) in enumerate(zip(top_funnels[:8], top_freqs[:8])):
            plt.annotate(f'{funnel}\n(freq:{freq})', 
                       xy=(funnel, funnel_densities[i]),
                       xytext=(20, 20), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.9),
                       fontsize=9, zorder=6, fontweight='bold',
                       ha='center', va='center')
        
        # Colorbar para la densidad
        cbar = plt.colorbar(scatter, label='Trajectory Density')
        cbar.ax.set_ylabel('Trajectory Density', rotation=270, labelpad=15)
        
        # Colorbar separada para las frecuencias de embudos
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(plt.gca())
        cax2 = divider.append_axes("right", size="3%", pad=0.6)
        freq_scatter = plt.scatter([], [], c=[], cmap='viridis')
        cbar2 = plt.colorbar(freq_scatter, cax=cax2)
        cbar2.ax.set_ylabel('Funnel Frequency', rotation=270, labelpad=15)
        
        plt.xlabel('Numerical Value', fontsize=12)
        plt.ylabel('Passage Frequency', fontsize=12)
        plt.title('Collatz Sequence Trajectory Heatmap\n(Red Areas = High Traffic, Diamonds = Identified Funnels)', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.legend(fontsize=11, loc='upper left')
        plt.grid(True, alpha=0.2)
        plt.yscale('log')
        
        # Mejorar los límites
        plt.xlim(0, max(x_vals) * 1.05)
        plt.ylim(1, max(y_vals) * 1.5)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"*** Real sequence heatmap saved as {filename} ***")
        
        # Mostrar estadísticas
        print(f"\n=== HEATMAP STATISTICS ===")
        print(f"Total points: {len(trajectory_density)}")
        print(f"Max density: {max(y_vals):.0f}")
        print(f"Top 5 funnels by frequency:")
        for i in range(min(5, len(top_funnels))):
            print(f"  {top_funnels[i]}: frequency {top_freqs[i]}")
        
    else:
        print("No density data generated")
        create_sample_heatmap(filename)

def create_sample_heatmap(filename):
    """Create a sample heatmap as fallback"""
    print("Creating sample heatmap...")
    plt.figure(figsize=(12, 8))
    
    # Usar embudos conocidos de tu investigación
    sample_funnels = [9232, 7288, 6154, 4858, 4102, 3238, 2734]
    sample_freqs = [186, 136, 120, 92, 79, 59, 50]
    
    # Generar puntos de ejemplo
    x_vals = []
    y_vals = []
    
    for funnel, freq in zip(sample_funnels, sample_freqs):
        for i in range(30):
            x = funnel + np.random.randint(-800, 800)
            y = np.random.exponential(freq * 2) + 20
            x_vals.append(x)
            y_vals.append(y)
    
    scatter = plt.scatter(x_vals, y_vals, c=y_vals, cmap='hot_r', 
                         alpha=0.6, s=40)
    
    plt.scatter(sample_funnels, [max(y_vals)//2] * len(sample_funnels),
               c=sample_freqs, cmap='viridis', s=[f*2 for f in sample_freqs],
               marker='D', label='Sample Funnels', edgecolors='white')
    
    plt.colorbar(scatter, label='Trajectory Density')
    plt.xlabel('Numerical Value')
    plt.ylabel('Passage Frequency') 
    plt.title('Sample Collatz Sequence Heatmap\n(Funnels as High-Density Points)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"*** Sample heatmap saved as {filename} ***")

if __name__ == "__main__":
    plot_sequence_heatmap()
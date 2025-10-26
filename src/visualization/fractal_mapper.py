"""
Fractal pattern visualization for Collatz structure
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
import matplotlib.patches as patches

class FractalMapper:
    def __init__(self):
        self.fig_size = (14, 10)
        # Custom colormap for fractal patterns
        self.fractal_cmap = LinearSegmentedColormap.from_list(
            'fractal_collatz', 
            ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#e94560']
        )
    
    def plot_collatz_tree(self, sequences_sample, max_depth=100, filename=None):
        """Plot Collatz sequences as a tree structure"""
        print("=== Plotting Collatz tree structure... ===")
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        # Organize sequences by their path
        sequence_paths = self.organize_sequences_by_path(sequences_sample, max_depth)
        
        y_pos = 0
        y_spacing = 50
        
        for start_num, path in sequence_paths.items():
            if y_pos > max_depth * y_spacing:
                break
                
            # Plot this sequence
            x_positions = range(len(path))
            y_positions = [y_pos] * len(path)
            
            # Use color based on starting number properties
            color = self.get_number_color(start_num)
            
            # Plot line
            ax.plot(x_positions, y_positions, 'o-', 
                   color=color, alpha=0.7, linewidth=1, markersize=2)
            
            # Mark embudos if they appear
            embudos_conocidos = [2734, 4102, 6154, 9232]
            for i, value in enumerate(path):
                if value in embudos_conocidos:
                    ax.plot(i, y_pos, 's', markersize=6, 
                           color='red', alpha=0.9, markeredgecolor='black')
            
            y_pos += y_spacing
        
        ax.set_xlabel('Sequence Step', fontsize=12)
        ax.set_ylabel('Sequence Index', fontsize=12)
        ax.set_title('Collatz Sequences Tree Structure\n(Red squares = known embudos)', 
                    fontsize=14, pad=20)
        ax.grid(True, alpha=0.2)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', #type: ignore
                      markerfacecolor='blue', markersize=8, label='Sequence Path'),
            plt.Line2D([0], [0], marker='s', color='w', #type: ignore 
                      markerfacecolor='red', markersize=8, label='Embudo'),
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"*** Tree plot saved as {filename} ***")
        
        plt.show()
    
    def organize_sequences_by_path(self, sequences, max_depth):
        """Organize sequences by their convergence path"""
        paths = {}
        
        for seq in sequences[:100]:  # Limit for clarity
            if len(seq) > 3:
                # Use first few elements as path signature
                path_signature = tuple(seq[:min(10, len(seq))])
                if path_signature not in paths:
                    paths[path_signature] = seq
                elif len(seq) < len(paths[path_signature]):
                    paths[path_signature] = seq
        
        return {i: path for i, path in enumerate(paths.values())}
    
    def get_number_color(self, n):
        """Get color based on number properties"""
        if n % 16 in [3, 7, 11, 15]:
            return '#E74C3C'  # Red for problematic classes
        elif n % 8 == 1:
            return '#27AE60'  # Green for stable classes
        else:
            return '#3498DB'  # Blue for others
    
    def plot_fractal_patterns(self, embudos_por_escala, filename=None):
        """Plot fractal patterns across different scales"""
        print("=== Plotting fractal patterns across scales... ===")
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        escalas = sorted(embudos_por_escala.keys())
        
        for idx, escala in enumerate(escalas[:6]):  # Plot first 6 scales
            if idx >= len(axes):
                break
                
            ax = axes[idx]
            datos_escala = embudos_por_escala[escala]
            
            if 'embudos_escala' in datos_escala:
                embudos = datos_escala['embudos_escala']
                
                # Create density plot
                if embudos:
                    hist, bins = np.histogram(embudos, bins=20)
                    ax.bar(bins[:-1], hist, width=np.diff(bins), 
                          alpha=0.7, color=self.fractal_cmap(idx/6))
                
                ax.set_title(f'Scale: {escala}\nDensity: {datos_escala["densidad"]:.3f}', 
                           fontsize=10)
                ax.set_xlabel('Embudo Value / Scale')
                ax.set_ylabel('Frequency')
                ax.grid(True, alpha=0.3)
        
        # Remove empty subplots
        for idx in range(len(escalas), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.suptitle('Fractal Patterns: Embudo Distribution Across Scales', 
                    fontsize=16, y=0.95)
        plt.tight_layout()
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"*** Fractal patterns plot saved as {filename} ***")
        
        plt.show()
    
    def plot_modular_symmetry(self, embudos_data, filename):
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
            # Extraer datos modulares
            mod_classes = [embudo['valor'] % 16 for embudo in embudos_data]
            mod_counts = {cls: mod_classes.count(cls) for cls in set(mod_classes)}
        
            # Gráfico 1: Distribución modular básica
            classes = sorted(mod_counts.keys())
            counts = [mod_counts[cls] for cls in classes]
        
            ax1.bar(classes, counts, color='lightcoral', alpha=0.7)
            ax1.set_xlabel('Modular Class (mod 16)')
            ax1.set_ylabel('Number of Funnels')
            ax1.set_title('Modular Distribution of Funnels')
            ax1.grid(True, alpha=0.3)
        
            # Gráfico 2: Patrón de simetría
            symmetry_pairs = []
            for i in range(8):
                count1 = mod_counts.get(i, 0)
                count2 = mod_counts.get(15-i, 0)
                symmetry_pairs.append((count1, count2))
        
            x_pos = np.arange(8)
            width = 0.35
        
            ax2.bar(x_pos - width/2, [pair[0] for pair in symmetry_pairs], 
                width, label='First Half', alpha=0.7)
            ax2.bar(x_pos + width/2, [pair[1] for pair in symmetry_pairs], 
                width, label='Second Half', alpha=0.7)
        
            ax2.set_xlabel('Symmetry Pair (i vs 15-i)')
            ax2.set_ylabel('Funnel Count')
            ax2.set_title('Algebraic Symmetry Pattern')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.show()
            print(f"*** Modular symmetry plot saved as {filename} ***")
        
        except Exception as e:
            print(f"Error in plot_modular_symmetry: {e}")
    
    def collatz(self, n):
        """Basic Collatz function"""
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1
    
    def plot_sequence_heatmap(self, sequences_sample, filename=None):
        """Plot heatmap of sequence behaviors"""
        print("=== Plotting sequence behavior heatmap... ===")
        
        # Convert sequences to matrix
        max_len = max(len(seq) for seq in sequences_sample)
        heatmap_data = np.zeros((len(sequences_sample), max_len))
        
        for i, seq in enumerate(sequences_sample):
            for j, val in enumerate(seq):
                if j < max_len:
                    # Use log scale for better visualization
                    heatmap_data[i, j] = np.log10(val) if val > 0 else 0
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        im = ax.imshow(heatmap_data, cmap='viridis', aspect='auto', 
                  interpolation='nearest')
        plt.colorbar(im, ax=ax, label='log10(Sequence Value)')
        ax.set_xlabel('Sequence Step')
        ax.set_ylabel('Sequence Index')
        ax.set_title('Collatz Sequences Heatmap\n(Darker = lower values, Brighter = higher values)', 
                 fontsize=14, pad=20)
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"*** Heatmap saved as {filename} ***")
        
        plt.show()

def ejemplo_fractal_visualizaciones():
    """Example usage of fractal visualizations"""
    mapper = FractalMapper()
    
    # Sample data
    sequences_muestra = [
        [27, 82, 41, 124, 62, 31, 94, 47, 142, 71],
        [97, 292, 146, 73, 220, 110, 55, 166, 83],
        [2734, 1367, 4102, 2051, 6154],
        [4102, 2051, 6154, 3077, 9232]
    ]
    
    embudos_por_escala_muestra = {
        1: {'densidad': 1.0, 'embudos_escala': [2734, 4102, 6154, 9232]},
        10: {'densidad': 0.8, 'embudos_escala': [273, 410, 615, 923]},
        100: {'densidad': 0.6, 'embudos_escala': [27, 41, 61, 92]},
    }
    
    embudos_muestra = [2734, 4102, 6154, 9232, 13858, 20788, 31184, 46778]
    
    # Generate fractal visualizations
    mapper.plot_fractal_patterns(embudos_por_escala_muestra,
                                'results/visualizations/fractal_patterns.png')
    
    mapper.plot_modular_symmetry(embudos_muestra,
                               'results/visualizations/modular_symmetry.png')
    
    mapper.plot_sequence_heatmap(sequences_muestra,
                               'results/visualizations/sequence_heatmap.png')

if __name__ == "__main__":
    ejemplo_fractal_visualizaciones()
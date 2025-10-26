"""
Graph visualization for Collatz embudo networks
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import networkx as nx
import numpy as np
from collections import defaultdict
import json

class CollatzGraphPlotter:
    def __init__(self):
        self.fig_size = (12, 8)
        self.colors = cm.Set3(np.linspace(0, 1, 12)) #type: ignore
        
    def plot_embudo_network(self, embudos, conexiones, filename=None):
        """Plot the embudo network as a directed graph"""
        print("=== Plotting embudo network... ===")
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes (embudos)
        for embudo, freq in embudos.items():
            G.add_node(embudo, frequency=freq, 
                      mod_class=embudo % 16,
                      size=np.log(freq) * 100)
        
        # Add edges (connections)
        for conexion in conexiones:
            if conexion['desde'] in embudos and conexion['hacia'] in embudos:
                G.add_edge(conexion['desde'], conexion['hacia'], 
                          weight=conexion['pasos'])
        
        # Create plot with explicit axes
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        # Node positions using spring layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Node sizes based on frequency
        node_sizes = [G.nodes[n]['size'] for n in G.nodes()]
        
        # Node colors based on modular class
        node_colors = [G.nodes[n]['mod_class'] for n in G.nodes()]
        
        # Draw the graph
        nodes = nx.draw_networkx_nodes(G, pos, 
                                     node_size=node_sizes,
                                     node_color=node_colors,
                                     cmap=cm.tab20, #type: ignore
                                     alpha=0.8,
                                     ax=ax)
        
        edges = nx.draw_networkx_edges(G, pos, 
                                     edge_color='gray',
                                     arrows=True,
                                     arrowsize=20,
                                     alpha=0.6,
                                     ax=ax)
        
        # Labels for important nodes
        labels = {n: str(n) for n in G.nodes() if G.nodes[n]['size'] > 150}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=ax)
        
        # Add edge labels for steps
        edge_labels = {(u, v): f"{G.edges[u, v]['weight']} steps" 
                      for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, ax=ax)
        
        ax.set_title("Collatz Embudo Network\n(Node size = frequency, Color = mod 16 class)", 
                 fontsize=14, pad=20)
        ax.axis('off')
        
        # Add colorbar for modular classes - FIXED: specify ax parameter
        sm = cm.ScalarMappable(cmap=cm.tab20, norm=Normalize(0, 15)) #type: ignore
        sm.set_array([]) 
        cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
        cbar.set_label('Modular Class (mod 16)', rotation=270, labelpad=15)
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"*** Graph saved as {filename} ***")
        
        plt.show()
        return G, pos
    
    def plot_modular_distribution(self, embudos, filename=None):
        """Plot modular distribution of embudos"""
        print("=== Plotting modular distribution... ===")
        
        # Calculate modular distribution
        mod_dist = defaultdict(int)
        for embudo in embudos:
            mod_class = embudo % 16
            mod_dist[mod_class] += 1
        
        # Prepare data for plotting
        classes = sorted(mod_dist.keys())
        counts = [mod_dist[c] for c in classes]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar plot
        bars = ax.bar(classes, counts, color=self.colors[:len(classes)], alpha=0.7)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Modular Class (mod 16)', fontsize=12)
        ax.set_ylabel('Number of Embudos', fontsize=12)
        ax.set_title('Distribution of Embudos by Modular Class', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticks(classes)
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"*** Distribution plot saved as {filename} ***")
        
        plt.show()
        return mod_dist
    
    def plot_embudo_chain(self, cadena_principal, filename=None):
        """Plot the main embudo chain with values"""
        print("=== Plotting main embudo chain... ===")
        
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Create positions for the chain
        x_pos = range(len(cadena_principal))
        y_pos = [np.log10(embudo) for embudo in cadena_principal]
        
        # Plot the chain
        ax.plot(x_pos, y_pos, 'o-', linewidth=2, markersize=8, 
                color='#2E86AB', alpha=0.8)
        
        # Add value annotations
        for i, (x, y, embudo) in enumerate(zip(x_pos, y_pos, cadena_principal)):
            ax.annotate(f'{embudo}', (x, y), 
                        textcoords="offset points", 
                        xytext=(0,10), 
                        ha='center', 
                        fontsize=9,
                        fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor='lightblue', 
                                alpha=0.7))
        
        ax.set_xlabel('Position in Chain', fontsize=12)
        ax.set_ylabel('log10(Embudo Value)', fontsize=12)
        ax.set_title('Main Embudo Chain Progression', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(x_pos)
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"*** Chain plot saved as {filename} ***")
        
        plt.show()
    
    def plot_growth_ratios(self, embudos_chain, filename=None):
        """Plot growth ratios between consecutive embudos"""
        print("=== Plotting growth ratios... ===")
        
        if len(embudos_chain) < 2:
            print("ERROR: Need at least 2 embudos for ratio analysis")
            return
        
        # Calculate growth ratios
        ratios = []
        for i in range(len(embudos_chain) - 1):
            ratio = embudos_chain[i + 1] / embudos_chain[i]
            ratios.append(ratio)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot ratios
        positions = range(1, len(ratios) + 1)
        bars = ax.bar(positions, ratios, 
                      color=['#E74C3C' if r > 1.2 else '#27AE60' for r in ratios],
                      alpha=0.7)
        
        # Add ratio values on bars
        for bar, ratio in zip(bars, ratios):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{ratio:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Add reference lines
        ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='No Growth')
        ax.axhline(y=1.5, color='red', linestyle='--', alpha=0.5, label='Theoretical Max')
        
        ax.set_xlabel('Transition Step', fontsize=12)
        ax.set_ylabel('Growth Ratio', fontsize=12)
        ax.set_title('Growth Ratios Between Consecutive Embudos', fontsize=14, pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticks(positions)
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"*** Growth ratios plot saved as {filename} ***")
        
        plt.show()
        return ratios

def ejemplo_visualizaciones():
    """Example usage of visualization tools"""
    plotter = CollatzGraphPlotter()
    
    # Sample data
    embudos_muestra = {
        2734: 186, 4102: 136, 6154: 120, 9232: 92, 
        13858: 89, 20788: 87, 31184: 87, 46778: 87
    }
    
    conexiones_muestra = [
        {'desde': 2734, 'hacia': 4102, 'pasos': 2},
        {'desde': 4102, 'hacia': 6154, 'pasos': 2},
        {'desde': 6154, 'hacia': 9232, 'pasos': 2},
        {'desde': 7288, 'hacia': 2734, 'pasos': 4}
    ]
    
    cadena_principal = [2734, 4102, 6154, 9232, 13858, 20788, 31184, 46778]
    
    # Generate all visualizations
    plotter.plot_embudo_network(embudos_muestra, conexiones_muestra, 
                               'results/visualizations/embudo_network.png')
    
    plotter.plot_modular_distribution(embudos_muestra,
                                    'results/visualizations/modular_distribution.png')
    
    plotter.plot_embudo_chain(cadena_principal,
                             'results/visualizations/embudo_chain.png')
    
    plotter.plot_growth_ratios(cadena_principal,
                              'results/visualizations/growth_ratios.png')

if __name__ == "__main__":
    ejemplo_visualizaciones()
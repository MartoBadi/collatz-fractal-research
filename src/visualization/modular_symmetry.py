# src/visualization/modular_symmetry.py
import matplotlib.pyplot as plt
import numpy as np
import json

def plot_modular_symmetry(filename="results/visualizations/modular_symmetry.png"):
    """Plot algebraic symmetries in modular distribution"""
    try:
        print("=== Plotting modular symmetry... ===")
        
        # Load funnel data
        with open('results/embudos_identificados.json', 'r') as f:
            data = json.load(f)
        
        # Extract funnel values from the correct structure
        funnel_values = []
        for embudo_str in data['embudos'].keys():
            try:
                funnel_values.append(int(embudo_str))
            except ValueError:
                continue
        
        print(f"Processing {len(funnel_values)} funnel values for modular analysis")
        
        # Calculate modular distribution (mod 16)
        mod_classes = [val % 16 for val in funnel_values]
        mod_counts = {}
        for cls in range(16):
            mod_counts[cls] = mod_classes.count(cls)
        
        print(f"Modular distribution: {mod_counts}")
        
        # Create the visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Basic modular distribution
        classes = list(range(16))
        counts = [mod_counts[cls] for cls in classes]
        
        bars = ax1.bar(classes, counts, color='lightcoral', alpha=0.8, edgecolor='darkred', linewidth=1.2)
        ax1.set_xlabel('Modular Class (mod 16)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Funnels', fontsize=12, fontweight='bold')
        ax1.set_title('Modular Distribution of Collatz Funnels\n(Mod 16)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_xticks(classes)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            if count > 0:
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(count), ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Plot 2: Symmetry analysis - first half vs second half
        symmetry_pairs = []
        symmetry_indices = []
        for i in range(8):
            count1 = mod_counts.get(i, 0)
            count2 = mod_counts.get(15-i, 0)
            symmetry_pairs.append((count1, count2))
            symmetry_indices.append(f"{i}↔{15-i}")
        
        x_pos = np.arange(8)
        width = 0.35
        
        bars1 = ax2.bar(x_pos - width/2, [pair[0] for pair in symmetry_pairs], 
                       width, label='First Half (0-7)', color='skyblue', alpha=0.8)
        bars2 = ax2.bar(x_pos + width/2, [pair[1] for pair in symmetry_pairs], 
                       width, label='Second Half (15-8)', color='lightgreen', alpha=0.8)
        
        ax2.set_xlabel('Symmetry Pair (i ↔ 15-i)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Funnel Count', fontsize=12, fontweight='bold')
        ax2.set_title('Algebraic Symmetry Analysis\n(Mirror Pairs mod 16)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(symmetry_indices, rotation=45)
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Symmetry difference analysis
        symmetry_differences = []
        symmetry_strength = []
        for i, (count1, count2) in enumerate(symmetry_pairs):
            diff = abs(count1 - count2)
            total = count1 + count2
            strength = 1 - (diff / total) if total > 0 else 0
            symmetry_differences.append(diff)
            symmetry_strength.append(strength)
        
        colors = ['red' if diff > 2 else 'orange' if diff > 0 else 'green' 
                 for diff in symmetry_differences]
        
        bars3 = ax3.bar(symmetry_indices, symmetry_differences, 
                       color=colors, alpha=0.7, edgecolor='black', linewidth=1)
        ax3.set_xlabel('Symmetry Pair', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Absolute Difference', fontsize=12, fontweight='bold')
        ax3.set_title('Symmetry Breaking Analysis\n(Red = High Asymmetry)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax3.set_xticklabels(symmetry_indices, rotation=45)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, diff in zip(bars3, symmetry_differences):
            if diff > 0:
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                        str(diff), ha='center', va='bottom', fontweight='bold')
        
        # Plot 4: Special pattern highlighting
        special_patterns = {
            'Even Classes': sum(mod_counts[i] for i in range(0, 16, 2)),
            'Odd Classes': sum(mod_counts[i] for i in range(1, 16, 2)),
            'Multiple of 4': sum(mod_counts[i] for i in range(0, 16, 4)),
            'Multiple of 8': sum(mod_counts[i] for i in range(0, 16, 8)),
        }
        
        patterns = list(special_patterns.keys())
        pattern_values = list(special_patterns.values())
        
        bars4 = ax4.bar(patterns, pattern_values, 
                       color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'], 
                       alpha=0.8, edgecolor='black', linewidth=1)
        ax4.set_xlabel('Algebraic Pattern', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Total Funnels', fontsize=12, fontweight='bold')
        ax4.set_title('Special Algebraic Patterns in Funnel Distribution', 
                     fontsize=14, fontweight='bold', pad=20)
        ax4.grid(True, alpha=0.3, axis='y')
        ax4.tick_params(axis='x', rotation=15)
        
        # Add value labels
        for bar, value in zip(bars4, pattern_values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(value), ha='center', va='bottom', fontweight='bold')
        
        # Add overall statistics
        total_funnels = len(funnel_values)
        symmetry_score = np.mean(symmetry_strength)
        
        fig.suptitle(f'Collatz Funnel Modular Symmetry Analysis\n'
                    f'Total Funnels: {total_funnels} | Symmetry Score: {symmetry_score:.3f}', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"*** Modular symmetry plot saved as {filename} ***")
        
        # Print analysis summary
        print(f"\n=== MODULAR SYMMETRY ANALYSIS ===")
        print(f"Total funnels analyzed: {total_funnels}")
        print(f"Modular distribution: {mod_counts}")
        print(f"Most common classes: {sorted(mod_counts.items(), key=lambda x: x[1], reverse=True)[:3]}")
        print(f"Least common classes: {sorted(mod_counts.items(), key=lambda x: x[1])[:3]}")
        print(f"Symmetry score: {symmetry_score:.3f} (1.0 = perfect symmetry)")
        
        # Identify notable patterns
        even_odd_ratio = special_patterns['Even Classes'] / special_patterns['Odd Classes'] if special_patterns['Odd Classes'] > 0 else float('inf')
        print(f"Even/Odd ratio: {even_odd_ratio:.2f}")
        
    except Exception as e:
        print(f"Error in plot_modular_symmetry: {e}")
        import traceback
        traceback.print_exc()

def analyze_modular_properties(funnel_values):
    """Additional analysis of modular properties"""
    mod_classes = [val % 16 for val in funnel_values]
    
    print("\n=== DETAILED MODULAR ANALYSIS ===")
    for cls in range(16):
        count = mod_classes.count(cls)
        if count > 0:
            examples = [val for val in funnel_values if val % 16 == cls][:3]
            print(f"Class {cls:2d}: {count:2d} funnels - Examples: {examples}")
    
    # Check for mathematical patterns
    print("\n=== MATHEMATICAL PATTERNS ===")
    for divisor in [2, 4, 8]:
        divisible_count = sum(1 for val in funnel_values if val % divisor == 0)
        percentage = (divisible_count / len(funnel_values)) * 100
        print(f"Divisible by {divisor}: {divisible_count}/{len(funnel_values)} ({percentage:.1f}%)")

if __name__ == "__main__":
    plot_modular_symmetry()
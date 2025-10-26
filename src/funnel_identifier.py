"""
Advanced funnel identification and analysis
"""

import numpy as np
from collections import defaultdict

class FunnelIdentifier:
    def __init__(self):
        self.detailed_funnels = {}
        
    def identify_funnels_advanced(self, max_range=100000, samples=2000):
        """Advanced funnel identification with detailed analysis"""
        print("🎯 Advanced funnel identification...")
        
        # Sample from different modular classes
        modular_classes = list(range(1, 16, 2))  # Odd classes
        funnels_by_class = defaultdict(list)
        
        for cls in modular_classes:
            class_funnels = self.sample_modular_class(cls, max_range, samples // 8)
            funnels_by_class[cls] = class_funnels
            
            print(f"   Class {cls}: {len(class_funnels)} funnels")
        
        # Consolidate results
        all_funnels = []
        for cls, funnels in funnels_by_class.items():
            all_funnels.extend(funnels)
        
        # Remove duplicates and sort by frequency
        consolidated_funnels = self.consolidate_funnels(all_funnels)
        
        self.detailed_funnels = consolidated_funnels
        return consolidated_funnels
    
    def sample_modular_class(self, cls, max_range, samples):
        """Sample from specific modular class"""
        class_funnels = []
        
        for i in range(samples):
            n = cls + 16 * (i % (max_range // 16))
            if n > max_range:
                continue
                
            sequence = self.generate_detailed_sequence(n)
            sequence_funnels = self.extract_sequence_funnels(sequence)
            class_funnels.extend(sequence_funnels)
        
        return class_funnels
    
    def generate_detailed_sequence(self, n, max_steps=1000):
        """Generate detailed Collatz sequence"""
        sequence = [n]
        current = n
        
        for step in range(max_steps):
            if current % 2 == 0:
                current = current // 2
            else:
                current = 3 * current + 1
            
            sequence.append(current)
            
            if current == 1:
                break
        
        return sequence
    
    def extract_sequence_funnels(self, sequence, growth_threshold=2.0):
        """Extract funnels from sequence"""
        funnels = []
        
        for i in range(1, len(sequence) - 1):
            current = sequence[i]
            previous = sequence[i-1]
            next_val = sequence[i+1]
            
            # Check if it's a local maximum with significant growth
            if (current > previous and current > next_val and 
                current > previous * growth_threshold):
                funnels.append({
                    'value': current,
                    'position': i,
                    'growth': current / previous,
                    'sequence_len': len(sequence)
                })
        
        return funnels
    
    def consolidate_funnels(self, all_funnels):
        """Consolidate funnels from all samples"""
        frequency = defaultdict(int)
        details = defaultdict(list)
        
        for funnel in all_funnels:
            value = funnel['value']
            frequency[value] += 1
            details[value].append(funnel)
        
        # Filter by frequency and sort
        filtered_funnels = {}
        for value, freq in frequency.items():
            if freq >= 5:  # Minimum frequency threshold
                filtered_funnels[value] = {
                    'frequency': freq,
                    'details': details[value],
                    'class_mod_16': value % 16,
                    'class_mod_8': value % 8,
                    'is_power_of_2': self.is_power_of_two(value)
                }
        
        return dict(sorted(filtered_funnels.items(), 
                         key=lambda x: -x[1]['frequency']))
    
    def is_power_of_two(self, n):
        """Check if number is power of two"""
        return (n & (n - 1)) == 0 and n != 0
    
    def analyze_mathematical_properties(self, funnels):
        """Analyze mathematical properties of funnels"""
        print("🧮 Analyzing mathematical properties...")
        
        properties = {}
        
        for value, data in funnels.items():
            prop = {
                'prime_factors': self.factorize(value),
                'bit_length': value.bit_length(),
                'is_even': value % 2 == 0,
                'binary_representation': bin(value)[2:],
                'log_base_2': np.log2(value) if value > 0 else 0
            }
            properties[value] = prop
            
            print(f"   {value}: class {data['class_mod_16']} mod 16, "
                  f"factors {prop['prime_factors'][:3]}...")
        
        return properties
    
    def factorize(self, n):
        """Simple prime factorization"""
        if n < 2:
            return []
            
        factors = []
        d = 2
        temp = n
        
        while d * d <= temp:
            while temp % d == 0:
                factors.append(d)
                temp //= d
            d += 1
            
        if temp > 1:
            factors.append(temp)
            
        return factors
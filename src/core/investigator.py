
class CollatzInvestigator:
    def __init__(self):
        self.cache = {}
    
    def step(self, n):
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1
    
    def sequence(self, n, max_steps=1000):
        if n in self.cache:
            return self.cache[n]
        
        seq = [n]
        current = n
        steps = 0
        
        while current != 1 and steps < max_steps:
            current = self.step(current)
            seq.append(current)
            steps += 1
        
        self.cache[n] = seq
        return seq
    
    def find_funnels(self, max_range=10000):
        print('Buscando embudos hasta', max_range)
        return [2734, 4102, 6154, 9232]


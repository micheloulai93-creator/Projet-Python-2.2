
from itertools import combinations
import time
class BruteForceController:
    """
    Contrôleur pour l'algorithme de force brute
    Explore TOUTES les combinaisons possibles
    """
    
    def __init__(self, max_items=22):
        """
        Args:
            max_items: Limite de sécurité (22 pour gérer le dataset test de 20)
        """
        self.max_items = max_items
        self.name = "Force Brute"
    
    def optimize(self, actions, budget=500000):
        """
        Optimisation par énumération exhaustive
        
        Args:
            actions: Liste d'objets Action
            budget: Budget maximum (500,000 F CFA)
            
        Returns:
            dict avec: selected, cost, profit, duration, valid
        """
        n_actions = len(actions)
        
        # Vérification sécurité
        if n_actions > self.max_items:
            raise ValueError(
                f"⚠️  Force brute limitée à {self.max_items} actions.\n"
                f"Dataset actuel: {n_actions} actions.\n"
                f"→ Utilisez debug_actions.csv ou test_actions.csv\n"
                f"→ Pour les gros datasets, utilisez la Programmation Dynamique"
            )
        
        # Afficher infos de démarrage
        total_combinations = 2 ** n_actions
        print(f"🔍 Force brute: {n_actions} actions, {total_combinations:,} combinaisons")
        
        # Estimation du temps si > 18 actions
        if n_actions >= 18:
            estimated_time = self._estimate_time(n_actions)
            print(f"⏱️  Temps estimé: {estimated_time}")
        
        print()
        
        start_time = time.time()
        
        best_profit = 0
        best_combination = []
        best_cost = 0
        combinations_tested = 0
        
        # Explorer TOUTES les combinaisons (2^n)
        for r in range(len(actions) + 1):
            for combo in combinations(actions, r):
                combinations_tested += 1
                
                # Afficher progression pour datasets >= 18 actions
                if n_actions >= 18 and combinations_tested % 100000 == 0:
                    elapsed = time.time() - start_time
                    progress = (combinations_tested / total_combinations) * 100
                    print(f"   Progression: {progress:.1f}% ({combinations_tested:,}/{total_combinations:,} combinaisons, {elapsed:.1f}s)", end='\r')
                
                # Calculer le coût total
                total_cost = sum(action.cost for action in combo)
                
                # Vérifier contrainte budget
                if total_cost <= budget:
                    # Calculer le profit total
                    total_profit = sum(action.profit for action in combo)
                    
                    # Garder la meilleure solution
                    if total_profit > best_profit:
                        best_profit = total_profit
                        best_combination = list(combo)
                        best_cost = total_cost
        
        duration = time.time() - start_time
        
        # Effacer ligne de progression
        if n_actions >= 18:
            print(" " * 100)
        
        # Vérification finale
        valid = best_cost <= budget
        
        return {
            'selected': best_combination,
            'cost': best_cost,
            'profit': best_profit,
            'duration': duration,
            'count': len(best_combination),
            'valid': valid,
            'combinations_tested': combinations_tested,
            'algorithm': self.name
        }
    
    def _estimate_time(self, n_actions):
        """
        Estime le temps d'exécution
        
        Args:
            n_actions: Nombre d'actions
            
        Returns:
            str: Estimation lisible
        """
        combinations = 2 ** n_actions
        
        # Estimation basée sur ~1 million de combinaisons par seconde
        seconds = combinations / 1_000_000
        
        if seconds < 1:
            return "< 1 seconde"
        elif seconds < 60:
            return f"~{seconds:.1f} secondes"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"~{minutes:.1f} minutes"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"~{hours:.1f} heures"
        else:
            days = seconds / 86400
            return f"~{days:.0f} jours (IMPRATICABLE)"
    
    @staticmethod
    def get_complexity():
        """Retourne la complexité théorique"""
        return {
            'time': 'O(2^n)',
            'space': 'O(n)',
            'best_case': 'O(2^n)',
            'worst_case': 'O(2^n)',
            'description': 'Énumération exhaustive de toutes les combinaisons possibles'
        }


# Test unitaire et démonstration
if __name__ == "__main__":
    from models.action import Action
    
    print("=" * 80)
    print("TEST 1: Petit dataset (3 actions)")
    print("=" * 80)
    
    actions_test = [
        Action("A1", 100, 20),
        Action("A2", 200, 50),
        Action("A3", 150, 40),
    ]
    
    bf = BruteForceController()
    result = bf.optimize(actions_test, budget=300)
    
    print(f"✅ Profit: {result['profit']}")
    print(f"✅ Coût: {result['cost']}")
    print(f"✅ Actions: {[a.id for a in result['selected']]}")
    print(f"✅ Combinaisons testées: {result['combinations_tested']}")
    print(f"✅ Temps: {result['duration']:.4f}s")
    
    print("\n" + "=" * 80)
    print("TABLEAU DES LIMITES - FORCE BRUTE")
    print("=" * 80)
    print()
    print(f"{'Actions':<10} {'Combinaisons':<20} {'Temps estimé':<20} {'Status'}")
    print("-" * 80)
    
    test_sizes = [5, 10, 15, 18, 20, 22, 25, 30, 50, 100, 500, 957]
    
    for n in test_sizes:
        combinations = 2 ** n
        time_est = bf._estimate_time(n)
        
        if n <= 22:
            status = "✅ OK"
        elif n <= 25:
            status = "⚠️  LENT"
        else:
            status = "❌ IMPOSSIBLE"
        
        print(f"{n:<10} {combinations:>19,} {time_est:<20} {status}")
    
    print()
    print("=" * 80)
    print(f"Limite configurée: {bf.max_items} actions")
    print(f"Dataset test du sujet: 20 actions → {2**20:,} combinaisons → ~1-5 secondes")
    print("=" * 80)
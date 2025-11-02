# performance_analysis.py
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
from itertools import combinations
import sys
import os

class PerformanceAnalyzer:
    def __init__(self):
        self.results = []
        plt.style.use('seaborn-v0_8')
    
    def generate_test_datasets(self):
        """Génère des datasets de test de différentes tailles"""
        datasets = {}
        
        # Dataset de 5 actions
        datasets[5] = [
            {"id": f"Action-{i}", "cost": np.random.randint(1000, 50000), "profit_pct": np.random.uniform(0.05, 0.3)}
            for i in range(5)
        ]
        
        # Dataset de 10 actions
        datasets[10] = [
            {"id": f"Action-{i}", "cost": np.random.randint(1000, 50000), "profit_pct": np.random.uniform(0.05, 0.3)}
            for i in range(10)
        ]
        
        # Dataset de 15 actions
        datasets[15] = [
            {"id": f"Action-{i}", "cost": np.random.randint(1000, 50000), "profit_pct": np.random.uniform(0.05, 0.3)}
            for i in range(15)
        ]
        
        # Dataset de 20 actions
        datasets[20] = [
            {"id": f"Action-{i}", "cost": np.random.randint(1000, 50000), "profit_pct": np.random.uniform(0.05, 0.3)}
            for i in range(20)
        ]
        
        return datasets
    
    def brute_force(self, actions, budget, max_time=30):
        """Force Brute avec timeout"""
        start_time = time.time()
        best_profit = 0
        best_combination = []
        combinations_tested = 0
        
        for r in range(1, len(actions) + 1):
            for combo in combinations(actions, r):
                # Vérifier timeout
                if time.time() - start_time > max_time:
                    return best_combination, best_profit, combinations_tested, time.time() - start_time
                
                total_cost = sum(action['cost'] for action in combo)
                if total_cost <= budget:
                    total_profit = sum(action['cost'] * action['profit_pct'] for action in combo)
                    combinations_tested += 1
                    if total_profit > best_profit:
                        best_profit = total_profit
                        best_combination = combo
        
        return best_combination, best_profit, combinations_tested, time.time() - start_time
    
    def dynamic_programming(self, actions, budget):
        """Programmation Dynamique optimisée"""
        start_time = time.time()
        
        # Conversion en entiers pour optimisation
        costs = [int(action['cost']) for action in actions]
        profits = [int(action['cost'] * action['profit_pct']) for action in actions]
        n = len(actions)
        
        # Optimisation : utilisation de précision
        precision = 100
        scaled_budget = budget // precision
        
        dp = [0] * (scaled_budget + 1)
        
        for i in range(n):
            cost = max(1, costs[i] // precision)
            profit = profits[i] // precision
            
            for w in range(scaled_budget, cost - 1, -1):
                dp[w] = max(dp[w], dp[w - cost] + profit)
        
        exec_time = time.time() - start_time
        return dp[scaled_budget] * precision, exec_time
    
    def greedy_algorithm(self, actions, budget):
        """Algorithme Glouton"""
        start_time = time.time()
        
        # Trier par ratio profit/coût décroissant
        sorted_actions = sorted(actions, key=lambda x: x['profit_pct'], reverse=True)
        
        total_cost = 0
        total_profit = 0
        selected_actions = []
        
        for action in sorted_actions:
            if total_cost + action['cost'] <= budget:
                selected_actions.append(action)
                total_cost += action['cost']
                total_profit += action['cost'] * action['profit_pct']
        
        exec_time = time.time() - start_time
        return total_profit, exec_time
    
    def run_comparative_analysis(self, budget=500000):
        """Exécute l'analyse comparative complète"""
        datasets = self.generate_test_datasets()
        
        print("🔄 EXÉCUTION DE L'ANALYSE COMPARATIVE...")
        print("=" * 60)
        
        for size, actions in datasets.items():
            print(f"\n📊 Dataset {size} actions:")
            print("-" * 30)
            
            # Force Brute (avec timeout pour grandes tailles)
            if size <= 20:
                bf_combination, bf_profit, bf_combinations, bf_time = self.brute_force(actions, budget)
                print(f"🔍 Force Brute: {bf_time:.3f}s | Profit: {bf_profit:,.0f}F | Combinaisons: {bf_combinations}")
            else:
                bf_time = float('inf')
                bf_profit = 0
                print(f"🔍 Force Brute: TIMEOUT (>30s)")
            
            # Programmation Dynamique
            dp_profit, dp_time = self.dynamic_programming(actions, budget)
            print(f"⚡ Prog. Dyn.: {dp_time:.6f}s | Profit: {dp_profit:,.0f}F")
            
            # Algorithme Glouton
            greedy_profit, greedy_time = self.greedy_algorithm(actions, budget)
            print(f"🚀 Glouton:    {greedy_time:.6f}s | Profit: {greedy_profit:,.0f}F")
            
            # Qualité relative
            if bf_profit > 0:
                dp_quality = (dp_profit / bf_profit) * 100
                greedy_quality = (greedy_profit / bf_profit) * 100
                print(f"📈 Qualité: DP={dp_quality:.1f}% | Glouton={greedy_quality:.1f}%")
            
            self.results.append({
                'size': size,
                'brute_force_time': bf_time if size <= 20 else float('inf'),
                'dp_time': dp_time,
                'greedy_time': greedy_time,
                'brute_force_profit': bf_profit,
                'dp_profit': dp_profit,
                'greedy_profit': greedy_profit
            })
    
    def plot_performance_comparison(self):
        """Génère les graphiques de comparaison"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Préparer les données
        sizes = [r['size'] for r in self.results]
        bf_times = [r['brute_force_time'] for r in self.results]
        dp_times = [r['dp_time'] for r in self.results]
        greedy_times = [r['greedy_time'] for r in self.results]
        
        # 1. TEMPS D'EXÉCUTION (échelle linéaire)
        ax1.plot(sizes, bf_times, 'ro-', linewidth=2, markersize=8, label='Force Brute')
        ax1.plot(sizes, dp_times, 'bo-', linewidth=2, markersize=8, label='Programmation Dynamique')
        ax1.plot(sizes, greedy_times, 'go-', linewidth=2, markersize=8, label='Algorithme Glouton')
        ax1.set_xlabel('Nombre d\'actions')
        ax1.set_ylabel('Temps d\'exécution (secondes)')
        ax1.set_title('COMPARAISON DES TEMPS D\'EXÉCUTION\n(Échelle Linéaire)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. TEMPS D'EXÉCUTION (échelle logarithmique)
        ax2.semilogy(sizes, bf_times, 'ro-', linewidth=2, markersize=8, label='Force Brute')
        ax2.semilogy(sizes, dp_times, 'bo-', linewidth=2, markersize=8, label='Programmation Dynamique')
        ax2.semilogy(sizes, greedy_times, 'go-', linewidth=2, markersize=8, label='Algorithme Glouton')
        ax2.set_xlabel('Nombre d\'actions')
        ax2.set_ylabel('Temps d\'exécution (secondes - échelle log)')
        ax2.set_title('COMPARAISON DES TEMPS D\'EXÉCUTION\n(Échelle Logarithmique)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. COMPARAISON DES PROFITS
        bf_profits = [r['brute_force_profit'] for r in self.results]
        dp_profits = [r['dp_profit'] for r in self.results]
        greedy_profits = [r['greedy_profit'] for r in self.results]
        
        x = np.arange(len(sizes))
        width = 0.25
        
        ax3.bar(x - width, bf_profits, width, label='Force Brute', color='red', alpha=0.7)
        ax3.bar(x, dp_profits, width, label='Programmation Dynamique', color='blue', alpha=0.7)
        ax3.bar(x + width, greedy_profits, width, label='Algorithme Glouton', color='green', alpha=0.7)
        
        ax3.set_xlabel('Nombre d\'actions')
        ax3.set_ylabel('Profit (F CFA)')
        ax3.set_title('COMPARAISON DES PROFITS OBTENUS')
        ax3.set_xticks(x)
        ax3.set_xticklabels(sizes)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. ACCÉLÉRATION RELATIVE
        accelerations_dp = [bf_times[i] / dp_times[i] if bf_times[i] < float('inf') else 0 for i in range(len(sizes))]
        accelerations_greedy = [bf_times[i] / greedy_times[i] if bf_times[i] < float('inf') else 0 for i in range(len(sizes))]
        
        ax4.bar(x - width/2, accelerations_dp, width, label='DP vs Force Brute', color='blue', alpha=0.7)
        ax4.bar(x + width/2, accelerations_greedy, width, label='Glouton vs Force Brute', color='green', alpha=0.7)
        
        ax4.set_xlabel('Nombre d\'actions')
        ax4.set_ylabel('Facteur d\'accélération (x fois)')
        ax4.set_title('ACCÉLÉRATION DES ALGORITHMES OPTIMISÉS')
        ax4.set_xticks(x)
        ax4.set_xticklabels(sizes)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('comparaison_algorithmes.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_comparison_table(self):
        """Génère un tableau de comparaison détaillé"""
        print("\n" + "=" * 80)
        print("📋 TABLEAU COMPARATIF DÉTAILLÉ")
        print("=" * 80)
        
        headers = ["Taille", "Force Brute", "Prog. Dyn.", "Glouton", "Accél. DP", "Accél. Glouton", "Qualité DP", "Qualité Glouton"]
        print(f"{headers[0]:<8} {headers[1]:<15} {headers[2]:<15} {headers[3]:<15} {headers[4]:<12} {headers[5]:<15} {headers[6]:<12} {headers[7]:<12}")
        print("-" * 110)
        
        for result in self.results:
            size = result['size']
            bf_time = result['brute_force_time']
            dp_time = result['dp_time']
            greedy_time = result['greedy_time']
            bf_profit = result['brute_force_profit']
            dp_profit = result['dp_profit']
            greedy_profit = result['greedy_profit']
            
            # Formatage des temps
            bf_time_str = f"{bf_time:.3f}s" if bf_time < float('inf') else "Timeout"
            dp_time_str = f"{dp_time:.6f}s"
            greedy_time_str = f"{greedy_time:.6f}s"
            
            # Calcul des accélérations
            accel_dp = f"{bf_time/dp_time:.0f}x" if bf_time < float('inf') else "N/A"
            accel_greedy = f"{bf_time/greedy_time:.0f}x" if bf_time < float('inf') else "N/A"
            
            # Calcul des qualités
            quality_dp = f"{(dp_profit/bf_profit)*100:.1f}%" if bf_profit > 0 else "100%"
            quality_greedy = f"{(greedy_profit/bf_profit)*100:.1f}%" if bf_profit > 0 else "100%"
            
            print(f"{size:<8} {bf_time_str:<15} {dp_time_str:<15} {greedy_time_str:<15} {accel_dp:<12} {accel_greedy:<15} {quality_dp:<12} {quality_greedy:<12}")

# UTILISATION
if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()
    
    print("🚀 LANCEMENT DE L'ANALYSE DE PERFORMANCE")
    print("Génération des courbes de comparaison Force Brute vs Algorithmes Optimisés")
    print("=" * 70)
    
    # Exécuter l'analyse
    analyzer.run_comparative_analysis()
    
    # Générer les graphiques
    analyzer.plot_performance_comparison()
    
    # Afficher le tableau détaillé
    analyzer.generate_comparison_table()
    
    print("\n✅ Analyse terminée! Graphique sauvegardé sous 'comparaison_algorithmes.png'")
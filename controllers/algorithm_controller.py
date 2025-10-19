import time
from itertools import combinations
from models.portfolio import Portfolio

class AlgorithmController:
    """Contrôleur pour les algorithmes d'optimisation"""
    
    def __init__(self, budget=500000):
        self.budget = budget
    
    def brute_force(self, actions):
        """Algorithme de force brute"""
        best_portfolio = Portfolio()
        
        # Génère toutes les combinaisons possibles
        for r in range(1, len(actions) + 1):
            for combination in combinations(actions, r):
                portfolio = Portfolio(combination)
                if (portfolio.total_cost <= self.budget and 
                    portfolio.total_profit > best_portfolio.total_profit):
                    best_portfolio = portfolio
        
        return best_portfolio
    
    def dynamic_programming(self, actions):
        """Algorithme de programmation dynamique"""
        n = len(actions)
        budget_int = int(self.budget)
        
        # Initialisation matrice DP
        dp = [[0] * (budget_int + 1) for _ in range(n + 1)]
        
        # Remplissage de la matrice
        for i in range(1, n + 1):
            cost = actions[i-1].cost
            profit = actions[i-1].profit
            
            for w in range(1, budget_int + 1):
                if cost <= w:
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w - cost] + profit)
                else:
                    dp[i][w] = dp[i-1][w]
        
        # Reconstruction de la solution
        best_profit = dp[n][budget_int]
        w = budget_int
        selected_actions = []
        
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_actions.append(actions[i-1])
                w -= actions[i-1].cost
        
        return Portfolio(selected_actions)
    
    def greedy_optimized(self, actions):
        """Algorithme glouton optimisé"""
        # Trie par ratio profit/coût décroissant
        sorted_actions = sorted(actions, 
                              key=lambda x: x.profit_pct, 
                              reverse=True)
        
        selected_actions = []
        total_cost = 0
        
        for action in sorted_actions:
            if total_cost + action.cost <= self.budget:
                selected_actions.append(action)
                total_cost += action.cost
        
        return Portfolio(selected_actions)
    
    def execute_algorithm(self, algorithm_name, actions):
        """Exécute un algorithme et retourne les résultats avec le temps d'exécution"""
        start_time = time.time()
        
        if algorithm_name == "brute_force":
            portfolio = self.brute_force(actions)
        elif algorithm_name == "dynamic_programming":
            portfolio = self.dynamic_programming(actions)
        elif algorithm_name == "greedy":
            portfolio = self.greedy_optimized(actions)
        else:
            raise ValueError(f"Algorithme inconnu: {algorithm_name}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return portfolio, execution_time
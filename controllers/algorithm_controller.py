import time
from itertools import combinations
from models.portfolio import Portfolio

class AlgorithmController:
    """Contrôleur optimisé pour les algorithmes d'optimisation"""
    
    def __init__(self, budget=500000):
        self.budget = budget
    
    def brute_force(self, actions):
        """
        Algorithme de force brute avec sécurité
        Complexité: O(2^n)
        """
        if len(actions) > 20:
            print("⚠️  Force brute désactivée: trop d'actions (>20)")
            print("   → Utilisez debug_actions.csv ou test_actions.csv")
            return Portfolio()
        
        best_portfolio = Portfolio()
        total_combinations = 2 ** len(actions)
        
        print(f"🔍 Force brute: {len(actions)} actions, {total_combinations:,} combinaisons")
        
        # Génère TOUTES les combinaisons possibles
        for r in range(len(actions) + 1):  # Inclure combinaison vide (r=0)
            for combination in combinations(actions, r):
                portfolio = Portfolio(list(combination))
                
                # ⚠️ VÉRIFICATION STRICTE DU BUDGET
                if portfolio.total_cost <= self.budget:
                    if portfolio.total_profit > best_portfolio.total_profit:
                        best_portfolio = portfolio
        
        return best_portfolio
    
    def dynamic_programming(self, actions):
        """
        Algorithme de programmation dynamique optimisé
        Complexité: O(n * W/precision)
        """
        if not actions:
            return Portfolio()
            
        n = len(actions)
        
        # OPTIMISATION: Réduction de précision pour économiser la mémoire
        if self.budget > 100000:
            precision = 100  # Regrouper par 100 F CFA
        else:
            precision = 1
            
        reduced_budget = self.budget // precision
        
        print(f"⚡ DP optimisée: {n} actions, précision: {precision}F")
        
        # Utilisation d'un dictionnaire pour économiser la mémoire
        # budget_réduit -> (profit_total, liste_actions)
        dp = {0: (0, [])}
        
        for action in actions:
            cost = action.cost
            profit = action.profit
            reduced_cost = max(1, cost // precision)
            
            new_dp = {}
            
            for budget_used, (current_profit, current_actions) in dp.items():
                # Option 1: NE PAS prendre cette action
                if budget_used not in new_dp or current_profit > new_dp[budget_used][0]:
                    new_dp[budget_used] = (current_profit, current_actions)
                
                # Option 2: PRENDRE cette action
                new_budget = budget_used + reduced_cost
                
                if new_budget <= reduced_budget:
                    new_actions = current_actions + [action]
                    
                    # ⚠️ VÉRIFICATION CRITIQUE: Calculer le coût RÉEL
                    real_cost = sum(a.cost for a in new_actions)
                    
                    # ⚠️ VÉRIFIER LE BUDGET RÉEL
                    if real_cost <= self.budget:
                        new_profit = current_profit + profit
                        
                        if new_budget not in new_dp or new_profit > new_dp[new_budget][0]:
                            new_dp[new_budget] = (new_profit, new_actions)
            
            dp = new_dp
        
        # Trouver la meilleure solution valide
        best_profit = 0
        best_actions = []
        
        for budget_used, (profit, actions_list) in dp.items():
            # ⚠️ DOUBLE VÉRIFICATION du coût réel
            real_cost = sum(a.cost for a in actions_list)
            
            if real_cost <= self.budget and profit > best_profit:
                best_profit = profit
                best_actions = actions_list
        
        return Portfolio(best_actions)
    
    def greedy_optimized(self, actions):
        """
        Algorithme glouton avec stratégies multiples
        Complexité: O(n log n)
        """
        if not actions:
            return Portfolio()
        
        # Essayer différentes stratégies et garder la meilleure
        strategies = []
        
        # Stratégie 1: Ratio profit/coût (meilleure en général)
        strategies.append(self._greedy_by_ratio(actions))
        
        # Stratégie 2: Profit absolu
        strategies.append(self._greedy_by_profit(actions))
        
        # Stratégie 3: Coût faible d'abord
        strategies.append(self._greedy_by_cost(actions))
        
        # Retourner la meilleure stratégie
        best = max(strategies, key=lambda p: p.total_profit)
        
        # ⚠️ VÉRIFICATION FINALE DU BUDGET
        if best.total_cost > self.budget:
            print(f"⚠️  WARNING: Greedy dépasse budget!")
            # Retirer des actions jusqu'à respecter le budget
            return self._fix_budget_overflow(best)
        
        return best
    
    def _fix_budget_overflow(self, portfolio):
        """Corrige un portfolio qui dépasse le budget"""
        actions_list = list(portfolio.actions)
        
        # Trier par ratio décroissant
        actions_list.sort(key=lambda a: a.profit / a.cost if a.cost > 0 else 0, reverse=True)
        
        total_cost = sum(a.cost for a in actions_list)
        
        # Retirer les actions les moins rentables jusqu'à respecter le budget
        while total_cost > self.budget and actions_list:
            removed = actions_list.pop()  # Retirer la moins rentable
            total_cost -= removed.cost
        
        return Portfolio(actions_list)
    
    def _greedy_by_ratio(self, actions):
        """Glouton par ratio profit/coût"""
        sorted_actions = sorted(
            actions, 
            key=lambda x: x.profit_pct, 
            reverse=True
        )
        return self._select_greedy(sorted_actions)
    
    def _greedy_by_profit(self, actions):
        """Glouton par profit absolu"""
        sorted_actions = sorted(
            actions,
            key=lambda x: x.profit,
            reverse=True
        )
        return self._select_greedy(sorted_actions)
    
    def _greedy_by_cost(self, actions):
        """Glouton par coût croissant"""
        sorted_actions = sorted(
            actions,
            key=lambda x: x.cost
        )
        return self._select_greedy(sorted_actions)
    
    def _select_greedy(self, sorted_actions):
        """
        Sélection gloutonne standard
        ⚠️ GARANTIT: total_cost <= budget
        """
        selected_actions = []
        total_cost = 0
        
        for action in sorted_actions:
            if total_cost + action.cost <= self.budget:
                selected_actions.append(action)
                total_cost += action.cost
                
        return Portfolio(selected_actions)
    
    def execute_algorithm(self, algorithm_name, actions):
        """Exécute un algorithme avec gestion des erreurs"""
        if not actions:
            return Portfolio(), 0.0
            
        start_time = time.time()
        
        try:
            if algorithm_name == "brute_force":
                portfolio = self.brute_force(actions)
            elif algorithm_name == "dynamic_programming":
                portfolio = self.dynamic_programming(actions)
            elif algorithm_name == "greedy":
                portfolio = self.greedy_optimized(actions)
            else:
                raise ValueError(f"Algorithme inconnu: {algorithm_name}")
            
            execution_time = time.time() - start_time
            
            # ⚠️ VÉRIFICATION FINALE CRITIQUE
            if portfolio.total_cost > self.budget:
                print(f"\n❌ ERREUR CRITIQUE: {algorithm_name} dépasse le budget!")
                print(f"   Budget: {self.budget:,} F CFA")
                print(f"   Coût: {portfolio.total_cost:,} F CFA")
                print(f"   Dépassement: {portfolio.total_cost - self.budget:,} F CFA")
                
                # Tentative de correction
                portfolio = self._fix_budget_overflow(portfolio)
                print(f"   ✓ Corrigé: {portfolio.total_cost:,} F CFA")
            
            return portfolio, execution_time
            
        except MemoryError:
            print(f"💥 Mémoire insuffisante pour {algorithm_name}")
            return Portfolio(), time.time() - start_time
        except Exception as e:
            print(f"❌ Erreur {algorithm_name}: {e}")
            import traceback
            traceback.print_exc()
            return Portfolio(), time.time() - start_time
    
    def get_recommended_algorithms(self, num_actions):
        """
        Retourne les algorithmes recommandés selon la taille du dataset
        """
        recommendations = []
        
        if num_actions <= 20:
            recommendations.append("brute_force")
        
        if num_actions <= 1000:
            recommendations.append("dynamic_programming")
        
        recommendations.append("greedy")  # Toujours disponible
        
        return recommendations
    
    @staticmethod
    def get_complexity(algorithm_name):
        """
        Retourne la complexité théorique d'un algorithme
        Pour la présentation / rapport
        """
        complexities = {
            "brute_force": {
                "time": "O(2^n)",
                "space": "O(n)",
                "best": "O(2^n)",
                "worst": "O(2^n)",
                "description": "Énumération exhaustive de toutes les combinaisons possibles"
            },
            "dynamic_programming": {
                "time": "O(n × W/p)",
                "space": "O(W/p)",
                "best": "O(n × W/p)",
                "worst": "O(n × W/p)",
                "description": "Programmation dynamique avec précision p (p=100 par défaut)",
                "note": "W = budget (500,000), p = précision, n = nombre d'actions"
            },
            "greedy": {
                "time": "O(n log n)",
                "space": "O(n)",
                "best": "O(n log n)",
                "worst": "O(n log n)",
                "description": "Tri + sélection gloutonne par ratio profit/coût",
                "note": "Rapide mais ne garantit pas l'optimalité"
            }
        }
        return complexities.get(algorithm_name, {})
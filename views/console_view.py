"""
Console View - Interface professionnelle optimisée
Projet d'Analyse Décisionnelle
SANS ÉMOJIS - Format compact et élégant
"""
import os
import time
from typing import List, Dict, Any


class ConsoleView:
    """Vue console professionnelle et compacte"""
    
    # Codes couleur ANSI
    class Color:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        GRAY = '\033[90m'
        BOLD = '\033[1m'
        DIM = '\033[2m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'
    
    @classmethod
    def _c(cls, text, *styles):
        """Applique des styles au texte"""
        codes = ''.join(getattr(cls.Color, style.upper(), '') for style in styles)
        return f"{codes}{text}{cls.Color.RESET}"
    
    @classmethod
    def _line(cls, char="─", width=80, color=None):
        """Ligne de séparation"""
        line = char * width
        if color:
            print(cls._c(line, color))
        else:
            print(line)
    
    @classmethod
    def _header(cls, title, width=80, color='cyan'):
        """En-tête de section"""
        print()
        print(cls._c("╔" + "═" * (width - 2) + "╗", color, 'bold'))
        padding = (width - len(title) - 2) // 2
        centered = f"║{' ' * padding}{title}{' ' * (width - len(title) - padding - 2)}║"
        print(cls._c(centered, color, 'bold'))
        print(cls._c("╚" + "═" * (width - 2) + "╝", color, 'bold'))
    
    # ========================================================================
    # ÉCRAN D'ACCUEIL
    # ========================================================================
    
    @classmethod
    def display_welcome(cls):
        """Écran d'accueil compact"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print()
        cls._header("OPTIMISATEUR D'INVESTISSEMENT", color='cyan')
        print(cls._c("Projet d'Analyse Décisionnelle - Maximisation du profit".center(80), 'gray'))
        print()
        cls._line("─", 80, 'blue')
        
        # Informations essentielles sur une ligne
        budget = cls._c("Budget: 500,000 F CFA", 'yellow', 'bold')
        horizon = cls._c("Horizon: 2 ans", 'cyan')
        objectif = cls._c("Objectif: Maximiser profit", 'green')
        print(f"  {budget}  |  {horizon}  |  {objectif}")
        
        cls._line("─", 80, 'blue')
        print()
    
    # ========================================================================
    # MENU DE SÉLECTION
    # ========================================================================
    
    @classmethod
    def display_dataset_menu(cls, files_info):
        """Menu compact avec meilleure UX"""
        print(cls._c("DATASETS DISPONIBLES", 'cyan', 'bold'))
        cls._line("─", 80, 'blue')
        
        file_mapping = {}
        
        for i, (file_path, file_info) in enumerate(files_info, 1):
            file_name = os.path.basename(file_path)
            
            # Classification
            if "PETIT" in file_info:
                badge = cls._c(" PETIT  ", 'green', 'bold')
                info = cls._c("Force Brute OK", 'green')
            elif "MOYEN" in file_info:
                badge = cls._c(" MOYEN  ", 'yellow', 'bold')
                info = cls._c("Algorithmes optimisés", 'yellow')
            elif "GRAND" in file_info:
                badge = cls._c(" GRAND  ", 'yellow', 'bold')
                info = cls._c("DP recommandée", 'yellow')
            else:
                badge = cls._c("EXPERT ", 'red', 'bold')
                info = cls._c("DP uniquement", 'red')
            
            # Affichage compact sur 2 lignes
            num = cls._c(f"[{i}]", 'cyan', 'bold')
            name = cls._c(file_name, 'white', 'bold')
            print(f"{num} {name}")
            print(f"    {badge} {file_info} - {info}")
            
            file_mapping[str(i)] = file_path
        
        print()
        cls._line("─", 80, 'blue')
        
        return file_mapping
    
    @classmethod
    def get_file_choice(cls, file_mapping):
        """Prompt de sélection amélioré"""
        if not file_mapping:
            cls.display_error("Aucun fichier disponible")
            return None
        
        max_choice = max(int(k) for k in file_mapping.keys())
        
        # Affichage des options
        options = cls._c(f"1-{max_choice}", 'cyan', 'bold')
        quit_opt = cls._c("q", 'red', 'bold')
        prompt = f"Sélectionnez un dataset ({options}) ou ({quit_opt}) pour quitter: "
        
        while True:
            try:
                choice = input(prompt).strip()
                
                if choice.lower() == 'q':
                    return None
                
                if choice in file_mapping:
                    selected = file_mapping[choice]
                    file_name = os.path.basename(selected)
                    print(cls._c(f">>> Dataset sélectionné: {file_name}", 'green', 'bold'))
                    return selected
                
                print(cls._c(f"Erreur: Choisissez entre 1 et {max_choice}", 'red'))
                
            except ValueError:
                print(cls._c("Erreur: Nombre invalide", 'red'))
            except KeyboardInterrupt:
                print()
                return None
    
    # ========================================================================
    # MENU DE SÉLECTION DES ALGORITHMES (NOUVEAU)
    # ========================================================================
    
    @classmethod
    def display_algorithm_selection_menu(cls, recommended, name_mapping, n_actions):
        """
        Menu interactif de sélection des algorithmes
        
        Args:
            recommended: Liste des algorithmes recommandés
            name_mapping: Dict {key: (name, key)}
            n_actions: Nombre d'actions dans le dataset
        
        Returns:
            Liste des algorithmes sélectionnés [(name, key), ...]
        """
        print()
        print("=" * 80)
        print(cls._c("SÉLECTION DES ALGORITHMES", 'cyan', 'bold'))
        print("=" * 80)
        print()
        
        # Construire les options disponibles
        available_algorithms = []
        
        for i, algo_key in enumerate(recommended, 1):
            if algo_key in name_mapping:
                name, key = name_mapping[algo_key]
                available_algorithms.append((i, name, key))
        
        # Afficher les options avec détails
        print(cls._c("Algorithmes disponibles pour ce dataset:", 'white', 'bold'))
        print()
        
        for num, name, key in available_algorithms:
            # Couleur selon l'algorithme
            if "Force Brute" in name:
                color = 'magenta'
                desc = "Enumeration exhaustive - OPTIMAL mais LENT"
                time_est = "< 1s" if n_actions <= 15 else f"~{2**n_actions/1000000:.1f}s"
            elif "Dynamique" in name:
                color = 'cyan'
                desc = "Programmation dynamique - OPTIMAL et RAPIDE"
                time_est = f"~{n_actions * 500000 / 1000000:.1f}s"
            else:  # Glouton
                color = 'green'
                desc = "Heuristique gloutonne - TRES RAPIDE (~98% optimal)"
                time_est = "< 0.01s"
            
            num_str = cls._c(f"[{num}]", color, 'bold')
            name_str = cls._c(name, color, 'bold')
            
            print(f"{num_str} {name_str}")
            print(f"    {desc}")
            print(f"    Temps estime: {cls._c(time_est, 'gray')}")
            print()
        
        # Avertissement Force Brute si > 20
        if n_actions > 20 and "brute_force" not in recommended:
            print(cls._c("[ATTENTION] Force Brute desactivee: dataset trop grand (>20 actions)", 'yellow', 'bold'))
            print()
        
        # Options spéciales
        print(cls._c("[A]", 'yellow', 'bold') + " Executer TOUS les algorithmes disponibles")
        print(cls._c("[Q]", 'red', 'bold') + " Retour au menu principal")
        print()
        
        cls._line("─", 80, 'blue')
        
        # PROMPT DE SÉLECTION
        max_num = len(available_algorithms)
        
        if max_num == 1:
            prompt = f"Votre choix (1, A=tous, Q=quitter): "
        else:
            prompt = f"Votre choix (1-{max_num}, A=tous, Q=quitter): "
        
        while True:
            choice = input(prompt).strip().upper()
            
            # Quitter
            if choice == 'Q':
                return None
            
            # Tous les algorithmes
            if choice == 'A':
                print()
                print(cls._c(">>> Tous les algorithmes selectionnes", 'green', 'bold'))
                return [(name, key) for _, name, key in available_algorithms]
            
            # Sélection individuelle
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= max_num:
                    selected = available_algorithms[choice_num - 1]
                    _, name, key = selected
                    print()
                    print(cls._c(f">>> {name} selectionne", 'green', 'bold'))
                    return [(name, key)]
                else:
                    print(cls._c(f"Erreur: Choisissez entre 1 et {max_num}", 'red'))
            except ValueError:
                print(cls._c("Erreur: Entree invalide", 'red'))
    
    # ========================================================================
    # EN-TÊTE DE TRAITEMENT
    # ========================================================================
    
    @classmethod
    def display_dataset_header(cls, filename):
        """En-tête compact"""
        print()
        cls._header(f"TRAITEMENT: {filename}", color='magenta')
    
    # ========================================================================
    # STATISTIQUES DU DATASET
    # ========================================================================
    
    @classmethod
    def display_actions_summary(cls, actions):
        """Statistiques compactes"""
        if not actions:
            cls.display_error("Aucune action à afficher")
            return
        
        total_cost = sum(action.cost for action in actions)
        total_profit = sum(action.profit for action in actions)
        valid_actions = [a for a in actions if a.cost > 0]
        
        best_profit = max(actions, key=lambda x: x.profit) if actions else None
        best_ratio = max(valid_actions, key=lambda x: x.profit/x.cost) if valid_actions else None
        
        print(cls._c("STATISTIQUES", 'blue', 'bold'))
        cls._line("─", 80, 'gray')
        
        # Affichage compact sur 2 lignes
        line1 = f"Actions: {cls._c(f'{len(actions):,}', 'cyan', 'bold')}  |  "
        line1 += f"Valeur totale: {cls._c(f'{int(total_cost):,} F', 'yellow', 'bold')}  |  "
        line1 += f"Profit potentiel: {cls._c(f'{int(total_profit):,} F', 'green', 'bold')}"
        print(line1)
        
        if best_profit and best_ratio:
            ratio = (best_ratio.profit / best_ratio.cost) * 100
            line2 = f"Meilleur profit: {cls._c(best_profit.id, 'magenta', 'bold')} "
            line2 += f"({cls._c(f'{best_profit.profit:,.0f} F', 'green')})  |  "
            line2 += f"Meilleur rendement: {cls._c(best_ratio.id, 'magenta', 'bold')} "
            line2 += f"({cls._c(f'{ratio:.1f}%', 'green')})"
            print(line2)
        
        cls._line("─", 80, 'gray')
    
    # ========================================================================
    # RÉSULTATS DES ALGORITHMES
    # ========================================================================
    
    @classmethod
    def display_algorithm_result(cls, algorithm_name, portfolio, execution_time):
        """Affichage compact des résultats"""
        
        # Couleurs par algorithme
        algo_colors = {
            "Force Brute": 'magenta',
            "Programmation Dynamique": 'cyan',
            "Algorithme Glouton": 'green'
        }
        algo_color = algo_colors.get(algorithm_name, 'blue')
        
        # En-tête compact
        print()
        cls._header(f"RÉSULTATS: {algorithm_name.upper()}", color=algo_color)
        
        # Métriques sur 2 lignes
        budget_used = (portfolio.total_cost / 500000) * 100
        efficiency = (portfolio.total_profit / portfolio.total_cost) * 100 if portfolio.total_cost > 0 else 0
        
        # Ligne 1: Temps, Coût, Profit
        l1 = f"Temps: {cls._c(f'{execution_time:.3f}s', 'white', 'bold')}  |  "
        l1 += f"Coût: {cls._c(f'{portfolio.total_cost:,} F', 'yellow', 'bold')}  |  "
        l1 += f"Profit: {cls._c(f'{portfolio.total_profit:,.0f} F', 'green', 'bold')}"
        print(l1)
        
        # Ligne 2: Budget, Rendement, Actions
        l2 = f"Budget: {cls._c(f'{budget_used:.1f}%', 'cyan', 'bold')}  |  "
        l2 += f"Rendement: {cls._c(f'{efficiency:.1f}%', 'magenta', 'bold')}  |  "
        l2 += f"Actions: {cls._c(f'{len(portfolio.actions)}', 'white', 'bold')}"
        print(l2)
        
        # Validation contrainte
        if portfolio.total_cost > 500000:
            depassement = portfolio.total_cost - 500000
            print(cls._c(f"ATTENTION: Budget dépassé de {depassement:,} F - SOLUTION INVALIDE", 'red', 'bold'))
        else:
            print(cls._c("Contrainte budgétaire: OK", 'green', 'bold'))
        
        cls._line("─", 80, 'gray')
        
        # Tableau des actions (TOP 15 pour compacité)
        print(cls._c("TOP 15 ACTIONS SÉLECTIONNÉES", 'white', 'bold'))
        cls._line("─", 80, 'gray')
        
        sorted_actions = sorted(portfolio.actions, key=lambda x: x.profit, reverse=True)
        display_limit = min(15, len(sorted_actions))
        
        # En-tête tableau compact
        header = f"{'N°':<3} {'ACTION':<18} {'COÛT':>12} {'PROFIT':>14} {'REND.':>8}"
        print(cls._c(header, 'white', 'bold'))
        
        # Lignes du tableau
        for i, action in enumerate(sorted_actions[:display_limit], 1):
            rentability = f"{(action.profit_pct * 100):.1f}%"
            
            # Couleur selon performance
            if i <= 3:
                color = 'green'
            elif action.profit_pct >= 0.5:
                color = 'yellow'
            else:
                color = 'white'
            
            num = cls._c(f"{i:>2}.", 'gray')
            action_id = cls._c(f"{action.id:<18}", color)
            cost = cls._c(f"{action.cost:>12,}", 'yellow')
            profit = cls._c(f"{action.profit:>14,.0f}", 'green')
            rend = cls._c(f"{rentability:>8}", color)
            
            print(f"{num} {action_id} {cost} {profit} {rend}")
        
        # Résumé si plus d'actions
        if len(sorted_actions) > display_limit:
            remaining = len(sorted_actions) - display_limit
            print(cls._c(f"... et {remaining} autres actions", 'gray', 'dim'))
        
        avg_return = (portfolio.total_profit / portfolio.total_cost * 100) if portfolio.total_cost > 0 else 0
        print(cls._c(f"Rendement moyen: {avg_return:.2f}%", 'cyan', 'bold'))
    
    # ========================================================================
    # ANALYSE DE COMPLEXITÉ
    # ========================================================================
    
    @classmethod
    def display_complexity(cls, algo_key, complexity):
        """Affichage compact de la complexité"""
        print()
        print(cls._c("COMPLEXITÉ", 'magenta', 'bold'))
        cls._line("─", 80, 'gray')
        
        # Sur une ligne
        temps = cls._c(f"Temporelle: {complexity.get('time', 'N/A')}", 'cyan', 'bold')
        espace = cls._c(f"Spatiale: {complexity.get('space', 'N/A')}", 'yellow', 'bold')
        print(f"{temps}  |  {espace}")
        
        if 'description' in complexity:
            print(cls._c(f"{complexity['description']}", 'gray'))
        
        cls._line("─", 80, 'gray')
    
    # ========================================================================
    # COMPARAISON DES ALGORITHMES
    # ========================================================================
    
    @classmethod
    def display_comparison(cls, file_results):
        """Comparaison compacte"""
        print()
        cls._header("COMPARAISON DES ALGORITHMES", color='cyan')
        
        # Tableau comparatif
        header = f"{'ALGORITHME':<30} {'PROFIT':>16} {'COÛT':>14} {'TEMPS':>10}"
        print(cls._c(header, 'white', 'bold'))
        cls._line("─", 80, 'gray')
        
        best_profit = -1
        best_algo = ""
        fastest_time = float('inf')
        fastest_algo = ""
        
        for algo_name, result in file_results.items():
            profit = result['profit']
            cost = result['cost']
            time_val = result['time']
            
            if profit > best_profit:
                best_profit = profit
                best_algo = algo_name
            
            if time_val < fastest_time:
                fastest_time = time_val
                fastest_algo = algo_name
            
            # Affichage
            name_color = 'green' if profit == best_profit else 'white'
            name = cls._c(f"{algo_name:<30}", name_color, 'bold')
            profit_str = cls._c(f"{profit:>16,.0f}", 'green')
            cost_str = cls._c(f"{cost:>14,}", 'yellow')
            time_str = cls._c(f"{time_val:>10.3f}s", 'cyan')
            
            print(f"{name} {profit_str} {cost_str} {time_str}")
        
        cls._line("─", 80, 'gray')
        
        # Résumé compact
        if len(file_results) > 1:
            best_result = file_results[best_algo]
            
            summary = f"Meilleur: {cls._c(best_algo, 'green', 'bold')} "
            summary += f"({cls._c(f'{best_result['profit']:,.0f} F', 'green', 'bold')})  |  "
            summary += f"Plus rapide: {cls._c(fastest_algo, 'cyan', 'bold')} "
            summary += f"({cls._c(f'{fastest_time:.3f}s', 'cyan', 'bold')})"
            print(summary)
            
            # Écart si différents
            if best_algo != fastest_algo:
                speedup = best_result['time'] / fastest_time
                print(cls._c(f"Accélération: x{speedup:.0f}", 'magenta', 'bold'))
            
            # Écart de profit
            profits = [r['profit'] for r in file_results.values()]
            if len(set(profits)) > 1:
                profit_diff = max(profits) - min(profits)
                profit_pct = (profit_diff / max(profits)) * 100
                print(cls._c(f"Écart de profit: {profit_diff:,.0f} F ({profit_pct:.2f}%)", 'yellow'))
        
        cls._line("═", 80, 'cyan')
    
    # ========================================================================
    # MENU DE CONTINUATION
    # ========================================================================
    
    @classmethod
    def display_continuation_prompt(cls):
        """Menu compact"""
        print()
        cls._line("─", 80, 'blue')
        
        opt1 = cls._c("[1]", 'green', 'bold')
        opt2 = cls._c("[2]", 'red', 'bold')
        print(f"{opt1} Analyser un autre dataset  |  {opt2} Quitter")
        
        cls._line("─", 80, 'blue')
        
        while True:
            choice = input("Votre choix: ").strip()
            
            if choice in ['1', '2']:
                return choice
            
            print(cls._c("Erreur: Choisissez 1 ou 2", 'red'))
    
    # ========================================================================
    # MESSAGES SYSTÈME
    # ========================================================================
    
    @classmethod
    def display_success(cls, message):
        print(cls._c(f"[OK] {message}", 'green', 'bold'))
    
    @classmethod
    def display_error(cls, message):
        print(cls._c(f"[ERREUR] {message}", 'red', 'bold'))
    
    @classmethod
    def display_info(cls, message):
        print(cls._c(f"[INFO] {message}", 'cyan'))
    
    @classmethod
    def display_warning(cls, message):
        print(cls._c(f"[ATTENTION] {message}", 'yellow', 'bold'))
    
    @classmethod
    def display_loading(cls, message):
        print(cls._c(f"[-->] {message}...", 'cyan'), end='', flush=True)
        time.sleep(0.2)
        print(cls._c(" OK", 'green', 'bold'))
    
    # ========================================================================
    # COMPATIBILITÉ
    # ========================================================================
    
    @classmethod
    def display_simple_menu(cls, files_info):
        return cls.display_dataset_menu(files_info)
    
    @classmethod
    def display_detailed_comparison(cls, results):
        cls.display_comparison(results)
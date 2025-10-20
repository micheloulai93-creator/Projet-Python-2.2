# views/console_view.py - VERSION FINALE OPTIMISÉE
import os
import time

class ConsoleView:
    """Vue console optimisée"""
    
    # Couleurs
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    @classmethod
    def _c(cls, text, color_code):
        return f"{color_code}{text}{cls.RESET}"
    
    @classmethod
    def display_welcome(cls):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(cls._c("╔══════════════════════════════════════════════╗", cls.BLUE))
        print(cls._c("║           OPTIMISATEUR D'INVESTISSEMENT     ║", cls.BOLD + cls.WHITE))
        print(cls._c("║           Maximisez vos profits            ║", cls.WHITE))
        print(cls._c("╚══════════════════════════════════════════════╝", cls.BLUE))
        print(cls._c("Budget: 500,000 F CFA | 3 algorithmes | CSV/Excel", cls.GREEN))
        print()
    
    @classmethod
    def display_menu(cls, files):
        print(cls._c("┌────────────────────────────────────────────┐", cls.BLUE))
        print(cls._c("│             SELECTION DATASET             │", cls.BOLD + cls.WHITE))
        print(cls._c("└────────────────────────────────────────────┘", cls.BLUE))
        print()
        
        file_mapping = {}
        for i, file_path in enumerate(files, 1):
            file_name = os.path.basename(file_path)
            info = cls._quick_analyze(file_path)
            print(cls._c(f" [{i}] {file_name}", cls.YELLOW))
            print(cls._c(f"     {info}", cls.WHITE))
            file_mapping[i] = file_path
        
        print()
        return file_mapping

    @classmethod
    def _quick_analyze(cls, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for line in f) - 1
            
            if line_count <= 10: return f"{line_count} actions • Rapide • Test"
            elif line_count <= 50: return f"{line_count} actions • Standard • Complet"
            else: return f"{line_count} actions • Long • Avancé"
        except: return "Infos non disponibles"
    
    @classmethod
    def get_file_choice(cls, file_mapping):
        if not file_mapping:
            print(cls._c(" Aucun fichier disponible", cls.RED))
            return None
        
        max_choice = max(file_mapping.keys())
        
        while True:
            try:
                choice = input(cls._c(f" Sélection (1-{max_choice}): ", cls.BOLD))
                if choice.lower() == 'q':
                    return None
                choice_int = int(choice)
                if choice_int in file_mapping:
                    selected = file_mapping[choice_int]
                    print(cls._c(f" ✓ {os.path.basename(selected)}", cls.GREEN))
                    time.sleep(0.3)
                    return selected
                print(cls._c(f" Choix 1-{max_choice} seulement", cls.RED))
            except ValueError:
                print(cls._c(" Nombre requis", cls.RED))
    
    @classmethod
    def display_actions_summary(cls, actions):
        total_cost = sum(action.cost for action in actions)
        total_profit = sum(action.profit for action in actions)
        
        print(cls._c("┌────────────────────────────────────────────┐", cls.BLUE))
        print(cls._c("│               RESUME DATASET              │", cls.BOLD + cls.WHITE))
        print(cls._c("└────────────────────────────────────────────┘", cls.BLUE))
        print()
        
        print(cls._c(f" Actions: {len(actions)}", cls.WHITE))
        print(cls._c(f" Coût total: {int(total_cost):,} F CFA", cls.WHITE))
        print(cls._c(f" Profit: {int(total_profit):,} F CFA", cls.GREEN))
        print()
    
    @classmethod
    def display_algorithm_result(cls, algorithm_name, portfolio, execution_time):
        print(cls._c("┌────────────────────────────────────────────┐", cls.BLUE))
        print(cls._c(f"│ {algorithm_name.upper():<40} │", cls.BOLD + cls.WHITE))
        print(cls._c("└────────────────────────────────────────────┘", cls.BLUE))
        print()
        
        print(cls._c(f" Temps: {execution_time:.3f}s", cls.WHITE))
        print(cls._c(f" Investi: {int(portfolio.total_cost):,} F CFA", cls.WHITE))
        print(cls._c(f" Profit: {int(portfolio.total_profit):,} F CFA", cls.GREEN))
        print(cls._c(f" Actions: {len(portfolio.actions)}", cls.WHITE))
        
        efficiency = (portfolio.total_profit / portfolio.total_cost) * 100 if portfolio.total_cost > 0 else 0
        print(cls._c(f" Efficacité: {efficiency:.1f}%", cls.YELLOW))
        
        print()
        print(cls._c(" Actions sélectionnées:", cls.BOLD))
        print(cls._c("─" * 45, cls.BLUE))
        
        for i, action in enumerate(portfolio.actions, 1):
            rentability = f"{action.profit_pct * 100:.1f}%"
            print(cls._c(f" {i:2d}. {action.id:<15} {int(action.cost):>8,} {rentability:>8}", cls.WHITE))
        
        print()
    
    @classmethod
    def display_comparison(cls, results):
        print(cls._c("┌────────────────────────────────────────────┐", cls.BLUE))
        print(cls._c("│              COMPARAISON                  │", cls.BOLD + cls.WHITE))
        print(cls._c("└────────────────────────────────────────────┘", cls.BLUE))
        print()
        
        best_profit = max(result['profit'] for result in results.values())
        
        print(cls._c(" Algorithme           Profit    Temps   Eff.%", cls.BOLD))
        print(cls._c("─" * 45, cls.BLUE))
        
        for algo_name, result in results.items():
            profit_int = int(result['profit'])
            efficiency = (result['profit'] / result['cost']) * 100 if result['cost'] > 0 else 0
            
            if result['profit'] == best_profit:
                line = cls._c(f"{algo_name:<18} {profit_int:>8,} {result['time']:>6.3f}s {efficiency:>5.1f}%", cls.GREEN)
            else:
                line = cls._c(f"{algo_name:<18} {profit_int:>8,} {result['time']:>6.3f}s {efficiency:>5.1f}%", cls.WHITE)
            
            print(line)
        
        print()
        best_algo = [name for name, result in results.items() if result['profit'] == best_profit][0]
        print(cls._c(f" Recommandation: {best_algo}", cls.YELLOW))
        print()
    
    @classmethod
    def display_continuation_prompt(cls):
        print()
        print(cls._c("┌────────────────────────────────────────────┐", cls.BLUE))
        print(cls._c("│               SUIVANT ?                   │", cls.BOLD + cls.WHITE))
        print(cls._c("└────────────────────────────────────────────┘", cls.BLUE))
        print()
        print(cls._c(" [1] Nouvelle analyse", cls.YELLOW))
        print(cls._c(" [2] Quitter", cls.YELLOW))
        print()
        
        while True:
            choice = input(cls._c(" Votre choix (1-2): ", cls.BOLD))
            if choice in ['1', '2']:
                return choice
            print(cls._c(" Choix 1-2 seulement", cls.RED))
    
    @classmethod
    def display_loading(cls, message):
        print(f"\n{message}...", end='', flush=True)
        for i in range(3):
            print('.', end='', flush=True)
            time.sleep(0.3)
        print(' ✓')
    
    @classmethod
    def display_success(cls, message):
        print(cls._c(f" ✓ {message}", cls.GREEN))
    
    @classmethod
    def display_error(cls, message):
        print(cls._c(f" ✗ {message}", cls.RED))
    
    @classmethod
    def display_info(cls, message):
        print(cls._c(f" i {message}", cls.BLUE))
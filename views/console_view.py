# views/console_view.py
import os
import time

class ConsoleView:
    """Vue pour l'affichage console amélioré"""
    
    @staticmethod
    def display_welcome():
        """Affiche l'écran d'accueil amélioré"""
        print("┌" + "─" * 60 + "┐")
        print("│" + " " * 20 + "🎯 OPTIMISATEUR D'INVESTISSEMENT" + " " * 20 + "│")
        print("│" + " " * 60 + "│")
        print("│" + " " * 15 + "Maximisez vos profits sous contrainte" + " " * 15 + "│")
        print("└" + "─" * 60 + "┘")
        print()
        print("📊 Budget maximum: 500,000 F CFA")
        print("🔍 3 algorithmes d'optimisation disponibles")
        print("📁 Support: CSV et Excel")
        print()
    
    @staticmethod
    def display_menu(files):
        """Affiche un menu amélioré"""
        print("┌" + "─" * 50 + "┐")
        print("│" + " " * 15 + "📁 CHOIX DU DATASET" + " " * 15 + "│")
        print("└" + "─" * 50 + "┘")
        print()
        
        print("📊 Datasets disponibles:")
        for i, file_path in enumerate(files, 1):
            file_name = os.path.basename(file_path)
            print(f"   {i}️⃣  {file_name}")
        
        print()
        print("💡 Conseils:")
        print("   • 1-3 : Tests rapides (Force Brute activée)")
        print("   • 4 : Analyse complète (Programmation Dynamique)")
        print()
    
    @staticmethod
    def get_file_choice(files_count):
        """Demande le choix du fichier"""
        while True:
            try:
                choice = input(f"👉 Choisissez un dataset (1-{files_count}): ").strip()
                choice_int = int(choice)
                if 1 <= choice_int <= files_count:
                    return choice_int
                else:
                    print(f"❌ Veuillez choisir entre 1 et {files_count}")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")
    
    @staticmethod
    def display_actions_summary(actions):
        """Affiche le résumé des actions"""
        total_cost = sum(action.cost for action in actions)
        total_profit = sum(action.profit for action in actions)
        
        print("┌" + "─" * 50 + "┐")
        print("│" + " " * 15 + "📈 RÉSUMÉ DU DATASET" + " " * 15 + "│")
        print("└" + "─" * 50 + "┘")
        print()
        
        print(f"🔢 Nombre d'actions: {len(actions)}")
        print(f"💰 Coût total: {total_cost:,} F CFA")
        print(f"📈 Profit potentiel: {total_profit:,.0f} F CFA")
        print(f"🎯 Budget disponible: 500,000 F CFA")
        
        if total_cost > 0:
            coverage = min(100, (500000 / total_cost) * 100)
            print(f"📊 Couverture: {coverage:.1f}% du portefeuille total")
        
        print()
    
    @staticmethod
    def display_algorithm_result(algorithm_name, portfolio, execution_time):
        """Affiche les résultats d'un algorithme"""
        print(f"┌{'─' * 70}┐")
        print(f"│ 🎯 {algorithm_name.upper():<62} │")
        print(f"└{'─' * 70}┘")
        
        print(f"⏱️  Temps d'exécution: {execution_time:.4f} secondes")
        print(f"💰 Coût total: {portfolio.total_cost:,} F CFA")
        print(f"📈 Profit total: {portfolio.total_profit:,.0f} F CFA")
        print(f"🔢 Nombre d'actions: {len(portfolio.actions)}")
        print(f"💵 Budget restant: {500000 - portfolio.total_cost:,} F CFA")
        
        efficiency = (portfolio.total_profit / portfolio.total_cost) * 100 if portfolio.total_cost > 0 else 0
        print(f"📊 Efficacité: {efficiency:.2f}%")
        
        print()
        print("📋 Actions sélectionnées:")
        print("┌" + "─" * 70 + "┐")
        print(f"│ {'N°':<3} {'Action':<20} {'Coût':<12} {'Profit':<12} {'Rentabilité':<12} │")
        print("├" + "─" * 70 + "┤")
        
        for i, action in enumerate(portfolio.actions, 1):
            rentability = f"{action.profit_pct * 100:.1f}%"
            print(f"│ {i:<3} {action.id:<20} {action.cost:<12,} {action.profit:<12,.0f} {rentability:<12} │")
        
        print("└" + "─" * 70 + "┘")
        print()
    
    @staticmethod
    def display_comparison(results):
        """Affiche la comparaison des algorithmes"""
        print("┌" + "─" * 70 + "┐")
        print("│" + " " * 20 + "📊 COMPARAISON FINALE" + " " * 20 + "│")
        print("└" + "─" * 70 + "┘")
        print()
        
        print("┌" + "─" * 70 + "┐")
        print(f"│ {'Algorithme':<25} {'Profit':<12} {'Temps':<10} {'Actions':<8} {'Efficacité':<10} │")
        print("├" + "─" * 70 + "┤")
        
        for algo_name, result in results.items():
            efficiency = (result['profit'] / result['cost']) * 100 if result['cost'] > 0 else 0
            print(f"│ {algo_name:<25} {result['profit']:>11,.0f} {result['time']:>8.4f}s {result['count']:>7} {efficiency:>9.1f}% │")
        
        print("└" + "─" * 70 + "┘")
        print()
    
    @staticmethod
    def display_continuation_prompt():
        """Demande à l'utilisateur s'il veut continuer"""
        print()
        print("┌" + "─" * 50 + "┐")
        print("│" + " " * 10 + "🎯 QUE SOUHAITEZ-VOUS FAIRE ?" + " " * 10 + "│")
        print("└" + "─" * 50 + "┘")
        print()
        print("1️⃣  Analyser un autre dataset")
        print("2️⃣  Quitter le programme")
        print()
        
        while True:
            choice = input("👉 Votre choix (1-2): ").strip()
            if choice in ['1', '2']:
                return choice
            else:
                print("❌ Choix invalide. Veuillez choisir 1 ou 2.")
    
    @staticmethod
    def display_success(message):
        print(f"✅ {message}")
    
    @staticmethod
    def display_error(message):
        print(f"❌ {message}")
    
    @staticmethod
    def display_info(message):
        print(f"ℹ️  {message}")
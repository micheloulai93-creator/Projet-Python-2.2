import sys
import os
from controllers.file_controller import FileController
from controllers.algorithm_controller import AlgorithmController
from views.console_view import ConsoleView

class InvestmentApp:
    """Application principale MVC avec boucle continue"""
    
    def __init__(self):
        self.file_controller = FileController()
        self.algorithm_controller = AlgorithmController()
        self.console_view = ConsoleView()
    
    def list_data_files(self):
        """Liste tous les fichiers de données disponibles"""
        available_files = []
        for file in os.listdir('data'):
            if file.lower().endswith(('.xlsx', '.xls', '.csv')):
                full_path = os.path.join('data', file)
                available_files.append(full_path)
        return available_files
    
    def process_file(self, file_path):
        """Traite un fichier spécifique"""
        file_name = os.path.basename(file_path)
        
        print(f"\n{'='*70}")
        print(f"🎯 TRAITEMENT DU FICHIER: {file_name}")
        print(f"{'='*70}")
        
        # Chargement des données
        actions = self.file_controller.read_actions(file_path)
        if not actions:
            self.console_view.display_error("Aucune action valide chargée")
            return
        
        self.console_view.display_actions_summary(actions)
        
        # Détermination des algorithmes à utiliser
        algorithms_to_test = []
        if len(actions) <= 20:
            algorithms_to_test.append(("Force Brute", "brute_force"))
            self.console_view.display_info("Force brute activée (dataset ≤ 20 actions)")
        else:
            self.console_view.display_info("Force brute désactivée (dataset trop grand)")
        
        algorithms_to_test.extend([
            ("Programmation Dynamique", "dynamic_programming"),
            ("Algorithme Glouton", "greedy")
        ])
        
        file_results = {}
        
        # Exécution des algorithmes
        for algo_name, algo_key in algorithms_to_test:
            try:
                self.console_view.display_info(f"Exécution de {algo_name}...")
                portfolio, exec_time = self.algorithm_controller.execute_algorithm(algo_key, actions)
                
                file_results[algo_name] = {
                    'profit': portfolio.total_profit,
                    'cost': portfolio.total_cost,
                    'time': exec_time,
                    'count': len(portfolio.actions)
                }
                
                self.console_view.display_algorithm_result(algo_name, portfolio, exec_time)
                
                # Export des résultats
                os.makedirs('results', exist_ok=True)
                export_name = f"results/{file_name.split('.')[0]}_{algo_key}.csv"
                self.file_controller.export_results(export_name, portfolio, algo_name, exec_time)
                
            except Exception as e:
                self.console_view.display_error(f"{algo_name}: {str(e)}")
        
        # Comparaison des résultats
        if len(file_results) > 1:
            self.console_view.display_comparison(file_results)
    
    def run(self):
        """Méthode principale avec boucle continue"""
        self.console_view.display_welcome()
        
        while True:  # 🎯 BOUCLE PRINCIPALE AJOUTÉE ICI
            # Liste des fichiers disponibles
            available_files = self.list_data_files()
            
            if not available_files:
                self.console_view.display_error("Aucun fichier de données trouvé dans 'data/'")
                print("💡 Placez vos fichiers CSV ou Excel dans le dossier 'data/'")
                break
            
            self.console_view.display_menu(available_files)
            
            # Sélection du fichier
            try:
                choice = input("👉 Choisissez un dataset (1-4) ou 'q' pour quitter: ").strip()
                
                if choice.lower() == 'q':
                    self.console_view.display_info("Au revoir ! 👋")
                    break
                
                file_index = int(choice) - 1
                if 0 <= file_index < len(available_files):
                    selected_file = available_files[file_index]
                    self.process_file(selected_file)
                else:
                    self.console_view.display_error("Choix invalide")
                    continue
                    
            except ValueError:
                self.console_view.display_error("Veuillez entrer un nombre valide")
                continue
            except KeyboardInterrupt:
                self.console_view.display_info("\nInterruption par l'utilisateur. Au revoir ! 👋")
                break
            
            # 🎯 DEMANDE DE CONTINUATION APRÈS CHAQUE ANALYSE
            continuation = self.console_view.display_continuation_prompt()
            if continuation == '2':
                self.console_view.display_info("Merci d'avoir utilisé l'optimisateur d'investissement ! 👋")
                break

def main():
    """Point d'entrée principal"""
    try:
        app = InvestmentApp()
        app.run()
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        print("💡 Vérifiez que tous les fichiers nécessaires sont présents")
    finally:
        print("\n" + "="*70)
        print("🎯 OPTIMISATEUR D'INVESTISSEMENT - FIN DU PROGRAMME")
        print("="*70)

if __name__ == "__main__":
    main()
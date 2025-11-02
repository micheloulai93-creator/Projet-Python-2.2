"""
Application principale - Optimisateur d'investissement
Projet d'Analyse Décisionnelle
Architecture MVC
"""
import sys
import os
# Assurez-vous que ces modules existent dans l'architecture
from controllers.file_controller import FileController
from controllers.algorithm_controller import AlgorithmController
from views.console_view import ConsoleView
from controllers.sienna_comparator import SiennaComparator


class InvestmentApp:
    """Application principale MVC - Version finale optimisée"""
    
    def __init__(self):
        """Initialisation des contrôleurs et vue"""
        self.file_controller = FileController()
        self.algorithm_controller = AlgorithmController()
        self.console_view = ConsoleView()
    
    def list_data_files(self):
        """
        Liste tous les fichiers de données disponibles dans le dossier data/
        
        Returns:
            list: Liste des chemins complets des fichiers CSV/Excel
        """
        available_files = []
        data_dir = 'data'
        
        # Créer le dossier data s'il n'existe pas
        if not os.path.exists(data_dir):
            print(f"[INFO] Creation du dossier {data_dir}/")
            os.makedirs(data_dir)
            return available_files
        
        # Chercher tous les fichiers CSV et Excel
        for file in os.listdir(data_dir):
            if file.lower().endswith(('.xlsx', '.xls', '.csv')):
                full_path = os.path.join(data_dir, file)
                available_files.append(full_path)
        
        return available_files
    
    def quick_file_analysis(self, file_path):
        """
        Analyse rapide d'un fichier sans charger toutes les données
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            str: Description du fichier (taille et recommandation)
        """
        try:
            # Compter rapidement les lignes
            # Note: cela peut être lent pour de très gros fichiers Excel
            # mais fonctionne bien pour les CSV.
            if file_path.lower().endswith('.csv'):
                 with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for line in f) - 1  # -1 pour l'en-tête
            else:
                # Approximation pour les fichiers non CSV (moins précis sans pandas)
                file_size_bytes = os.path.getsize(file_path)
                line_count = round(file_size_bytes / 100) # Approximation basée sur 100 bytes/ligne
            
            # Classification selon la taille
            if line_count <= 20:
                return f"{line_count} actions • PETIT • Rapide"
            elif line_count <= 100:
                return f"{line_count} actions • MOYEN • Standard"
            elif line_count <= 500:
                return f"{line_count} actions • GRAND • Avance"
            else:
                return f"{line_count}+ actions • TRES GRAND • Expert"
                
        except Exception as e:
            return f"Infos non disponibles (erreur: {str(e)})"
    
    def process_file(self, file_path):
        """
        Traite un fichier de données complet
        
        Args:
            file_path: Chemin du fichier à traiter
        """
        file_name = os.path.basename(file_path)
        
        # En-tête du traitement
        self.console_view.display_dataset_header(file_name)
        
        # ===================================================================
        # CHARGEMENT DES DONNÉES
        # ===================================================================
        
        self.console_view.display_info("Chargement des donnees...")
        actions = self.file_controller.read_actions(file_path)
        
        if not actions:
            self.console_view.display_error("Aucune action valide chargee")
            return
        
        # ===================================================================
        # STATISTIQUES DU DATASET
        # ===================================================================
        
        self.console_view.display_actions_summary(actions)
        
        # ===================================================================
        # SÉLECTION DES ALGORITHMES (NOUVEAU)
        # ===================================================================
        
        n_actions = len(actions)
        recommended = self.algorithm_controller.get_recommended_algorithms(n_actions)
        
        # Mapping des noms d'algorithmes
        name_mapping = {
            "brute_force": ("Force Brute", "brute_force"),
            "dynamic_programming": ("Programmation Dynamique", "dynamic_programming"),
            "greedy": ("Algorithme Glouton", "greedy")
        }
        
        # NOUVEAU : Menu de sélection interactif
        selected_algorithms = self.console_view.display_algorithm_selection_menu(
            recommended, 
            name_mapping,
            n_actions
        )
        
        # Si l'utilisateur quitte
        if selected_algorithms is None:
            self.console_view.display_info("Retour au menu principal")
            return
        
        if not selected_algorithms:
            self.console_view.display_error("Aucun algorithme selectionne")
            return
        
        print()
        print("-" * 80)
        print()
        
        # ===================================================================
        # EXÉCUTION DES ALGORITHMES
        # ===================================================================
        
        file_results = {}
        
        for algo_name, algo_key in selected_algorithms:
            try:
                print(f"[INFO] Execution de {algo_name}...")
                print()
                
                # Exécuter l'algorithme
                portfolio, exec_time = self.algorithm_controller.execute_algorithm(
                    algo_key, actions
                )
                
                # Vérifier si une solution a été trouvée
                if portfolio and hasattr(portfolio, 'actions') and portfolio.actions:
                    # Stocker les résultats
                    file_results[algo_name] = {
                        'profit': portfolio.total_profit,
                        'cost': portfolio.total_cost,
                        'time': exec_time,
                        'count': len(portfolio.actions),
                        'portfolio': portfolio
                    }
                    
                    # Afficher les résultats
                    self.console_view.display_algorithm_result(
                        algo_name, portfolio, exec_time
                    )
                    
                    # Afficher la complexité
                    complexity = self.algorithm_controller.get_complexity(algo_key)
                    if complexity:
                        self.console_view.display_complexity(algo_key, complexity)
                    
                    # Exporter les résultats
                    os.makedirs('results', exist_ok=True)
                    export_name = f"results/{file_name.split('.')[0]}_{algo_key}.csv"
                    self.file_controller.export_results(
                        export_name, portfolio, algo_name, exec_time
                    )
                    
                else:
                    self.console_view.display_error(
                        f"{algo_name}: Aucune solution trouvee"
                    )
                
            except Exception as e:
                # 💥 CORRECTION DE L'ERREUR ICI (LIGNE 217) 💥
                # La ligne originale était : self.console_view.display_error(f"{algo_nameself.console_view.display_error(f"{algo_name}: {str(e)}")
                self.console_view.display_error(f"{algo_name}: {str(e)}")
                # Décommenter pour debug détaillé:
                # import traceback
                # traceback.print_exc()
        
        # ===================================================================
        # COMPARAISON ENTRE ALGORITHMES
        # ===================================================================
        
        if len(file_results) > 1:
            self.console_view.display_comparison(file_results)
            
        elif file_results:
            best_algo = list(file_results.keys())[0]
            self.console_view.display_success(f"Solution optimale: {best_algo}")
            
        else:
            self.console_view.display_error(
                "Aucun algorithme n'a trouve de solution"
            )
            return
        
        # ===================================================================
        # COMPARAISON AVEC SIENNA (CRITÈRE D'ÉVALUATION)
        # ===================================================================
        
        if file_results and SiennaComparator.has_reference(file_name):
            # Trouver le meilleur résultat
            best_algo_item = max(
                file_results.items(),
                key=lambda x: x[1]['profit']
            )
            best_name, best_result = best_algo_item
            
            print()
            print("-" * 80)
            print(f"Meilleur algorithme pour comparaison: {best_name}")
            print("-" * 80)
            
            # Effectuer la comparaison
            comparison = SiennaComparator.compare(
                file_name,
                best_result['profit'],
                best_result['cost'],
                best_result['count']
            )
            
            # Afficher les résultats
            if comparison:
                SiennaComparator.display(comparison)
    
    def run(self):
        """
        Boucle principale de l'application
        """
        # Afficher l'écran d'accueil
        self.console_view.display_welcome()
        
        while True:
            try:
                # ============================================================
                # LISTE DES FICHIERS DISPONIBLES
                # ============================================================
                
                available_files = self.list_data_files()
                
                if not available_files:
                    self.console_view.display_error(
                        "Aucun fichier de donnees trouve dans 'data/'"
                    )
                    print("[INFO] Placez vos fichiers CSV dans le dossier 'data/'")
                    break
                
                # ============================================================
                # PRÉPARATION DU MENU
                # ============================================================
                
                files_info = []
                for file_path in available_files:
                    file_info = self.quick_file_analysis(file_path)
                    files_info.append((file_path, file_info))
                
                # ============================================================
                # AFFICHAGE DU MENU ET SÉLECTION
                # ============================================================
                
                file_mapping = self.console_view.display_dataset_menu(files_info)
                selected_file = self.console_view.get_file_choice(file_mapping)
                
                # Sortie si l'utilisateur quitte
                if not selected_file:
                    self.console_view.display_info("Session terminee")
                    break
                
                # ============================================================
                # TRAITEMENT DU FICHIER SÉLECTIONNÉ
                # ============================================================
                
                self.process_file(selected_file)
                
                # ============================================================
                # MENU DE CONTINUATION
                # ============================================================
                
                continuation = self.console_view.display_continuation_prompt()
                
                if continuation == '2':
                    self.console_view.display_info(
                        "Merci d'avoir utilise l'optimisateur d'investissement"
                    )
                    break
                
            except KeyboardInterrupt:
                print()
                self.console_view.display_info(
                    "Interruption par l'utilisateur"
                )
                break
                
            except Exception as e:
                self.console_view.display_error(
                    f"Erreur lors du traitement: {str(e)}"
                )
                # Décommenter pour debug détaillé:
                import traceback
                traceback.print_exc()
                
                # Proposer de continuer
                print()
                retry = input("Continuer ? (o/n): ").strip().lower()
                if retry != 'o':
                    break


def main():
    """
    Point d'entrée principal du programme
    """
    try:
        # Créer et lancer l'application
        app = InvestmentApp()
        app.run()
        
    except Exception as e:
        print()
        print("=" * 80)
        print("ERREUR CRITIQUE")
        print("=" * 80)
        print(f"Erreur: {str(e)}")
        print()
        print("[INFO] Verifiez que tous les fichiers necessaires sont presents")
        print("       et que le systeme est correctement configure.")
        print()
        
        # Afficher la trace complète pour debug
        import traceback
        traceback.print_exc()
        
    finally:
        # Message de fin
        print()
        print("=" * 80)
        print("OPTIMISATEUR D'INVESTISSEMENT - FIN DU PROGRAMME")
        print("=" * 80)
        print()


if __name__ == "__main__":
    main()
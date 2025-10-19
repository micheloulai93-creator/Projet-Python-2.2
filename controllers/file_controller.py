import pandas as pd
import os
from models.action import Action

class FileController:
    """Contrôleur pour la gestion des fichiers"""
    
    @staticmethod
    def list_available_files(directory="data"):
        """Liste tous les fichiers Excel et CSV disponibles"""
        available_files = []
        
        if not os.path.exists(directory):
            print(f"📁 Création du dossier {directory}/")
            os.makedirs(directory)
            return available_files
            
        # Chercher fichiers Excel et CSV
        for file in os.listdir(directory):
            if file.lower().endswith(('.xlsx', '.xls', '.csv')):
                full_path = os.path.join(directory, file)
                available_files.append(full_path)
        
        return available_files
    
    @staticmethod
    def read_actions(filename):
        """Lit un fichier Excel ou CSV et retourne une liste d'actions"""
        actions = []
        try:
            # Vérifier l'extension du fichier
            file_extension = os.path.splitext(filename)[1].lower()
            
            if file_extension in ['.xlsx', '.xls']:
                # Lecture fichier Excel
                df = pd.read_excel(filename)
            elif file_extension == '.csv':
                # Lecture fichier CSV
                df = pd.read_csv(filename)
            else:
                print(f"Format de fichier non supporté: {file_extension}")
                return actions
            
            print(f"📊 Colonnes détectées: {list(df.columns)}")
            print(f"📈 Nombre de lignes total: {len(df)}")
            
            # Détection automatique du format
            column_mapping = {}
            
            for col in df.columns:
                col_lower = col.lower()
                if 'action' in col_lower or 'name' in col_lower or 'id' in col_lower or 'share' in col_lower:
                    column_mapping['id'] = col
                elif 'cout' in col_lower or 'cost' in col_lower or 'price' in col_lower or 'prix' in col_lower:
                    column_mapping['cost'] = col
                elif 'benefice' in col_lower or 'profit' in col_lower or 'rendement' in col_lower or '%' in col_lower:
                    column_mapping['profit_pct'] = col
            
            print(f"🔍 Mapping détecté: {column_mapping}")
            
            # Vérifier que toutes les colonnes nécessaires sont trouvées
            required_columns = ['id', 'cost', 'profit_pct']
            if not all(col in column_mapping for col in required_columns):
                print("❌ Format non reconnu. Colonnes attendues:")
                print("   - Nom de l'action (Action-1, Share-XXXX, etc.)")
                print("   - Coût (en euros/F CFA)")
                print("   - Bénéfice (en pourcentage)")
                print(f"📋 Colonnes trouvées: {list(df.columns)}")
                return actions
            
            # Renommer les colonnes
            df = df.rename(columns=column_mapping)
            
            # Nettoyer les données
            df_clean = df.dropna(subset=required_columns)
            
            # Nettoyer la colonne profit_pct (enlever les % et convertir)
            def clean_profit_pct(value):
                if isinstance(value, str):
                    # Enlever les % et espaces
                    value = value.replace('%', '').strip()
                    # Remplacer les virgules par des points
                    value = value.replace(',', '.')
                try:
                    return float(value)
                except:
                    return None
            
            df_clean['profit_pct'] = df_clean['profit_pct'].apply(clean_profit_pct)
            df_clean = df_clean.dropna(subset=['profit_pct'])
            
            # Filtrer les coûts positifs
            df_clean = df_clean[df_clean['cost'] > 0]
            
            print(f"✅ Données valides après nettoyage: {len(df_clean)} actions")
            
            # Créer les objets Action
            for index, row in df_clean.iterrows():
                try:
                    # Si le profit_pct est > 1, c'est probablement un pourcentage (15.5 → 0.155)
                    profit_pct_value = row['profit_pct']
                    if profit_pct_value > 1:
                        profit_pct_value = profit_pct_value / 100.0
                    
                    action = Action(
                        action_id=row['id'],
                        cost=row['cost'],
                        profit_pct=profit_pct_value
                    )
                    actions.append(action)
                    
                except (ValueError, KeyError, TypeError) as e:
                    print(f"Erreur création action {row['id']}: {e}")
                    continue
                    
            print(f"🎯 {len(actions)} actions créées avec succès")
                    
        except FileNotFoundError:
            print(f"❌ Fichier {filename} non trouvé")
        except Exception as e:
            print(f"❌ Erreur lecture fichier {filename}: {e}")
            
        return actions
    
    @staticmethod
    def export_results(filename, portfolio, algorithm_name, execution_time):
        """Exporte les résultats dans un fichier CSV"""
        try:
            # Créer le dossier si nécessaire
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                file.write(f"Algorithme,{algorithm_name}\n")
                file.write(f"Temps d'exécution,{execution_time:.4f}s\n")
                file.write(f"Coût total,{portfolio.total_cost}\n")
                file.write(f"Profit total,{portfolio.total_profit:.0f}\n")
                file.write(f"Nombre d'actions,{len(portfolio.actions)}\n")
                file.write(f"Budget restant,{500000 - portfolio.total_cost}\n")
                file.write("\n")
                file.write("Actions sélectionnées,Coût,Profit,Rentabilité (%)\n")
                
                for action in portfolio.actions:
                    file.write(f"{action.id},{action.cost},{action.profit:.0f},{action.profit_pct*100:.2f}%\n")
                    
        except Exception as e:
            print(f"❌ Erreur lors de l'export: {e}")
"""
Comparateur avec les résultats de référence de Sienna
Conforme aux exigences du projet d'analyse décisionnelle
"""


class SiennaComparator:
    """
    Compare les résultats avec ceux fournis par Sienna dans l'énoncé
    """
    
    # Résultats de référence de Sienna (depuis l'énoncé du projet)
    SIENNA_RESULTS = {
        'actions.csv': {
            'name': 'Dataset 1',
            'cost': 498760,
            'profit': 196610,
            'shares': ['Share-GRUT'],
            'note': 'Un seul Share mentionne dans l\'enonce'
        },
        'actions_medium.csv': {
            'name': 'Dataset 2',
            'cost': 489240,
            'profit': 193780,
            'shares': [
                'Share-ECAQ', 'Share-IXCI', 'Share-FWBE', 'Share-ZOFA',
                'Share-PLLK', 'Share-YFVZ', 'Share-ANFX', 'Share-PATS',
                'Share-NDKR', 'Share-ALIY', 'Share-JWGF', 'Share-JGTW',
                'Share-FAPS', 'Share-VCAX', 'Share-LFXB', 'Share-DWSK',
                'Share-XQII', 'Share-ROOM'
            ],
            'count': 18
        }
    }
    
    @classmethod
    def has_reference(cls, filename):
        """
        Vérifie si on a une référence Sienna pour ce fichier
        
        Args:
            filename: nom du fichier (ex: 'actions_medium.csv')
            
        Returns:
            bool: True si référence existe
        """
        return filename in cls.SIENNA_RESULTS
    
    @classmethod
    def compare(cls, filename, your_profit, your_cost, your_count):
        """
        Compare votre résultat avec Sienna
        
        Args:
            filename: nom du dataset
            your_profit: votre profit total
            your_cost: votre coût total
            your_count: nombre d'actions sélectionnées
            
        Returns:
            dict ou None: comparaison détaillée
        """
        if not cls.has_reference(filename):
            return None
        
        ref = cls.SIENNA_RESULTS[filename]
        
        # Calculs des différences
        profit_diff = your_profit - ref['profit']
        profit_pct = (profit_diff / ref['profit'] * 100) if ref['profit'] > 0 else 0
        
        cost_diff = your_cost - ref['cost']
        
        # Déterminer le verdict
        if your_profit > ref['profit']:
            verdict = 'MEILLEUR QUE SIENNA'
            symbol = '[+++]'
        elif abs(profit_pct) < 1:
            verdict = 'EQUIVALENT A SIENNA'
            symbol = '[===]'
        else:
            verdict = 'INFERIEUR A SIENNA'
            symbol = '[---]'
        
        return {
            'dataset_name': ref['name'],
            'your_profit': your_profit,
            'sienna_profit': ref['profit'],
            'profit_diff': profit_diff,
            'profit_pct': profit_pct,
            'your_cost': your_cost,
            'sienna_cost': ref['cost'],
            'cost_diff': cost_diff,
            'your_count': your_count,
            'sienna_count': ref.get('count', len(ref.get('shares', []))),
            'verdict': verdict,
            'symbol': symbol,
            'budget_ok': your_cost <= 500000,
            'note': ref.get('note', '')
        }
    
    @classmethod
    def display(cls, comparison):
        """
        Affiche la comparaison avec Sienna - Format professionnel
        
        Args:
            comparison: dict retourné par compare()
        """
        if not comparison:
            return
        
        # Codes couleur
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        
        # Déterminer la couleur selon le verdict
        if 'MEILLEUR' in comparison['verdict']:
            color = GREEN
        elif 'EQUIVALENT' in comparison['verdict']:
            color = YELLOW
        else:
            color = RED
        
        print()
        print(f"{CYAN}{BOLD}╔{'═' * 78}╗{RESET}")
        print(f"{CYAN}{BOLD}║{'COMPARAISON AVEC LES RESULTATS DE SIENNA':^78}║{RESET}")
        print(f"{CYAN}{BOLD}╚{'═' * 78}╝{RESET}")
        print()
        
        # Dataset
        print(f"{WHITE}{BOLD}Dataset: {CYAN}{comparison['dataset_name']}{RESET}")
        print()
        
        # Verdict
        print(f"{color}{BOLD}{comparison['symbol']} {comparison['verdict']}{RESET}")
        print("─" * 80)
        print()
        
        # Comparaison des profits
        print(f"{WHITE}{BOLD}PROFIT:{RESET}")
        print(f"  Votre resultat  : {GREEN}{BOLD}{comparison['your_profit']:>15,.2f} F CFA{RESET}")
        print(f"  Sienna          : {WHITE}{comparison['sienna_profit']:>15,.2f} F CFA{RESET}")
        
        diff_color = GREEN if comparison['profit_diff'] >= 0 else RED
        sign = "+" if comparison['profit_diff'] >= 0 else ""
        print(f"  Difference      : {diff_color}{BOLD}{sign}{comparison['profit_diff']:>15,.2f} F CFA ({comparison['profit_pct']:+.2f}%){RESET}")
        print()
        
        # Comparaison des coûts
        print(f"{WHITE}{BOLD}COUT:{RESET}")
        print(f"  Votre resultat  : {YELLOW}{comparison['your_cost']:>15,} F CFA{RESET}")
        print(f"  Sienna          : {WHITE}{comparison['sienna_cost']:>15,} F CFA{RESET}")
        print(f"  Difference      : {comparison['cost_diff']:>15,} F CFA")
        print()
        
        # Nombre d'actions
        print(f"{WHITE}{BOLD}NOMBRE D'ACTIONS:{RESET}")
        print(f"  Votre resultat  : {comparison['your_count']:>15}")
        print(f"  Sienna          : {comparison['sienna_count']:>15}")
        print()
        
        # Budget respecté ?
        if not comparison['budget_ok']:
            print(f"{RED}{BOLD}ATTENTION: BUDGET DEPASSE!{RESET}")
            print(f"  Limite      : 500,000 F CFA")
            print(f"  Votre cout  : {comparison['your_cost']:,} F CFA")
            print()
        else:
            print(f"{GREEN}{BOLD}[OK] Budget respecte (<= 500,000 F CFA){RESET}")
            print()
        
        # Note si présente
        if comparison['note']:
            print(f"{WHITE}Note: {comparison['note']}{RESET}")
            print()
        
        print("═" * 80)
        print()
# 🎯 Optimisateur d'Investissement

**Système intelligent d'optimisation de portefeuille sous contrainte budgétaire**

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Terminé-success.svg)

*Maximisez vos profits avec 500,000 F CFA*

</div>

## 📖 Présentation

Ce projet résout un problème classique d'optimisation financière : **sélectionner le meilleur portefeuille d'actions** pour maximiser le profit tout en respectant une contrainte budgétaire de **500,000 F CFA**.

## 🚀 Fonctionnalités

### 🎯 Algorithmes Implémentés
- **Force Brute** : Solution exacte garantie (petits datasets)
- **Programmation Dynamique** : Solution optimale et efficace  
- **Algorithme Glouton** : Solution rapide et approchée

### 📊 Interface
- Interface console épurée et intuitive
- Classification automatique des datasets
- Comparaison détaillée des algorithmes
- Résultats en temps réel avec métriques

## 🛠️ Installation & Utilisation

### Prérequis
- Python 3.8 ou supérieur

### Lancement
```bash
# Cloner le projet
git clone https://github.com/micheloulai93-creator/Projet-Python-2.2.git
cd Projet-Python-2.2

# Lancer l'application
python main.py
Format des données
Créez un fichier CSV dans le dossier data/ :

csv
action,coût,profit
Action_A,50000,15000
Action_B,75000,22000
Action_C,120000,45000
🏗️ Architecture
text
Projet-Python-2.2/
├── algorithms/          # Moteurs d'optimisation
│   ├── brute_force.py  # Solution exacte
│   ├── dynamic.py      # Solution optimisée
│   └── greedy.py       # Solution efficace
├── models/             # Classes métier
│   ├── action.py       # Modèle Action
│   └── portfolio.py    # Modèle Portfolio
├── views/              # Interface utilisateur
│   └── console_view.py # Vue console minimaliste
├── controllers/        # Logique applicative
├── data/               # Datasets d'exemple
└── main.py            # Point d'entrée
📈 Exemple de Résultats
text
══════════════════════════════════════════════
      OPTIMISATEUR D'INVESTISSEMENT
Budget: 500,000 F CFA
══════════════════════════════════════════════

DATASETS DISPONIBLES:
──────────────────────────────
 1. debug_actions.csv
    5 actions • Rapide
 2. test_actions.csv
    15 actions • Standard

Choix (1-2): 1
→ debug_actions.csv

──────────────────────────────
Actions: 5
Profit max: 85,000 F CFA

──────────────────────────────
Force Brute
Profit: 45,000 F CFA
Temps: 0.12s
Actions: 2
Efficacité: 52.9%

──────────────────────────────
COMPARAISON
Force Brute: 45,000 F CFA ✓
Algorithme Glouton: 45,000 F CFA

1. Nouvelle analyse
2. Quitter
🎯 Stratégies d'Optimisation
Le programme classe automatiquement les datasets :

Petits datasets (≤20 actions) : Force Brute activée

Datasets moyens (20-100 actions) : Programmation Dynamique

Grands datasets (>100 actions) : Algorithme Glouton

👨‍💻 Auteur
Michel Oulai

GitHub: @micheloulai93-creator

📝 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

<div align="center">
Développé avec Python 🐍

</div> ```
📋 Fichiers à mettre à jour sur GitHub
1. Fichiers MODIFIÉS :
views/console_view.py ✅ (votre version finale)

README.md ✅ (celui ci-dessus)

2. Fichiers EXISTANTS (déjà sur GitHub) :
main.py

algorithms/ (brute_force.py, dynamic.py, greedy.py)

models/ (action.py, portfolio.py)

controllers/

data/ (vos fichiers CSV)

requirements.txt
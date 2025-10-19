# 🎯 Optimisateur d'Investissement

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Terminé-success.svg)

**Système d'optimisation de portefeuille sous contrainte budgétaire**

*Maximisez vos profits avec 500,000 F CFA*

</div>

## 📖 Présentation

Application Python qui résout le problème de sélection d'actions pour maximiser le profit sous une contrainte budgétaire de **500,000 F CFA**.

## ✨ Fonctionnalités

- 🎯 **3 algorithmes d'optimisation** : Force Brute, Glouton, Programmation Dynamique
- 📊 **Interface console avancée** avec design ASCII
- 📁 **Support multiple formats** : CSV et Excel
- ⚡ **Analyse comparative** des performances
- 💰 **Calcul d'efficacité** et métriques détaillées


📁 Structure
text
projet/
├── algorithms/    # Algorithmes d'optimisation
├── models/       # Classes Action et Portfolio  
├── views/        # Interface console
├── data/         # Fichiers CSV/Excel
└── main.py       # Programme principal
📊 Utilisation
Préparez un fichier CSV :

csv
action,coût,profit
Action_A,50000,15000
Action_B,75000,22000
## 🚀 Installation & Utilisation

### Prérequis
- Python 3.8+
- Fichiers CSV/Excel avec colonnes : action, coût, profit

### Installation
```bash
# Cloner le projet
git clone https://github.com/votre-username/optimisateur-investissement.git
cd optimisateur-investissement

# Lancer l'application
python main.py


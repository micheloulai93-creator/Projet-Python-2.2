# 🎯 Optimisateur d'Investissement

**Sélectionner le meilleur portefeuille d'actions pour maximiser le profit avec un budget de 500,000 F CFA**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Terminé-success.svg)

---

## 📖 À propos

Ce programme résout un problème d'optimisation financière : **choisir les meilleures actions à acheter** pour maximiser le profit après 2 ans, avec un budget limité à 500,000 F CFA.

**Contraintes** :
- Budget maximum : 500,000 F CFA
- Chaque action peut être achetée 0 ou 1 fois (pas de fractions)
- Objectif : Maximiser le profit total

---

## 🚀 Installation et Lancement

```bash
# Cloner le projet
git clone https://github.com/micheloulai93-creator/Projet-Python-2.2.git
cd Projet-Python-2.2

# Lancer le programme
python main.py
```

**Prérequis** : Python 3.8 ou supérieur (aucune librairie externe nécessaire)

---

## 💡 Comment ça marche ?

### 1. Le programme liste automatiquement vos fichiers CSV dans `data/`

```
DATASETS DISPONIBLES
────────────────────────────────────────────────────
[1] actions.csv          (957 actions - Très grand)
[2] actions_medium.csv   (541 actions - Grand)
[3] debug_actions.csv    (5 actions - Petit)
[4] test_actions.csv     (20 actions - Test)
```

### 2. Vous choisissez un dataset

```
Sélectionnez un dataset (1-4) ou (q) pour quitter: 3
```

### 3. Vous choisissez les algorithmes à exécuter

```
[1] Force Brute           - Optimal mais lent (≤ 22 actions)
[2] Programmation Dynamique - Optimal et rapide
[3] Algorithme Glouton    - Très rapide (~98% optimal)
[A] Tous les algorithmes

Votre choix: A
```

### 4. Le programme affiche les résultats

```
╔═══════════════════════════════════════════════════╗
║         RÉSULTATS: PROGRAMMATION DYNAMIQUE        ║
╚═══════════════════════════════════════════════════╝

Profit: 311,489 F CFA
Coût: 499,870 F CFA (99.9% du budget)
Actions sélectionnées: 24
Rendement: 62.3%
Temps d'exécution: 10.8s

TOP 5 ACTIONS SÉLECTIONNÉES:
 1. Share-NWDK    42,830 F → 32,037 F (74.8%)
 2. Share-MJEL    32,780 F → 30,551 F (93.2%)
 3. Share-JEZT    31,060 F → 28,047 F (90.3%)
 4. Share-OQKF    36,800 F → 22,301 F (60.6%)
 5. Share-GSGQ    43,320 F → 21,383 F (49.4%)
```

### 5. Comparaison automatique avec les résultats de référence

```
COMPARAISON AVEC SIENNA
────────────────────────────────────────────────────
[+++] MEILLEUR QUE SIENNA

Votre profit  : 311,489 F CFA
Sienna        : 196,610 F CFA
Différence    : +114,879 F CFA (+58.43%)
```

---

## 🎯 Les 3 Algorithmes

### 1️⃣ Force Brute
- **Ce qu'il fait** : Teste toutes les combinaisons possibles
- **Avantage** : Garantit la meilleure solution
- **Limite** : Fonctionne jusqu'à 22 actions maximum (après c'est trop lent)
- **Temps** : Quelques secondes pour 20 actions

### 2️⃣ Programmation Dynamique
- **Ce qu'il fait** : Résout le problème intelligemment en mémorisant les résultats
- **Avantage** : Optimal et rapide, fonctionne pour tous les datasets
- **Temps** : ~10 secondes pour 957 actions

### 3️⃣ Algorithme Glouton
- **Ce qu'il fait** : Sélectionne les actions par meilleur ratio profit/coût
- **Avantage** : Ultra-rapide (millisecondes)
- **Limite** : Pas toujours optimal, mais proche (~98%)
- **Temps** : < 0.01 seconde pour 957 actions

---

## 📊 Format des Données

Créez vos fichiers CSV dans le dossier `data/` avec ce format :

```csv
id,cost,profit_pct
Action-1,20000,0.05
Action-2,30000,0.10
Action-3,50000,0.15
```

**Colonnes** :
- `id` : Nom de l'action
- `cost` : Coût en F CFA
- `profit_pct` : Profit après 2 ans (0.10 = 10%)

**Le programme nettoie automatiquement** les données invalides (coûts négatifs, valeurs nulles, etc.)

---

## 📁 Structure du Projet

```
Projet-Python-2.2/
│
├── main.py                  # Lancer ce fichier
│
├── controllers/             # Logique du programme
│   ├── algorithm_controller.py
│   ├── brute_force_controller.py
│   ├── dynamic_controller.py
│   ├── greedy_controller.py
│   └── sienna_comparator.py
│
├── models/                  # Données
│   ├── action.py
│   └── portfolio.py
│
├── views/                   # Interface console
│   └── console_view.py
│
├── data/                    # Vos fichiers CSV ici
│   ├── actions.csv
│   ├── actions_medium.csv
│   ├── debug_actions.csv
│   └── test_actions.csv
│
└── results/                 # Résultats exportés (CSV)
```

---

## ✨ Fonctionnalités

✅ **Classification automatique** : Le programme détecte la taille du dataset et recommande les algorithmes adaptés

✅ **Comparaison entre algorithmes** : Compare automatiquement les résultats (profit, temps, efficacité)

✅ **Comparaison avec Sienna** : Vérifie si vous faites mieux que la référence

✅ **Export automatique** : Tous les résultats sont sauvegardés dans `results/`

✅ **Interface intuitive** : Menu interactif avec affichage en temps réel

✅ **Statistiques détaillées** : Profit, rendement, utilisation du budget, temps d'exécution

---

## 📈 Performances

| Dataset | Actions | Force Brute | Prog. Dynamique | Glouton |
|---------|---------|-------------|-----------------|---------|
| debug (5) | 5 | 0.001s | 0.002s | < 0.001s |
| test (20) | 20 | ~2-5s | 0.5s | < 0.01s |
| medium (541) | 541 | ❌ Impossible | 5.1s | 0.002s |
| large (957) | 957 | ❌ Impossible | 10.8s | 0.003s |

---

## 🎓 Pourquoi 3 algorithmes ?

**Force Brute** : Pour comprendre le problème et valider les autres algorithmes sur de petits exemples

**Programmation Dynamique** : La vraie solution pour les datasets réels (optimal + rapide)

**Algorithme Glouton** : Quand on a besoin d'une réponse en millisecondes

---

## 🛠️ Dépannage

**"Aucun fichier trouvé"** → Placez vos fichiers CSV dans le dossier `data/`

**"Force brute limitée à 22 actions"** → C'est normal ! Pour les gros datasets, utilisez la Programmation Dynamique

**"Aucune action valide"** → Vérifiez le format CSV (id, cost, profit_pct) et supprimez les lignes avec coûts négatifs

---

## 👨‍💻 Auteur

**Michel Oulai**
- GitHub: [@micheloulai93-creator](https://github.com/micheloulai93-creator)

---

## 📝 Licence

MIT License - Utilisez librement ce code

---

<div align="center">

**Développé avec Python 🐍**

*Projet d'Analyse Décisionnelle*

</div>
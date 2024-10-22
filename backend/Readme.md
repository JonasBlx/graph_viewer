# Graph Viewer - Backend

## Description du projet

Le projet **Graph Viewer** est une application web qui permet de générer et visualiser un graphe aléatoire en 3D. L'utilisateur peut spécifier le nombre de nœuds ainsi que le taux de connectivité (probabilité de connexion entre les nœuds). Une fois généré, le graphe peut être coloré à l'aide de l'algorithme de coloration **DSATUR**, fourni par la librairie **pyclustering**.

Le backend de ce projet est construit avec **FastAPI**, et il fournit deux endpoints principaux :
1. **Génération de graphe aléatoire**.
2. **Coloration de graphe avec l'algorithme DSATUR**.

Le projet complet est disponible sur GitHub à l'adresse suivante :  
[https://github.com/JonasBlx/graph_viewer](https://github.com/JonasBlx/graph_viewer)

---

## Prérequis

Avant de démarrer, assurez-vous d'avoir les éléments suivants installés sur votre machine :
- Python 3.x
- **virtualenv** pour créer des environnements virtuels Python

---

## Installation et configuration du backend

Suivez ces étapes pour configurer et lancer le backend.

### 1. Cloner le projet

```bash
git clone https://github.com/JonasBlx/graph_viewer.git
cd graph_viewer/backend
```

### 2. Créer un environnement virtuel

Créez et activez un environnement virtuel pour isoler les dépendances du projet.

#### Sur macOS/Linux :

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Sur Windows :

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Installer les dépendances

Installez les dépendances listées dans le fichier `requirements.txt` à l'aide de `pip` :

```bash
pip install -r requirements.txt
```

### 4. Lancer le serveur backend

Une fois les dépendances installées, vous pouvez lancer le serveur backend avec **uvicorn**.

```bash
uvicorn api:app --reload --port 9191
```

Le serveur sera disponible à l'adresse suivante : [http://localhost:9191](http://localhost:9191).

Vous pouvez accéder à la documentation interactive de l'API générée par FastAPI à l'adresse [http://localhost:9191/docs](http://localhost:9191/docs).

---

## Fichier `requirements.txt`

Le fichier `requirements.txt` contient les bibliothèques Python nécessaires pour exécuter le backend du projet.

```txt
fastapi
uvicorn
pyclustering
random-color
```

---

## Points d'API

Le backend fournit deux endpoints principaux :

### 1. Génération d'un graphe aléatoire
- **Méthode** : `GET`
- **URL** : `/random`
- **Paramètres** :
  - `number_of_nodes` (int) : Le nombre de nœuds dans le graphe.
  - `probability_connection` (float) : La probabilité de connexion entre les nœuds (valeur entre 0 et 1).
- **Réponse** : Un objet `Graph` avec les nœuds et les liens générés.

### 2. Coloration d'un graphe avec l'algorithme DSATUR
- **Méthode** : `POST`
- **URL** : `/graph/color/dsatur`
- **Corps de la requête** : Un objet `Graph` représentant le graphe à colorer.
- **Réponse** : Un objet `Graph` avec les nœuds colorés par l'algorithme DSATUR.

---

## Technologies utilisées

- **FastAPI** : Framework pour construire des API rapides en Python.
- **Pydantic** : Gestion et validation des modèles de données.
- **pyclustering** : Algorithme de coloration de graphe (DSATUR).
- **random-color** : Génération de couleurs aléatoires pour les nœuds du graphe.

---

## Auteur

Développé par [JonasBlx].

Le projet est hébergé sur GitHub :  
[https://github.com/JonasBlx/graph_viewer](https://github.com/JonasBlx/graph_viewer)

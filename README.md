# Gamedle

Bienvenue sur le projet **Gamedle**, un jeu en ligne inspiré de Wordle ou LoLdle (selon votre référence), mais pour les jeux de société ! Testez vos connaissances en devinant un jeu à partir de ses caractéristiques.

---

## Installation et Lancement

### 1. Cloner le repo
```sh
git clone https://github.com/Adri-dou/Gamedle.git
cd Gamedle
```

### 2️. Installer les dépendances
#### Backend (Node.js + Express + MySQL)
```bash
npm install
```
#### Frontend (Vue.js)
```bash
cd frontend
npm install
```

### 2. Acquérir le dataset et créer la base de données
Les datasets qui vont constituer notre base de données se trouvent [sur ce lien Kaggle](https://www.kaggle.com/datasets/joebeachcapital/board-games).
- Téléchargez les deux fichiers `.csv` et mettez-les dans le dossier `dataset`.
- Lancez le fichier python `create-insertion-file.py`

Ce script va créer le fichier `insertion-file.sql` qui servira à peupler notre base de données.

### 3️. Configurer la base de données et variables d'environnement
- Ayez **MySQL** installé et en cours d'exécution.
- Dans **MySQL Workbench**, créez une base de données nommée `gamedle` (ou comme vous voulez).
- Lancez le fichier `table-creation.sql` pour créer les tables de notre BDD.
- Puis peuplez la base de données en lançant le fichier `insertion-file.sql` précédemment créé.

- Dans la racine du projet, créez votre variable d'environnement `.env` comme suit :
```bash
PORT=3000
DB_HOST=localhost
DB_USER=root
DB_PASS=votreMDP
DB_NAME=gamedle
```
Notez que ce sont des données génériques, nous utiliserons le port 3000 pour l'API (si vous devez le changer, changez-le aussi dans le `main.js` du frontend).
Remplacez les autres telles qu'elles sont dans votre connexion MySQL.

### 4️. Lancer l'application
#### Démarrer le backend
Tapez dans un terminal depuis la racine du projet :
```bash
node backend/index.js
```
#### Démarrer le frontend
Ouvrez un 2e terminal et lancez le client depuis le frontend :
```bash
cd frontend
npm run serve
```

L'application devrait se lancer sur `http://localhost:8080`

---

## Fonctionnalités
- Page d'accueil 
- Page de jeu 
- Page "À propos" (Liste des jeux)
- Connexion administrateur
  

---

## Prérequis
- **Backend** : Node.js, Express.js, MySQL
- **Frontend** : Vue.js

---

**Amusez-vous bien avec Gamedle !**


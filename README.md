# Gamedle

Bienvenue sur le projet **Gamedle**, un jeu en ligne inspiré de Wordle ou LoLdle (selon votre référence), mais pour les jeux de société ! Testez vos connaissances en devinant un jeu à partir de ses caractéristiques.

---

## Installation et Lancement

### 1. Cloner le repo
```sh
git clone https://github.com/votre-utilisateur/boardgame-loldle.git
cd Gamedle
```

### 2️. Installer les dépendances
#### Backend (Node.js + Express + MySQL)
```sh
npm install
```
#### Frontend (Vue.js)
```sh
cd frontend
npm install
```

### 3️. Configurer la base de données et variables d'environnement
- Ayez **MySQL** installé et en cours d'exécution.
- Dans **MySQL Workbench**, créez une base de données nommée `gamedle` (ou comme vous voulez).
- Complétez la base de données en exécutant ces requêtes SQL : 
**`To Do : donner le fichier SQL pour comléter la BDD`**

- Allez dans le dossier `backend` et créez votre variable d'environnement `.env` comme suit :
```
PORT=3000
DB_HOST=localhost
DB_USER=root
DB_PASS=votreMDP
DB_NAME=gamedle
```
Notez que ce sont des données génériques, vous pouvez changer le port de l'API au besoin, et remplacez les autres telles qu'elles sont dans votre connexion MySQL.

### 4️. Lancer l'application
#### Démarrer le backend
Depuis la racine du projet :
```sh
node backend/index.js
```
#### Démarrer le frontend
```sh
cd frontend
npm run serve
```

L'application devrait se lancer sur `http://localhost:8080`

---

## Fonctionnalités
- 🔹 Page d'accueil (pas encore de style)
- 🔹 Page de jeu (idem, et logique de jeu non implémentée)
- 🔹 Page "À propos" (toujours aucun style)
- 🔹 Connexion administrateur (à venir)

---

## Prérequis
- **Backend** : Node.js, Express.js, MySQL
- **Frontend** : Vue.js

---

**Amusez-vous bien avec Gamedle !**


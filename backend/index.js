require('dotenv').config();

const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Connexion à la base de données
const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME
});


db.connect(err => {
  if (err) {
    console.error('Échec de la connexion à MySQL:', err);
  } else {
    console.log('Connecté à MySQL');
    initializeGameOfTheDay(); // Ajout de l'initialisation
  }
});

// Nouvelle fonction à ajouter
function initializeGameOfTheDay() {
  const today = new Date().toISOString().split('T')[0];
  
  const checkQuery = 'SELECT * FROM GameOfTheDay WHERE date = ?';
  db.query(checkQuery, [today], (err, results) => {
    if (err) {
      console.error('Erreur lors de la vérification de la date:', err);
      return;
    }
    
    if (results.length === 0) {
      db.query('CALL get_random_game()', (err, randomResults) => {
        if (err) {
          console.error('Erreur lors de la récupération du jeu aléatoire:', err);
          return;
        }
        
        const randomGame = randomResults[0][0];
        const insertQuery = 'INSERT INTO GameOfTheDay (date, game_id) VALUES (?, ?)';
        
        db.query(insertQuery, [today, randomGame.game_id], (err) => {
          if (err) {
            console.error('Erreur lors de l\'insertion du jeu du jour:', err);
          } else {
            console.log(`Jeu du jour (${today}) inséré avec l'ID ${randomGame.game_id}`);
          }
        });
      });
    } else {
      console.log(`Jeu du jour (${today}) déjà présent`);
    }
  });
}


// Route test
app.get('/', (req, res) => {
  res.send('<h1>Gamedle API is running</h1>');
});
//-----------------------------------------------------------------------------------------------------------
// A-propos 
// Tous les jeux (via la vue GameDetails)
app.get('/games', (req, res) => {
  const query = `SELECT * FROM GameDetails ORDER BY Classement ASC`;
  db.query(query, (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(results);
  });
});

// Rechercher un jeu par son nom via la procédure stockée
app.get('/search', (req, res) => {
    const gameName = req.query.name;
    if (!gameName) {
      return res.status(400).json({ error: 'Le nom du jeu est requis dans le paramètre ?name=' });}
    const query = `CALL search_game(?)`;
    db.query(query, [gameName], (err, results) => {
      if (err) return res.status(500).json({ error: err.message });
      // Résultat de procédure stockée = tableau avec 1er élément : résultats de SELECT
      res.json(results[0]);
    });
  });  

// Jeu aléatoire (via procédure)
app.get('/random-game', (req, res) => {
  db.query('CALL get_random_game()', (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(results[0][0]); // Résultat de la procédure
  });
});

// Détails d’un jeu par ID (via GameDetails)
app.get('/games/:id', (req, res) => {
  const id = req.params.id;
  const query = 'SELECT * FROM GameDetails WHERE game_id = ?';
  db.query(query, [id], (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    if (results.length === 0) return res.status(404).json({ error: 'Jeu non trouvé' });
    res.json(results[0]);
  });
});

// Jeu par nom exact
app.get('/games/:name', (req, res) => {
  const name = req.params.name;
  const query = 'CALL search_game(?)';
  db.query(query, [name], (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    if (results[0].length === 0) return res.status(404).json({ error: 'Jeu non trouvé' });
    res.json(results[0][0]);
  });
});

// Route pour récupérer le jeu du jour
app.get('/game-of-the-day', (req, res) => {
  const today = new Date().toISOString().split('T')[0];
  const query = `
    SELECT * FROM View_GameOfTheDay where date = ?;
  `;
  
  db.query(query, [today], (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    if (results.length === 0) return res.status(404).json({ error: 'Jeu du jour non trouvé' });
    res.json(results[0]);
  });
});

// Lancement du serveur
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ API Gamedle dispo sur http://localhost:${PORT}`));

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
  }
});

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

//-----------------------------------------------------------------------------------------------------------
// GameViews 
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
app.get('/games/name/:name', (req, res) => {
  const name = req.params.name;
  const query = 'SELECT * FROM GameDetails WHERE name = ?';
  db.query(query, [name], (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    if (results.length === 0) return res.status(404).json({ error: 'Jeu non trouvé' });
    res.json(results[0]);
  });
});

// Lancement du serveur
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ API Gamedle dispo sur http://localhost:${PORT}`));

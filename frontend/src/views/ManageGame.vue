<template>
    <div class="manage-game">
      <h2>Gérer les jeux</h2>
  
      <!-- Formulaire d’ajout -->
      <form @submit.prevent="addGame" class="game-form">
  <h2>Ajouter un nouveau jeu</h2>

  <label>ID du jeu</label>
  <input v-model.number="game.game_id" type="number" placeholder="ID du jeu" required />

  <label>Nom du jeu</label>
  <input v-model="game.name" placeholder="Nom du jeu" required />

  <label>Classement</label>
  <input v-model.number="game.ranking" type="number" placeholder="Classement" required />

  <label>Âge minimum</label>
  <input v-model.number="game.minAge" type="number" placeholder="Âge minimum" required />

  <label>Min joueurs</label>
  <input v-model.number="game.minPlayer" type="number" placeholder="Min joueurs" required />

  <label>Max joueurs</label>
  <input v-model.number="game.maxPlayer" type="number" placeholder="Max joueurs" required />

  <label>Année de publication</label>
  <input v-model.number="game.year" type="number" placeholder="Année de publication" required />

  <label>Description</label>
  <input v-model="game.description" placeholder="Description" />

  <label>Durée (minutes)</label>
  <input v-model.number="game.playingTimeMinutes" type="number" placeholder="Durée (minutes)" />

  <label>ID de l'éditeur</label>
  <input v-model.number="game.publisher_id" type="number" placeholder="ID de l'éditeur" />

  <button type="submit">Ajouter le jeu</button>
</form>

  
      <p v-if="message">{{ message }}</p>
  
      <h3>Liste des jeux</h3>
<div class="game-list">
  <div class="game-card" v-for="game in games" :key="game.game_id">
    <h4>{{ game.name }}</h4>
    <p><strong>ID:</strong> {{ game.game_id }}</p>
    <p><strong>Âge minimum:</strong> {{ game.minAge }} ans</p>
    <p><strong>Joueurs:</strong> {{ game.minPlayer }} - {{ game.maxPlayer }}</p>
    <p><strong>Année:</strong> {{ new Date(game.yearPublished).getFullYear() }}</p>
    <button @click="deleteGame(game.game_id, game.name)">Supprimer</button>
  </div>
</div>

    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, getCurrentInstance } from 'vue';
  
  const game = ref({
    game_id: null,
    name: '',
    ranking: 0,
    minAge: 0,
    minPlayer: 0,
    maxPlayer: 0,
    year: null, // Année (sera transformée)
    description: '',
    playingTimeMinutes: 0, // Minutes (sera transformé)
    publisher_id: null
  });
  
  const games = ref([]);
  const message = ref('');
  const { proxy } = getCurrentInstance();
  const apiBase = proxy.$apiBase;
  
  // Charger tous les jeux
  const fetchGames = async () => {
  try {
    const res = await fetch(`${apiBase}/all-games`);
    const data = await res.json();
    games.value = data;
  } catch (err) {
    console.error('Erreur lors du chargement des jeux:', err);
  }
};

  
  // Ajouter un jeu
  const addGame = async () => {
    const gameData = {
      game_id: game.value.game_id,
      name: game.value.name,
      ranking: game.value.ranking,
      minAge: game.value.minAge,
      minPlayer: game.value.minPlayer,
      maxPlayer: game.value.maxPlayer,
      yearPublished: `${game.value.year}-01-01`,
      description: game.value.description,
      playingTime: formatTime(game.value.playingTimeMinutes),
      publisher_id: game.value.publisher_id || null
    };
  
    try {
      const res = await fetch(`${apiBase}/add-game`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gameData)
      });
      const data = await res.json();
      message.value = data.message;
      fetchGames();
    } catch (err) {
      message.value = 'Erreur lors de l’ajout du jeu';
    }
  };
  
  // Convertir des minutes en HH:MM:SS
  const formatTime = (minutes) => {
    const hrs = Math.floor(minutes / 60).toString().padStart(2, '0');
    const mins = (minutes % 60).toString().padStart(2, '0');
    return `${hrs}:${mins}:00`;
  };
  
  // Supprimer un jeu
  const deleteGame = async (id, name) => {
  const confirmed = confirm(`Voulez-vous vraiment supprimer le jeu "${name}" (ID: ${id}) ?`);
  if (!confirmed) {
    return; // Si l'utilisateur annule, on quitte sans rien faire
  }

  try {
    const res = await fetch(`${apiBase}/delete-game/${id}`, {
      method: 'DELETE'
    });
    const data = await res.json();
    message.value = data.message;
    fetchGames();
  } catch (err) {
    message.value = 'Erreur lors de la suppression';
  }
};

  
  onMounted(fetchGames);
  </script>
  
  <style scoped>
  .manage-game {
    padding: 20px;
  }
  
  .game-form {
    display: grid;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  input {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    margin: 10px 0;
  }

  .game-form {
  background-color: rgba(0, 0, 0, 0.1); /* Fond léger et transparent */
  padding: 20px;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 500px;
  margin: 30px auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Petite ombre sympa */
}

.game-form h2 {
  text-align: center;
  margin-bottom: 10px;
  color: #333;
}

.game-form input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1em;
}

.game-form input:focus {
  border-color: #6aaa64; /* Vert clair au focus */
  outline: none;
}

.game-form button {
  padding: 12px;
  background-color: #6aaa64;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.game-form button:hover {
  background-color: #5c9a58;
}
.game-form label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

h2{
  text-align: center;
  color: #333;
  margin-bottom: 20px;
  
}

.game-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.game-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.game-card:hover {
  transform: translateY(-5px);
}

.game-card h4 {
  margin-top: 0;
  color: #333;
  font-size: 1.2em;
}

.game-card p {
  margin: 5px 0;
  color: #555;
}

.game-card button {
  margin-top: 10px;
  width: 100%;
  background-color: #e74c3c;
  border: none;
  padding: 10px;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.game-card button:hover {
  background-color: #c0392b;
}

  </style>

  
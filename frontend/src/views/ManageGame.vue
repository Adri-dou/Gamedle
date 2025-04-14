<template>
    <div class="manage-game">
      <h2>Gérer les jeux</h2>
  
      <!-- Formulaire d’ajout -->
      <form @submit.prevent="addGame" class="game-form">
        <input v-model.number="game.game_id" type="number" placeholder="ID du jeu" required />
        <input v-model="game.name" placeholder="Nom du jeu" required />
        <input v-model.number="game.ranking" type="number" placeholder="Classement" required />
        <input v-model.number="game.minAge" type="number" placeholder="Âge minimum" required />
        <input v-model.number="game.minPlayer" type="number" placeholder="Min joueurs" required />
        <input v-model.number="game.maxPlayer" type="number" placeholder="Max joueurs" required />
        <input v-model.number="game.year" type="number" placeholder="Année de publication" required />
        <input v-model="game.description" placeholder="Description" />
        <input v-model="game.playingTimeMinutes" type="number" placeholder="Durée (minutes)" />
        <input v-model.number="game.publisher_id" type="number" placeholder="ID de l'éditeur" />
        <button type="submit">Ajouter le jeu</button>
      </form>
  
      <p v-if="message">{{ message }}</p>
  
      <h3>Liste des jeux</h3>
      <ul>
        <li v-for="game in games" :key="game.game_id">
          {{ game.name }} (ID: {{ game.game_id }}) - 
          <button @click="deleteGame(game.game_id, game.name)">Supprimer</button>
        </li>
      </ul>
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
      const res = await fetch(`${apiBase}/games`);
      games.value = await res.json();
    } catch (err) {
      message.value = 'Erreur lors du chargement des jeux';
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
  const deleteGame = async (id) => {
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
  </style>
  
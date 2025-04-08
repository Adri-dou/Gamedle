<template>
  <div class="main-container">
    <h1 class="about-title">À propos</h1>  

    <div class="rules-container">
      <h2>Règles de Gamedle</h2>
      <p>
        Gamedle est un jeu où vous devez deviner le nom d'un jeu de société en utilisant les indices qui vous sont donnés.
        Chaque indice vous rapproche un peu plus de la solution. À chaque tentative, vous serez informé des catégories,
        du nombre de joueurs, de l'année de publication, et d'autres caractéristiques du jeu.
        Faites vos meilleurs choix pour deviner rapidement le jeu !
      </p>
    </div>

    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchQuery" 
        @input="filterGames" 
        placeholder="Rechercher un jeu..." 
        class="search-input"
      />
    </div>

    <!-- Liste des jeux filtrée -->
    <ul class="game-list">
      <li v-for="game in filteredGames" :key="game.game_id" class="game-item">
        <div class="game-header">
          <strong class="game-title">{{ game.Nom_Jeu }}</strong>
          <span class="game-ranking">Classement : {{ game.Classement }}</span>
        </div>
        <div class="game-details">
          <p><strong>Catégories :</strong> {{ game.Catégories || 'Non classé' }}</p>
          <p><strong>Joueurs :</strong> {{ game.Min_Joueurs }} à {{ game.Max_Joueurs }}</p>
          <p><strong>Année de Sortie :</strong> {{ game.Annee_Publication || 'Inconnue' }}</p>
          <p><strong>Éditeur :</strong> {{ game.Editeur || 'Inconnu' }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>


<script setup>
import { ref, onMounted, getCurrentInstance } from 'vue';

const games = ref([]);
const searchQuery = ref('');
const filteredGames = ref([]);

// Accès à $apiBase défini dans main.js
const { proxy } = getCurrentInstance();
const apiBase = proxy.$apiBase;

const fetchGames = async () => {
  try {
    const response = await fetch(`${apiBase}/games`);
    games.value = await response.json();
    filteredGames.value = games.value;
  } catch (error) {
    console.error('Erreur lors du chargement des jeux :', error);
  }
};

const filterGames = async () => {
  if (!searchQuery.value) {
    filteredGames.value = games.value;
    return;
  }
  try {
    const response = await fetch(`${apiBase}/search?name=${encodeURIComponent(searchQuery.value)}`);
    const result = await response.json();
    filteredGames.value = result;
  } catch (error) {
    console.error('Erreur lors de la recherche :', error);
    filteredGames.value = [];
  }
};

onMounted(fetchGames);
</script>


<style scoped>

.main-container {
  padding: 20px;
}

.about-title {
  text-align: center;
  color: #3f51b5;
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.rules-container {
  background-color: rgba(249, 249, 249, 0.8);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.rules-container h2 {
  font-size: 1.8rem;
  color: #3f51b5;
  margin-bottom: 10px;
}

.rules-container p {
  font-size: 1rem;
  color: #555;
}

.search-bar {
  margin-bottom: 20px;
  text-align: center;
}

.search-bar input {
  font-family: "ADLaM Display", sans-serif;
  font-size: 15px;
  border-radius: 20px;
  border: inset #b0efb1 3px;
}

.search-input {
  width: 60%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #3f51b5;
}

.game-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.game-item {
  background-color: rgba(249, 249, 249, 0.8);
  border-radius: 8px;
  margin: 10px 0;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.game-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.game-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.game-title {
  font-size: 1.5rem;
  color: #333;
  font-weight: bold;
}

.game-ranking {
  font-size: 1rem;
  color: #4caf50; 
}

.game-details p {
  margin: 5px 0;
  font-size: 1rem;
  color: #555;
}

.game-details strong {
  color: #3f51b5;
}
</style>

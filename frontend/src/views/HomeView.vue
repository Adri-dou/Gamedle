<template>
  <div class="game-container">
    <img src="@/assets/Gamedle_Logo.png" alt="Gamedle" class="logo" />

    <h2>Devine un jeu de société</h2>

    <div class="button-container">
      <router-link to="/jeu" class="mode-button">Classique</router-link>
      <p class="hint">Des indices à chaque essai</p>
    </div>

    <router-link to="/a-propos" class="about-button">À propos</router-link>
  </div>
</template>


<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%; /* Prend toute la largeur */
  text-align: center;
  color: white;
  position: relative;
  padding-bottom: 20%; /* Ajout d'espace en bas pour le bouton "À propos" */
}


/* Logo */
.logo {
  width: 400px;
  margin-top: 20px;
  margin-bottom: 20px;
}

/* Titre */
h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color:black;
}

/* Conteneur du bouton "Classique" */
.button-container {
  background: rgba(255, 255, 255, 0.5);
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50%;
  height: 100px;    
}

/* Bouton "Classique" */
.mode-button {
  background: rgba(255, 255, 255, 0.7);
  border: none;
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
  color: black;
  transition: 0.3s;
  width: 25%;
  height: 200px;  
  display: flex; 
  align-items: center; 
  justify-content: center;
  text-align: center; 
}


.mode-button:hover {
  background: #ddd;
}

/* Texte d'indice */
.hint {
  font-size: 14px;
  font-weight: bold;
  color: black;
}

/* Bouton "À propos" */
.about-button {
  position: absolute;
  bottom: 20px;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background: rgba(0, 0, 0, 0.6);
  padding: 10px 20px;
  border-radius: 8px;
  transition: 0.3s;
}

.about-button:hover {
  background: rgba(0, 0, 0, 0.8);
}
</style>

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
  width: 100%;
  text-align: center;
  color: white;
  padding-bottom: 8rem;
  position: relative;
}

/* Logo */
.logo {
  width: 25rem;
  margin: 2rem 0;
}

/* Titre */
h2 {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

/* Conteneur du bouton */
.button-container {
  background-color: rgba(255, 255, 255, 0.5);
  padding: 1.5rem;
  border-radius: 0.75rem;
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

/* Bouton "Classique" */
.mode-button {
  background-color: rgba(255, 255, 255, 0.7);
  border: none;
  padding: 1rem 2rem;
  font-size: 1.25rem;
  font-weight: bold;
  color: black;
  text-decoration: none;
  border-radius: 0.5rem;
  transition: background-color 0.3s;
  font-family: "ADLaM Display", sans-serif;
  width: 100%;
  max-width: 15rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mode-button:hover {
  background-color: #ddd;
}

/* Indice */
.hint {
  font-size: 0.9rem;
  font-weight: bold;
  color: black;
}

/* Bouton "À propos" */
.about-button {
  position: absolute;
  bottom: 1.5rem;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  text-decoration: none;
  border-radius: 0.5rem;
  font-family: "ADLaM Display", sans-serif;
  transition: background-color 0.3s;
}

.about-button:hover {
  background-color: rgba(0, 0, 0, 0.8);
}
</style>

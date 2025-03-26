<template>
  <div>
    <nav>
      <router-link to="/">Accueil</router-link> |
      <router-link to="/jeu">Jouer</router-link> |
      <router-link to="/a-propos">À propos</router-link>
    </nav>
    <router-view />
  </div>
</template>


<script>

</script>

<style>
body {
  margin: 0;
  padding: 0;
  min-height: 100vh; /* Prend toute la hauteur de l'écran */
  width: 100%;
  background-image: url("@/assets/Ecran_Fond.png"); /* Image de fond */
  background-size: cover; /* Couvre tout l'écran */
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed; /* Empêche le défilement */
}

</style>

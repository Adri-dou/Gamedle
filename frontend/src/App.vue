<template>
  <div>
    <nav>
      <router-link to="/">Accueil</router-link> 
      <router-link to="/jeu">Jouer</router-link> 
      <router-link to="/SignIn">Login</router-link>
      <router-link to="/SignUp">Register</router-link>
      <router-link to="/a-propos">À propos</router-link>
      <!-- Visible uniquement pour les admins -->
      <router-link v-if="isAdmin" to="/manage-game">Manage Game</router-link>
    </nav>

    <router-view />    
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';

const isAdmin = ref(false);

onMounted(() => {
  const role = localStorage.getItem('userRole');
  isAdmin.value = role === 'administrateur';
});
</script>


<style>
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  width: 100%;
  background-image: url("@/assets/Ecran_Fond.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


nav {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-color: #212121;
  margin-bottom: 20px;
  gap: 10px;
}

nav a {
  color: #ffffff;
  font-size: 18px;
  font-weight: bold;
  text-decoration: none;
  padding: 10px 20px;
  min-width: 160px;
  text-align: center;
  transition: background-color 0.3s ease, color 0.3s ease;
  border-radius: 6px;
}

nav a:hover {
  background-color: #8c8b8b;
  color: #ffa500;
}

nav a.logo {
  padding: 0;
}

#logout {
  background-color: #ffa500;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  font-size: 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

#logout:hover {
  background-color: #ff8c00;
}

#liButton button {
  background-color: #ffa500;
  color: #ffffff;
  font-size: 14px;
  padding: 10px 20px;
  width: 100%;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s ease;
}

#liButton button:hover {
  background-color: #ff8c00;
}

</style>

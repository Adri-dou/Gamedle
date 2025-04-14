<template>
  <div>
    <nav>
      <router-link to="/">Accueil</router-link> 
      <router-link to="/jeu">Jouer</router-link> 

      <!-- Cacher login/register si connecté -->
      <router-link v-if="!isLoggedIn" to="/SignIn">Login</router-link>
      <router-link v-if="!isLoggedIn" to="/SignUp">Register</router-link>

      <!-- Visible uniquement pour les admins -->
      <router-link v-if="isAdmin" to="/manage-user">Manage User</router-link>
      <router-link v-if="isAdmin" to="/manage-game">Manage Game</router-link>

      <router-link to="/a-propos">À propos</router-link>
      <router-link v-if="isLoggedIn" @click.prevent="logout" to="#">Se déconnecter</router-link>

    </nav>

    <router-view />    
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAdmin = ref(false);
const isLoggedIn = ref(false);

const updateUserState = () => {
  const role = localStorage.getItem('userRole');
  const username = localStorage.getItem('username');

  isAdmin.value = role === 'administrateur';
  isLoggedIn.value = !!username;
};

const logout = () => {
  localStorage.removeItem('userRole');
  localStorage.removeItem('username');
  isAdmin.value = false;
  isLoggedIn.value = false;
  router.push('/');
};

onMounted(updateUserState);

</script>


<style>
@import url('https://fonts.cdnfonts.com/css/adlam-display');

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

h1 {
  font-family: "ADLaM Display", sans-serif;
  font-size: 40px;
  color: black;
}

h2 {
  font-family: "ADLaM Display", sans-serif;
  font-size: 30px;
  color: black;
}

p {
  font-family: "ADLaM Display", sans-serif;
  font-size: 20px;
  color: black;
}

input {
  font-family: "ADLaM Display", sans-serif;
  font-size: 15px;
  border-radius: 20px;
  border: inset #b0efb1 3px;
}

button {
  font-family: "ADLaM Display", sans-serif;
  border-radius: 20px;
  background-color: rgb(192, 192, 192);
  border: inset 3px rgb(176, 239, 177);
}

a {
  font-family: "ADLaM Display", sans-serif;
  font-size: 15px;
  color: #1b00cb;
}

</style>

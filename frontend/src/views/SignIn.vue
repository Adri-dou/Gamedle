<template>
    <div class="login-container">
      <h2>Connexion</h2>
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Nom d'utilisateur" required />
        <input v-model="password" type="password" placeholder="Mot de passe" required />
        <button type="submit">Se connecter</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, getCurrentInstance } from 'vue';
  const username = ref('');
  const password = ref('');
  const message = ref('');
  const { proxy } = getCurrentInstance();
  const apiBase = proxy.$apiBase;
  
  const login = async () => {
    try {
      const res = await fetch(`${apiBase}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.value, user_password: password.value })
      });
  
      const data = await res.json();
      if (res.ok) {
        message.value = `Bienvenue ${data.username}`;
        // Exemple de login après succès
        localStorage.setItem("userRole", data.user_role); // 'user' ou 'administrateur'
        localStorage.setItem("username", data.username); // si besoin
        window.location.href = "/"; // Redirige vers la page d'accueil ou une autre page
      } else {
        message.value = data.error;
      }
    } catch (err) {
      message.value = 'Erreur lors de la connexion';
    }
  };
  </script>
  
<style scoped>

.register-container,
.login-container {
  max-width: 400px;
  margin: 60px auto;
  padding: 30px;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.register-container h2,
.login-container h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.register-container form,
.login-container form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input,
select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus,
select:focus {
  border-color: #007BFF;
}

button {
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #e74c3c;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #0056b3;
}

p {
  text-align: center;
  margin-top: 10px;
  color: #444;
}


</style>

<template>
    <div class="register-container">
      <h2>Ajouter un utilisateur</h2>
      <form @submit.prevent="registerUser">
        <input v-model="form.username" placeholder="Nom d'utilisateur" required />
        <input v-model="form.user_password" type="password" placeholder="Mot de passe" required />
  
        <select v-model="form.user_role">
          <option value="user">Utilisateur</option>
          <option value="administrateur">Administrateur</option>
        </select>
  
        <button type="submit">Ajouter</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, getCurrentInstance } from 'vue';
  const form = ref({
    username: '',
    user_password: '',
    user_role: 'user'
  });
  const message = ref('');
  const { proxy } = getCurrentInstance();
  const apiBase = proxy.$apiBase;
  
  const registerUser = async () => {
    try {
      const res = await fetch(`${apiBase}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      });
      const data = await res.json();
      message.value = data.message || data.error;
    } catch (err) {
      message.value = 'Erreur lors de l’inscription';
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
  background-color: #007BFF;
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
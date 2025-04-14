<template>
    <div class="manage-user">
      <h2>Gérer les utilisateurs</h2>
  
      <table>
        <thead>
          <tr>
            <th>Nom d'utilisateur</th>
            <th>Rôle</th>
            <th>Changer le rôle</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.username">
            <td>{{ user.username }}</td>
            <td>{{ user.user_role }}</td>
            <td>
              <select v-model="user.newRole">
                <option value="user">Utilisateur</option>
                <option value="administrateur">Administrateur</option>
              </select>
              <button @click="updateRole(user)">Modifier</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, getCurrentInstance } from 'vue';
  
  const users = ref([]);
  const message = ref('');
  const { proxy } = getCurrentInstance();
  const apiBase = proxy.$apiBase;
  
  const fetchUsers = async () => {
    const res = await fetch(`${apiBase}/users`);
    const data = await res.json();
    users.value = data.map(u => ({ ...u, newRole: u.user_role }));
  };
  
  const updateRole = async (user) => {
    try {
      const res = await fetch(`${apiBase}/users/update-role`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user.username, newRole: user.newRole })
      });
      const data = await res.json();
      message.value = data.message;
      fetchUsers(); // Refresh
    } catch (err) {
      message.value = 'Erreur lors de la mise à jour';
    }
  };
  
  onMounted(fetchUsers);
  </script>
  
  <style scoped>
  .manage-user {
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.9);
    max-width: 800px;
    margin: auto;
    border-radius: 10px;
    box-shadow: 0 0 10px #ccc;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  thead {
    background-color: #212121;
    color: white;
  }
  
  td, th {
    padding: 10px;
    text-align: center;
    border: 1px solid #ccc;
  }
  
  select {
    padding: 5px;
    margin-right: 10px;
  }
  
  button {
    background-color: #FFA500;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
  }
  button:hover {
    background-color: #FF8C00;
  }
  </style>
  
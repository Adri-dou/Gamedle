<template>
  <div class="chatbot-box">
    <div class="chatbot-header">🤖 Assistant</div>
    
    <div class="chatbot-messages" id="chat-box">

      <p
        v-for="(msg, index) in historyMessages"
        :key="index"
        :class="msg.type === 'user' ? 'user-message' : 'bot-message'"
      >
        {{ msg.message }}
      </p>
    </div>
    <div class="chatbot-input">
      <input
        v-model="userInput"
        placeholder="Posez votre question..."
        @keyup.enter="handleSend"
      />
      <button @click="handleSend">Envoyer</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: '',
      historyMessages: [],
      gameNames: [],
      intents: []
    };
  },
  mounted() {
    this.loadMessages();
    this.fetchGameNames();
    this.fetchRandomGame();
    this.fetchJSON("/intents.json");
    window.addEventListener("beforeunload", this.saveMessages);
  },
beforeUnmount() {
  this.saveMessages();
  window.removeEventListener("beforeunload", this.saveMessages);
},
  methods: {
      async fetchRandomGame() {
    try {
      const response = await fetch('http://localhost:8000/game-of-the-day');
      if (!response.ok) throw new Error('Erreur lors de la récupération du jeu du jour');
      
      const game = await response.json();

      console.log("🎯 Jeu du jour reçu depuis l'API :", game); // 👈 ICI

      // Si les catégories sont fournies en chaîne, les transformer en tableau
      if (game.Catégories) {
        game.Catégories = Array.isArray(game.Catégories)
          ? game.Catégories
          : game.Catégories.split(', ');
      } else {
        game.Catégories = []; // fallback si la propriété est absente
      }
      
    game.Nom_Jeu = game.name;
    game.Min_Joueurs = game.minPlayer;
    game.Max_Joueurs = game.maxPlayer;
    game.Annee_Publication = new Date(game.yearPublished).getFullYear();
    game.Classement = game.ranking;
    game.Editeur = game.publisher;


      this.targetGame = game;
    } catch (error) {
      console.error('Erreur dans fetchRandomGame:', error);
    }
  },//jeux du jour a recuperer dans le json
    fetchGameNames() {
      fetch("http://localhost:8000/games")
        .then((res) => res.json())
        .then((data) => {
          this.gameNames = data.map((game) => game.Nom_Jeu);
        })
        .catch(console.error);
    },
    async handleSend() {
      const userInput = this.userInput.trim();
      if (!userInput) return;

      this.showMessage(userInput, "user");

      const botResponse = await this.processMessage(userInput);
      if (botResponse.startsWith("__API_CALL__")) {
        const url = "http://localhost:8000" + botResponse.replace("__API_CALL__", "");
          if (botResponse === "__API_CALL__/game-of-the-day") {
            await this.fetchRandomGame();
            const game = this.targetGame;
            const formatted = `Jeu du jour : ${game.Nom_Jeu}`;
            this.showMessage(formatted, "bot");}
          else{
        try {
          const res = await fetch(url);
          const jeux = await res.json();
          const formatted = jeux.map(j => 
            `Le descritpion du jeu ${j.name} est (${j.description}) `
          ).join("\n");
          this.showMessage(formatted, "bot");
        } catch (e) {
          this.showMessage("Une erreur est survenue lors de la recherche du jeu.", "bot");
        }}
      } else {
        this.showMessage(botResponse, "bot");
      }

      this.userInput = "";
    },

    async processMessage(message) {
      const lowerMsg = message.toLowerCase();

      const fgame = this.gameNames.find(name =>
      lowerMsg.includes(name.toLowerCase())
    );
    if (fgame) {
      return `__API_CALL__/search-bot?name=${encodeURIComponent(fgame)}`;
    }

      // 1. Vérifier les intents
        for (const intent of this.intents) {
      for (const keyword of intent.patterns) {
        if (lowerMsg.includes(keyword.toLowerCase())) {
          const response =
            intent.responses[Math.floor(Math.random() * intent.responses.length)];
          return response;
        }
      }
    }

      // 2. Vérifier les noms de jeux
      const foundGame = this.gameNames.find(name =>
        lowerMsg.includes(name.toLowerCase())
      );
      if (foundGame) {
        return `__API_CALL__/search-bot?name=${encodeURIComponent(foundGame)}`;
      }

      // 3. Réponse par défaut
      return "Je suis désolé, je ne comprends pas votre question.";
    },

    showMessage(message, type) {
      this.historyMessages.push({ message, type });
      this.$nextTick(() => {
        const chatBox = this.$el.querySelector("#chat-box");
        chatBox.scrollTop = chatBox.scrollHeight;
      });
    },

    saveMessages() {
      sessionStorage.setItem(
        "chatHistory",
        JSON.stringify(this.historyMessages)
      );
    },

    loadMessages() {
      const chatHistory = JSON.parse(sessionStorage.getItem("chatHistory"));
      if (chatHistory) {
        this.historyMessages = chatHistory;
      }
    },

    fetchJSON(path) {
      fetch(path)
        .then((res) => res.json())
        .then((data) => {
          this.intents = data.intents;
        })
        .catch(console.error);
    },


  }
};
</script>

<style scoped>
.chatbot-box {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 300px;
  max-height: 400px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1000;
  font-family: 'Arial', sans-serif;
}

.chatbot-header {
  background: #4c4cff;
  color: white;
  padding: 10px 16px;
  font-weight: bold;
}

.chatbot-messages {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
  font-size: 14px;
  color: #333;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bot-message,
.user-message {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 16px;
  word-wrap: break-word;
  line-height: 1.4;
}

.bot-message {
  background-color: #f1f1f1;
  align-self: flex-start;
  color: #333;
}

.user-message {
  background-color: #4c4cff;
  color: white;
  align-self: flex-end;
}

.chatbot-input {
  border-top: 1px solid #ccc;
  display: flex;
  padding: 8px;
}

.chatbot-input input {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.chatbot-input button {
  margin-left: 8px;
  background: #4c4cff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: 0.2s;
}

.chatbot-input button:hover {
  background: #3737cc;
}
</style>
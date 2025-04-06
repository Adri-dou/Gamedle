<template>
  <div class="game-container">
    <div class="header">
      <img src="@/assets/Gamedle_Logo.png" alt="Gamedle" class="logo" />
      <p>Devinez le jeu de société du jour !</p>
      <div v-if="targetGame" class="target-info">
        Jeu aléatoire chargé : {{ targetGame.Nom_Jeu }} (debug)
      </div>
    </div>

    <div class="guess-input">
      <input
        v-model="currentGuess"
        type="text"
        placeholder="Entrez le nom d'un jeu..."
        @keyup.enter="submitGuess"
        :disabled="gameWon"
      />
      <button @click="submitGuess" :disabled="gameWon">Deviner</button>
    </div>

    <div class="attempts-list">
      <div v-for="(attempt, index) in attempts" :key="index" class="attempt">
        <div class="game-name">{{ attempt.Nom_Jeu }}</div>
        <div class="game-properties">
          <div v-for="(property, key) in comparableProperties" :key="key" class="property-cell">
            <div
              class="property-box"
              :class="getStatusClass(key, attempt[key], targetGame[key])"
            >
              <template v-if="property.type === 'numeric'">
                {{ attempt[key] }}
                <span v-if="showArrow(key)" class="arrow">
                  {{ getArrow(key, attempt[key], targetGame[key]) }}
                </span>
              </template>

              <template v-else-if="property.type === 'array'">
                <div v-for="item in attempt[key]" :key="item" class="array-item">
                  {{ item }}
                </div>
              </template>

              <template v-else>
                {{ attempt[key] }}
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="gameWon" class="win-message">
      Félicitations ! Vous avez trouvé le jeu en {{ attempts.length }} essais !
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentGuess: '',
      targetGame: null,
      attempts: [],
      gameWon: false,
      comparableProperties: {
        Catégories: { type: 'array', name: 'Catégories' },
        Min_Joueurs: { type: 'numeric', name: 'Joueurs min' },
        Max_Joueurs: { type: 'numeric', name: 'Joueurs max' },
        Annee_Publication: { type: 'numeric', name: 'Année' },
        Editeur: { type: 'text', name: 'Éditeur' },
        Classement: { type: 'numeric', name: 'Classement' },
      }
    }
  },
  async mounted() {
    await this.fetchRandomGame();
  },
  methods: {
    async fetchRandomGame() {
      // À remplacer par l'appel API plus tard
      const mockGame = {
        game_id: 3,
        Nom_Jeu: "Samurai",
        Catégories: ["Abstract Strategy", "Medieval"],
        Min_Joueurs: 2,
        Max_Joueurs: 4,
        Annee_Publication: 1998,
        Editeur: "Fantasy Flight Games",
        Classement: 231
      };
      this.targetGame = mockGame;
    },

    async submitGuess() {
      if (!this.currentGuess) return;

      // À remplacer par l'appel API aussi
      const mockResponse = {
        game_id: 1,
        Nom_Jeu: this.currentGuess,
        Catégories: ["Strategy", "Medieval"],
        Min_Joueurs: 2,
        Max_Joueurs: 5,
        Annee_Publication: 2005,
        Editeur: "Mock Publisher",
        Classement: 150
      };

      this.attempts.push({
        ...mockResponse,
        Catégories: mockResponse.Catégories.split(', ')
      });

      if (mockResponse.Nom_Jeu === this.targetGame.Nom_Jeu) {
        this.gameWon = true;
      }

      this.currentGuess = '';
    },

    getStatusClass(propertyKey, attemptValue, targetValue) {
      if (propertyKey === 'Catégories') {
        const commonCategories = attemptValue.filter(c => 
          this.targetGame.Catégories.includes(c)
        );
        if (commonCategories.length === 0) return 'incorrect';
        return commonCategories.length === this.targetGame.Catégories.length ? 'correct' : 'partial';
      }

      if (attemptValue === targetValue) return 'correct';
      return 'incorrect';
    },

    showArrow(key) {
      return ['Classement', 'Annee_Publication'].includes(key);
    },

    getArrow(key, attemptValue, targetValue) {
      if (attemptValue === targetValue) return '';
      return attemptValue > targetValue ? '↓' : '↑';
    }
  }
}
</script>

<style scoped>
.game-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.logo {
  width: 400px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.guess-input {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 8px;
}

.attempts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.game-properties {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.property-box {
  padding: 10px;
  border-radius: 5px;
  text-align: center;
  min-height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.correct { background-color: #6aaa64; color: white; }
.partial { background-color: #c9b458; color: white; }
.incorrect { background-color: #787c7e; color: white; }

.arrow {
  font-size: 1.2em;
  margin-left: 5px;
}

.win-message {
  margin-top: 20px;
  padding: 15px;
  background-color: #6aaa64;
  color: white;
  text-align: center;
  border-radius: 5px;
}
</style>
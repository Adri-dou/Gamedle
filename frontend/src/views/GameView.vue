<template>
  <div class="game-container">
    <div class="header">
      <img src="@/assets/Gamedle_Logo.png" alt="Gamedle" class="logo" />
      <div class="game-info-container">
        <h2>Devinez le jeu de société du jour !</h2>
        <div v-if="targetGame" class="target-info">
          Jeu aléatoire chargé : {{ targetGame.name }} (debug)
        </div>
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
        <!-- Ligne d'en-têtes -->
      <div class="header-row">
        <div v-for="(property, key) in comparableProperties" :key="key" class="header-cell">
          {{ property.name }}
        </div>
      </div>
      <div v-for="(attempt, index) in attempts" :key="index" class="attempt">
        <div class="game-name"><strong>{{ attempt.Nom_Jeu }}</strong></div>
        <div class="game-properties">
        <div v-for="(property, key) in comparableProperties" :key="key" class="property-cell">
            <div
              class="property-box"
              :class="getStatusClass(key, attempt[key], targetGame[key])">
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

    <div class="instructions">
  <h3>Comment interpréter les indices :</h3>
  <ul>
    <li><span class="box incorrect">⬛</span> → Cet attribut ne correspond pas du tout au jeu recherché.</li>
    <li><span class="box partial">🟨</span> → Cet attribut est partiellement correct (presque ou partiellement similaire).</li>
    <li><span class="box correct">🟩</span> → Cet attribut correspond exactement au jeu recherché.</li>
    <li><span class="arrow">↑</span> → La valeur proposée est plus petite que celle du jeu recherché.</li>
    <li><span class="arrow">↓</span> → La valeur proposée est plus grande que celle du jeu recherché.</li>
  </ul>
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
  },

  async submitGuess() {
  if (!this.currentGuess) return;

  try {
    const response = await fetch(`http://localhost:8000/search?name=${encodeURIComponent(this.currentGuess)}`);
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Erreur API:", errorData.error);
      return;
    }

    const results = await response.json();
    
    if (results.length === 0) {
      console.warn('Aucun jeu trouvé pour:', this.currentGuess);
      return;
    }

    let game = results[0];

    game.Catégories = game.Catégories
      ? Array.isArray(game.Catégories)
        ? game.Catégories
        : game.Catégories.split(', ')
      : [];

    this.attempts.push(game);

    if (game.Nom_Jeu === this.targetGame.Nom_Jeu) {
      this.gameWon = true;
    }

    this.currentGuess = '';
  } catch (error) {
    console.error('Erreur dans submitGuess:', error);
  }
},

getStatusClass(propertyKey, attemptValue, targetValue) {
  if (propertyKey === 'Catégories') {
    const attemptCategories = Array.isArray(attemptValue)
      ? attemptValue.map(c => c.trim().toLowerCase())
      : String(attemptValue).split(',').map(c => c.trim().toLowerCase());

    const targetCategories = Array.isArray(targetValue)
      ? targetValue.map(c => c.trim().toLowerCase())
      : String(targetValue).split(',').map(c => c.trim().toLowerCase());

    const common = attemptCategories.filter(cat =>
      targetCategories.includes(cat)
    );

    const result =
      common.length === 0
        ? 'incorrect'
        : common.length === targetCategories.length &&
          attemptCategories.length === targetCategories.length
        ? 'correct'
        : 'partial';

    console.log(`🧩 [Catégories]`, { attemptCategories, targetCategories, common, result });

    return result;
  }

  if (['Classement', 'Annee_Publication'].includes(propertyKey)) {
    const a = parseInt(attemptValue);
    const b = parseInt(targetValue);
    const result = isNaN(a) || isNaN(b) ? 'incorrect' : a === b ? 'correct' : 'incorrect';

    console.log(`📅 [${propertyKey}]`, { attempt: a, target: b, result });

    return result;
  }

  if (['Min_Joueurs', 'Max_Joueurs'].includes(propertyKey)) {
    const a = parseInt(attemptValue);
    const b = parseInt(targetValue);

    let result = 'incorrect';
    if (!isNaN(a) && !isNaN(b)) {
      result = a === b ? 'correct' : Math.abs(a - b) <= 1 ? 'partial' : 'incorrect';
    }

    console.log(`👥 [${propertyKey}]`, { attempt: a, target: b, result });

    return result;
  }

  const a = String(attemptValue).trim().toLowerCase();
  const b = String(targetValue).trim().toLowerCase();
  const result = a === b ? 'correct' : 'incorrect';

  console.log(`🏷️ [${propertyKey}]`, { attempt: a, target: b, result });

  return result;
}
,


    showArrow(key) {
      return ['Classement', 'Annee_Publication'].includes(key);
    },

    getArrow(key, attemptValue, targetValue) {
  const a = parseFloat(attemptValue);
  const b = parseFloat(targetValue);
  if (isNaN(a) || isNaN(b) || a === b) return '';
  return a > b ? '↓' : '↑';
}

  }
}
</script>

<style scoped>

.instructions {
  margin-top: 30px;
  background-color: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  border-radius: 12px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.instructions h3 {
  margin-bottom: 15px;
  text-align: center;
  color: #333;
}

.instructions ul {
  list-style: none;
  padding: 0;
}

.instructions li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 1em;
  color: #444;
}

.instructions .box {
  width: 25px;
  height: 25px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  font-size: 1.5em;
}

.instructions .arrow {
  font-size: 1.5em;
  margin-right: 10px;
}

.game-name{
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 10px;
  text-align: center;
  background-color: rgba(0,0,0,0.51);
  border-radius: 20px;
  color: white;
  padding: 10px;
  margin: 10px;
}

.header-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  margin-bottom: 10px;
}

.header-cell {
  text-align: center;
  font-weight: bold;
  font-size: 0.9em;
  background-color: #e0e0e0;
  padding: 10px;
  border-radius: 5px;
  
}

.property-title {
  font-weight: bold;
  font-size: 0.8em;
  margin-bottom: 5px;
  text-align: center;
  color: rgb(0, 0, 0);
}


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
.incorrect { background-color: #766d6d; color: white; }

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

.target-info {
  font-family: "ADLaM Display", sans-serif;
  color: white;
  margin: 10px;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.game-info-container {
  display: flex;
  flex-direction: column;
  background-color: rgba(0,0,0,0.51);
  border-radius: 20px;
}

.game-info-container h2{
  color: white;
  margin: 10px;
}

</style>
// src/components/GameGuess.vue
<template>
  <div class="grid grid-cols-7 gap-2 mb-2">
    <div v-for="(value, key) in displayedFields" :key="key" :class="getColorClass(key)">
      <span class="block text-sm text-center p-2">{{ guess[key] }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed, toRefs } from 'vue';

const props = defineProps({
  guess: Object,
  target: Object
});
const { guess, target } = toRefs(props);

const displayedFields = computed(() => ({
  Nom_Jeu: 'Nom_Jeu',
  Catégories: 'Catégories',
  Min_Joueurs: 'Min_Joueurs',
  Max_Joueurs: 'Max_Joueurs',
  Annee_Publication: 'Annee_Publication',
  Editeur: 'Editeur',
  Classement: 'Classement'
}));

const getColorClass = (key) => {
  const guessVal = guess.value[key];
  const targetVal = target.value[key];

  if (!targetVal || !guessVal) return 'bg-gray-200';

  // Comparaisons personnalisées
  if (key === 'Classement' || key.includes('Joueurs') || key.includes('Annee')) {
    const diff = guessVal - targetVal;
    if (diff === 0) return 'bg-green-400';
    return diff > 0 ? 'bg-red-400' : 'bg-orange-400';
  }

  // Catégories peut contenir plusieurs valeurs
  if (key === 'Catégories') {
    const guessedCats = guessVal.split(',').map(c => c.trim());
    const targetCats = targetVal.split(',').map(c => c.trim());
    const match = guessedCats.some(cat => targetCats.includes(cat));
    return match ? 'bg-orange-300' : 'bg-red-400';
  }

  return guessVal === targetVal ? 'bg-green-400' : 'bg-red-400';
};
</script>

<style scoped>
.bg-green-400 {
  background-color: #4ade80;
  color: black;
}
.bg-orange-400 {
  background-color: #fb923c;
  color: black;
}
.bg-orange-300 {
  background-color: #fdba74;
  color: black;
}
.bg-red-400 {
  background-color: #f87171;
  color: white;
}
.bg-gray-200 {
  background-color: #e5e7eb;
  color: black;
}
</style>

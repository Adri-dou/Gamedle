// src/components/GameIndicators.vue
<template>
  <div class="mt-6 border rounded p-4 w-full bg-white">
    <h2 class="text-lg font-semibold mb-2">Indicateurs de couleur</h2>
    <div class="grid grid-cols-4 gap-4">
      <div class="flex items-center">
        <div class="w-6 h-6 rounded bg-green-400 mr-2"></div>
        <span>Correct</span>
      </div>
      <div class="flex items-center">
        <div class="w-6 h-6 rounded bg-orange-400 mr-2"></div>
        <span>Proche / Partiel</span>
      </div>
      <div class="flex items-center">
        <div class="w-6 h-6 rounded bg-red-400 mr-2"></div>
        <span>Incorrect</span>
      </div>
      <div class="flex items-center">
        <div class="w-6 h-6 rounded bg-gray-200 mr-2"></div>
        <span>Manquant</span>
      </div>
    </div>
  </div>
</template>

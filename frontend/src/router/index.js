import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import GameView from '../views/GameView.vue';
import AboutView from '../views/AboutView.vue';

const routes = [
    { path: '/', component: HomeView },
    { path: '/jeu', component: GameView },
    { path: '/a-propos', component: AboutView }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

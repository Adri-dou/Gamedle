import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import GameView from '../views/GameView.vue';
import AboutView from '../views/AboutView.vue';
import SignIn from '../views/SignIn.vue';
import SignUp from '../views/SignUp.vue';
import ManageGame from '@/views/ManageGame.vue';
import ManageUser from '@/views/ManageUser.vue';

const routes = [
    { path: '/', component: HomeView },
    { path: '/jeu', component: GameView },
    { path: '/a-propos', component: AboutView },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
    { path: '/manage-game', component: ManageGame },
    { path: '/manage-user', component: ManageUser },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

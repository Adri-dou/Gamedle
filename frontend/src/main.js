
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

const app = createApp(App);

//const PORT = process.env.PORT;

app.config.globalProperties.$apiBase = `http://localhost:3000`;

app.use(router);
app.mount('#app');

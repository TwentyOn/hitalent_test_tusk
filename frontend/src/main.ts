/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Composables
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import { useAuthStore } from './auth';

// Plugins
import { registerPlugins } from '@/plugins';

// Components
import App from './App.vue';

// Styles
import 'unfonts.css';

const pinia = createPinia();
const app = createApp(App);

app.use(pinia);
app.use(router);

registerPlugins(app);

await useAuthStore().checkAuth()

app.mount('#app');

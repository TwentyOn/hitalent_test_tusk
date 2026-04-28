/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Composables
import { createApp } from 'vue'
import router from './router'

import { authStore } from './auth';

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Styles
import 'unfonts.css'

const app = createApp(App)

// проверка авторизации
await authStore.checkAuth();

app.use(router)

registerPlugins(app)

app.mount('#app')

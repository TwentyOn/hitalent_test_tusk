import { createMemoryHistory, createRouter } from 'vue-router';
import { useAuthStore } from './auth'

import ProfileView from './views/ProfileView.vue';
import RegisterView from './views/RegisterView.vue';
import LoginView from './views/LoginView.vue';

const routes = [
    { path: '/', redirect: 'profile', title: 'хуета' },
    { path: '/:userId', name: 'profile', component: ProfileView, meta: { requiresAuth: true, title: 'Личный кабинет' } },
    { path: '/register', component: RegisterView, meta: { requiresAuth: false, title: 'Регистрация' } },
    { path: '/login', name: 'login', component: LoginView, meta: { requiresAuth: false, title: 'Вход' } }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes
})

router.beforeEach(async (to, from) => {
    const authStore = useAuthStore()

    if (
        to.meta.requiresAuth &&
        !authStore.isAuthenticated &&
        to.path !== '/login') {
        return { 'path': '/login' }
    } else if (!to.meta.requiresAuth && authStore.isAuthenticated && ['/login', '/register'].includes(to.path)) {
        return false
    }
});

export default router;

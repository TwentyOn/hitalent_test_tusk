import router from './router.ts';
import { jwtDecode } from 'jwt-decode';
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: localStorage.getItem('token') || '',
        refreshToken: localStorage.getItem('refresh') || '',
    }),

    getters: {
        isAuthenticated: (state) => {
            return !!(state.accessToken && state.refreshToken)
        },
        decodeAccess: (state) => {
            if (state.accessToken) {
                return jwtDecode(state.accessToken)
            }
        },
        decodeRefresh: (state) => {
            if (state.refreshToken) {
                return jwtDecode(state.refreshToken)
            }
        },
        needRefresh(): boolean {
            const currentTime = Math.floor(Date.now() / 1000);

            if (this.decodeAccess['exp'] < currentTime) {
                if (this.decodeRefresh['exp'] > currentTime) {
                    return true;
                }
            }
            return false
        },
    },

    actions: {
        async login(credentials: object) {
            const response = await fetch(import.meta.env.VITE_API_URL + 'token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(credentials)
            });

            if (!response.ok) {
                if (response.status === 401) {
                    const errors = await response.json()
                    return { success: false, errors: errors }
                }
                throw new Error(`${response.status}: ${response.statusText}`)
            }

            const content = await response.json();
            this.accessToken = content['access'];
            this.refreshToken = content['refresh'];
            localStorage.setItem('token', this.accessToken);
            localStorage.setItem('refresh', this.refreshToken);

            return { success: true }
        },

        async register(userData: object) {
            try {
                const response = await fetch(import.meta.env.VITE_API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(userData)
                });

                if (!response.ok) {
                    if (response.status === 400) {
                        const errors = await response.json()
                        return { success: false, errors: errors }
                    }
                    throw Error(`${response.status}: ${response.statusText}`)
                }

                return { success: true }

            } catch (error) {
                console.error(`Ошибка регистрации ${error}`);
                throw error;
            }
        },

        async logout() {
            this.accessToken = '';
            this.refreshToken = '';

            localStorage.removeItem('token');
            localStorage.removeItem('refresh');
            router.push({ name: 'login' })
        },

        async fetchUser() {
            const userId = this.decodeAccess['user_id']
            const response = await fetch(import.meta.env.VITE_API_URL + userId, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + this.accessToken
                },
            })

            if (response.ok) {
                const user = await response.json()
                return user
            }

        },

        async checkAuth() {
            const currentTime = Math.floor((Date.now() / 1000) + 1);
            if (this.accessToken && this.refreshToken) {
                if (this.decodeAccess['exp'] < currentTime) {
                    if (this.decodeRefresh['exp'] < currentTime) {
                        localStorage.removeItem('token')
                        localStorage.removeItem('refresh')
                    } else {
                        await this.updateTokens()
                    }
                }
            }
        },

        async updateTokens() {
            const response = await fetch(import.meta.env.VITE_API_URL + 'refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'refresh': this.refreshToken
                }),
            })

            if (response.ok) {
                const content = await response.json();

                this.accessToken = content['access'];
                this.refreshToken = content['refresh'];

                localStorage.setItem('token', this.accessToken)
                localStorage.setItem('refresh', this.refreshToken)

                return true;
            } else {
                console.log('не удалось обновить токен: ', response.status, response.statusText)
                return false
            }
        }
    }
})
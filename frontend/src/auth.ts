import router from './router.ts';
import { inject, reactive, computed, watch } from 'vue';
import { jwtDecode } from 'jwt-decode';
import { th, tr } from 'vuetify/locale';

export const authStore = reactive({
    accessToken: '',
    refreshToken: '',
    user: null,
    isAuthenticated() {
        return !!(this.accessToken && this.refreshToken)
    },
    user_id() {
        return jwtDecode(this.accessToken)['user_id']
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

    async login(credentials: object) {
        try {
            const response = await fetch(import.meta.env.VITE_API_URL + 'token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(credentials)
            });

            if (!response.ok) {
                throw Error(`${response.status}: ${response.statusText}`)
            }

            const content = await response.json();
            this.accessToken = content['access'];
            this.refreshToken = content['refresh'];
            localStorage.setItem('token', this.accessToken);
            localStorage.setItem('refresh', this.refreshToken);

            return { success: true }

        } catch (error) {
            console.error(`Ошибка входа ${error}`)
            throw error
        }
    },

    async logout() {
        this.accessToken = '';
        this.refreshToken = '';

        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        router.push({ name: 'login' })
    },

    async fetchUser(userId: string) {
        try {
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
        } catch (error) {
            console.log(`ошибка загрузки пользователя: ${error}`)
        }

    },

    async checkAuth(): Promise<Boolean> {
        this.accessToken = localStorage.getItem('token') || ''
        this.refreshToken = localStorage.getItem('refresh') || ''


        if (!(this.accessToken && this.refreshToken)) {
            return false;
        }

        const jwtConent = jwtDecode(this.accessToken);
        const cur_time = Math.floor(Date.now() / 1000)
        const tokenExp: number = jwtConent['exp'] || 0

        if (cur_time > tokenExp) {
            const result = await this.refreshAccessToken();
            if (!result) {
                localStorage.removeItem('token');
                localStorage.removeItem('refresh');
                return false;
            } else {
                console.log('получен новый токен')
                this.accessToken = result['access'];
                this.refreshToken = result['refresh'];
                localStorage.setItem('token', this.accessToken);
                localStorage.setItem('refresh', this.refreshToken);

                return true;
            }
        } return true
    },

    async refreshAccessToken(): Promise<boolean> {
        const refresh = localStorage.getItem('refresh');
        try {
            const response = await fetch(import.meta.env.VITE_API_URL + 'refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'refresh': refresh
                }),
            })

            if (response.ok) {
                const content = await response.json();
                return content;

            } else {
                return false
            }
        } catch (error) {
            console.log(`ошибка обновления токена: ${error}`)
            return false
        }
    }

});
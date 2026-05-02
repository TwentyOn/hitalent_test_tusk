<template>
    <v-container class="profile-container">
        <v-row justify="center">
            <v-col cols="12" md="8" lg="6">
                <v-card>
                    <v-card-title>Личный кабинет</v-card-title>
                    <v-card-item>
                        <v-card-text class="mb-7"><v-icon icon="mdi-email" /> E-mail: {{ user.email }}</v-card-text>
                        <v-btn color="info" v-on:click="getNewActivationKey">Обновить ключ активации</v-btn>
                    </v-card-item>
                    <v-card-item>
                        <v-card class="border" flat>
                            <v-card-title class="text-h5 text-center mb-4">
                                Смена пароля
                            </v-card-title>
                            <v-card-text>
                                <v-form >
                                    <v-text-field label="Текущий пароль"></v-text-field>
                                    <v-text-field label="Новый пароль"></v-text-field>
                                    <v-text-field label="Подтвердите новый пароль"></v-text-field>
                                    <send-button btn-text="Изменить пароль" :loading="pass"></send-button>
                                </v-form>
                            </v-card-text>
                        </v-card>
                    </v-card-item>
                    <send-mail-snackbar v-model="snackbar"/>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
    import { watch, ref } from 'vue';
    import { useAuthStore } from '@/auth';
    import SendButton from '@/components/SendButton.vue';
    import sendMailSnackbar from '@/components/sendMailSnackbar.vue';

    const authStore = useAuthStore();
    const loading = ref(true);
    const pass = ref(false)
    const user = ref({});
    const snackbar = ref(false)

        async function getNewActivationKey() {
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + `${authStore.decodeAccess['user_id']}/update-key/`, {
                    'method': 'POST',
                    headers: {
                        'Authorization': `Bearer ${authStore.accessToken}`,
                        'Content-Type': 'application/json'
                    },
                })
                
                if (!response.ok) {
                    throw new Error(`${response.status}: {response.statusText}`)
                }
                snackbar.value = true;

            } catch (error) {
                alert(`Ошибка при изменении ключа: ${error}`)
            }
    }

    // todo: возможно надо убрать
    watch(() => authStore.isAuthenticated, async (newStatus) => {
        try {
            if (newStatus) {
                user.value = await authStore.fetchUser()
                loading.value = false;
            } else {
                user.value = {}
                loading.value = true;
            }
        } catch (error) {
            alert(`Не удалось загрузить профиль: ${error}`)
            throw error
        }
        
        
        
    },{immediate: true})
</script>
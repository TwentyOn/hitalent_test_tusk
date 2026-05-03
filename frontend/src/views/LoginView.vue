<template>
    <form-container>
        <v-card flat>
                <v-card-title class="text-h5 text-center mb-4">
                    Вход
                </v-card-title>
                <v-divider class="my-3" />
                <v-card-text>
                    <v-form v-model="formValid" v-on:submit.prevent="handleSubmit">
                        <v-text-field 
                        label="E-mail" 
                        v-model="credentials.email"
                        v-bind:rules="emailRules"></v-text-field>
                        <v-text-field
                        label="Пароль"
                        v-model="credentials.password"
                        v-bind:rules="passwordRules"
                        type="password"></v-text-field>
                        <send-button v-bind:loading="loading" btnText="Войти" />
                        <v-divider class="my-7">или</v-divider>
                        <v-btn to="register" class="mt-2" block border>Создать аккаунт</v-btn>
                        <v-snackbar color="error" v-model="snackbar" timeout="3000">{{ error }}</v-snackbar>
                    </v-form>
                </v-card-text>
            </v-card>
    </form-container>
</template>

<script setup>
    import { ref } from 'vue';
    import { useAuthStore } from '@/auth.ts';
    import { useRouter } from 'vue-router';
    import SendButton from '@/components/SendButton.vue';
    import FormContainer from '@/components/FormContainer.vue';

    const router = useRouter()
    const authStore = useAuthStore();

    const formValid = ref(false);
    const loading = ref(false);
    const snackbar = ref(false);
    const error = ref('');
    const credentials = ref({
        'email': '',
        'password': ''
    })

    async function handleSubmit() {
        try {
            if (formValid.value) {
            loading.value = true
            const result = await authStore.login(credentials.value);
            if (result['success']) {
                router.push({name: 'profile', params: {userId: authStore.decodeAccess.user_id}})
                } else {
                error.value = result.error.detail
                snackbar.value = true
            }
            }
        } catch (error) {
            alert(`Ошибка входа: ${error}`)
        } finally {
            loading.value = false
        }
    }

    const emailRules = [
        value => {
            if (value) return true
            return "Введите e-mail"
        },
    ]

    const passwordRules = [
        value => {
            if (value) return true
            return "Введите пароль"
        },

    ]
</script>
<template>
    <v-container class="fill-height d-flex flex-column justify-center" fluid>
        <v-sheet width="300" class="mx-auto">
            <v-card class="border" flat>
                <v-card-title class="text-h5 text-center mb-4">
                    Вход
                </v-card-title>
                <v-card-text>
                    <v-form v-model="isValidForm" v-on:submit.prevent="handle">
                        <v-text-field 
                        label="E-mail" 
                        v-model="credentials.email"
                        v-bind:rules="emailRules"></v-text-field>
                        <v-text-field
                        label="Пароль"
                        v-model="credentials.password"
                        v-bind:rules="passwordRules"
                        type="password"></v-text-field>
                        <v-btn color="success" v-bind:loading="loading" class="mt-2" type="submit" block>
                            Войти

                            <v-icon icon="mdi-chevron-right" end></v-icon>
                        </v-btn>
                        <v-divider class="my-7">или</v-divider>
                        <v-btn to="register" class="mt-2" block>Создать аккаунт</v-btn>
                        <v-snackbar color="error" v-model="snackbar" timeout="5000">{{ error }}</v-snackbar>
                    </v-form>
                </v-card-text>
            </v-card>
        </v-sheet>
    </v-container>
</template>

<script setup>
    import { ref, inject } from 'vue';
    import { authStore } from '@/auth.ts';
    import router from '@/router';


    const isValidForm = ref(false);
    const loading = ref(false);

    const snackbar = ref(false);
    const error = ref('');

    const credentials = ref({
        'email': '',
        'password': ''
    })


    async function handle() {
        if (isValidForm.value) {
            loading.value = true
            const result = await authStore.login(credentials.value);
            if (result['success']) {
                router.push({name: 'profile', params: {userId: 25}})
        }
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
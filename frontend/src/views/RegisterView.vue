<template>
    <form-container>
        <v-card flat>
                <v-card-title class="text-h5 text-center mb-4">
                    Регистрация
                </v-card-title>
                <v-divider class="my-3" />
                <v-card-text>
                    <v-form v-model="formValid" v-on:submit.prevent="handleSubmit">
                        <v-text-field 
                        label="E-mail" 
                        v-on:update:model-value="clear_errors"
                        v-bind:error-messages="errors.email" 
                        v-bind:rules="emailRules" 
                        v-model="formData.email"></v-text-field>
                        <v-text-field
                        label="Пароль"
                        v-on:update:model-value="clear_errors"
                        v-bind:rules="passwordRules"
                        v-bind:error-messages="errors.password"
                        v-model="formData.password"
                        type="password"></v-text-field>
                        <v-text-field v-bind:rules="confPasswordRules" label="Подтвердите пароль" type="password"></v-text-field>
                        <send-button v-bind:disabled="!formValid" v-bind:loading="loading" btnText="Зарегистрироваться" />
                        <v-divider class="my-7">или</v-divider>
                        <v-btn to="login" class="mt-2" block border>Войти</v-btn>
                        <send-mail-snackbar v-model="snackbar"/>
                    </v-form>
                </v-card-text>
            </v-card>
    </form-container>
</template>

<script setup>
    import { ref, watch } from 'vue';
    import { useRouter } from 'vue-router';
    import { useAuthStore } from '../auth.ts';
    import SendButton from '@/components/SendButton.vue';
    import sendMailSnackbar from '@/components/SendMailSnackbar.vue';
    import FormContainer from '@/components/FormContainer.vue';

    const router = useRouter();
    const authStore = useAuthStore();

    const formValid = ref(false);
    const loading = ref(false);
    const formData = ref({});
    const errors = ref({})

    const snackbar = ref(false);

    function clear_errors() {
        errors.value = {}
    }

    async function handleSubmit() {
        try {
            loading.value = true
            const result = await authStore.register(formData.value)

            if (result['success']) {
                snackbar.value = true;
            } else {
                errors.value = result['errors']
            }
        } catch (error) {
            alert(`Ошибка регистрации: ${error}`)
            throw error
        } finally {
            loading.value = false
        }
    }

    watch (snackbar, (newVal, oldVal) => {
        if (oldVal === true && newVal === false) {
            router.push({'name': 'login'})
        }
    })

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
    const confPasswordRules = [
        value => {
            if (value) return true
            return "Подтвердите пароль"
        },
        value => {
            if (value == formData.value.password) return true
            return "Пароли не совпадают"
        }
    ]

</script>
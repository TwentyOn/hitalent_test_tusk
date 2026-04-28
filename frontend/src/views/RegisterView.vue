<template>
    <v-container class="fill-height d-flex flex-column justify-center" fluid>
        <v-sheet width="300" class="mx-auto">
            <v-card flat>
                <v-card-title class="text-h5 text-center mb-4">
                    Регистрация
                </v-card-title>
                <v-card-text>
                    <v-form v-model="isValidForm" v-on:submit.prevent="handle">
                        <v-text-field 
                        label="E-mail" 
                        v-on:update:model-value="clear_errors"
                        v-bind:error-messages="email_error" 
                        v-bind:rules="emailRules" 
                        v-model="userData.email"></v-text-field>
                        <v-text-field
                        label="Пароль"
                        v-on:update:model-value="clear_errors"
                        v-bind:rules="passwordRules"
                        v-bind:error-messages="password_error"
                        v-model="userData.password"
                        type="password"></v-text-field>
                        <v-text-field v-bind:rules="confPasswordRules" label="Подтвердите пароль" type="password"></v-text-field>
                        <v-btn color="success" v-bind:loading="loading" class="mt-2" type="submit" block>
                            Зарегистрироваться

                            <v-icon icon="mdi-chevron-right" end></v-icon>
                        </v-btn>
                        <v-divider class="my-7">или</v-divider>
                        <v-btn to="login" class="mt-2" block>Войти</v-btn>
                        <v-snackbar v-bind:color="snackColor" v-model="snackbar" timeout="5000">Письмо с ключом отправлено на почту</v-snackbar>
                    </v-form>
                </v-card-text>
            </v-card>
        </v-sheet>
    </v-container>
</template>

<script setup>
    import { ref } from 'vue';
    import { authStore } from '../auth.ts';

    const email_error = ref('');
    const password_error = ref('');

    const snackbar = ref(false);
    const snackColor = ref('success');

    const isValidForm = ref(false);
    const loading = ref(false);
    const userData = ref({
        email: "",
        password: "",
    });

    function clear_errors() {
        email_error.value = ''
        password_error.value = ''
    }

    async function handle() {
        if (isValidForm.value) {
            try {
                loading.value = true;
                const result = await authStore.register(userData.value);
                if (result['success']) {
                    snackbar.value = true;
                } else {
                    const errors = result['errors'];
                    email_error.value = errors.email;
                    password_error.value = errors.password;
                }
            } catch (error) {
                console.log(error)
                snackColor.value = 'error';
                snackbar.value = true;
                snackColor.value = 'success'
            } finally {
                loading.value = false;
            }
            
        }
    }

    // async function clear_errors() {
    //     email_error.value = '';
    //     password_error.value = '';
    // }

    // async function handle() {
    //     await clear_errors();

    //     if (isValidForm.value) {
    //         loading.value = true
    //         try {
    //             const result = await register(userData.value)
    //             if (result.status === 200) {
                    
    //                 snackbar.value = true;

    //             } else if (result.status === 400) {
    //                 const errors = await result.json()
    //                 email_error.value = errors['email']
    //                 password_error.value = errors['password']
    //             } else {
    //                 throw new Error(`${result.status} ${result.statusText}`)
    //             }
    //         } catch (error) {
    //             alert('Ошибка запроса: ' + error.message)
                
    //         } finally {
    //             loading.value = false
    //         }
    //     }
        
    // }

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
            if (value == userData.value.password) return true
            return "Пароли не совпадают"
        }
    ]

</script>
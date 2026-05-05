<template>
    <v-container class="mx-auto fill-height">
        <v-row justify="center">
            <v-col cols="12" md="8" lg="6">
                <v-card class="profile-card" :loading="loading">
                    <v-card-title>Персональные данные</v-card-title>
                    <v-card-item>
                        <div class="d-flex align-center justify-space-between mb-4">
                            <div class="d-flex align-center ga-3">
                                <v-avatar color="primary" size="32">
                                    <v-icon icon="mdi-email" color="white" size="20" />
                                </v-avatar>
                                <div>
                                    <div class="text-caption text-grey">Email</div>
                                    <div class="email-value">
                                        <span v-if="loading">Загрузка...</span>
                                        <span v-else>{{ user.email }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <v-divider class="my-3" />

                        <div class="d-flex align-center justify-space-between mb-4">
                            <div class="d-flex align-center ga-3">
                                <v-avatar color="warning" size="32">
                                <v-icon icon="mdi-key" color="white" size="20" />
                                    </v-avatar>
                                <div>
                                    <div class="text-caption text-grey">Ключ активации</div>
                                    <div class="activation-value">
                                        <span v-if="loading">Загрузка...</span>
                                        <span v-else-if="user.activation_key">{{ user.activation_key }}</span>
                                        <span v-else class="text-error">Нет ключа активации</span>
                                    </div>
                                </div>
                            </div>
                            <v-btn
                                v-if="!loading"
                                color="warning"
                                variant="text"
                                size="small"
                                prepend-icon="mdi-sync"
                                @click="getNewActivationKey">Обновить</v-btn>
                        </div>
                    </v-card-item>
                    <v-card-item>
                            <v-card-title class="text-h5 mb-4">
                                Смена пароля
                            </v-card-title>
                            <v-card-text>
                                <v-sheet class="mx-auto border pa-12" rounded="xl">
                                    <v-form v-model="formData.formValid" validate-on="input" v-on:submit.prevent="changePassword">
                                        <v-text-field
                                        label="Текущий пароль"
                                        type="password"
                                        :rules="passwordRules"
                                        :error-messages="formData.errors.old_password"
                                        v-model="formData.oldPassword"></v-text-field>
                                        <v-text-field
                                        label="Новый пароль"
                                        type="password"
                                        :rules="passwordRules"
                                        :error-messages="formData.errors.new_password"
                                        v-model="formData.newPassword"></v-text-field>
                                        <v-text-field
                                        label="Подтвердите новый пароль"
                                        type="password"
                                        :rules="confPasswordRules"></v-text-field>
                                        <send-button btn-text="Изменить пароль" :disabled="!formData.formValid" v-bind:loading="formData.loading"></send-button>
                                    </v-form>
                                </v-sheet>
                            </v-card-text>
                    </v-card-item>
                    <send-mail-snackbar v-model="keySnackbar"/>
                    <v-snackbar v-model="changePassSnackbar" color="success" timeout="4000">Пароль успешно изменен</v-snackbar>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
    import { watch, ref, reactive } from 'vue';
    import { useAuthStore } from '@/auth';
    import SendButton from '@/components/SendButton.vue';
    import sendMailSnackbar from '@/components/sendMailSnackbar.vue';

    const authStore = useAuthStore();
    const loading = ref(true);
    const user = ref({});

    const keySnackbar = ref(false)
    const changePassSnackbar = ref(false)

    const formData = reactive({
        oldPassword: '',
        newPassword: '',
        loading: false,
        formValid: false,
        errors: {}
    })

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
            if (value == formData.newPassword) return true
            return "Пароли не совпадают"
        }
    ]

    watch(() => formData.newPassword, () => delete formData.errors.new_password)
    watch(() => formData.oldPassword, () => delete formData.errors.old_password)



    async function getNewActivationKey() {
        try {
            await authStore.checkAuth()
            const response = await fetch(import.meta.env.VITE_API_URL + `${authStore.decodeAccess['user_id']}/update-key/`, {
                'method': 'POST',
                headers: {
                    'Authorization': `Bearer ${authStore.accessToken}`,
                    'Content-Type': 'application/json'
                },
            })
                
            if (!response.ok) {
                throw new Error(`${response.status}: ${response.statusText}`)
            }
            keySnackbar.value = true;
            const content = await response.json()
            user.value.activation_key = content.activation_key

        } catch (error) {
            alert(`Ошибка при изменении ключа: ${error}`)
        }
    }

    async function changePassword() {
        try {
            formData.loading = true
            const result = await authStore.changePassword(formData.oldPassword, formData.newPassword)
            if (result.success) {
                localStorage.removeItem('token')
                localStorage.removeItem('refresh')

                changePassSnackbar.value = true
            } else {
                formData.errors = result.errors
            }
        } catch (error) {
            alert(`Ошибка изменения пароля: ${error}`)
        } finally {
            formData.loading = false
        }
    }

    watch (changePassSnackbar, async (newVal, oldVal) => {
            if (newVal === false && oldVal === true) {
                authStore.logout()
        }
    })

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
        },
    {immediate: true}
    )

</script>
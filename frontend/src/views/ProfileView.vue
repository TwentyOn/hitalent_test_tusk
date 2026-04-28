<template>
    <v-container class="profile-container">
        <v-row justify="center">
            <v-col cols="12" md="8" lg="6">
                <v-card>
                    <v-card-title>Личный кабинет</v-card-title>
                    <v-list-item v-if="loading" title="загрузка...">
                        <template #prepend>
                            <v-icon icon="mdi-loading" />
                        </template>
                    </v-list-item>
                    <v-list-item v-else v-bind:title="user['email']">
                        <template #prepend>
                            <v-icon icon="mdi-email" />
                            <p>E-mail:</p>
                        </template>
                    </v-list-item>
                        <v-list-item v-if="loading" title="загрузка...">
                        <template #prepend>
                            <v-icon icon="mdi-loading" />
                        </template>
                    </v-list-item>
                    <template v-else>
                        <v-list-item v-bind:title="user['activation_key']">
                        <template #prepend>
                            <v-icon icon="mdi-key" />
                        </template>
                        <template #append>
                            <v-btn v-on:click="getNewActivationKey">Обновить ключ</v-btn>
                        </template>
                    </v-list-item>
                    </template >
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
    import { watch, computed, ref } from 'vue';
    import { jwtDecode } from 'jwt-decode';
    import BaseForm from '@/components/BaseForm.vue';
    import { authStore } from '@/auth';

    
    const loading = ref(true);
    const user = ref({});

        async function getNewActivationKey() {
        try {
            const response = await fetch(import.meta.env.VITE_API_URL + `${authStore.user_id()}/`, {
                'method': 'PATCH',
                headers: {
                    'Authorization': `Bearer ${authStore.accessToken}`,
                    'Content-Type': 'application/json'
                },
            })
            
            if (!response.ok) {
                throw Error()
            }
            
            const content = await response.json()
            user.value['activation_key'] = content['activation_key']

        } catch (error) {
            alert(`Ошибка при изменини ключа: ${response.status}: {response.statusText}`)
        }
    }


    watch(() => authStore.isAuthenticated(), async (newStatus) => {
        if (newStatus) {
            const userId = jwtDecode(authStore.accessToken)['user_id'];
            user.value = await authStore.fetchUser(userId)
            loading.value = false;
        } else {
            user.value = {}
            loading.value = true;
        }
        
        
    },{immediate: true})
</script>
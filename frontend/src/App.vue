<template>
  <v-app>
    <v-main>
      <v-app-bar color="teal-darken-4" density="compact" v-bind:title="$route.meta.title">
        <v-btn v-if="authStore.isAuthenticated" v-on:click="authStore.logout()">выйти</v-btn>
      </v-app-bar> 
      <RouterView></RouterView>
    </v-main >
  </v-app>
</template>

<script setup>
  import { useAuthStore } from './auth';

  const authStore = useAuthStore();
</script>
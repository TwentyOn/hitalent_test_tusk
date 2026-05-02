<template>
    <v-snackbar color="success" v-model="snackbar" timeout="5000">Письмо с ключом отправлено на почту</v-snackbar>
</template>

<script setup>
    const snackbar = defineModel({type: Boolean, default: false})
</script>
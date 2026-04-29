<template>
    <v-btn color="success" v-bind:loading="loading" class="mt-2" type="submit" block>
    {{ btnText }}
    <v-icon icon="mdi-chevron-right" end></v-icon>
    </v-btn>
</template>

<script setup>
    const props = defineProps(["loading", 'btnText'])
</script>
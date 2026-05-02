<template>
    <v-btn color="success" v-bind:loading="loading" v-bind:disabled="disabled" class="mt-2" type="submit" block>
        {{ btnText }}
        <v-icon icon="mdi-chevron-right" end></v-icon>
    </v-btn>
</template>

<script setup lang="ts">
    interface Props {
        btnText: string,
        loading: boolean,
        disabled?: boolean
    }
    const { disabled = false } = defineProps<Props>()
</script>
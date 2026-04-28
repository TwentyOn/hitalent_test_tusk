<template>
    <v-container class="fill-height d-flex flex-column justify-center" fluid>
        <v-sheet width="300" class="mx-auto">
            <v-card flat>
                <v-card-title class="text-h5 text-center mb-4">
                    {{ title }}
                </v-card-title>
                <v-card-text>
                    <slot></slot>
                </v-card-text>
            </v-card>
        </v-sheet>
    </v-container>
</template>

<script setup>
    defineProps(['title'])
</script>
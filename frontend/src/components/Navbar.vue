<script setup>
import GTranslation from './GTranslation.vue';
</script>

<template>
    <nav class="bg-white shadow-md grid grid-cols-2 items-center justify-end h-16">
                <div class="flex col-span-1">
                    <GTranslation />
                </div>
                <div class="flex col-span-1 justify-end mx-5">
                    <a href="/" class="flex-shrink-0">
                        <img src="../assets/logo.png" alt="Logo" class="h-10 w-10">
                    </a>
                </div>
    </nav>
</template>
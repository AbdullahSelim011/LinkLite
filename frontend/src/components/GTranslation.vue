
<script setup>
import { onMounted } from 'vue';

onMounted(() => {
    // Set the GTranslate settings
    (window).gtranslateSettings = {
        wrapper_selector: ".gtranslate_wrapper",
        native_language_names: true,
        languages: ["ar", "en", "fr"],
        default_language: "ar",
        flag_style: "3d",
        switcher_horizontal_position: 'left',
        switcher_vertical_position: 'top',


    };

    // Load the GTranslate script
    const script = document.createElement('script');
    script.src = 'https://cdn.gtranslate.net/widgets/latest/dwf.js';
    script.async = true;
    script.onerror = () => console.error('Failed to load GTranslate widget');
    document.head.appendChild(script);
});
</script>

<template>
    <div class="gtranslate_wrapper"></div>
</template>
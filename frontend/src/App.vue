<template>
	<Toaster position="top-right" />
	<Layout v-if="!isLoginPage">
		<router-view />
	</Layout>
	<router-view v-else />
</template>

<script setup>
import { Toaster } from 'vue-sonner';
import Layout from './Layout.vue';
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
console.log(route.path)
const isLoginPage = computed(() => route.path === '/login')
</script>

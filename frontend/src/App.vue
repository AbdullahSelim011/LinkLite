<template>
  <Toaster position="top-right" />
	<Layout>
		<router-view />
	</Layout>
</template>

<script setup>
import { Toaster } from 'vue-sonner';
import Layout from './Layout.vue';
</script>

<template>
	<div class="flex h-screen w-full flex-row bg-surface-white shadow">
		<Sidebar :header="{
			title: 'LinkLite',
			logo: '/assets/linklite/logo.png',
			menuItems: [ { label: 'Toggle Theme', icon: Moon, onClick: toggleTheme },]
		}"

		:sections="[
			{
				label: '',
				items: [
					{label: 'Links', icon: Link, to: '/'},
					{label: 'Analytics', icon: ChartColumn, to: '/analytics'},
					{label: 'Delivery Trip', icon: Link, to: '/deliverytrip'},
				]
			}
		]"/>
		<div class="w-full m-5">
			<slot></slot>
		</div>
	</div>
</template>

<script setup>
import { onMounted } from 'vue';
import { Sidebar } from 'frappe-ui';
import Moon from '~icons/lucide/moon';
import Link from "~icons/lucide/link";
import { useStorage } from '@vueuse/core'
import ChartColumn from "~icons/lucide/chart-column";

const userTheme = useStorage('user-theme', 'light');

onMounted(() => {
  document.documentElement.setAttribute('data-theme', userTheme.value);
});

function toggleTheme() {
  const currentTheme = userTheme.value;
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  userTheme.value = newTheme;
}
</script>
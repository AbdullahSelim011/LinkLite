<template>


	<div class="flex items-baseline justify-between mb-4">
		<h2 class="text-ink-gray-9 font-semibold">Links</h2>
		<Button variant="solid" @click="createDialogShown = true">
			Create Link
			<template #suffix>
				<span class=" font-mono bg-white/80 text-gray-700 rounded-sm px-1">C</span>
			</template>
		</Button>
	</div>

	<ListView
		v-if="links.list.data"
		rowKey="name"
		:columns="[{
			label: 'Short Link',
			key: 'name',
			width: 0.3
		},
		{
			label: 'Destination',
			key: 'destination_url'
		},
		{
			key: 'copy_to_clipboard'
		},
		{
			key: 'more_actions'
		},]"

	:rows="links.list.data"

	:options="{
		showTooltip: false,
		selectable: false,
		emptyState: {
			title: 'No links found',
			description: 'Create a new short link to get started',
			button: {
				label: 'New Link',
				variant: 'solid',
				onClick: () => {
					createDialogShown = true;
				},
			},
		}
	}"
	 >
	 <template #cell="{ item, row, column }">
		<Button v-if="column.key === 'copy_to_clipboard'" class="cursor-pointer" icon="copy" @click.stop="copyShortLinkToClipboard(row.name)" variant="outline" theme="blue"></Button>

		<Dropdown
			v-else-if="column.key === 'more_actions'"
			:options="[
				{'label': 'Show QR Code', onClick: () => {
					if (!row.qr_code) {
						toast.warning('No QR Code found!')
						return;
					}
					qrCodeLink = row.qr_code;
					qrCodeShown = true;
				}}
			]"
			>
			<Button icon="more-horizontal" />
		</Dropdown>

      	<span v-else class="font-medium text-ink-gray-7">
        	{{ item }}
      	</span>
    </template>
	</ListView>


	 <Dialog :options="{
		title: 'New Short Link',
		size: 'xl',
		actions: [
			{
				label: 'Create',
				variant: 'solid',
				onClick: createShortLink
			}
		]
	 }" v-model="createDialogShown">
		<template #body-content>
			<form class="space-y-3">
				<FormControl
					type="text"
					label="Destination URL"
					placeholder="https://youtube.com/@buildwithhussain"
					v-model="newLink.destination_url"
					autofocus
				/>

				<FormControl
					type="text"
					placeholder="bwh"
					label="Short Link"
					v-model="newLink.short_link"
				/>

				<FormControl
					type="textarea"
					label="Description"
					v-model="newLink.description"
				/>
			</form>

			<ErrorMessage class="mt-2" :message="links.insert.error" />
		</template>
	 </Dialog>


	 <Dialog :options="{
		title: 'Edit Link',
		size: 'xl',
		actions: [
			{
				label: 'Save',
				variant: 'solid',
				onClick(close) {
					links.setValue.submit({
						name: newLink.name,
						description: newLink.description,
						destination_url: newLink.destination_url
					}, {
						onSuccess() {
							newLink.short_link = ''
							newLink.description = ''
							newLink.destination_url = ''
							close();
						}
					})
				}
			},
			{
				label: 'Delete',
				variant: 'outline',
				theme: 'red',
				onClick(close) {
					links.delete.submit(newLink.name, {
						onSuccess() {
							close();
						}
					})
				}
			}
		]
	 }" v-model="editDialogShown">
		<template #body-content>
			<form class="space-y-3">
				<FormControl
					type="text"
					label="Destination URL"
					placeholder="https://youtube.com/@buildwithhussain"
					v-model="newLink.destination_url"
				/>

				<FormControl
					type="textarea"
					label="Description"
					v-model="newLink.description"
				/>
			</form>

			<ErrorMessage class="mt-2" :message="links.insert.error" />
		</template>
	 </Dialog>


	 <Dialog
	 	v-model="qrCodeShown"
		:options="{
			title: 'QR Code'
		}"
	  >
	  <template #body-content>
		<div class="flex justify-center items-center">
			<img v-if="qrCodeLink" :src="qrCodeLink" alt="QR Code for short link">
		</div>
	  </template>
	</Dialog>
</template>

<script setup>
import { ref } from "vue";
import { onKeyStroke } from "@vueuse/core";
import { ListView, Dialog, FormControl, ErrorMessage, Dropdown } from "frappe-ui";
import { createListResource } from "frappe-ui";
import { reactive } from "vue";
import { toast } from 'vue-sonner'

const createDialogShown = ref(false);
const editDialogShown = ref(false);
const qrCodeShown = ref(false);
const qrCodeLink = ref(null);

const newLink = reactive({
	short_link: "",
	destination_url: "",
	description: "",
});

onKeyStroke(["c", "C"], () => {
	createDialogShown.value = true;
});

const links = createListResource({
	doctype: "Short Link",
	fields: ["name", "destination_url", "description", "qr_code"],
	orderBy: "creation desc",
});

links.fetch();

function createShortLink(close) {
	links.insert.submit(
		{
			...newLink,
		},
		{
			onSuccess() {
				newLink.short_link = "";
				newLink.description = "";
				newLink.destination_url = "";
				copyShortLinkToClipboard(newLink.short_link)
				close();
			},
		},
	);
}

function copyShortLinkToClipboard(text) {
	navigator.clipboard.writeText(`${window.location.origin}/${text}`);
	toast.success("Link copied to clipboard!")
}
</script>

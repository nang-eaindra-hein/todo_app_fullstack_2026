<script lang="ts">
	import { TodoStatusEnum, type TodoStatus } from '#lib/types/todo.ts';
	import Button from '#lib/ui/Button.svelte';
	import Modal from '#lib/ui/Modal.svelte';
	import { X, Plus } from '@lucide/svelte';
	import toast, { Toaster } from 'svelte-5-french-toast';

	let newAlbumModal = $state(false);

	let newAlbumNameInput = $state('');
	let newListNameInput = $state('');
	let listDescriptionInput = $state('');
	let listStatusInput = $state<TodoStatus>(TodoStatusEnum.Todo);

	let { createListMutation, newListModal = $bindable() } = $props();
	//album modal confirm
	function handleAlbumConfirm() {
		if (!newAlbumNameInput) {
			toast.error('Please fill all the fields.');
			return;
		}
	}

	//list modal confirm
	function handleListConfirm() {
		if (!newListNameInput || !listDescriptionInput) {
			toast.error('Please fill all the fields.');
			return;
		}
		createListMutation.mutate({
			title: newListNameInput,
			description: listDescriptionInput,
			status: listStatusInput
		});
	}
</script>

<Button
	onclick={() => {
		newAlbumModal = true;
	}}
	size="lg"
	text="Add new album"
	icon={Plus}
/>
<Button
	onclick={() => {
		newListModal = true;
	}}
	size="lg"
	text="Add new list"
	icon={Plus}
/>

{#if newListModal}
	<Modal
		><div class="space-y-4">
			<div class="flex w-full items-center justify-between">
				<h1>New List</h1>
				<Button
					variant="red"
					icon={X}
					onclick={() => {
						newAlbumModal = false;
						newListModal = false;
					}}
				/>
			</div>
			<input
				bind:value={newListNameInput}
				placeholder="Enter list's title"
				type="text"
				class="w-full rounded-full border border-amber-200 px-2 py-1 text-sm"
			/>
			<textarea
				bind:value={listDescriptionInput}
				placeholder="description"
				class="w-full rounded-lg border border-green-200 px-4 py-1 text-sm"></textarea>

			<div class="flex gap-x-4">
				<p>Status :</p>
				<Button
					variant={listStatusInput === TodoStatusEnum.Done ? 'line' : 'green'}
					onclick={() => {
						listStatusInput = TodoStatusEnum.Done;
					}}
					text="Done"
				/>
				<Button
					variant={listStatusInput === TodoStatusEnum.InProgress ? 'line' : 'default'}
					onclick={() => {
						listStatusInput = TodoStatusEnum.InProgress;
					}}
					text="In InProgress"
				/>
				<Button
					variant={listStatusInput === TodoStatusEnum.Todo ? 'line' : 'blue'}
					onclick={() => {
						listStatusInput = TodoStatusEnum.Todo;
					}}
					text="Todo"
				/>
			</div>
			<div class="flex justify-end">
				<Button
					onclick={() => handleListConfirm()}
					size="md"
					icon={Plus}
					variant="gray"
					text="Create"
				/>
			</div>
		</div></Modal
	>
{/if}
<!--album modal-->
{#if newAlbumModal}
	<Modal
		><div class="w-full space-y-4">
			<div class="flex items-center justify-between">
				<h1>New Album</h1>
				<Button
					variant="red"
					onclick={() => {
						newAlbumModal = false;
						newListModal = false;
					}}
					icon={X}
				/>
			</div>

			<input
				bind:value={newAlbumNameInput}
				placeholder="Enter album's name"
				type="text"
				class="w-full rounded-full border border-blue-200 px-2 py-1 text-sm"
			/>
			<div class="flex justify-end">
				<Button
					onclick={() => handleAlbumConfirm()}
					size="md"
					variant="gray"
					text="Create"
					icon={Plus}
				/>
			</div>
		</div>
	</Modal>{/if}
<Toaster />

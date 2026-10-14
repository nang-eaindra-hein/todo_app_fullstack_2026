<script lang="ts">
	import { createList, getLists, updateTodoStatus } from '#lib/api/todo.ts';
	import {
		TodoStatusEnum,
		type createListType,
		type TodoStatus,
		type updateStatus
	} from '#lib/types/todo.ts';
	import Modal from '#lib/ui/Modal.svelte';

	import { createMutation, createQuery, useQueryClient } from '@tanstack/svelte-query';
	import toast, { Toaster } from 'svelte-5-french-toast';

	const queryClient = useQueryClient();
	let newAlbumModal = $state(false);
	let newListModal = $state(false);
	let newAlbumNameInput = $state('');
	let newListNameInput = $state('');
	let listDescriptionInput = $state('');
	let listStatusInput = $state<TodoStatus>(TodoStatusEnum.Todo);

	const listsQuery = createQuery(() => ({
		queryKey: ['todos'],
		queryFn: getLists
	}));

	const updateStatusMutation = createMutation(() => ({
		mutationFn: (data: updateStatus) => updateTodoStatus(data),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['todos'] });
		},
		onError: () => {
			toast.error('Failed to update status!');
		}
	}));

	const createListMutation = createMutation(() => ({
		mutationFn: (data: createListType) => createList(data),
		onSuccess: () => {
			toast.success('List created!');
			queryClient.invalidateQueries({ queryKey: ['todos'] });
			newListModal = false;
		},
		onError: () => {
			toast.error('Failed to create a list!');
		}
	}));

	function handleAlbumConfirm() {
		if (!newAlbumNameInput) {
			toast.error('Please fill all the fields.');
			return;
		}
	}
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

	const nextStatus = {
		[TodoStatusEnum.Todo]: TodoStatusEnum.InProgress,
		[TodoStatusEnum.InProgress]: TodoStatusEnum.Done,
		[TodoStatusEnum.Done]: TodoStatusEnum.Todo
	} as const;
</script>

<div
	class="object-start flex h-screen w-full flex-col items-center justify-start overflow-auto bg-[url('/home.jpeg')] bg-cover bg-center bg-no-repeat"
>
	<h1 class="jsutify-center mt-10 flex items-center font-tangerine-bold text-5xl font-extrabold">
		Todo Lists
	</h1>
	<div class="mr-10 flex w-full items-center justify-end gap-x-5">
		<button
			onclick={() => {
				newAlbumModal = true;
			}}
			class="bg-opacity-5 mt-5 flex cursor-pointer justify-end rounded-full border border-amber-300 bg-gray-50 px-4 py-2 text-lg hover:bg-amber-100/30"
			>Add new album</button
		>
		<button
			onclick={() => {
				newListModal = true;
			}}
			class="bg-opacity-5 mt-5 flex cursor-pointer justify-end rounded-full border border-amber-300 bg-gray-50 px-4 py-2 text-lg hover:bg-amber-100/30"
			>Add new list</button
		>
	</div>
	<div class=" grid w-full grid-cols-2 gap-4 p-10">
		{#if listsQuery.isPending}
			<p>Loading...</p>
		{:else if listsQuery.isError}
			<p>Error...</p>
		{:else}
			{#each listsQuery.data ?? [] as list, i (list.id)}
				<div class="flex w-full items-start justify-between rounded-lg bg-white/20 p-4">
					<div class=" flex items-start gap-2">
						<p class="text-lg font-semibold">{i + 1}.</p>
						<div class="space-y-2">
							<p class="text-lg font-semibold">{list.title}</p>
							<ul class="text-md list-disc pl-5">
								<li>{list.description}</li>
							</ul>
						</div>
					</div>
					<button
						onclick={() => {
							updateStatusMutation.mutate({
								id: list.id,
								status: nextStatus[list.status as TodoStatus]
							});
						}}
						class="w-fit cursor-pointer rounded-full border bg-white/50 p-1 text-xs hover:bg-amber-100 {list.status ===
						TodoStatusEnum.Todo
							? 'border-red-400 text-red-400'
							: list.status === TodoStatusEnum.InProgress
								? 'border-yellow-400 text-yellow-400'
								: 'border-green-400 text-green-400'}"
					>
						{list.status === TodoStatusEnum.Todo
							? 'Todo'
							: list.status === TodoStatusEnum.InProgress
								? 'In Progress'
								: 'Done'}
					</button>
				</div>
			{/each}
		{/if}
	</div>
</div>

{#if newListModal}
	<Modal
		><div class="space-y-4">
			<div class="flex w-full items-center justify-between">
				<h1>New List</h1>
				<button
					class="cursor-pointer"
					onclick={() => {
						newAlbumModal = false;
						newListModal = false;
					}}>X</button
				>
			</div>
			<input
				bind:value={newListNameInput}
				placeholder="Enter list's title"
				type="text"
				class="w-full rounded-full border px-2 py-1 text-sm"
			/>
			<textarea
				bind:value={listDescriptionInput}
				placeholder="description"
				class="w-full rounded-lg border px-4 py-1 text-sm"></textarea>

			<div class="flex gap-x-4">
				<p>Status :</p>
				<button
					class="rounded-full bg-green-50 px-2 {listStatusInput === TodoStatusEnum.Done
						? 'line-through'
						: ''}"
					onclick={() => {
						listStatusInput = TodoStatusEnum.Done;
					}}>Done</button
				>
				<button
					class="rounded-full bg-green-50 px-2 {listStatusInput === TodoStatusEnum.InProgress
						? 'line-through'
						: ''}"
					onclick={() => {
						listStatusInput = TodoStatusEnum.InProgress;
					}}>In Progress</button
				><button
					class="rounded-full bg-red-50 px-2 {listStatusInput === TodoStatusEnum.Todo
						? 'line-through'
						: ''}"
					onclick={() => {
						listStatusInput = TodoStatusEnum.Todo;
					}}>Todo</button
				>
			</div>
			<div class="flex justify-end">
				<button
					onclick={() => handleListConfirm()}
					class="cursor-pointer rounded-full border border-amber-300 bg-white px-2 py-1 hover:bg-white/20"
					>Done</button
				>
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
				<button
					class="cursor-pointer"
					onclick={() => {
						newAlbumModal = false;
						newListModal = false;
					}}>X</button
				>
			</div>

			<input
				bind:value={newAlbumNameInput}
				placeholder="Enter album's name"
				type="text"
				class="w-full rounded-full border px-2 py-1 text-sm"
			/>
			<div class="flex justify-end">
				<button
					onclick={() => handleAlbumConfirm()}
					class="cursor-pointer rounded-full border border-amber-300 bg-white px-2 py-1 hover:bg-white/20"
					>Done</button
				>
			</div>
		</div>
	</Modal>{/if}
<Toaster />

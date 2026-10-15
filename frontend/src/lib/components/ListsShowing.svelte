<script lang="ts">
	import { TodoStatusEnum, type TodoStatus } from '#lib/types/todo.ts';
	import Button from '#lib/ui/Button.svelte';
	import {
		CircleDashedCheck,
		CircleCheck,
		CircleDashed,
		Sparkle,
		Trash,
		Pencil,
		X,
		Check
	} from '@lucide/svelte';

	let {
		editingId = $bindable(),
		listsQuery,
		updateListMutation,
		updateStatusMutation,
		deleteListMutation
	} = $props();
	let listTitleInput = $state('');
	let listDescriptionInput = $state('');

	//status change btn
	const nextStatus = {
		[TodoStatusEnum.Todo]: TodoStatusEnum.InProgress,
		[TodoStatusEnum.InProgress]: TodoStatusEnum.Done,
		[TodoStatusEnum.Done]: TodoStatusEnum.Todo
	} as const;
</script>

{#each listsQuery.data?.items ?? [] as list, i (list.id)}
	<div class="w-full space-y-2 rounded-lg bg-white/20 p-4">
		<div class="flex w-full items-start justify-between gap-2">
			<!--list details-->
			<div class=" flex items-start gap-2">
				<p class="text-md flex items-center font-semibold">
					{i + 1}<Sparkle class="h-3 w-3" />
				</p>
				{#if editingId === list.id}
					<input
						bind:value={listTitleInput}
						placeholder={list.title}
						type="text"
						class="w-full rounded-full border border-blue-200 px-2 py-1 text-sm"
					/>
				{:else}
					<p class="text-lg font-semibold">{list.title}</p>
				{/if}
			</div>
			<!--btns-->
			<div class="flex gap-4">
				<!--status btn-->
				<Button
					icon={list.status === TodoStatusEnum.Todo
						? CircleDashed
						: list.status === TodoStatusEnum.InProgress
							? CircleDashedCheck
							: CircleCheck}
					onclick={() => {
						updateStatusMutation.mutate({
							id: list.id,
							status: nextStatus[list.status as TodoStatus]
						});
					}}
					variant={list.status === TodoStatusEnum.Todo
						? 'blue'
						: list.status === TodoStatusEnum.InProgress
							? 'default'
							: 'green'}
					text={list.status === TodoStatusEnum.Todo
						? 'Todo'
						: list.status === TodoStatusEnum.InProgress
							? 'In Progress'
							: 'Done'}
				/>
				<!--delete btn-->
				<Button
					variant="red"
					onclick={() => {
						deleteListMutation.mutate(list.id);
					}}
					text="Delete"
					icon={Trash}
				/>
				<!--edit btn-->
				<Button
					variant="blue"
					text="Edit"
					icon={Pencil}
					onclick={() => {
						editingId = list.id;
						listTitleInput = list.title;
						listDescriptionInput = list.description;
					}}
				/>
				<!--edit mode btns-->
				{#if editingId === list.id}
					<Button
						icon={Check}
						text="Confirm"
						variant="green"
						onclick={() => {
							updateListMutation.mutate({
								id: list.id,
								title: listTitleInput,
								description: listDescriptionInput,
								status: list.status
							});
						}}
					/>
					<Button
						icon={X}
						text="Cancel"
						variant="red"
						onclick={() => {
							editingId = null;
						}}
					/>
				{/if}
			</div>
		</div>

		{#if editingId === list.id}
			<textarea
				bind:value={listDescriptionInput}
				placeholder={list.description}
				class="w-full rounded-lg border border-green-200 px-4 py-1 text-sm"></textarea>
		{:else}
			<ul class="text-md list-disc pl-5">
				<li>{list.description}</li>
			</ul>
		{/if}
	</div>
{/each}

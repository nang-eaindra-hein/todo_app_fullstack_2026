<script lang="ts">
	import {
		createList,
		deleteList,
		deleteLists,
		getLists,
		updateList,
		updateTodoStatus
	} from '#lib/api/todo.ts';
	import CreateButtons from '#lib/components/CreateButtons.svelte';
	import ListsShowing from '#lib/components/ListsShowing.svelte';
	import type {
		createListType,
		TodoStatus,
		updateListType,
		updateStatusType
	} from '#lib/types/todo.ts';
	import Button from '#lib/ui/Button.svelte';
	import { Trash, ScrollText } from '@lucide/svelte';
	import {
		createMutation,
		createQuery,
		keepPreviousData,
		useQueryClient
	} from '@tanstack/svelte-query';
	import toast from 'svelte-5-french-toast';

	const queryClient = useQueryClient();
	let filter = $state<TodoStatus | undefined>(undefined);
	let newListModal = $state(false);
	let editingId = $state<number | null>(null);

	//get lists
	const listsQuery = createQuery(() => ({
		queryKey: ['todos', filter],
		queryFn: () => getLists(filter),
		placeholderData: keepPreviousData
	}));
	//create list
	const createListMutation = createMutation(() => ({
		mutationFn: (data: createListType) => createList(data),
		onSuccess: () => {
			toast.success('List created!');
			queryClient.invalidateQueries({ queryKey: ['todos', filter] });
			newListModal = false;
		},
		onError: () => {
			toast.error('Failed to create a list!');
		}
	}));

	//delete lists
	const deleteListsMutation = createMutation(() => ({
		mutationFn: () => deleteLists(),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['todos', filter] });
			toast.success('Clear all lists!');
		},
		onError: () => {
			toast.error('Failed to clear all!');
		}
	}));

	//update status
	const updateStatusMutation = createMutation(() => ({
		mutationFn: (data: updateStatusType) => updateTodoStatus(data),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['todos', filter] });
		},
		onError: () => {
			toast.error('Failed to update status!');
		}
	}));

	//update data in a list
	const updateListMutation = createMutation(() => ({
		mutationFn: (data: updateListType) => updateList(data),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['todos', filter] });
			toast.success('Update Successfully!');
			editingId = null;
		},
		onError: () => {
			toast.error('Failed to update!');
		}
	}));

	//delete list
	const deleteListMutation = createMutation(() => ({
		mutationFn: (id: number) => deleteList({ id }),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['todos', filter] });
			toast.success('deleted a list!');
		},
		onError: () => {
			toast.error('Failed to delete a list!');
		}
	}));

	const tabs = $derived([
		{ label: 'All', value: undefined, count: listsQuery.data?.count?.all ?? 0 },
		{ label: 'Todo', value: 'Todo' as TodoStatus, count: listsQuery.data?.count?.todo ?? 0 },
		{
			label: 'In Progress',
			value: 'In_Progress' as TodoStatus,
			count: listsQuery.data?.count?.in_progress ?? 0
		},
		{ label: 'Done', value: 'Done' as TodoStatus, count: listsQuery.data?.count?.done ?? 0 }
	]);
	let total = $derived(listsQuery.data?.count?.all ?? 0);
</script>

<div
	class="object-start flex h-screen w-full flex-col items-center justify-start overflow-auto bg-[url('/home.jpeg')] bg-cover bg-center bg-no-repeat"
>
	<h1
		class="jsutify-center mt-10 flex items-center gap-1 font-tangerine-bold text-5xl font-extrabold"
	>
		Todo Lists <ScrollText class="h-10 w-10 text-gray-500" />
	</h1>
	<!--new list/album-->
	<div class="mt-5 mr-10 flex w-full items-center justify-end gap-x-5">
		<CreateButtons bind:newListModal {createListMutation} />
	</div>
	<!--filters-->

	<div class="flex gap-2">
		{#each tabs as tab}
			<Button
				variant={filter === tab.value ? 'blue' : 'default'}
				onclick={() => (filter = tab.value)}
				text="{tab.label} ({tab.count})"
			/>
		{/each}
	</div>

	<!--clear all btn-->
	{#if total > 0}
		<div class="mt-5 mr-10 flex w-full items-center justify-end">
			<Button
				variant="red"
				onclick={() => {
					deleteListsMutation.mutate();
				}}
				text="Clear All"
				icon={Trash}
			/>
		</div>
	{/if}
	<!--lists showing-->
	<div class=" grid w-full grid-cols-2 gap-4 p-10">
		<ListsShowing
			{listsQuery}
			{updateListMutation}
			{updateStatusMutation}
			{deleteListMutation}
			bind:editingId
		/>
	</div>
</div>

<script lang="ts">
	import { deleteLists, getLists } from '#lib/api/todo.ts';
	import CreateButtons from '#lib/components/CreateButtons.svelte';
	import ListsShowing from '#lib/components/ListsShowing.svelte';
	import Button from '#lib/ui/Button.svelte';
	import { Trash, ScrollText } from '@lucide/svelte';
	import { createMutation, createQuery, useQueryClient } from '@tanstack/svelte-query';
	import toast from 'svelte-5-french-toast';

	const queryClient = useQueryClient();

	//get lists
	const listsQuery = createQuery(() => ({
		queryKey: ['todos'],
		queryFn: getLists
	}));

	//delete lists
	const deleteListsMutation = createMutation(() => ({
		mutationFn: () => deleteLists(),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['todos'] });
			toast.success('Clear all lists!');
		},
		onError: () => {
			toast.error('Failed to clear all!');
		}
	}));
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
		<CreateButtons />
	</div>
	<!--clear all btn-->
	{#if listsQuery.data}
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
		<ListsShowing {listsQuery} />
	</div>
</div>

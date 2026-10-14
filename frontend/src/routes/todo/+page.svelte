<script lang="ts">
  import { createList, getLists, updateTodoStatus } from "$lib/api/todo";
  import {
    TodoStatusEnum,
    type createListType,
    type TodoStatus,
    type updateStatus,
  } from "$lib/types/todo";
  import Modal from "$lib/ui/Modal.svelte";
  import {
    createMutation,
    createQuery,
    useQueryClient,
  } from "@tanstack/svelte-query";
  import toast, { Toaster } from "svelte-french-toast";

  const queryClient = useQueryClient();
  let newAlbumModal = $state(false);
  let newListModal = $state(false);
  let newAlbumNameInput = $state("");
  let newListNameInput = $state("");
  let listDescriptionInput = $state("");
  let listStatusInput = $state<TodoStatus>(TodoStatusEnum.Todo);

  const listsQuery = createQuery(() => ({
    queryKey: ["todos"],
    queryFn: getLists,
  }));

  const updateStatusMutation = createMutation(() => ({
    mutationFn: (data: updateStatus) => updateTodoStatus(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
    onError: () => {
      toast.error("Failed to update status!");
    },
  }));

  const createListMutation = createMutation(() => ({
    mutationFn: (data: createListType) => createList(data),
    onSuccess: () => {
      toast.success("List created!");
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      newListModal = false;
    },
    onError: () => {
      toast.error("Failed to create a list!");
    },
  }));

  function handleAlbumConfirm() {
    if (!newAlbumNameInput) {
      toast.error("Please fill all the fields.");
      return;
    }
  }
  function handleListConfirm() {
    if (!newListNameInput || !listDescriptionInput) {
      toast.error("Please fill all the fields.");
      return;
    }
    createListMutation.mutate({
      title: newListNameInput,
      description: listDescriptionInput,
      status: listStatusInput,
    });
  }

  const nextStatus = {
    [TodoStatusEnum.Todo]: TodoStatusEnum.InProgress,
    [TodoStatusEnum.InProgress]: TodoStatusEnum.Done,
    [TodoStatusEnum.Done]: TodoStatusEnum.Todo,
  } as const;
</script>

<div
  class="h-screen overflow-auto w-full bg-[url('/home.jpeg')] bg-cover bg-center bg-no-repeat object-start flex-col flex justify-start items-center"
>
  <h1
    class="mt-10 font-tangerine-bold text-5xl flex jsutify-center items-center font-extrabold"
  >
    Todo Lists
  </h1>
  <div class="flex w-full gap-x-5 justify-end items-center mr-10">
    <button
      onclick={() => {
        newAlbumModal = true;
      }}
      class="flex mt-5 justify-end text-lg py-2 px-4 cursor-pointer rounded-full bg-gray-50 bg-opacity-5 hover:bg-amber-100/30 border border-amber-300"
      >Add new album</button
    >
    <button
      onclick={() => {
        newListModal = true;
      }}
      class="flex mt-5 justify-end text-lg py-2 px-4 cursor-pointer rounded-full bg-gray-50 bg-opacity-5 hover:bg-amber-100/30 border border-amber-300"
      >Add new list</button
    >
  </div>
  <div class=" w-full p-10 grid grid-cols-2 gap-4">
    {#if listsQuery.isPending}
      <p>Loading...</p>
    {:else if listsQuery.isError}
      <p>Error...</p>
    {:else}
      {#each listsQuery.data ?? [] as list, i (list.id)}
        <div
          class="p-4 bg-white/20 w-full rounded-lg flex justify-between items-start"
        >
          <div class=" flex gap-2 items-start">
            <p class="font-semibold text-lg">{i + 1}.</p>
            <div class="space-y-2">
              <p class="font-semibold text-lg">{list.title}</p>
              <ul class="text-md pl-5 list-disc">
                <li>{list.description}</li>
              </ul>
            </div>
          </div>
          <button
            onclick={() => {
              updateStatusMutation.mutate({
                id: list.id,
                status: nextStatus[list.status as TodoStatus],
              });
            }}
            class="rounded-full hover:bg-amber-100 cursor-pointer border bg-white/50 w-fit p-1 text-xs {list.status ===
            TodoStatusEnum.Todo
              ? 'text-red-400 border-red-400'
              : list.status === TodoStatusEnum.InProgress
                ? 'text-yellow-400 border-yellow-400'
                : 'text-green-400 border-green-400'}"
          >
            {list.status === TodoStatusEnum.Todo
              ? "Todo"
              : list.status === TodoStatusEnum.InProgress
                ? "In Progress"
                : "Done"}
          </button>
        </div>
      {/each}
    {/if}
  </div>
</div>

{#if newListModal}
  <Modal
    ><div class="space-y-4">
      <div class="flex justify-between w-full items-center">
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
        class="py-1 px-2 text-sm w-full border rounded-full"
      />
      <textarea
        bind:value={listDescriptionInput}
        placeholder="description"
        class="py-1 px-4 text-sm w-full border rounded-lg"
      ></textarea>

      <div class="flex gap-x-4">
        <p>Status :</p>
        <button
          class="bg-green-50 rounded-full px-2 {listStatusInput ===
          TodoStatusEnum.Done
            ? 'line-through'
            : ''}"
          onclick={() => {
            listStatusInput = TodoStatusEnum.Done;
          }}>Done</button
        >
        <button
          class="bg-green-50 rounded-full px-2 {listStatusInput ===
          TodoStatusEnum.InProgress
            ? 'line-through'
            : ''}"
          onclick={() => {
            listStatusInput = TodoStatusEnum.InProgress;
          }}>In Progress</button
        ><button
          class="bg-red-50 rounded-full px-2 {listStatusInput ===
          TodoStatusEnum.Todo
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
          class="hover:bg-white/20 cursor-pointer bg-white border border-amber-300 rounded-full py-1 px-2"
          >Done</button
        >
      </div>
    </div></Modal
  >
{/if}
<!--album modal-->
{#if newAlbumModal}
  <Modal
    ><div class="space-y-4 w-full">
      <div class="flex justify-between items-center">
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
        class="py-1 px-2 text-sm w-full border rounded-full"
      />
      <div class="flex justify-end">
        <button
          onclick={() => handleAlbumConfirm()}
          class="hover:bg-white/20 cursor-pointer bg-white border border-amber-300 rounded-full py-1 px-2"
          >Done</button
        >
      </div>
    </div>
  </Modal>{/if}
<Toaster />

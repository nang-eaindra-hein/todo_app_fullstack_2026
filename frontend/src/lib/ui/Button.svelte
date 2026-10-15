<script lang="ts">
	import type { Component } from 'svelte';
	import type { LucideProps } from '@lucide/svelte';

	type Variant = 'default' | 'red' | 'green' | 'blue' | 'line' | 'gray';

	type Size = 'md' | 'sm' | 'lg';
	let {
		text,
		icon: Icon,
		variant = 'default',
		onclick,
		size = 'sm'
	}: {
		text?: string;
		icon?: Component<LucideProps>;
		variant?: Variant;
		onclick?: () => void;
		size?: Size;
	} = $props();

	const variantClass: Record<Variant, string> = {
		red: 'border-red-400 bg-red-50 text-red-400 ',
		blue: ' border-blue-400 bg-blue-50 text-blue-400',
		green: 'border-green-400 bg-green-50 text-green-400',
		default: 'border-amber-400 bg-amber-50 text-amber-400',
		line: 'line-through ',
		gray: 'text-gray-500 '
	};

	const sizeClass: Record<Size, string> = {
		sm: 'p-1 text-xs',
		md: 'p-2 text-md',
		lg: 'p-3 text-lg'
	};
</script>

<button
	class="flex w-fit cursor-pointer items-center gap-1 rounded-full border {sizeClass[
		size
	]} hover:bg-amber-100 {variantClass[variant]}"
	{onclick}
>
	{text}
	{#if Icon}
		<Icon class="h-4 w-4" />
	{/if}
</button>

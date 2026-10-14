<script lang="ts">
	import { login } from '#lib/api/users.ts';
	import type { LoginType } from '#lib/types/signup.ts';
	import { goto } from '$app/navigation';
	import { createMutation } from '@tanstack/svelte-query';
	import toast, { Toaster } from 'svelte-5-french-toast';

	let usernameInput = $state('');

	let passwordInput = $state('');

	const loginMutation = createMutation(() => ({
		mutationFn: (data: LoginType) => login(data),

		onSuccess: (data) => {
			toast.success('Log in successfully!');
			localStorage.setItem('token', data.token);

			goto('/todo');
		},
		onError: (error) => toast.error(`${error}. Log in Unsuccessful!`)
	}));

	function handleConfirm() {
		if (!usernameInput || !passwordInput) {
			toast.error('Please fill all the fields');
		}
		loginMutation.mutate({
			username: usernameInput,
			password: passwordInput
		});
	}
</script>

<div
	class="flex h-screen w-full flex-col items-center justify-center gap-y-6 bg-[url('/login.jpeg')] bg-cover bg-center bg-no-repeat object-center"
>
	<h1 class="font-tangerine-bold text-5xl font-extrabold">Log In</h1>
	<div
		class="flex flex-col gap-y-4 rounded-2xl border border-white/30 bg-white/20 p-6 shadow-2xl backdrop-blur-lg"
	>
		<input
			class="rounded-full border bg-white px-3 py-2"
			type="text"
			placeholder="Username"
			bind:value={usernameInput}
		/>

		<input
			placeholder="password"
			type="password"
			class="rounded-full border bg-white px-3 py-2"
			bind:value={passwordInput}
		/>
	</div>
	<button
		class="bg-opacity-5 rounded-full bg-gray-50 px-6 font-tangerine-bold text-2xl hover:bg-white/60"
		onclick={() => {
			handleConfirm();
		}}>Confirm</button
	>
	<Toaster />

	<p
		class="bg-opacity-5 rounded-full bg-gray-50 px-6 font-tangerine-bold text-2xl hover:bg-white/60"
	>
		Doesn't have an account? <button
			class="cursor-pointer text-3xl text-green-900 hover:underline"
			onclick={() => goto('/signup')}>Sign Up</button
		> here.
	</p>
</div>

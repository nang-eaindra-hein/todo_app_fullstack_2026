<script lang="ts">
	import { signup } from '#lib/api/users.ts';
	import type { SignupType } from '#lib/types/signup.ts';
	import { goto } from '$app/navigation';
	import { createMutation } from '@tanstack/svelte-query';
	import toast, { Toaster } from 'svelte-5-french-toast';

	let usernameInput = $state('');
	let emailInput = $state('');
	let passwordInput = $state('');
	let confirmPasswordInput = $state('');

	const signupMutation = createMutation(() => ({
		mutationFn: (data: SignupType) => signup(data),
		onSuccess: () => {
			(toast.success('Sign up successfully!'), goto('/login'));
		},
		onError: (error) => toast.error(`${error}. Sign up Unsuccessful!`)
	}));

	function handleConfirm() {
		if (passwordInput !== confirmPasswordInput) {
			toast.error('password and confirm password are not the same');
		}
		if (!usernameInput || !emailInput || !passwordInput || !confirmPasswordInput) {
			toast.error('Please fill all the fields');
		}
		signupMutation.mutate({
			username: usernameInput,
			email: emailInput,
			password: passwordInput
		});
	}
</script>

<div
	class="flex h-screen w-full flex-col items-center justify-center gap-y-6 bg-[url('/login.jpeg')] bg-cover bg-center bg-no-repeat object-center"
>
	<h1 class="font-tangerine-bold text-5xl font-extrabold">Sign Up</h1>
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
			placeholder="Email"
			type="email"
			class="rounded-full border bg-white px-3 py-2"
			bind:value={emailInput}
		/>
		<input
			placeholder="password"
			type="password"
			class="rounded-full border bg-white px-3 py-2"
			bind:value={passwordInput}
		/>
		<input
			placeholder="confirm password"
			type="password"
			class="rounded-full border bg-white px-3 py-2"
			bind:value={confirmPasswordInput}
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
		Already have an account? <button
			class="cursor-pointer text-3xl text-green-900 hover:underline"
			onclick={() => goto('/login')}>Log In</button
		> here.
	</p>
</div>

<script lang="ts">
  import { goto } from "$app/navigation";
  import { signup } from "$lib/api/users";
  import type { SignupType } from "$lib/types/signup";
  import { createMutation } from "@tanstack/svelte-query";
  import toast, { Toaster } from "svelte-french-toast";

  let usernameInput = $state("");
  let emailInput = $state("");
  let passwordInput = $state("");
  let confirmPasswordInput = $state("");

  const signupMutation = createMutation(() => ({
    mutationFn: (data: SignupType) => signup(data),
    onSuccess: () => {
      (toast.success("Sign up successfully!"), goto("/login"));
    },
    onError: (error) => toast.error(`${error}. Sign up Unsuccessful!`),
  }));

  function handleConfirm() {
    if (passwordInput !== confirmPasswordInput) {
      toast.error("password and confirm password are not the same");
    }
    if (
      !usernameInput ||
      !emailInput ||
      !passwordInput ||
      !confirmPasswordInput
    ) {
      toast.error("Please fill all the fields");
    }
    signupMutation.mutate({
      username: usernameInput,
      email: emailInput,
      password: passwordInput,
    });
  }
</script>

<div
  class="h-screen w-full bg-[url('/login.jpeg')] bg-cover bg-center bg-no-repeat object-center flex flex-col gap-y-6 justify-center items-center"
>
  <h1 class="font-tangerine-bold text-5xl font-extrabold">Sign Up</h1>
  <div
    class="bg-white/20 backdrop-blur-lg shadow-2xl border border-white/30 rounded-2xl p-6 flex flex-col gap-y-4"
  >
    <input
      class="border bg-white py-2 px-3 rounded-full"
      type="text"
      placeholder="Username"
      bind:value={usernameInput}
    />
    <input
      placeholder="Email"
      type="email"
      class="border bg-white py-2 px-3 rounded-full"
      bind:value={emailInput}
    />
    <input
      placeholder="password"
      type="password"
      class="border bg-white py-2 px-3 rounded-full"
      bind:value={passwordInput}
    />
    <input
      placeholder="confirm password"
      type="password"
      class="border bg-white py-2 px-3 rounded-full"
      bind:value={confirmPasswordInput}
    />
  </div>
  <button
    class="font-tangerine-bold text-2xl rounded-full bg-gray-50 bg-opacity-5 px-6 hover:bg-white/60"
    onclick={() => {
      handleConfirm();
    }}>Confirm</button
  >
  <Toaster />

  <p
    class="font-tangerine-bold text-2xl rounded-full bg-gray-50 bg-opacity-5 px-6 hover:bg-white/60"
  >
    Already have an account? <button
      class="text-3xl text-green-900 cursor-pointer hover:underline"
      onclick={() => goto("/login")}>Log In</button
    > here.
  </p>
</div>

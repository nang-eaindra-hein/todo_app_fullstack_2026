<script lang="ts">
  import { goto } from "$app/navigation";
  import { login } from "$lib/api/users";
  import type { LoginType } from "$lib/types/signup";

  import { createMutation } from "@tanstack/svelte-query";
  import toast, { Toaster } from "svelte-french-toast";

  let usernameInput = $state("");

  let passwordInput = $state("");

  const loginMutation = createMutation(() => ({
    mutationFn: (data: LoginType) => login(data),

    onSuccess: (data) => {
      toast.success("Log in successfully!");
      localStorage.setItem("token", data.access_token);

      goto("/todo");
    },
    onError: (error) => toast.error(`${error}. Log in Unsuccessful!`),
  }));

  function handleConfirm() {
    if (!usernameInput || !passwordInput) {
      toast.error("Please fill all the fields");
    }
    loginMutation.mutate({
      username: usernameInput,
      password: passwordInput,
    });
  }
</script>

<div
  class="h-screen w-full bg-[url('/login.jpeg')] bg-cover bg-center bg-no-repeat object-center flex flex-col gap-y-6 justify-center items-center"
>
  <h1 class="font-tangerine-bold text-5xl font-extrabold">Log In</h1>
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
      placeholder="password"
      type="password"
      class="border bg-white py-2 px-3 rounded-full"
      bind:value={passwordInput}
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
    Doesn't have an account? <button
      class="text-3xl text-green-900 cursor-pointer hover:underline"
      onclick={() => goto("/signup")}>Sign Up</button
    > here.
  </p>
</div>

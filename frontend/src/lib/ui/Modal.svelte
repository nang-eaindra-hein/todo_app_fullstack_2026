<script lang="ts">
  let { children } = $props();
</script>

<div class="inset-0 w-full h-screen fixed grid place-items-center">
  <div
    class="grid place-items-center h-fit bg-amber-50 rounded-2xl shadow-xl opacity-90 p-4 min-w-90 max-w-90"
  >
    {@render children?.()}
  </div>
</div>

<script>
  import { onMount } from 'svelte';

  let glowEl;

  onMount(() => {
    function handleMouseMove(e) {
      if (glowEl) {
        glowEl.style.left = e.clientX + 'px';
        glowEl.style.top = e.clientY + 'px';
      }
    }
    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  });
</script>

<div class="cursor-glow" aria-hidden="true" bind:this={glowEl}></div>

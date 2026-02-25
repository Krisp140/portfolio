<script>
  import Nav from '$lib/components/Nav.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import CursorGlow from '$lib/components/CursorGlow.svelte';
  import { base } from '$app/paths';

  let { children } = $props();
</script>

<svelte:head>
  <link rel="stylesheet" href="{base}/style.css">
</svelte:head>

<CursorGlow />
<Nav />

{@render children()}

<Footer />

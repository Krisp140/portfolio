<script>
  import ProjectCard from '$lib/components/ProjectCard.svelte';
  import { projects } from '$lib/data/projects.js';
</script>

<svelte:head>
  <title>Projects - Kristian Praizner</title>
</svelte:head>

<div class="coord coord--top">002 / Projects</div>
<div class="coord coord--bottom">04 entries</div>

<main>
  <span class="page-label">002 / Selected Work</span>
  <h1>Projects</h1>

  <h2>Selected Work</h2>
  <div class="projects-grid">
    {#each projects as project}
      <ProjectCard {project} />
    {/each}
  </div>
</main>

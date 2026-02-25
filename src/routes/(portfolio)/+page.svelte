<script>
  import { base } from '$app/paths';
  import ProjectCard from '$lib/components/ProjectCard.svelte';
  import ReadingItem from '$lib/components/ReadingItem.svelte';
  import { projects } from '$lib/data/projects.js';
  import { readingList } from '$lib/data/reading-list.js';

  const featuredProjects = projects.filter((p) => p.featured);
</script>

<svelte:head>
  <title>Kristian Praizner - Home</title>
</svelte:head>

<div class="coord coord--top">48.2082&deg; N</div>
<div class="coord coord--bottom">16.3738&deg; E</div>

<main>
  <span class="page-label">001 / Home</span>
  <h1>Kristian<br>Praizner</h1>

  <div class="profile">
    <img src="{base}/images/kristian.JPG" alt="Photo of Kristian Praizner">
    <div class="profile-text">
      <p>
        Hi, I'm Kristian &mdash; a developer interested in building clean, functional
        software. I enjoy working across the stack, from crafting user interfaces
        to designing backend systems.
      </p>
      <p>
        When I'm not coding, you'll find me exploring new technologies, reading,
        or working on side projects. Take a look around to see what I've been
        working on.
      </p>
    </div>
  </div>

  <h2>Featured Projects</h2>
  <div class="home-section-heading">
    <span></span>
    <a href="{base}/projects">View all projects &rarr;</a>
  </div>
  <div class="projects-grid">
    {#each featuredProjects as project}
      <ProjectCard {project} />
    {/each}
  </div>

  <h2>What I'm Reading</h2>
  <div class="reading-list">
    {#each readingList as item}
      <ReadingItem {item} />
    {/each}
  </div>
</main>

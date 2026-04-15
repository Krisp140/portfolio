<script>
  import { base } from '$app/paths';

  let { project } = $props();
  let isExternalLink = $derived(project.link?.startsWith('http'));
  let href = $derived(isExternalLink ? project.link : `${base}${project.link}`);
</script>

<div class="project-card">
  {#if project.link}
    <a
      href={href}
      target={isExternalLink ? '_blank' : undefined}
      rel={isExternalLink ? 'noopener noreferrer' : undefined}
      style="text-decoration:none;color:inherit;display:block;"
    >
      <img src="{project.image.startsWith('/') ? base + project.image : project.image}" alt="{project.title} screenshot" class="project-img">
      <div class="project-body">
        <h3>{project.title}</h3>
        <span class="project-year">{project.year}</span>
        <p>{project.description}</p>
        <div class="project-tags">
          {#each project.tags as tag}
            <span>{tag}</span>
          {/each}
        </div>
      </div>
    </a>
  {:else}
    <img src="{project.image.startsWith('/') ? base + project.image : project.image}" alt="{project.title} screenshot" class="project-img">
    <div class="project-body">
      <h3>{project.title}</h3>
      <span class="project-year">{project.year}</span>
      <p>{project.description}</p>
      <div class="project-tags">
        {#each project.tags as tag}
          <span>{tag}</span>
        {/each}
      </div>
    </div>
  {/if}
</div>

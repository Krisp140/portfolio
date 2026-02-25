<script>
  import { base } from '$app/paths';

  let { project } = $props();
</script>

<div class="project-card">
  {#if project.link}
    <a href="{base}{project.link}" style="text-decoration:none;color:inherit;display:block;">
      <img src="{project.image.startsWith('/') ? base + project.image : project.image}" alt="{project.title} screenshot" class="project-img">
      <div class="project-body">
        <h3>{project.title}</h3>
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
      <p>{project.description}</p>
      <div class="project-tags">
        {#each project.tags as tag}
          <span>{tag}</span>
        {/each}
      </div>
    </div>
  {/if}
</div>

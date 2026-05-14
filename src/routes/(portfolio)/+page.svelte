<script>
  import { base } from '$app/paths';
  import { onMount } from 'svelte';
  import ProjectCard from '$lib/components/ProjectCard.svelte';
  import { projects } from '$lib/data/projects.js';

  const featuredProjects = projects.filter((p) => p.featured);

  let githubData = $state(null);
  let repoStats = $state(null);
  let loading = $state(true);
  let error = $state(null);

  onMount(async () => {
    try {
      const [profileRes, reposRes] = await Promise.all([
        fetch('https://api.github.com/users/krisp140'),
        fetch('https://api.github.com/users/krisp140/repos?per_page=100&sort=updated')
      ]);
      if (!profileRes.ok || !reposRes.ok) {
        throw new Error('GitHub API error');
      }
      githubData = await profileRes.json();
      const repos = await reposRes.json();

      const languages = {};
      let totalStars = 0;
      for (const repo of repos) {
        totalStars += repo.stargazers_count;
        if (repo.language) {
          languages[repo.language] = (languages[repo.language] || 0) + 1;
        }
      }
      const topLanguage = Object.entries(languages)
        .sort((a, b) => b[1] - a[1])[0]?.[0] ?? 'N/A';
      const languageCount = Object.keys(languages).length;
      const accountCreated = new Date(githubData.created_at);
      const yearsActive = Math.floor(
        (Date.now() - accountCreated.getTime()) / (365.25 * 24 * 60 * 60 * 1000)
      );

      repoStats = { totalStars, topLanguage, languageCount, yearsActive };
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  });
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
        When I'm not coding, you'll find me running, reading,
        or working on side projects. Take a look around to see what I've been
        working on.
      </p>
    </div>
  </div>

  <h2>GitHub Stats</h2>
  <div class="github-stats">
    {#if loading}
      <p class="stats-loading">Loading GitHub data&hellip;</p>
    {:else if error}
      <p class="stats-error">Could not load GitHub stats.</p>
    {:else if githubData && repoStats}
      <dl class="stats-grid">
        <div class="stat-item">
          <dt>Repositories</dt>
          <dd>{githubData.public_repos}</dd>
        </div>
        <div class="stat-item">
          <dt>Years on GitHub</dt>
          <dd>{repoStats.yearsActive}</dd>
        </div>
        <div class="stat-item">
          <dt>Languages Used</dt>
          <dd>{repoStats.languageCount}</dd>
        </div>
        <div class="stat-item">
          <dt>Top Language</dt>
          <dd class="stat-text">{repoStats.topLanguage}</dd>
        </div>
      </dl>
    {/if}
  </div>

  <h2>Featured Projects</h2>
  <div class="home-section-heading">
    <span></span>
    <a href="{base}/projects/">View all projects &rarr;</a>
  </div>
  <div class="projects-grid">
    {#each featuredProjects as project}
      <ProjectCard {project} />
    {/each}
  </div>
</main>

<style>
  .github-stats {
    margin-bottom: 2rem;
  }

  .stats-loading,
  .stats-error {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    color: var(--text-faint);
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1.5rem;
    margin: 0;
    padding: 0;
  }

  .stat-item {
    border: 1px solid var(--wire-strong);
    padding: 1.25rem;
    transition: border-color 0.3s, background 0.3s;
  }

  .stat-item:hover {
    border-color: var(--accent);
    background: rgba(255, 61, 0, 0.03);
  }

  .stat-item dt {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 0.5rem;
  }

  .stat-item dd {
    font-family: var(--font-display);
    font-size: 2.5rem;
    color: var(--accent);
    margin: 0;
    line-height: 1;
  }

  .stat-item dd.stat-text {
    font-size: 1.6rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
</style>

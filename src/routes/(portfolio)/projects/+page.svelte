<script>
  import * as d3 from 'd3';
  import ProjectCard from '$lib/components/ProjectCard.svelte';
  import ProjectNarrative from '$lib/components/ProjectNarrative.svelte';
  import ProjectsBar from '$lib/components/ProjectsBar.svelte';
  import { projects } from '$lib/data/projects.js';

  const years = projects.map((p) => p.year);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);
  const yearRange = maxYear - minYear;

  // Count projects per year
  const yearCounts = d3.rollup(projects, v => v.length, d => d.year);
  const chartData = Array.from(yearCounts, ([year, count]) => ({
    label: String(year),
    value: count
  })).sort((a, b) => Number(a.label) - Number(b.label));
</script>

<svelte:head>
  <title>Projects - Kristian Praizner</title>
</svelte:head>

<div class="coord coord--top">002 / Projects</div>
<div class="coord coord--bottom">{projects.length} entries</div>

<main>
  <span class="page-label">002 / Selected Work</span>
  <h1>{projects.length} Projects over {yearRange} Years</h1>

  <p class="projects-intro">
    A chronological journey through my work &mdash; from early JavaScript experiments
    to data-driven visual stories. Scroll through the narrative below to explore
    each project in context, then browse the full grid.
  </p>

  <div class="chart-container">
    <ProjectsBar data={chartData} title="Projects by Year" />
  </div>

  <ProjectNarrative />

  <h2>All Projects</h2>
  <div class="projects-grid">
    {#each projects as project}
      <ProjectCard {project} />
    {/each}
  </div>
</main>

<style>
  .projects-intro {
    font-size: 1.1rem;
    line-height: 1.8;
    max-width: 60ch;
    margin-bottom: 2rem;
  }

  .chart-container {
    margin: 2rem 0 3rem;
  }
</style>

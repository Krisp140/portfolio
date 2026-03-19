<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';
  import ProjectCard from '$lib/components/ProjectCard.svelte';
  import ProjectNarrative from '$lib/components/ProjectNarrative.svelte';
  import { projects } from '$lib/data/projects.js';

  const years = projects.map((p) => p.year);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);
  const yearRange = maxYear - minYear;

  let chartContainer;

  // Count projects per year
  const yearCounts = d3.rollup(projects, v => v.length, d => d.year);
  const chartData = Array.from(yearCounts, ([year, count]) => ({ year, count }))
    .sort((a, b) => a.year - b.year);

  onMount(() => {
    renderChart();
  });

  function renderChart() {
    if (!chartContainer) return;

    const margin = { top: 50, right: 30, bottom: 50, left: 50 };
    const width = 500;
    const height = 320;

    d3.select(chartContainer).selectAll('*').remove();

    const svg = d3.select(chartContainer)
      .append('svg')
      .attr('viewBox', `0 0 ${width + margin.left + margin.right + 180} ${height + margin.top + margin.bottom}`)
      .attr('width', '100%')
      .attr('style', 'max-width: 750px;');

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const colorScale = d3.scaleOrdinal(d3.schemeTableau10)
      .domain(chartData.map(d => d.year));

    const x = d3.scaleBand()
      .domain(chartData.map(d => d.year))
      .range([0, width])
      .padding(0.3);

    const maxCount = d3.max(chartData, d => d.count);
    const y = d3.scaleLinear()
      .domain([0, maxCount])
      .nice()
      .range([height, 0]);

    // X axis
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).tickFormat(d => String(d)))
      .selectAll('text')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem');

    // Y axis with whole numbers only
    g.append('g')
      .call(d3.axisLeft(y).ticks(maxCount).tickFormat(d3.format('d')))
      .selectAll('text')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem');

    g.selectAll('.domain, .tick line').attr('stroke', 'var(--wire-strong)');

    // Bars
    g.selectAll('.bar')
      .data(chartData)
      .join('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.year))
      .attr('y', d => y(d.count))
      .attr('width', x.bandwidth())
      .attr('height', d => height - y(d.count))
      .attr('fill', d => colorScale(d.year));

    // Title
    svg.append('text')
      .attr('x', margin.left + width / 2)
      .attr('y', 22)
      .attr('text-anchor', 'middle')
      .style('fill', 'var(--text)')
      .style('font-family', 'var(--font-display)')
      .style('font-size', '1.3rem')
      .text('Projects by Year');

    // X-axis label
    g.append('text')
      .attr('x', width / 2)
      .attr('y', height + 42)
      .attr('text-anchor', 'middle')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem')
      .text('Year');

    // Y-axis label
    g.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -height / 2)
      .attr('y', -35)
      .attr('text-anchor', 'middle')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem')
      .text('Number of Projects');

    // Legend (side by side with chart)
    const legend = svg.append('g')
      .attr('transform', `translate(${margin.left + width + 30}, ${margin.top + 10})`);

    chartData.forEach((d, i) => {
      const row = legend.append('g')
        .attr('transform', `translate(0, ${i * 24})`);
      row.append('rect')
        .attr('width', 14)
        .attr('height', 14)
        .attr('fill', colorScale(d.year));
      row.append('text')
        .attr('x', 20)
        .attr('y', 11)
        .style('fill', 'var(--text-dim)')
        .style('font-family', 'var(--font-mono)')
        .style('font-size', '0.7rem')
        .text(String(d.year));
    });

    // Annotation: year with most projects
    const maxYearData = chartData.reduce((a, b) => a.count > b.count ? a : b);
    const annotX = x(maxYearData.year) + x.bandwidth() / 2;
    const annotY = y(maxYearData.count);

    // Leader line
    g.append('line')
      .attr('x1', annotX)
      .attr('y1', annotY - 5)
      .attr('x2', annotX + 40)
      .attr('y2', annotY - 35)
      .attr('stroke', 'var(--accent)')
      .attr('stroke-width', 1.5);

    // Annotation text
    g.append('text')
      .attr('x', annotX + 45)
      .attr('y', annotY - 38)
      .style('fill', 'var(--accent)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.7rem')
      .style('font-weight', '500')
      .text(`${maxYearData.year}: ${maxYearData.count} projects`);
  }
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

  <div class="chart-container" bind:this={chartContainer}></div>

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

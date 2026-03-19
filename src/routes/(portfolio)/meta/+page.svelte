<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import * as d3 from 'd3';

  let locContainer;
  let locData = $state([]);

  onMount(async () => {
    const res = await fetch(`${base}/loc.csv`);
    const text = await res.text();
    const rows = d3.csvParseRows(text);

    locData = rows
      .filter(row => row[1] !== 'SUM' && row[1] !== 'language')
      .map(row => ({
        language: row[1],
        code: +row[4]
      }))
      .sort((a, b) => b.code - a.code);

    renderLocChart();
  });

  function renderLocChart() {
    if (!locContainer || locData.length === 0) return;

    const margin = { top: 50, right: 30, bottom: 50, left: 120 };
    const width = 700;
    const barHeight = 36;
    const height = locData.length * barHeight + margin.top + margin.bottom;

    d3.select(locContainer).selectAll('*').remove();

    const svg = d3.select(locContainer)
      .append('svg')
      .attr('viewBox', `0 0 ${width + margin.left + margin.right + 200} ${height}`)
      .attr('width', '100%')
      .attr('style', 'max-width: 900px;');

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const colorScale = d3.scaleOrdinal(d3.schemeTableau10)
      .domain(locData.map(d => d.language));

    const x = d3.scaleLinear()
      .domain([0, d3.max(locData, d => d.code)])
      .nice()
      .range([0, width]);

    const y = d3.scaleBand()
      .domain(locData.map(d => d.language))
      .range([0, height - margin.top - margin.bottom])
      .padding(0.25);

    g.append('g')
      .attr('transform', `translate(0,${height - margin.top - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(6))
      .selectAll('text')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.7rem');

    g.append('g')
      .call(d3.axisLeft(y))
      .selectAll('text')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem');

    g.selectAll('.domain, .tick line').attr('stroke', 'var(--wire-strong)');

    g.selectAll('.bar')
      .data(locData)
      .join('rect')
      .attr('class', 'bar')
      .attr('x', 0)
      .attr('y', d => y(d.language))
      .attr('width', d => x(d.code))
      .attr('height', y.bandwidth())
      .attr('fill', d => colorScale(d.language));

    // Title
    svg.append('text')
      .attr('x', margin.left + width / 2)
      .attr('y', 20)
      .attr('text-anchor', 'middle')
      .style('fill', 'var(--text)')
      .style('font-family', 'var(--font-display)')
      .style('font-size', '1.3rem')
      .text('Lines of Code by Language');

    // X-axis label
    g.append('text')
      .attr('x', width / 2)
      .attr('y', height - margin.top - margin.bottom + 40)
      .attr('text-anchor', 'middle')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem')
      .text('Lines of Code');

    // Y-axis label
    g.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -(height - margin.top - margin.bottom) / 2)
      .attr('y', -100)
      .attr('text-anchor', 'middle')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem')
      .text('Language');

    // Legend
    const legend = svg.append('g')
      .attr('transform', `translate(${margin.left + width + 30}, ${margin.top})`);

    locData.forEach((d, i) => {
      const row = legend.append('g')
        .attr('transform', `translate(0, ${i * 22})`);
      row.append('rect')
        .attr('width', 14)
        .attr('height', 14)
        .attr('fill', colorScale(d.language));
      row.append('text')
        .attr('x', 20)
        .attr('y', 11)
        .style('fill', 'var(--text-dim)')
        .style('font-family', 'var(--font-mono)')
        .style('font-size', '0.7rem')
        .text(d.language);
    });

    // Annotation: language with most LOC
    const maxLang = locData[0];
    const annotX = x(maxLang.code) + 5;
    const annotY = y(maxLang.language) + y.bandwidth() / 2;

    // Leader line
    g.append('line')
      .attr('x1', annotX)
      .attr('y1', annotY)
      .attr('x2', annotX + 40)
      .attr('y2', annotY - 25)
      .attr('stroke', 'var(--accent)')
      .attr('stroke-width', 1.5);

    // Annotation text
    g.append('text')
      .attr('x', annotX + 45)
      .attr('y', annotY - 28)
      .style('fill', 'var(--accent)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.7rem')
      .style('font-weight', '500')
      .text(`${maxLang.language}: ${maxLang.code.toLocaleString()} lines`);
  }
</script>

<svelte:head>
  <title>Meta - Kristian Praizner</title>
</svelte:head>

<div class="coord coord--top">005 / Meta</div>
<div class="coord coord--bottom">site stats</div>

<main>
  <span class="page-label">005 / Meta</span>
  <h1>Site Statistics</h1>

  <p class="meta-intro">
    A look under the hood &mdash; how this portfolio is built, measured in lines of code
    across languages.
  </p>

  <div class="chart-container" bind:this={locContainer}></div>
</main>

<style>
  .meta-intro {
    font-size: 1.1rem;
    line-height: 1.8;
    max-width: 60ch;
    margin-bottom: 2rem;
  }

  .chart-container {
    margin: 2rem 0 3rem;
  }
</style>

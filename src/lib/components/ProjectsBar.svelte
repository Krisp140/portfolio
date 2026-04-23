<script>
  import * as d3 from 'd3';

  export let data = []; // [{ label, value }]
  export let title = 'Projects by Year';

  const width = 500;
  const height = 320;
  const margin = { top: 50, right: 30, bottom: 50, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  let selectedIndex = -1;
  let liveText = '';
  let showChart = true;

  $: xScale = d3.scaleBand()
    .domain(data.map((d) => d.label))
    .range([0, innerWidth])
    .padding(0.3);

  $: maxValue = d3.max(data, (d) => d.value) || 0;

  $: yScale = d3.scaleLinear()
    .domain([0, maxValue])
    .nice()
    .range([innerHeight, 0]);

  $: colorScale = d3.scaleOrdinal()
    .domain(data.map((d) => d.label))
    .range(d3.quantize(d3.interpolateBlues, Math.max(data.length, 2)));

  $: maxYearData = data.length ? data.reduce((a, b) => (a.value > b.value ? a : b)) : null;

  $: description = `A bar chart showing project counts by year. ${data
    .map((d) => `${d.label}: ${d.value} projects`)
    .join(', ')}.`;

  let xAxisEl, yAxisEl;

  $: if (xAxisEl && yAxisEl) {
    d3.select(xAxisEl)
      .call(d3.axisBottom(xScale).tickFormat((d) => String(d)))
      .selectAll('text')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem');

    d3.select(yAxisEl)
      .call(d3.axisLeft(yScale).ticks(maxValue).tickFormat(d3.format('d')))
      .selectAll('text')
      .style('fill', 'var(--text-dim)')
      .style('font-family', 'var(--font-mono)')
      .style('font-size', '0.75rem');

    d3.select(xAxisEl).selectAll('.domain, .tick line').attr('stroke', 'var(--wire-strong)');
    d3.select(yAxisEl).selectAll('.domain, .tick line').attr('stroke', 'var(--wire-strong)');
  }

  function toggleBar(index, event) {
    if (!event || !event.key || event.key === 'Enter' || event.key === ' ') {
      if (event && event.key === ' ') event.preventDefault();
      selectedIndex = selectedIndex === index ? -1 : index;
      if (selectedIndex === -1) {
        liveText = 'Selection cleared.';
      } else {
        const d = data[index];
        liveText = `${d.label}: ${d.value} projects selected.`;
      }
    }
  }

  function toggleView() {
    showChart = !showChart;
    liveText = showChart ? 'Bar chart view shown.' : 'Table view shown.';
  }
</script>

<div class="bar-wrapper">
  <button
    type="button"
    class="toggle-button"
    on:click={toggleView}
    aria-pressed={!showChart}
    aria-label="Toggle between bar chart and table view"
  >
    {showChart ? 'Show Table' : 'Show Chart'}
  </button>

  {#if showChart}
    <div class="container">
      <svg
        viewBox="0 0 {width + 180} {height}"
        role="img"
        aria-labelledby="bar-title bar-desc"
        preserveAspectRatio="xMidYMid meet"
      >
        <title id="bar-title">{title}</title>
        <desc id="bar-desc">{description}</desc>

        <text
          x={margin.left + innerWidth / 2}
          y={22}
          text-anchor="middle"
          class="chart-title"
        >
          {title}
        </text>

        <g transform="translate({margin.left},{margin.top})">
          <g transform="translate(0,{innerHeight})" bind:this={xAxisEl} />
          <g bind:this={yAxisEl} />

          {#each data as d, index (d.label)}
            <rect
              x={xScale(d.label)}
              y={yScale(d.value)}
              width={xScale.bandwidth()}
              height={innerHeight - yScale(d.value)}
              fill={colorScale(d.label)}
              opacity={selectedIndex === -1 || selectedIndex === index ? 1 : 0.45}
              stroke="black"
              stroke-width="1"
              tabindex="0"
              role="button"
              aria-label="{d.label}: {d.value} projects"
              aria-pressed={selectedIndex === index}
              on:click={(e) => toggleBar(index, e)}
              on:keyup={(e) => toggleBar(index, e)}
            />
          {/each}

          <text
            x={innerWidth / 2}
            y={innerHeight + 42}
            text-anchor="middle"
            class="axis-label"
          >
            Year
          </text>

          <text
            transform="rotate(-90)"
            x={-innerHeight / 2}
            y={-35}
            text-anchor="middle"
            class="axis-label"
          >
            Number of Projects
          </text>

          {#if maxYearData}
            {@const annotX = xScale(maxYearData.label) + xScale.bandwidth() / 2}
            {@const annotY = yScale(maxYearData.value)}
            <line
              x1={annotX}
              y1={annotY - 5}
              x2={annotX + 40}
              y2={annotY - 35}
              stroke="var(--accent)"
              stroke-width="1.5"
            />
            <text x={annotX + 45} y={annotY - 38} class="annotation">
              {maxYearData.label}: {maxYearData.value} projects
            </text>
          {/if}
        </g>

        <g transform="translate({margin.left + innerWidth + 30},{margin.top + 10})" aria-hidden="true">
          {#each data as d, i (d.label)}
            <g transform="translate(0,{i * 24})">
              <rect width="14" height="14" fill={colorScale(d.label)} stroke="black" stroke-width="1" />
              <text x="20" y="11" class="legend-label">{d.label}</text>
            </g>
          {/each}
        </g>
      </svg>
    </div>
  {:else}
    <table aria-label="Table showing project counts by year" class="data-table">
      <caption>Projects by Year</caption>
      <thead>
        <tr>
          <th id="year-header" scope="col">Year</th>
          <th id="projects-header" scope="col">Projects</th>
        </tr>
      </thead>
      <tbody>
        {#each data as d, i}
          <tr>
            <th id="row-{i}" scope="row">{d.label}</th>
            <td aria-labelledby="row-{i} projects-header">{d.value}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}

  <p aria-live="polite" class="sr-only">{liveText}</p>
</div>

<style>
  .bar-wrapper {
    margin: 2rem 0 3rem;
  }

  .toggle-button {
    display: inline-block;
    margin-bottom: 1rem;
    padding: 0.5rem 1rem;
    font-family: var(--font-mono, monospace);
    font-size: 0.8rem;
    color: var(--text, #eee);
    background: transparent;
    border: 1px solid var(--wire-strong, #888);
    cursor: pointer;
    transition: 200ms;
  }

  .toggle-button:hover,
  .toggle-button:focus-visible {
    background: var(--accent, #4ea1ff);
    color: #000;
    outline: none;
  }

  .toggle-button:focus-visible {
    outline: 2px dashed var(--accent, #4ea1ff);
    outline-offset: 2px;
  }

  .container {
    max-width: 750px;
  }

  svg {
    width: 100%;
    height: auto;
    overflow: visible;
  }

  rect {
    transition: opacity 300ms, stroke 150ms;
    outline: none;
    cursor: pointer;
  }

  svg:hover rect:not(:hover),
  .container:focus-within rect:not(:focus-visible) {
    opacity: 0.5;
  }

  rect:focus-visible {
    stroke: white;
    stroke-width: 2px;
    stroke-dasharray: 4;
  }

  .chart-title {
    fill: var(--text, #eee);
    font-family: var(--font-display, sans-serif);
    font-size: 1.3rem;
  }

  .axis-label,
  .legend-label {
    fill: var(--text-dim, #aaa);
    font-family: var(--font-mono, monospace);
    font-size: 0.75rem;
  }

  .legend-label {
    font-size: 0.7rem;
  }

  .annotation {
    fill: var(--accent, #4ea1ff);
    font-family: var(--font-mono, monospace);
    font-size: 0.7rem;
    font-weight: 500;
  }

  .data-table {
    margin-top: 1rem;
    margin-bottom: 1rem;
    border-collapse: collapse;
    width: 100%;
    max-width: 30em;
    color: var(--text, #eee);
    font-family: var(--font-mono, monospace);
  }

  .data-table caption {
    font-weight: bold;
    margin-bottom: 0.5em;
    text-align: left;
    color: var(--text, #eee);
    font-family: var(--font-display, sans-serif);
    font-size: 1.1rem;
  }

  .data-table th,
  .data-table td {
    border: 1px solid var(--wire-strong, #888);
    padding: 0.5em 0.75em;
    text-align: left;
  }

  .data-table thead th {
    background: rgba(255, 255, 255, 0.06);
  }

  .sr-only {
    position: absolute;
    left: -9999px;
    width: 1px;
    height: 1px;
    overflow: hidden;
  }
</style>

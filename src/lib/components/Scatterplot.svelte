<script>
  import * as d3 from 'd3';

  export let commits = [];
  export let selectedCommits = [];
  export let clickedCommits = [];
  export let onClickCommit = () => {};
  export let onBrush = () => {};

  const width = 1000;
  const height = 600;
  const margin = { top: 10, right: 10, bottom: 30, left: 20 };

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  let hoveredIndex = -1;
  let svg;
  let brushSelection = null;
  let cursor = { x: 0, y: 0 };

  $: xScale = d3.scaleTime()
    .domain(d3.extent(commits, d => d.datetime))
    .range([usableArea.left, usableArea.right])
    .nice();

  $: yScale = d3.scaleLinear()
    .domain([0, 24])
    .range([usableArea.bottom, usableArea.top]);

  $: rScale = d3.scaleSqrt()
    .domain(d3.extent(commits, d => d.totalLines))
    .range([2, 30]);

  let xAxis, yAxis;

  $: {
    d3.select(xAxis).call(d3.axisBottom(xScale));
    d3.select(yAxis).call(
      d3.axisLeft(yScale)
        .tickFormat(d => String(d % 24).padStart(2, '0') + ':00')
    );
  }

  $: hoveredCommit = hoveredIndex >= 0 ? commits[hoveredIndex] : null;

  function isHovered(commit) {
    return hoveredCommit && commit.id === hoveredCommit.id;
  }

  function brushed(evt) {
    brushSelection = evt.selection;
    if (!brushSelection) {
      onBrush([]);
      return;
    }
    const [[x0, y0], [x1, y1]] = brushSelection;
    const brushed = commits.filter(d => {
      const cx = xScale(d.datetime);
      const cy = yScale(d.hourFrac);
      return cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1;
    });
    onBrush(brushed);
  }

  $: {
    d3.select(svg).call(d3.brush()
      .extent([[usableArea.left, usableArea.top], [usableArea.right, usableArea.bottom]])
      .on("start brush end", brushed));
    d3.select(svg).selectAll(".dots, .overlay ~ *").raise();
  }

  // Sort commits so smaller circles render on top
  $: sortedCommits = [...commits].sort((a, b) => b.totalLines - a.totalLines);
</script>

<svg viewBox="0 0 {width} {height}" bind:this={svg}
  style="overflow: visible; max-width: 100%;"
  on:mousemove={(e) => cursor = { x: e.clientX, y: e.clientY }}
>
  <!-- Axes -->
  <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
  <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

  <!-- Dots -->
  <g class="dots">
    {#each sortedCommits as commit, i (commit.id)}
      <circle
        class:selected={selectedCommits.includes(commit)}
        cx={xScale(commit.datetime)}
        cy={yScale(commit.hourFrac)}
        r={isHovered(commit) ? rScale(commit.totalLines) * 1.3 : rScale(commit.totalLines)}
        fill="steelblue"
        opacity={isHovered(commit) ? 1 : 0.7}
        on:mouseenter={() => {
          hoveredIndex = commits.indexOf(commit);
        }}
        on:mouseleave={() => hoveredIndex = -1}
        on:click={() => onClickCommit(commit)}
      />
    {/each}
  </g>
</svg>

{#if hoveredCommit}
  <dl class="info tooltip" style="position: fixed; left: {cursor.x + 15}px; top: {cursor.y + 15}px;">
    <dt>Commit</dt>
    <dd><a href="https://github.com/kristianpraizner/portfolio/commit/{hoveredCommit.id}">{hoveredCommit.id}</a></dd>
    <dt>Date</dt>
    <dd>{hoveredCommit.datetime.toLocaleString("en", {dateStyle: "full"})}</dd>
    <dt>Time</dt>
    <dd>{hoveredCommit.datetime.toLocaleString("en", {timeStyle: "short"})}</dd>
    <dt>Lines edited</dt>
    <dd>{hoveredCommit.totalLines}</dd>
  </dl>
{/if}

<style>
  svg {
    cursor: crosshair;
  }

  circle {
    transition: r 200ms, opacity 200ms;
    cursor: pointer;
  }

  circle.selected {
    fill: var(--accent, orange);
    opacity: 1;
  }

  .tooltip {
    background: var(--ink);
    border: 1px solid var(--wire-strong);
    border-radius: 6px;
    padding: 0.8em 1em;
    font-family: var(--font-mono, monospace);
    font-size: 0.8rem;
    color: var(--text);
    z-index: 10;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.2em 0.6em;
    margin: 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .tooltip dt {
    font-weight: 600;
    color: var(--text-dim);
  }

  .tooltip dd {
    margin: 0;
  }

  @keyframes marching-ants {
    to {
      stroke-dashoffset: -8;
    }
  }

  svg :global(.selection) {
    fill-opacity: 10%;
    stroke: black;
    stroke-opacity: 70%;
    stroke-dasharray: 5 3;
    animation: marching-ants 2s linear infinite;
  }
</style>

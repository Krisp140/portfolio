<script>
  import * as d3 from 'd3';

  export let data = [];
  export let title = "Lines of Code";

  const width = 1000;
  const height = 300;
  const margin = { top: 10, right: 10, bottom: 30, left: 100 };

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  $: languageCounts = d3.rollups(data, v => v.length, d => d.language)
    .map(([language, count]) => ({ language, count }))
    .sort((a, b) => b.count - a.count);

  $: yScale = d3.scaleBand()
    .domain(languageCounts.map(d => d.language))
    .range([usableArea.top, usableArea.bottom])
    .padding(0.2);

  $: xScale = d3.scaleLinear()
    .domain([0, d3.max(languageCounts, d => d.count) || 0])
    .range([usableArea.left, usableArea.right])
    .nice();

  $: colorScale = d3.scaleOrdinal(d3.schemeTableau10)
    .domain(languageCounts.map(d => d.language));

  let xAxisEl, yAxisEl;

  $: {
    d3.select(xAxisEl).call(d3.axisBottom(xScale).ticks(5));
    d3.select(yAxisEl).call(d3.axisLeft(yScale));
  }
</script>

<h3 style="text-align: center;">{title}</h3>

<svg viewBox="0 0 {width} {height}" style="overflow: visible; max-width: 100%;">
  <g transform="translate(0, {usableArea.bottom})" bind:this={xAxisEl} />
  <g transform="translate({usableArea.left}, 0)" bind:this={yAxisEl} />

  {#each languageCounts as d}
    <rect
      x={usableArea.left}
      y={yScale(d.language)}
      width={xScale(d.count) - usableArea.left}
      height={yScale.bandwidth()}
      fill={colorScale(d.language)}
    />
  {/each}
</svg>

<style>
  h3 {
    font-family: var(--font-display, sans-serif);
    color: var(--text, #eee);
    margin-bottom: 0.5rem;
  }
</style>

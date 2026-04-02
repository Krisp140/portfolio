<script>
  import * as d3 from 'd3';

  export let data = [];

  const width = 1000;
  const height = 300;
  const margin = { top: 20, right: 20, bottom: 40, left: 60 };

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  let hoveredDay = null;

  $: xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date) || [new Date(), new Date()])
    .range([usableArea.left, usableArea.right]);

  $: yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.count) || 0])
    .range([usableArea.bottom, usableArea.top])
    .nice();

  $: line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.count))
    .curve(d3.curveBumpX);

  let xAxisEl, yAxisEl;

  $: {
    d3.select(xAxisEl).call(d3.axisBottom(xScale));
    d3.select(yAxisEl).call(d3.axisLeft(yScale));
  }

  $: dayRegions = (() => {
    if (data.length === 0) return [];
    return data.map((d, i, arr) => {
      const prev = arr[i - 1];
      const next = arr[i + 1];
      const left = prev ? new Date((d.date.getTime() + prev.date.getTime()) / 2) : d.date;
      const right = next ? new Date((d.date.getTime() + next.date.getTime()) / 2) : d.date;
      return {
        date: d.date,
        weekday: d.date.toLocaleString("en", { weekday: "long" }),
        x: xScale(left),
        width: xScale(right) - xScale(left),
      };
    });
  })();

  $: titleText = hoveredDay
    ? `Lines Edited on ${hoveredDay}s`
    : "Lines Edited by Day";
</script>

<h3 style="text-align: center;">{titleText}</h3>

<svg viewBox="0 0 {width} {height}"
  style="overflow: visible; max-width: 100%;"
  on:mouseleave={() => hoveredDay = null}
>
  <!-- Axes -->
  <g transform="translate(0, {usableArea.bottom})" bind:this={xAxisEl} />
  <g transform="translate({usableArea.left}, 0)" bind:this={yAxisEl} />

  <!-- x-axis label -->
  <text
    x={usableArea.left + (usableArea.right - usableArea.left) / 2}
    y={height - 5}
    text-anchor="middle"
    class="axis-label">
    Date
  </text>

  <!-- y-axis label -->
  <text
    x={-(usableArea.top + (usableArea.bottom - usableArea.top) / 2)}
    y={10}
    text-anchor="middle"
    transform="rotate(-90)"
    class="axis-label">
    Number of Lines Edited
  </text>

  <!-- Highlight bands for hovered day -->
  {#each dayRegions as region}
    {#if region.weekday === hoveredDay}
      <rect
        x={region.x}
        y={usableArea.top}
        width={region.width}
        height={usableArea.bottom - usableArea.top}
        fill="var(--accent, orange)"
        opacity="0.15"
      />
    {/if}
  {/each}

  <!-- Invisible hover regions -->
  {#each dayRegions as region}
    <rect
      x={region.x}
      y={usableArea.top}
      width={region.width}
      height={usableArea.bottom - usableArea.top}
      fill="transparent"
      on:mouseenter={() => hoveredDay = region.weekday}
    />
  {/each}

  <!-- Line path -->
  <path
    d={line(data)}
    fill="none"
    stroke="steelblue"
    stroke-width="2"
  />

  <!-- Dots at each data point -->
  {#each data as d}
    {@const isHighlighted = d.date.toLocaleString("en", { weekday: "long" }) === hoveredDay}
    <circle
      cx={xScale(d.date)}
      cy={yScale(d.count)}
      r={isHighlighted ? 5 : 3}
      fill={isHighlighted ? "var(--accent, orange)" : "steelblue"}
    />
    {#if isHighlighted}
      <text
        x={xScale(d.date)}
        y={usableArea.top + 15}
        text-anchor="middle"
        font-size="12"
        fill="var(--accent, orange)"
      >
        {Math.round(d.count)}
      </text>
    {/if}
  {/each}
</svg>

<style>
  h3 {
    font-family: var(--font-display, sans-serif);
    color: var(--text, #eee);
    margin-bottom: 0.5rem;
  }

  .axis-label {
    font-size: 0.8em;
    fill: currentColor;
  }
</style>

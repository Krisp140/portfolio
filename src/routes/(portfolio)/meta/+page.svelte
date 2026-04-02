<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import * as d3 from 'd3';
  import Scatterplot from '$lib/components/Scatterplot.svelte';
  import Bar from '$lib/components/Bar.svelte';
  import LineChart from '$lib/components/LineChart.svelte';

  let locData = [];
  let commits = [];
  let clickedCommits = [];
  let brushedCommits = [];
  let linesByDate = [];

  $: selectedCommits = Array.from(new Set([...clickedCommits, ...brushedCommits]));
  $: selectedLines = (selectedCommits.length > 0 ? selectedCommits : commits).flatMap(d => d.lines);

  $: barTitle = selectedCommits.length > 0
    ? `Lines of Code: ${selectedCommits.length} Selected Commits`
    : `Lines of Code: ${commits.length} Total Commits`;

  $: {
    if (locData.length > 0) {
      // Lines edited by date for the line chart
      const rolled = d3.rollups(locData, v => d3.sum(v, d => d.lines), d => d3.timeDay.floor(d.date))
        .map(([date, count]) => ({ date, count }));

      if (rolled.length > 0) {
        const [minDate, maxDate] = d3.extent(rolled, d => d.date);
        const allDays = d3.timeDays(minDate, d3.timeDay.offset(maxDate, 1));

        linesByDate = allDays.map(date => ({
          date,
          count: rolled.find(r => r.date.getTime() === date.getTime())?.count ?? 0
        }));
      }
    }
  }

  onMount(async () => {
    const res = await fetch(`${base}/commit_data.csv`);
    const text = await res.text();
    const raw = d3.csvParse(text, row => ({
      commit: row.commit,
      date: new Date(row.date),
      file: row.file,
      language: row.language,
      lines: +row.lines,
    }));

    locData = raw;

    // Group by commit to create commit objects
    const grouped = d3.groups(raw, d => d.commit);
    commits = grouped.map(([id, lines]) => {
      const datetime = lines[0].date;
      return {
        id,
        datetime,
        hourFrac: datetime.getHours() + datetime.getMinutes() / 60,
        totalLines: d3.sum(lines, d => d.lines),
        lines,
      };
    }).sort((a, b) => a.datetime - b.datetime);
  });

  function handleClickCommit(commit) {
    const idx = clickedCommits.indexOf(commit);
    if (idx >= 0) {
      clickedCommits = [...clickedCommits.slice(0, idx), ...clickedCommits.slice(idx + 1)];
    } else {
      clickedCommits = [...clickedCommits, commit];
    }
  }

  function handleBrush(brushed) {
    brushedCommits = brushed;
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
    A look under the hood &mdash; how this portfolio is built, measured in commits,
    lines of code, and editing patterns over time.
  </p>

  {#if commits.length > 0}
    <h2>Commits by Time of Day</h2>
    <Scatterplot
      {commits}
      {selectedCommits}
      {clickedCommits}
      onClickCommit={handleClickCommit}
      onBrush={handleBrush}
    />

    <Bar data={selectedLines} title={barTitle} />

    <LineChart data={linesByDate} />
  {:else}
    <p>Loading commit data&hellip;</p>
  {/if}
</main>

<style>
  .meta-intro {
    font-size: 1.1rem;
    line-height: 1.8;
    max-width: 60ch;
    margin-bottom: 2rem;
  }

  h2 {
    margin-top: 2rem;
    margin-bottom: 0.5rem;
  }
</style>

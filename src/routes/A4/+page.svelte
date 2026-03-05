<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';

  onMount(async () => {
    const res = await fetch(`${base}/A4/data.json`);
    const data = await res.json();

    const d3Script = document.createElement('script');
    d3Script.src = 'https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js';
    d3Script.onload = () => {
      renderDumbbell(data.viz1_dumbbell);
      renderScatter(data.all_states);
    };
    document.head.appendChild(d3Script);
  });

  function renderDumbbell(rawData) {
    const d3 = window.d3;
    // Filter: positive gap, exclude DC, top 12
    const data = rawData
      .filter(d => d.state !== 'District of Columbia' && (d.rate_residence - d.rate_occurrence) > 0)
      .slice(0, 12);

    const margin = { top: 40, right: 40, bottom: 50, left: 140 };
    const width = 840;
    const rowH = 38;
    const height = data.length * rowH + margin.top + margin.bottom;

    const container = d3.select('#viz1');
    container.selectAll('*').remove();

    const svg = container.append('svg')
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('width', '100%')
      .style('display', 'block');

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const innerW = width - margin.left - margin.right;
    const innerH = data.length * rowH;

    const maxRate = d3.max(data, d => Math.max(d.rate_occurrence, d.rate_residence)) * 1.15;
    const x = d3.scaleLinear().domain([0, maxRate]).range([0, innerW]);
    const y = d3.scaleBand().domain(data.map(d => d.state)).range([0, innerH]).padding(0.35);

    // Grid lines
    g.selectAll('.grid-line')
      .data(x.ticks(6))
      .join('line')
      .attr('class', 'grid-line')
      .attr('x1', d => x(d)).attr('x2', d => x(d))
      .attr('y1', 0).attr('y2', innerH)
      .attr('stroke', '#2a2a30').attr('stroke-dasharray', '2,3');

    // Connecting bars
    g.selectAll('.connector')
      .data(data)
      .join('rect')
      .attr('x', d => x(Math.min(d.rate_occurrence, d.rate_residence)))
      .attr('y', d => y(d.state) + y.bandwidth() / 2 - 3)
      .attr('width', d => Math.abs(x(d.rate_residence) - x(d.rate_occurrence)))
      .attr('height', 6)
      .attr('fill', 'url(#grad-connector)')
      .attr('rx', 3)
      .attr('opacity', 0.6);

    // Gradient
    const defs = svg.append('defs');
    const grad = defs.append('linearGradient').attr('id', 'grad-connector');
    grad.append('stop').attr('offset', '0%').attr('stop-color', '#555');
    grad.append('stop').attr('offset', '100%').attr('stop-color', '#e74c3c');

    // Occurrence dots (gray, small)
    g.selectAll('.dot-occ')
      .data(data)
      .join('circle')
      .attr('cx', d => x(d.rate_occurrence))
      .attr('cy', d => y(d.state) + y.bandwidth() / 2)
      .attr('r', 5)
      .attr('fill', '#666')
      .attr('stroke', '#888')
      .attr('stroke-width', 1);

    // Residence dots (red, bold)
    g.selectAll('.dot-res')
      .data(data)
      .join('circle')
      .attr('cx', d => x(d.rate_residence))
      .attr('cy', d => y(d.state) + y.bandwidth() / 2)
      .attr('r', 7)
      .attr('fill', '#e74c3c')
      .attr('stroke', '#ff6b6b')
      .attr('stroke-width', 1.5);

    // Travel % labels
    g.selectAll('.travel-label')
      .data(data)
      .join('text')
      .attr('x', d => x(d.rate_residence) + 12)
      .attr('y', d => y(d.state) + y.bandwidth() / 2 + 4)
      .text(d => `${d.pct_travel_out}% left state`)
      .attr('fill', '#e74c3c')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '9px')
      .attr('opacity', 0.8);

    // Y axis
    g.append('g')
      .call(d3.axisLeft(y).tickSize(0))
      .select('.domain').remove();

    g.selectAll('.tick text')
      .attr('fill', '#ccc')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '11px');

    // X axis
    g.append('g')
      .attr('transform', `translate(0,${innerH})`)
      .call(d3.axisBottom(x).ticks(6).tickFormat(d => d))
      .selectAll('text').attr('fill', '#999').attr('font-size', '10px');

    g.select('.domain').attr('stroke', '#444');

    // X label
    g.append('text')
      .attr('x', innerW / 2)
      .attr('y', innerH + 40)
      .attr('text-anchor', 'middle')
      .attr('fill', '#888')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '10px')
      .text('Abortions per 1,000 women aged 15\u201344 (2020)');

    // Legend
    const legend = g.append('g').attr('transform', `translate(${innerW - 240}, -25)`);
    legend.append('circle').attr('cx', 0).attr('cy', 0).attr('r', 5).attr('fill', '#666');
    legend.append('text').attr('x', 10).attr('y', 4).text('In-state rate')
      .attr('fill', '#999').attr('font-size', '10px').attr('font-family', "'JetBrains Mono', monospace");
    legend.append('circle').attr('cx', 120).attr('cy', 0).attr('r', 7).attr('fill', '#e74c3c');
    legend.append('text').attr('x', 132).attr('y', 4).text('Out-of-state rate')
      .attr('fill', '#e74c3c').attr('font-size', '10px').attr('font-family', "'JetBrains Mono', monospace");

    // Missouri annotation
    const mo = data.find(d => d.state === 'Missouri');
    if (mo) {
      const annoG = g.append('g');
      const annoX = x(mo.rate_residence) - 160;
      const annoY = y(mo.state) + y.bandwidth() / 2 - 50;

      annoG.append('rect')
        .attr('x', annoX - 120).attr('y', annoY - 22)
        .attr('width', 260).attr('height', 42)
        .attr('fill', '#1a1a1f').attr('stroke', '#e74c3c')
        .attr('stroke-width', 1).attr('rx', 4);

      annoG.append('text')
        .attr('x', annoX + 10).attr('y', annoY - 4)
        .attr('text-anchor', 'middle')
        .attr('fill', '#e74c3c')
        .attr('font-family', "'JetBrains Mono', monospace")
        .attr('font-size', '9px')
        .attr('font-weight', '600')
        .text('99% traveled out of state');

      annoG.append('text')
        .attr('x', annoX + 10).attr('y', annoY + 12)
        .attr('text-anchor', 'middle')
        .attr('fill', '#aaa')
        .attr('font-family', "'JetBrains Mono', monospace")
        .attr('font-size', '8px')
        .text('170 in-state vs 11,710 by residents');

      // Arrow
      annoG.append('line')
        .attr('x1', annoX + 10).attr('y1', annoY + 20)
        .attr('x2', x(mo.rate_residence)).attr('y2', y(mo.state) + y.bandwidth() / 2 - 8)
        .attr('stroke', '#e74c3c').attr('stroke-width', 1)
        .attr('stroke-dasharray', '3,2');
    }
  }

  function renderScatter(allStates) {
    const d3 = window.d3;

    // Filter: need both fields, exclude DC (extreme outlier that complicates the narrative)
    const data = allStates.filter(d =>
      d.state !== 'District of Columbia' &&
      d.pct_counties_no_clinic !== null &&
      d.rate_residence !== null
    );

    const margin = { top: 30, right: 30, bottom: 60, left: 65 };
    const width = 840;
    const height = 480;
    const innerW = width - margin.left - margin.right;
    const innerH = height - margin.top - margin.bottom;

    const container = d3.select('#viz2');
    container.selectAll('*').remove();

    const svg = container.append('svg')
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('width', '100%')
      .style('display', 'block');

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear().domain([0, 100]).range([0, innerW]);
    const y = d3.scaleLinear().domain([0, 32]).range([innerH, 0]);

    // Grid
    g.selectAll('.grid-h')
      .data(y.ticks(6))
      .join('line')
      .attr('x1', 0).attr('x2', innerW)
      .attr('y1', d => y(d)).attr('y2', d => y(d))
      .attr('stroke', '#2a2a30').attr('stroke-dasharray', '2,3');

    g.selectAll('.grid-v')
      .data(x.ticks(5))
      .join('line')
      .attr('x1', d => x(d)).attr('x2', d => x(d))
      .attr('y1', 0).attr('y2', innerH)
      .attr('stroke', '#2a2a30').attr('stroke-dasharray', '2,3');

    // Linear regression
    const n = data.length;
    const sumX = d3.sum(data, d => d.pct_counties_no_clinic);
    const sumY = d3.sum(data, d => d.rate_residence);
    const sumXY = d3.sum(data, d => d.pct_counties_no_clinic * d.rate_residence);
    const sumX2 = d3.sum(data, d => d.pct_counties_no_clinic ** 2);
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX ** 2);
    const intercept = (sumY - slope * sumX) / n;

    // R²
    const meanY = sumY / n;
    const ssRes = d3.sum(data, d => (d.rate_residence - (slope * d.pct_counties_no_clinic + intercept)) ** 2);
    const ssTot = d3.sum(data, d => (d.rate_residence - meanY) ** 2);
    const r2 = 1 - ssRes / ssTot;

    // Trend line
    const x0 = 0, x1 = 100;
    g.append('line')
      .attr('x1', x(x0)).attr('y1', y(slope * x0 + intercept))
      .attr('x2', x(x1)).attr('y2', y(slope * x1 + intercept))
      .attr('stroke', '#f59e0b')
      .attr('stroke-width', 2)
      .attr('stroke-dasharray', '8,4')
      .attr('opacity', 0.8);

    // Color scale: more restricted (high %) = calming teal, less restricted = alarming red
    const color = d3.scaleLinear()
      .domain([0, 50, 100])
      .range(['#e74c3c', '#888', '#2dd4bf']);

    // Tooltip
    const tooltip = d3.select('#viz2').append('div')
      .style('position', 'absolute')
      .style('pointer-events', 'none')
      .style('background', '#1a1a1f')
      .style('border', '1px solid #555')
      .style('border-radius', '4px')
      .style('padding', '5px 9px')
      .style('font-family', "'JetBrains Mono', monospace")
      .style('font-size', '10px')
      .style('color', '#eee')
      .style('opacity', 0);

    d3.select('#viz2').style('position', 'relative');

    // Dots
    g.selectAll('.dot')
      .data(data)
      .join('circle')
      .attr('cx', d => x(d.pct_counties_no_clinic))
      .attr('cy', d => y(d.rate_residence))
      .attr('r', 6)
      .attr('fill', d => color(d.pct_counties_no_clinic))
      .attr('opacity', 0.75)
      .attr('stroke', d => color(d.pct_counties_no_clinic))
      .attr('stroke-width', 1)
      .style('cursor', 'default')
      .on('mouseenter', function(event, d) {
        d3.select(this).attr('r', 8).attr('opacity', 1).attr('stroke', '#fff').attr('stroke-width', 2);
        tooltip
          .html(`<strong>${d.state}</strong><br>${d.rate_residence} per 1k &middot; ${d.pct_counties_no_clinic}% w/o clinic`)
          .style('opacity', 1);
      })
      .on('mousemove', function(event) {
        const bounds = d3.select('#viz2').node().getBoundingClientRect();
        tooltip
          .style('left', (event.clientX - bounds.left + 12) + 'px')
          .style('top', (event.clientY - bounds.top - 10) + 'px');
      })
      .on('mouseleave', function(event, d) {
        d3.select(this).attr('r', 6).attr('opacity', 0.75).attr('stroke', color(d.pct_counties_no_clinic)).attr('stroke-width', 1);
        tooltip.style('opacity', 0);
      });

    // Label select states for narrative anchoring
    const labelled = [
      'New York', 'New Jersey', 'California', 'Florida',  // high-access, high-rate
      'Wyoming', 'Missouri', 'South Dakota', 'Utah',      // low-access, low-rate
      'Illinois', 'Maryland'                               // high-access outliers
    ];

    const labelData = data.filter(d => labelled.includes(d.state));
    g.selectAll('.label')
      .data(labelData)
      .join('text')
      .attr('x', d => x(d.pct_counties_no_clinic))
      .attr('y', d => y(d.rate_residence) - 10)
      .attr('text-anchor', 'middle')
      .attr('fill', '#ccc')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '8px')
      .text(d => d.state.length > 10 ? d.state.replace(/\s/g, '\u00A0').slice(0, 10) + '.' : d.state);

    // R² annotation box
    const r2X = innerW - 150;
    const r2Y = 10;
    g.append('rect')
      .attr('x', r2X).attr('y', r2Y)
      .attr('width', 140).attr('height', 50)
      .attr('fill', '#1a1a1f').attr('stroke', '#f59e0b')
      .attr('rx', 4).attr('opacity', 0.95);

    g.append('text')
      .attr('x', r2X + 70).attr('y', r2Y + 20)
      .attr('text-anchor', 'middle')
      .attr('fill', '#f59e0b')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '12px')
      .attr('font-weight', '600')
      .text(`R\u00B2 = ${r2.toFixed(2)}`);

    g.append('text')
      .attr('x', r2X + 70).attr('y', r2Y + 38)
      .attr('text-anchor', 'middle')
      .attr('fill', '#aaa')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '9px')
      .text('negative correlation');

    // "More clinics = more abortions" annotation arrow zone
    g.append('text')
      .attr('x', x(15)).attr('y', y(26))
      .attr('fill', '#e74c3c')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '9px')
      .attr('opacity', 0.7)
      .text('\u2190 more clinics, higher rates');

    g.append('text')
      .attr('x', x(72)).attr('y', y(2.5))
      .attr('fill', '#2dd4bf')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '9px')
      .attr('opacity', 0.7)
      .text('fewer clinics, lower rates \u2192');

    // Axes
    g.append('g')
      .attr('transform', `translate(0,${innerH})`)
      .call(d3.axisBottom(x).ticks(5).tickFormat(d => d + '%'))
      .selectAll('text').attr('fill', '#999').attr('font-size', '10px');

    g.append('g')
      .call(d3.axisLeft(y).ticks(6))
      .selectAll('text').attr('fill', '#999').attr('font-size', '10px');

    g.selectAll('.domain').attr('stroke', '#444');

    // Axis labels
    g.append('text')
      .attr('x', innerW / 2).attr('y', innerH + 45)
      .attr('text-anchor', 'middle')
      .attr('fill', '#888')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '10px')
      .text('% of counties without an abortion clinic (2020)');

    g.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -innerH / 2).attr('y', -50)
      .attr('text-anchor', 'middle')
      .attr('fill', '#888')
      .attr('font-family', "'JetBrains Mono', monospace")
      .attr('font-size', '10px')
      .text('Abortions per 1,000 women aged 15\u201344 (by residence, 2020)');
  }
</script>

<svelte:head>
  <title>Persuasive Visualization &middot; Abortion Access &amp; Displacement</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=JetBrains+Mono:wght@300;400;600&display=swap" rel="stylesheet">
</svelte:head>

<div class="a4-page">

<!-- MASTHEAD -->
<div class="masthead">
  <div class="masthead-kicker">A4: Persuasive Visualization &middot; Rhetoric &amp; Framing</div>
  <h1><br>Framing Abortion Access Through Selective Visualization</h1>
  <div class="masthead-meta">
    <span><span class="dot-accent"></span>Guttmacher Institute, 2020</span>
    <span><span class="dot-accent"></span>50 States + DC</span>
    <span><span class="dot-accent"></span>Clinic access, travel, &amp; rates</span>
    <span><span class="dot-accent"></span>Analysis: March 2026</span>
  </div>
</div>

<!-- PROPOSITION -->
<div class="abstract">
  <strong>Proposition:</strong> &ldquo;Restricting abortion clinic access displaces abortions to neighboring states rather than preventing them.&rdquo;
</div>

<!-- VISUALIZATION 1: FOR -->
<h2>Visualization 1 &mdash; For the Proposition</h2>

<div class="figure">
  <div class="figure-label">Figure 1</div>
  <div class="figure-title">Where Clinic Closures Pushed Abortions Across State Lines</div>
  <div class="figure-subtitle">Abortion rates per 1,000 women aged 15&ndash;44, by state of occurrence vs. state of residence (2020)</div>
  <div class="chart-wrap"><div id="viz1"></div></div>
</div>

<!-- VISUALIZATION 2: AGAINST -->
<h2>Visualization 2 &mdash; Against the Proposition</h2>

<div class="figure">
  <div class="figure-label">Figure 2</div>
  <div class="figure-title">Fewer Clinics, Fewer Abortions: States with Limited Access See Significantly Lower Rates</div>
  <div class="figure-subtitle">Abortion rate (by state of residence) vs. percentage of counties without a clinic, all 50 states (2020)</div>
  <div class="chart-wrap"><div id="viz2"></div></div>
</div>

<!-- DESIGN DECISIONS -->
<h2>Design Decisions &amp; Scores</h2>

<h3>Figure 1: Dumbbell Chart (For the Proposition)</h3>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">1. Data filtering: only states with &gt;20% out-of-state travel</span>
    <span class="score deceptive">Score: &minus;2</span>
  </div>
  <p>I filtered the dataset to show only the 12 states where more than 20% of residents traveled out of state for abortion care. This is the most consequential deceptive choice in the visualization: it cherry-picks the states that most dramatically support the displacement narrative while hiding the majority of states where travel is minimal. I considered showing all 50 states on the dumbbell, but the effect was diluted. Most states have small gaps, and the chart became noisy. The filtered version is far more persuasive precisely because it excludes the counterevidence.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">2. Color encoding: red for residence rate, gray for occurrence rate</span>
    <span class="score deceptive">Score: &minus;1</span>
  </div>
  <p>Red is visually dominant and emotionally charged; gray recedes. By encoding the residence rate (the &ldquo;true demand&rdquo; number) in bold red and the occurrence rate (the &ldquo;suppressed&rdquo; number) in muted gray, the chart guides the viewer to see gray as the artificially deflated figure and red as the reality being hidden. An alternative was to use neutral colors for both and let the gap speak for itself, but that weakened the emotional pull. The current encoding essentially tells the viewer which number to trust before they&rsquo;ve formed their own judgment.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">3. Missouri callout annotation</span>
    <span class="score deceptive">Score: &minus;0.5</span>
  </div>
  <p>Missouri is annotated with a callout box reading &ldquo;99% traveled out of state &mdash; 170 in-state vs 11,710 by residents.&rdquo; The data is accurate, and Missouri genuinely is the most extreme case. But by placing it at the top of the chart with a prominent annotation, it becomes the cognitive anchor for interpreting every other state. Viewers unconsciously generalize from the most extreme example. I considered annotating a mid-range state instead, but that undermined the persuasive impact. The score is only &minus;0.5 because the underlying data is truthful; the deception is in emphasis, not fabrication.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">4. Title: &ldquo;Pushed Abortions Across State Lines&rdquo;</span>
    <span class="score deceptive">Score: &minus;1</span>
  </div>
  <p>The title presupposes a causal mechanism: that clinic closures <em>caused</em> the cross-state travel. The chart actually shows a correlation between low clinic access and high out-of-state travel, but the title converts this into a confident causal claim. &ldquo;Pushed&rdquo; implies coercion and agency. I considered more neutral titles like &ldquo;Occurrence vs. Residence Rates in High-Travel States,&rdquo; but the editorial framing is what makes the chart persuasive at first glance &mdash; many viewers read the title and form their conclusion before examining the data.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">5. Dual-metric comparison (occurrence vs. residence rate)</span>
    <span class="score earnest">Score: 1</span>
  </div>
  <p>The core visual encoding is a genuinely informative analytical choice. The occurrence-vs-residence gap is a real and well-documented metric in reproductive health research, and it directly measures displacement. This is the one design decision that is earnest: if you stripped away the cherry-picking, the color framing, and the editorialized title, the underlying comparison would still be analytically sound. It is the honest foundation that the deceptive choices exploit.</p>
</div>

<h3>Figure 2: Scatter Plot (Against the Proposition)</h3>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">1. Showing all 50 states with a regression line and R&sup2;</span>
    <span class="score deceptive">Score: &minus;1</span>
  </div>
  <p>The scatter plot displays every state (except DC), a trend line, and an R&sup2; value. This creates a strong impression of statistical rigor and completeness. The deception is that statistical completeness is not the same as analytical completeness: showing all states on one metric distracts from the fact that the most revealing metric (occurrence vs. residence comparison) is entirely absent. The R&sup2; badge acts as an authority signal that discourages further questioning. I initially tried the chart without R&sup2; and it felt less convincing &mdash; the number gives viewers a reason to stop analyzing.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">2. Using only residence-based abortion rates</span>
    <span class="score deceptive">Score: &minus;2</span>
  </div>
  <p>This is the most important deceptive choice. Residence-based rates count abortions by where the patient lives, not where the procedure occurs, meaning that displaced abortions (e.g., a Missouri resident traveling to Illinois) still count toward Missouri&rsquo;s rate. Despite this, restricted states still show lower rates, which the chart frames as evidence that restrictions &ldquo;work.&rdquo; By hiding the occurrence-vs-residence comparison, the chart suppresses the very evidence that would reveal displacement. I considered showing both metrics as a dual-axis chart, but that would have undermined the persuasive narrative entirely.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">3. Color gradient: teal for restricted states, red for permissive states</span>
    <span class="score deceptive">Score: &minus;1</span>
  </div>
  <p>The color scale maps clinic access to an emotional spectrum: teal for states with few clinics, red for states with many. This subtly frames clinic availability as a problem and restriction as the normative baseline. The effect is strongest because it operates below conscious awareness. Viewers rarely interrogate why a particular color was chosen, but the emotional association shapes their interpretation. A neutral single-color scheme would have been more honest but less persuasive.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">4. Strategic state labeling</span>
    <span class="score deceptive">Score: &minus;0.5</span>
  </div>
  <p>Only ~10 states are labeled, and they are deliberately chosen: high-rate &ldquo;blue&rdquo; states (New York, New Jersey, California) at the top-left and low-rate &ldquo;red&rdquo; states (Wyoming, South Dakota, Utah) at the bottom-right. This anchors viewers on the most politically polarized comparisons and implicitly ties abortion rates to political identity rather than clinic access. The unlabeled middle states fade into the background. I considered labeling all states, but the chart became unreadable and the clean narrative was lost.</p>
</div>

<div class="decision">
  <div class="decision-header">
    <span class="decision-title">5. Title framing correlation as causation</span>
    <span class="score deceptive">Score: &minus;1.5</span>
  </div>
  <p>&ldquo;Fewer Clinics, Fewer Abortions&rdquo; presents a correlation as an implied causal chain. The structure (&ldquo;X, Y&rdquo;) suggests that the first causes the second. In reality, conservative states have both fewer clinics <em>and</em> lower baseline demand for abortion. The causal arrow almost certainly runs from cultural/political attitudes to both variables simultaneously, not from clinic counts to abortion rates. I considered &ldquo;Clinic Access and Abortion Rates Across 50 States&rdquo; but it felt descriptive rather than persuasive. The causal framing is what gives the chart its argumentative force.</p>
</div>

<!-- REFLECTION -->
<h2>Reflection</h2>

<p>The most straightforward part of this exercise was the data work: the Guttmacher dataset is clean, well-structured, and rich enough to support both arguments without any fabrication. What surprised me was how little it took to flip the narrative. The two visualizations use the same source, the same year, and overlapping subsets of the same columns. The only difference is which metric is foregrounded and which is hidden. Figure 1 shows the gap between occurrence and residence rates, revealing displacement. Figure 2 shows only residence rates, concealing it. Neither chart contains a single false data point, yet they lead to opposite conclusions. The most effective persuasive techniques were not visual at all. They were decisions about what <em>not</em> to show.</p>

<p>I now think &ldquo;ethical visualization&rdquo; is less about any individual design choice and more about whether the overall presentation enables or prevents the viewer from reaching an independent conclusion. Color choices, annotations, and even cherry-picking can be acceptable when they serve clarity. The line is crossed when design choices systematically prevent the viewer from noticing what&rsquo;s missing. Figure 1&rsquo;s cherry-picking is deceptive not because filtering data is inherently wrong, but because the filter hides contradictory evidence and the chart offers no signal that it exists. Figure 2&rsquo;s R&sup2; badge is deceptive not because statistics are misleading, but because it weaponizes the viewer&rsquo;s trust in quantitative rigor to shut down further inquiry. The hard boundary I&rsquo;d draw: a persuasive visualization becomes misleading when a reasonably attentive viewer cannot, from the chart alone, identify the strongest counterargument to the claim being made.</p>

<!-- FOOTER -->
<footer>
  Data: Guttmacher Institute, &ldquo;Abortion in the United States: State-Level Estimates,&rdquo; 2020 &middot; Rates per 1,000 women aged 15&ndash;44<br>
  Assignment A4: Persuasive Visualization &middot; Kristian Praizner &middot; March 2026
</footer>

</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  :root {
    --ink: #18181b;
    --paper: #faf9f7;
    --warm: #f5f2ec;
    --rule: #e2ddd6;
    --muted: #8a8278;
    --accent: #b5460f;
    --amber: #d97706;
    --teal: #0e7490;
    --c-bg: #111114;
    --c-surf: #17171c;
    --c-text: #E8E6E1;
    --c-muted: #55555f;
  }

  .a4-page {
    max-width: 880px;
    margin: 0 auto;
    padding: 0 32px 80px;
    background: var(--paper);
    color: var(--ink);
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 17px;
    line-height: 1.75;
    counter-reset: section;
  }

  .a4-page :global(*) { box-sizing: border-box; }

  .masthead {
    border-bottom: 3px solid var(--ink);
    padding: 56px 0 28px;
    margin-bottom: 48px;
  }

  .masthead-kicker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 16px;
  }

  .a4-page h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 5vw, 58px);
    line-height: 1.1;
    font-weight: 700;
    margin-bottom: 16px;
    background: none;
    -webkit-text-fill-color: var(--ink);
    -webkit-background-clip: unset;
    background-clip: unset;
    text-transform: none;
    animation: none;
    letter-spacing: normal;
  }

  .a4-page h1::after { display: none; }

  .a4-page h1 em {
    font-style: italic;
    color: var(--accent);
  }

  .masthead-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.1em;
    border-top: 1px solid var(--rule);
    padding-top: 16px;
    margin-top: 20px;
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
  }

  .masthead-meta span { display: flex; align-items: center; gap: 6px; }
  .dot-accent { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); display: inline-block; }

  .abstract {
    background: var(--warm);
    border-left: 3px solid var(--accent);
    padding: 20px 24px;
    margin-bottom: 48px;
    font-size: 15px;
    color: #3a3632;
    font-style: italic;
  }

  .abstract strong { font-style: normal; }

  .a4-page h2 {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    margin: 56px 0 20px;
    padding-top: 32px;
    border-top: 1px solid var(--rule);
    border-bottom: none;
    counter-increment: section;
    color: var(--ink);
    text-transform: none;
    letter-spacing: normal;
  }

  .a4-page h2::before {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    color: var(--accent);
    text-transform: uppercase;
    display: block;
    margin-bottom: 6px;
    content: "\00A7 " counter(section, decimal-leading-zero);
  }

  .a4-page p {
    margin-bottom: 16px;
    color: #2a2824;
    max-width: none;
  }

  .figure { margin: 32px 0 40px; }

  .figure-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 6px;
  }

  .figure-title {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 2px;
    line-height: 1.3;
  }

  .figure-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    margin-bottom: 4px;
  }

  .chart-wrap {
    background: var(--c-bg);
    border: 1px solid #222;
    margin: 12px 0;
    padding: 8px;
  }

  .figure-caption {
    font-size: 13.5px;
    color: var(--muted);
    line-height: 1.6;
    border-left: 2px solid var(--rule);
    padding-left: 14px;
    margin-top: 10px;
  }

  .figure-caption strong { color: var(--ink); }

  .question-card {
    border: 1px solid var(--rule);
    background: var(--warm);
    padding: 20px 24px;
    margin: 20px 0;
    position: relative;
  }

  .question-card::before {
    content: attr(data-q);
    position: absolute;
    top: -14px; left: 20px;
    background: var(--accent);
    color: white;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    padding: 3px 10px;
    text-transform: uppercase;
  }

  .q-text {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 10px;
    line-height: 1.4;
  }

  .q-motivation {
    font-size: 14px;
    color: var(--muted);
    line-height: 1.6;
  }

  .callout {
    background: #fff8f0;
    border: 1px solid #f5cba7;
    border-left: 3px solid var(--amber);
    padding: 14px 18px;
    margin: 20px 0;
    font-size: 14px;
    line-height: 1.6;
  }

  .callout strong {
    color: var(--amber);
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .a4-page footer {
    border-top: 1px solid var(--rule);
    padding-top: 24px;
    margin-top: 64px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.1em;
    line-height: 2;
    text-align: left;
    text-transform: none;
    border-bottom: none;
  }

  @media (max-width: 640px) {
    .a4-page { padding: 0 16px 60px; }
  }
</style>

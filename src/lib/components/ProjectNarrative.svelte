<script>
  import { base } from '$app/paths';
  import Scrolly from 'svelte-scrolly';
  import { projects } from '$lib/data/projects.js';

  const sorted = [...projects].sort((a, b) => a.year - b.year);
  const progressPerProject = 100 / sorted.length;

  let progress = $state(0);
  let activeProjectIdx = $derived(
    Math.min(
      Math.floor(progress / progressPerProject),
      sorted.length - 1
    )
  );
  let activeProject = $derived(sorted[activeProjectIdx]);
</script>

<section class="narrative">
  <Scrolly bind:progress>
    {#each sorted as project, i}
      <div class="step" class:active={i === activeProjectIdx}>
        <div class="step-marker">
          <span class="step-dot"></span>
          <span class="step-number">{String(i + 1).padStart(2, '0')}</span>
        </div>
        <div class="step-content">
          <span class="step-year">{project.year}</span>
          <h3>{project.title}</h3>
          <p>{project.story}</p>
          <div class="step-tags">
            {#each project.tags as tag}
              <span>{tag}</span>
            {/each}
          </div>
        </div>
      </div>
    {/each}

    <div slot="viz" class="viz-panel">
      <div class="viz-year-badge">{activeProject.year}</div>
      <img
        src={activeProject.image.startsWith('/') ? base + activeProject.image : activeProject.image}
        alt="{activeProject.title} screenshot"
        class="viz-image"
      />
      <div class="viz-caption">
        <span class="viz-index">{String(activeProjectIdx + 1).padStart(2, '0')} / {String(sorted.length).padStart(2, '0')}</span>
        <span class="viz-title">{activeProject.title}</span>
      </div>
      <div class="viz-progress">
        <div class="viz-progress-fill" style="width: {progress}%"></div>
      </div>
    </div>
  </Scrolly>
</section>

<style>
  .narrative {
    margin: 3rem 0;
    --scrolly-viz-top: 18vh;
    --scrolly-gap: 3rem;
  }

  /* ---- Story steps ---- */
  .step {
    min-height: 110vh;
    padding: 2rem 0 2rem 2.5rem;
    margin-bottom: 0;
    opacity: 0.15;
    transition: opacity 0.5s ease;
    display: flex;
    gap: 1.5rem;
    align-items: center;
    position: relative;
  }

  .step.active {
    opacity: 1;
  }

  .step-marker {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    position: absolute;
    left: 0;
  }

  .step-dot {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    border: 2px solid var(--wire-strong);
    background: var(--ink);
    transition: border-color 0.4s, background 0.4s, box-shadow 0.4s;
  }

  .step.active .step-dot {
    border-color: var(--accent);
    background: var(--accent);
    box-shadow: 0 0 12px var(--accent-glow);
  }

  .step-number {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    color: var(--text-faint);
    transition: color 0.4s;
  }

  .step.active .step-number {
    color: var(--accent);
  }

  .step-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    padding-left: 1rem;
    border-left: 1px solid var(--wire-strong);
    transition: border-color 0.4s;
  }

  .step.active .step-content {
    border-left-color: var(--accent);
  }

  .step-year {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
    display: block;
  }

  .step h3 {
    font-family: var(--font-display);
    font-size: 1.6rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    color: var(--text);
  }

  .step p {
    font-size: 0.95rem;
    line-height: 1.85;
    max-width: 38ch;
    color: var(--text-dim);
    margin-bottom: 1rem;
  }

  .step-tags {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }

  .step-tags span {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-faint);
    border: 1px solid var(--wire);
    padding: 0.15rem 0.5rem;
    transition: color 0.3s, border-color 0.3s;
  }

  .step.active .step-tags span {
    color: var(--text-dim);
    border-color: var(--wire-strong);
  }

  /* ---- Viz panel ---- */
  .viz-panel {
    background: var(--ink);
    border: 1px solid var(--wire-strong);
    overflow: hidden;
    position: relative;
  }

  .viz-year-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-family: var(--font-display);
    font-size: 1.4rem;
    letter-spacing: 0.04em;
    color: var(--ink);
    background: var(--accent);
    padding: 0.2rem 0.75rem;
    line-height: 1.2;
    z-index: 2;
  }

  .viz-image {
    width: 100%;
    aspect-ratio: 16 / 10;
    object-fit: cover;
    display: block;
    filter: grayscale(80%) contrast(1.1);
    transition: filter 0.6s ease;
  }

  .viz-panel:hover .viz-image {
    filter: grayscale(0%) contrast(1);
  }

  .viz-caption {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.25rem;
    border-top: 1px solid var(--wire-strong);
  }

  .viz-index {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: var(--text-faint);
  }

  .viz-title {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-dim);
    text-align: right;
  }

  .viz-progress {
    height: 2px;
    background: var(--wire);
  }

  .viz-progress-fill {
    height: 100%;
    background: var(--accent);
    transition: width 0.3s ease-out;
  }

  @media (max-width: 700px) {
    .step {
      min-height: 50vh;
      padding-left: 2rem;
    }

    .step h3 {
      font-size: 1.3rem;
    }

    .viz-year-badge {
      font-size: 1.1rem;
    }

    .narrative {
      --scrolly-viz-top: 10vh;
    }
  }
</style>

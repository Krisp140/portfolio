<script>
  import { base } from '$app/paths';
</script>

<svelte:head>
  <title>Links - Kristian Praizner</title>
</svelte:head>

<div class="coord coord--top">003 / Links</div>
<div class="coord coord--bottom">Site / Resume</div>

<main class="resume-links-page">
  <span class="page-label">003 / Resume</span>
  <h1>Links</h1>

  <section class="resume-link-stack" aria-label="Resume links">
    <a
      class="resume-link-panel resume-link-panel--site"
      href="https://kristianpraizner.com/"
      target="_blank"
      rel="noopener noreferrer"
    >
      <span class="panel-preview" aria-hidden="true">
        <img src="{base}/images/kristian-site.png" alt="" />
      </span>
      <span class="panel-copy">
        <span class="panel-kicker">External Site</span>
        <span class="panel-title">Main Site</span>
      </span>
    </a>

    <a
      class="resume-link-panel resume-link-panel--doc"
      href="{base}/Praizner%20resume%205.2.pdf"
      download
      rel="external"
    >
      <span class="panel-preview" aria-hidden="true">
        <img src="{base}/images/resume.png" alt="" />
      </span>
      <span class="panel-copy">
        <span class="panel-kicker">PDF Download</span>
        <span class="panel-title">Resume</span>
      </span>
    </a>
  </section>
</main>

<style>
  .resume-links-page {
    max-width: 1280px;
    min-height: calc(100vh - 56px);
  }

  .resume-link-stack {
    display: grid;
    gap: clamp(1.25rem, 3vw, 2rem);
    margin-top: 2rem;
  }

  @media (min-width: 900px) {
    .resume-link-stack {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      min-height: clamp(520px, 68vh, 760px);
    }

    .resume-link-panel {
      min-height: 100%;
    }

    .resume-link-panel--site,
    .resume-link-panel--doc {
      justify-content: center;
      text-align: center;
      padding: clamp(2rem, 5vw, 4rem);
    }

    .resume-link-panel--site .panel-preview {
      inset: clamp(1rem, 2vw, 1.5rem);
      width: auto;
      transform: none;
    }

    .resume-link-panel--doc .panel-preview {
      inset: clamp(1rem, 2vw, 1.5rem);
      width: auto;
      transform: none;
    }

    .panel-copy {
      max-width: 100%;
    }
  }

  .resume-link-panel {
    position: relative;
    min-height: clamp(260px, 36vh, 420px);
    display: flex;
    align-items: center;
    overflow: hidden;
    border: 1px solid var(--wire-strong);
    background: rgba(245, 242, 237, 0.025);
    isolation: isolate;
    transition:
      border-color 0.35s ease,
      background 0.35s ease;
  }

  .resume-link-panel:hover {
    border-color: var(--accent);
    background: rgba(255, 87, 34, 0.055);
  }

  .resume-link-panel::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -2;
    background:
      linear-gradient(to right, var(--wire) 1px, transparent 1px),
      linear-gradient(to bottom, var(--wire) 1px, transparent 1px);
    background-size: 44px 44px;
    opacity: 0.55;
    transition: opacity 0.35s ease;
  }

  .resume-link-panel:hover::before {
    opacity: 0;
  }

  .panel-preview {
    position: absolute;
    top: 1rem;
    bottom: 1rem;
    width: min(56vw, 700px);
    border: 1px solid var(--wire-strong);
    background: var(--paper);
    opacity: 0.2;
    filter: grayscale(55%) brightness(1.12) contrast(1);
    transform: none;
    transition:
      opacity 0.35s ease,
      filter 0.35s ease;
  }

  .resume-link-panel:hover .panel-preview {
    opacity: 0.58;
    filter: grayscale(55%) brightness(1.12) contrast(1);
  }

  .resume-link-panel--site {
    justify-content: flex-end;
    text-align: right;
    padding: clamp(2rem, 7vw, 5rem) clamp(1.5rem, 6vw, 4rem);
  }

  .resume-link-panel--site .panel-preview {
    left: 1rem;
  }

  .resume-link-panel--doc {
    justify-content: flex-start;
    padding: clamp(2rem, 7vw, 5rem) clamp(1.5rem, 6vw, 4rem);
  }

  .resume-link-panel--doc .panel-preview {
    right: 1rem;
  }

  .panel-copy {
    position: relative;
    z-index: 1;
    display: grid;
    gap: 0.35rem;
    max-width: min(48vw, 560px);
  }

  .panel-kicker {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
  }

    .panel-title {
      font-family: var(--font-display);
      font-size: clamp(2.75rem, 9vw, 7rem);
      line-height: 0.9;
    letter-spacing: 0.02em;
    text-transform: uppercase;
      color: var(--text);
    }

  .panel-preview img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: contain;
  }

  @media (max-width: 700px) {
    .resume-link-panel,
    .resume-link-panel--site,
    .resume-link-panel--doc {
      justify-content: flex-start;
      text-align: left;
      min-height: 240px;
      padding: 2rem 1.25rem;
    }

    .panel-preview {
      top: 1rem;
      right: 1rem;
      bottom: 1rem;
      left: 1rem;
      width: auto;
    }

    .resume-link-panel--site .panel-preview,
    .resume-link-panel--doc .panel-preview {
      left: 1rem;
      right: 1rem;
    }

    .panel-copy {
      max-width: 100%;
    }
  }
</style>

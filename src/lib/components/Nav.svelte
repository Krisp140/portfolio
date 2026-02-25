<script>
  import { page } from '$app/state';
  import { base } from '$app/paths';
</script>

<nav>
  <ul>
    <li><a href="{base}/" aria-current={page.url.pathname === `${base}/` ? 'page' : undefined}>Home</a></li>
    <li><a href="{base}/projects" aria-current={page.url.pathname === `${base}/projects` ? 'page' : undefined}>Projects</a></li>
    <li><a href="{base}/resume" aria-current={page.url.pathname === `${base}/resume` ? 'page' : undefined}>Resume</a></li>
    <li><a href="{base}/contact" aria-current={page.url.pathname === `${base}/contact` ? 'page' : undefined}>Contact</a></li>
    <li class="nav-github"><a href="https://github.com/krisp140" target="_blank" rel="noopener noreferrer">GitHub</a></li>
  </ul>
  <div class="scroll-progress" aria-hidden="true"></div>
</nav>

<svelte:head>
  <title>Contact - Kristian Praizner</title>
</svelte:head>

<div class="coord coord--top">004 / Contact</div>
<div class="coord coord--bottom">Signal open</div>

<main>
  <span class="page-label">004 / Get In Touch</span>
  <h1>Contact</h1>
  <p>Have a question or want to get in touch? Fill out the form below and I'll get back to you.</p>

  <form action="mailto:krisp@mit.edu" method="GET" enctype="text/plain">
    <div class="form-grid">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required placeholder="your@email.com">

      <label for="subject">Subject</label>
      <input type="text" id="subject" name="subject" required placeholder="What is this about?">

      <label for="message">Message</label>
      <textarea id="message" name="body" required placeholder="Write your message here..."></textarea>
    </div>

    <button type="submit">Send</button>
  </form>
</main>

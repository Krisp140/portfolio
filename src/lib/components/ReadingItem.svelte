<script>
  let { item } = $props();
</script>

<div class="reading-item">
  <img src={item.cover} alt="Cover of {item.title}">
  <div class="reading-info">
    <h3>{item.title}</h3>
    <span class="reading-author">{item.author}</span>
    <p>{item.description}</p>
  </div>
</div>

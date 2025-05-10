<template>
<div class="container">
  <div class="url-container"><span class="url-src-description">{{source_type}}: </span><a class="source-link" :href="url" target="_blank">{{ url }}</a></div>
</div>
</template>

<script lang="ts">
export default {
  name: 'SrcUrlBlock',
  props: {
    url: String,
    source_type: String,
  },
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  padding: 2px 20px;
}

.url-container {
  font-size: 0.75rem;
  background-color: var(--color-block);
  color: rgba(0, 0, 0, 0.5);
  text-wrap: nowrap;
  width: 100%;
  overflow: hidden;
  padding: 6px 12px;
  border-radius: 5px;
  text-overflow: ellipsis;
}

.url-src-description {
  font-weight: bold;
  color: var(--color-text-haze);
  margin-right: 5px;
}

.source-link {
  color: var(--color-text-haze);
  text-decoration: underline;
}

</style>

<script setup lang="ts">
</script>

<template>
  <main>
    <div></div>
    <form>
      <div class="url-input-container">
      <input
      type="url"
      placeholder="Enter URL to an article"
      class="url-input">
      <span class="material-icons paste-icon" @click="pasteUrl">content_paste</span>
      </div>
    </form>
  </main>
</template>

<style scoped>
.url-input-container {
  margin: auto;
  margin-top: 30vh;
  width: 40%;
  min-width: 300px;
  height: 3em;
  border: 2px solid;
  border-color: #545454;
  border-radius: 5px;
  background-color: rgba(212, 217, 228, 0.16);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.url-input {
  width: 90%;
  background-color: transparent;
  border: 0px transparent;
  padding-left: 16px;
  outline: none;
  caret-color: white;
  color: rgba(255,255,255,0.7);
}

.paste-icon {
  position: relative;
  padding: 10px 16px;
  opacity: 50%;
  cursor: pointer;
  user-select: none;
}
</style>

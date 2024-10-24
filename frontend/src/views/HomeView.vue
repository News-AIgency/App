<template>
  <main>
    <form>
      <p class="input-heading">Enter URL below</p>
      <p class="input-subheading">to generate topic ideas</p>
      <div class="url-input-container">
      <input
      type="url"
      placeholder="Enter URL to an article"
      class="url-input">
      <span class="material-icons paste-icon" @click="pasteUrl">content_paste</span>
      </div>
      <button @click.prevent="goToTopics" class="generate-btn">Generate</button>
    </form>
  </main>
</template>

<script lang="ts">
  export default {
    methods: {
      goToTopics() {
        this.$router.push('/topics');
      }
    },
  }
</script>

<style scoped>
.url-input-container {
  margin: auto;
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
form{
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 5em;
}
.generate-btn{
  background-color: var(--color-accent);
  color: var(--color-text);
  border: 0px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 12px;
  padding: 10px;
  margin-top: 40px;
  cursor: pointer;

  transition: box-shadow 0.4s ease;
}
.generate-btn:hover {
  box-shadow: 0 0 8px #9F00FF;
}
.input-heading {
  font-size: 24px;
}
.input-subheading {
  font-size: 16px;
  padding-bottom: 40px;
  opacity: 0.75;
}
</style>

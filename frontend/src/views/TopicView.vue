<template>
  <div class="topic-selection">
    <h2 class="title">Topic Suggestions</h2>

    <form class="topics">
      <button @click.prevent="goToArticle" class="topic-button">
        <span class="topic-num">1</span><p class="topic-label">Topic name #1</p>
        <span class="material-icons forward-arrow">arrow_forward</span>
      </button>

      <button @click.prevent="goToArticle" class="topic-button">
        <span class="topic-num">2</span><p class="topic-label">Topic name #2</p>
        <span class="material-icons forward-arrow">arrow_forward</span>
      </button>

      <button @click.prevent="goToArticle" class="topic-button">
        <span class="topic-num">3</span><p class="topic-label">Topic name #3</p>
        <span class="material-icons forward-arrow">arrow_forward</span>
      </button>
    </form>
  </div>
</template>

<script lang="ts">
export default {
  methods: {
  goToArticle() {
    this.$router.push('/article');
  }
},
}

</script>

<style scoped>
.topic-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 20px;
}

.title {
  color: var(--color-text);
  font-size: 2em;
  font-weight: bold;
  margin-top: 1%;
}

.topics {
  width: 60%;
  max-width: 80%;
  margin-top: 1%;
}

.topic-button {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  position: relative;
  font-size: 16px;
  width: 100%;
  height: 58px;
  margin: 2%;
  border-radius: 5px;
  border: 0px transparent;
  background-color: #38383E;
  color: rgba(255,255,255,1);
}

.topic-button:hover {
  background-color: #9F00FF;
  transition: 0.3s ease;
  cursor: pointer;
  box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)
}

.forward-arrow {
  color: rgba(255, 255, 255, 1);
  font-size: 24px;
  opacity: 0;
  position: absolute;
  right: 2%;
  transition: 0.3s ease;
}

.topic-button:hover .forward-arrow {
  opacity: 1;
}

.topic-num {
  width: auto;
  height: auto;
  padding: 10px 20px;
  color: #fff;
  text-align: center;
  font-weight: bold;
}
</style>

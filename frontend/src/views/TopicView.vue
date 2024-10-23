<template>
  <div class="topic-selection">
    <h2 class="title">Topic Suggestions</h2>

    <form class="topics">
      <button class="topic-button">
        <span class="topic-num">1</span>Topic name #1
        <span class="material-icons forward-arrow">arrow_forward</span>
      </button>

      <button class="topic-button">
        <span class="topic-num">2</span>Topic name #2
        <span class="material-icons forward-arrow">arrow_forward</span>
      </button>
      
      <button class="topic-button">
        <span class="topic-num">3</span>Topic name #3
        <span class="material-icons forward-arrow">arrow_forward</span>
      </button>
    </form>
  </div>
</template>

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
  color: rgba(255,255,255,0.7);
}

.topic-button:hover {
  background-color: #9F00FF;
  transition: 0.3s ease;
  cursor: pointer;
  box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)
}

.forward-arrow {
  color: rgba(255, 255, 255, 0.7);
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
  width: 5%;
  height: 50%;
  text-align: center;
  margin-right: 10%;
  margin-left: 2%;
  color: #fff;
  font-weight: bold;
}
</style>

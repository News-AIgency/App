<template>
  <div class="page-wrapper">
    <div class="textarea-wrapper">
      <h2 class="title">ARTICLE TOPIC</h2>
      <h3>Title</h3>
      <textarea></textarea>

      <h3>Perex</h3>
      <textarea></textarea>

      <h3>Body</h3>
      <textarea></textarea>

      <button class="export-button">Export</button>
    </div>

    <div class="suggestion-wrapper">
      <h3>Title suggestions</h3>
      <button>Title #1</button>
      <button>Title #2</button>
      <button>Title #3</button>
    </div>

  </div>
</template>

<style scoped>
.page-wrapper {
  display: flex;
  justify-content: center;
  flex-direction: row;
}

.suggestion-wrapper {
  display: flex;
  width: 20%;
  flex-direction: column;
}

.textarea-wrapper {
  display: flex;
  width: 60%;
  flex-direction: column;
  margin-right: 5%;
}

.export-button {
  width: 15%;
}

.title {
  font-size: 2em;
  font-weight: bold;
  margin-top: 1%;
}
</style>

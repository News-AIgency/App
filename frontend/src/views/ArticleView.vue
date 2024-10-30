<template>
  <div class="page-wrapper">
    <div class="textarea-wrapper">
      <h2 class="title">{{ selectedTopic }}</h2>
      <div class="textarea-container">
        <div class="header-container">
          <h3>Title</h3>
          <p class="word-counter">Word count: {{ titleWordCount }}</p>
        </div>
        <textarea id="title-textarea" v-model="title"></textarea>
      </div>

      <div class="textarea-container">
        <div class="header-container">
          <h3>Perex</h3>
          <p class="word-counter">Word count: {{ perexWordCount }}</p>
        </div>
        <textarea id="perex-textarea" v-model="perex"></textarea>
      </div>

      <div class="textarea-container">
        <div class="header-container">
          <h3>Body</h3>
          <p class="word-counter">Word count: {{ bodyWordCount }}</p>
        </div>
        <textarea id="body-textarea" v-model="body"></textarea>
      </div>
      <div class="action-bar">
        <button class="export-button" @click="exportText">Export</button>
      </div>
    </div>

    <div class="title-suggestion-wrapper">
      <h2 class="filler"></h2>
      <h3 class="header-container">Title suggestions</h3>
      <button
        v-for="(suggestion, index) in titleSuggestions"
        :key="index"
        class="title-btn"
        @click="copyTitle(suggestion)"
      >
        {{ suggestion }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { useArticleStore } from '@/stores/articleStore'

export default {
  setup() {
    const articleStore = useArticleStore();
    return {articleStore}
  },
  data() {
    return {
      title: '',
      perex: '',
      body: '',
    }
  },
  mounted() {
    this.loadFromLocalStorage()
  },
  computed: {
    titleWordCount(): number {
      return this.countWords(this.title)
    },
    perexWordCount(): number {
      return this.countWords(this.perex)
    },
    bodyWordCount(): number {
      return this.countWords(this.body)
    },
    selectedTopic(): string {
      return this.articleStore.selectedTopic;
    },
    titleSuggestions(): string[] {
      return this.articleStore.titleSuggestions;
    }
  },
  methods: {
    copyTitle(title: string) {
      this.title = title || ''
    },
    loadFromLocalStorage() {
      this.title = localStorage.getItem('title') || '';
      this.perex = localStorage.getItem('perex') || '';
      this.body = localStorage.getItem('body') || '';
      this.articleStore.selectedTopic = localStorage.getItem('selectedTopic') || '';
    },
    exportText() {
      const content = `Title:\n${this.title}\n\nPerex:\n${this.perex}\n\nBody:\n${this.body}`
      const blob = new Blob([content], { type: 'text/plain' })

      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'article.txt'
      a.click()

      URL.revokeObjectURL(url)
    },
    countWords(text: string): number {
      return text
        .trim()
        .split(/\s+/)
        .filter(word => word.length > 0).length
    },
  },
  watch: {
    title(newValue) {
      localStorage.setItem('title', newValue)
    },
    perex(newValue) {
      localStorage.setItem('perex', newValue)
    },
    body(newValue) {
      localStorage.setItem('body', newValue)
    },
  },
}
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}
.page-wrapper {
  margin: auto;
  display: flex;
  width: 95%;
  gap: 0 px;
  justify-content: flex-end;
  flex-direction: row;
  color: var(--color-text);
}

.filler {
  padding: 25.5px;
}

.title-btn {
  background-color: rgba(56, 56, 62, 0.75);
  color: rgba(255, 255, 255, 0.5);
  border: 0px;
  border-radius: 5px;
  padding: 8px;
  text-align: left;
  cursor: pointer;
  margin-bottom: 10px;
}

.title-btn:hover {
  background-color: rgba(76, 76, 83, 0.75);
  color: white;
}

.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.textarea-container textarea {
  width: 100%;
}

.title-suggestion-wrapper {
  display: flex;
  width: 30%;
  flex-direction: column;
}

.textarea-wrapper {
  display: flex;
  width: 50%;
  flex-direction: column;
  margin-right: 2%;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  margin-top: 2px;
}

.word-counter {
  font-size: 12px;
  opacity: 0.5;
}

.export-button {
  width: 15%;
  background-color: var(--color-accent);
  color: var(--color-text);
  border: 0px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 12px;
  padding: 10px;
  cursor: pointer;

  transition: box-shadow 0.4s ease;
}
.export-button:hover {
  box-shadow: 0 0 8px #9f00ff;
}

.title {
  font-size: 2em;
  font-weight: bold;
  text-align: center;
}

textarea {
  background-color: rgba(56, 56, 62, 0.75);
  border-radius: 5px;
  resize: none;
  outline: none;
  caret-color: white;
  padding: 10px;
  color: var(--color-text);
  border: 2px solid rgb(84, 84, 84);
}

h3 {
  font-weight: 600;
}

#perex-textarea {
  height: 6em;
}
#body-textarea {
  height: 25em;
}
</style>

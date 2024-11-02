<template>
  <div class="page-wrapper">
    <div class="textarea-wrapper">
      <h2 class="title">{{ selectedTopic }}</h2>
      <div class="textarea-container">
        <div class="header-container">
          <h3>Title</h3>
          <p class="word-counter">Word count: {{ titleWordCount }}</p>
        </div>
        <div class="textarea-copy-wrapper">
          <span class="material-icons copy-icon" @click="copyText('title-textarea')">content_copy</span>
          <textarea id="title-textarea" v-model="title"  @input="autoResize"></textarea>
        </div>
      </div>

      <div class="textarea-container">
        <div class="header-container">
          <h3>Engaging text</h3>
          <p class="word-counter">Word count: {{ engagingTextWordCount }}</p>
        </div>
        <div class="textarea-copy-wrapper">
          <span class="material-icons copy-icon" @click="copyText('engaging-textarea')">content_copy</span>
          <textarea id="engaging-textarea" v-model="engagingText" @input="autoResize"></textarea>
        </div>
      </div>

      <div class="textarea-container">
        <div class="header-container">
          <h3>Perex</h3>
          <p class="word-counter">Word count: {{ perexWordCount }}</p>
        </div>
        <div class="textarea-copy-wrapper">
          <span class="material-icons copy-icon" @click="copyText('perex-textarea')">content_copy</span>
          <textarea id="perex-textarea" v-model="perex" @input="autoResize"></textarea>
        </div>
      </div>

      <div class="textarea-container">
        <div class="header-container">
          <h3>Body</h3>
          <div class="word-count-time-to-read-wrapper">
            <p class="time-to-read">Time to read: {{ timeToRead }}</p>
            <p class="word-counter">Word count: {{ bodyWordCount }}</p>
          </div>
        </div>
        <div class="textarea-copy-wrapper">
          <span class="material-icons copy-icon" @click="copyText('body-textarea')">content_copy</span>
          <textarea id="body-textarea" v-model="body" @input="autoResize"></textarea>
        </div>
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
      engagingText: '',
    }
  },
  mounted() {
    this.loadFromLocalStorage()
  },
  computed: {
    titleWordCount(): number {
      return this.countWords(this.title);
    },
    perexWordCount(): number {
      return this.countWords(this.perex);
    },
    engagingTextWordCount(): number {
      return this.countWords(this.engagingText);
    },
    bodyWordCount(): number {
      return this.countWords(this.body);
    },
    selectedTopic(): string {
      return this.articleStore.selectedTopic;
    },
    titleSuggestions(): string[] {
      return this.articleStore.titleSuggestions;
    },
    timeToRead(): string {
      return this.calcTimeToRead(this.bodyWordCount);
    },
  },
  methods: {
    copyTitle(title: string) {
      this.title = title || ''
    },
    copyText(textarea_id: string) {
        const text = document.getElementById(textarea_id) as HTMLTextAreaElement | null;
        if (text) {
          text.select();
          navigator.clipboard.writeText(text.value);
        } else {
            console.error("Element with ID ", textarea_id, " not found");
        }
    },
    autoResize(event: Event) {
      const target = event.target as HTMLTextAreaElement;
      target.style.height = 'auto';
      target.style.height = `${target.scrollHeight}px`;
    },
    loadFromLocalStorage() {
      this.title = localStorage.getItem('title') || '';
      this.engagingText = localStorage.getItem('engagingText') || '';
      this.perex = localStorage.getItem('perex') || '';
      this.body = localStorage.getItem('body') || '';
      this.articleStore.selectedTopic = localStorage.getItem('selectedTopic') || '';
    },
    exportText() {
      const content = `Title:\n${this.title}\n\nEngaging text:\n${this.engagingText}\n\nPerex:\n${this.perex}\n\nBody:\n${this.body}`
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
    calcTimeToRead(wordNum: number) {
      const wordsPerMinute = 200;
      const totalSeconds = Math.ceil((wordNum / wordsPerMinute) * 60);

      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;

      return `${minutes} min ${seconds} sec`;
    },
  },
  watch: {
    title(newValue) {
      localStorage.setItem('title', newValue)
    },
    engagingText(newValue) {
      localStorage.setItem('engagingText', newValue)
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
  gap: 0px;
  justify-content: flex-end;
  flex-direction: row;
  color: var(--color-text);
}

.filler {
  padding: 25.5px;
}

.textarea-copy-wrapper {
  position: relative;
}

.textarea {
  padding-right: 10%;
}

.copy-icon {
  position: absolute;
  top: 9px;
  right: 5px;
  padding: 1%;
  opacity: 50%;
  cursor: pointer;
  user-select: none;
  font-size: 20px;
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
  padding-right: 40px;
  box-sizing: border-box;
  overflow: hidden;
  resize: none;
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

.time-to-read {
  font-size: 12px;
  opacity: 0.5;
}

.word-count-time-to-read-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
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
  min-height: 6em;
}
#engaging-textarea {
  height: 6em;
  min-height: 6em;
}
#body-textarea {
  height: 25em;
  min-height: 25em;
}
</style>

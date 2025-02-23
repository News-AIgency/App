<template>
  <main>
    <section class="article-section">
      <ProgressBar :currentStep="currentStep"></ProgressBar>
      <div class="loading-container" v-show="articleStore.loading">
        <LoadingSpinner></LoadingSpinner>
        Generating article...
      </div>

      <div class="intro-box">
        <div class="back-button" v-show="!articleStore.loading">Back to topic selection</div>
        <div class="time-to-read" v-show="!articleStore.loading">Time to read: <span class="bold">{{ timeToRead }}</span></div>
      </div>

      <div class="textarea-container" v-show="!articleStore.loading">
        <div class="topic-box">{{ selectedTopic }}</div>
      </div>
      <div class="textarea-container" v-show="!articleStore.loading">
        <textarea
          class="headline"
          id="title-textarea"
          v-model="title"
          @input="autoResize"
          spellcheck="false"
        >
Slovensko zaznamenalo historicky najvyšší rast obnoviteľných zdrojov energie</textarea
        >
      </div>
      <div class="textarea-container" v-show="!articleStore.loading">
        <ArticleBlock :text="engagingText" type="Engaging Text"></ArticleBlock>
      </div>
      <div class="textarea-container" v-show="!articleStore.loading">
        <ArticleBlock :text="perex" type="Perex"></ArticleBlock>
      </div>
      <div class="textarea-container" v-show="!articleStore.loading">
        <ArticleBlock :text="body" type="Body"></ArticleBlock>
      </div>
      <div class="tags-container" v-show="!articleStore.loading">
          <div class="tags">
            <div v-for="(tag, index) in tags" :key="index">
              {{ tag.toLocaleLowerCase() }}
              <span class="material-icons close-icon" @click="delTag(index)"
                >close</span
              >
            </div>
            <input
              v-if="isAddingTag"
              v-model="newTag"
              id="tag-input"
              class="tag-input"
              @keyup.enter="confirmTag"
              @blur="confirmTag"
              placeholder="Type tag and press Enter"
            />
            <div
              class="material-icons add-icon"
              @click="addTag"
              title="Add tag"
            >
              add
            </div>
          </div>
        </div>
    </section>
    <section class="sidebar-section">
      <div class="buttons-container">
        <button class="btn-primary btn">Publish</button>
        <button class="btn-secondary btn">Share</button>
      </div>
      <div class="suggestions-container">
        <p class="sidebar-label">Headline suggestions</p>
      <button
          v-for="(suggestion, index) in titleSuggestions"
          :key="index"
          class="title-btn"
          @click="copyTitle(suggestion)"
        >
          {{ suggestion }}
        </button></div>
    </section>
  </main>
</template>

<script lang="ts">
import { useArticleStore } from '@/stores/articleStore'
import ProgressBar from '@/components/ProgressBar.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import AiContent from '@/components/AiContent.vue'
import ArticleBlock from '@/components/ArticleBlock.vue';

export default {
  setup() {
    const articleStore = useArticleStore()
    return { articleStore }
  },
  components: {
    ProgressBar,
    LoadingSpinner,
    AiContent,
    ArticleBlock,
  },
  data() {
    return {
      title: '',
      titleSuggestions: [] as string[],
      engagingText: '',
      perex: '',
      body: '',
      tags: [] as string[],
      isAddingTag: false,
      newTag: '',
      originalUrl: '',
      currentStep: 3,
    }
  },
  mounted() {
    this.titleSuggestions = [...this.articleStore.titleSuggestions]
    this.tags = [...this.articleStore.tags]
    this.loadFromLocalStorage()

    const leftBox = document.getElementById('titleBox')
    const rightBox = document.getElementById('fillerBox')

    if (leftBox && rightBox) {
      rightBox.style.padding = `${leftBox.offsetHeight / 2}px`
    }
  },
  updated() {
    const leftBox = document.getElementById('titleBox')
    const rightBox = document.getElementById('fillerBox')

    if (leftBox && rightBox) {
      rightBox.style.padding = `${leftBox.offsetHeight / 2}px`
    }
  },
  computed: {
    titleWordCount(): number {
      return this.countWords(this.title)
    },
    perexWordCount(): number {
      return this.countWords(this.perex)
    },
    engagingTextWordCount(): number {
      return this.countWords(this.engagingText)
    },
    bodyWordCount(): number {
      return this.countWords(this.body)
    },
    selectedTopic(): string {
      return this.articleStore.selectedTopic
    },
    genTitleSuggestions(): string[] {
      return this.articleStore.getTitleSuggestions
    },
    genEngagingText(): string {
      return this.articleStore.getEngagingText
    },
    genPerex(): string {
      return this.articleStore.getPerex
    },
    genBody(): string {
      return this.articleStore.getBody
    },
    genTags(): string[] {
      return this.articleStore.getTags
    },
    timeToRead(): string {
      return this.calcTimeToRead(this.bodyWordCount)
    },
  },
  methods: {
    copyTitle(title: string) {
      this.title = title || ''
    },
    copyText(textarea_id: string) {
      const text = document.getElementById(
        textarea_id,
      ) as HTMLTextAreaElement | null
      if (text) {
        text.select()
        navigator.clipboard.writeText(text.value)
      } else {
        console.error('Element with ID ', textarea_id, ' not found')
      }
    },
    autoResize(event: Event) {
      const target = event.target as HTMLTextAreaElement
      target.style.height = 'auto'
      target.style.height = `${target.scrollHeight}px`
    },
    loadFromLocalStorage() {
      this.title = localStorage.getItem('title') || ''

      if (localStorage.getItem('titleSuggestions') != null) {
        const savedTitleSuggestions = localStorage.getItem('titleSuggestions')
        this.titleSuggestions = savedTitleSuggestions
          ? JSON.parse(savedTitleSuggestions)
          : []
      }
      this.engagingText = localStorage.getItem('engagingText') || ''
      this.perex = localStorage.getItem('perex') || ''
      this.body = localStorage.getItem('body') || ''

      if (localStorage.getItem('tags') != null) {
        const savedTags = localStorage.getItem('tags')
        this.tags = savedTags ? JSON.parse(savedTags) : []
      }
      this.articleStore.selectedTopic =
        localStorage.getItem('selectedTopic') || ''
      this.originalUrl = localStorage.getItem('originalUrl') || ''
    },
    exportText() {
      const tagsText = this.tags.length > 0 ? this.tags.join(', ') : 'No tags'
      const content = `Title:\n${this.title}\n\nEngaging text:\n${this.engagingText}\n\nPerex:\n${this.perex}\n\nBody:\n${this.body}\n\nTags:\n${tagsText}`
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
      const wordsPerMinute = 200
      const totalSeconds = Math.ceil((wordNum / wordsPerMinute) * 60)

      const minutes = Math.floor(totalSeconds / 60)
      const seconds = totalSeconds % 60

      return `${minutes} min ${seconds} sec`
    },
    delTag(index: number) {
      this.articleStore.tags.splice(index, 1)
      this.tags.splice(index, 1)
      this.tags = [...this.tags]
    },
    addTag() {
      this.isAddingTag = true
      this.$nextTick(() => {
        const input = document.getElementById('tag-input')
        input && input.focus()
      })
    },
    confirmTag() {
      if (this.newTag.trim()) {
        let hash_tag = this.newTag.trim()
        if (hash_tag[0] != '#') {
          hash_tag = '#' + hash_tag
        }
        this.articleStore.tags.push(hash_tag)
        this.tags.push(hash_tag)
        this.tags = [...this.tags]
      }
      this.newTag = ''
      this.isAddingTag = false
    },
    regenTitleSuggestions() {},
    regenTitle() {},
    regenEngagingText() {},
    regenPerex() {},
    regenBody() {},
    regenTags() {},
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
    tags(newValue) {
      localStorage.setItem('tags', JSON.stringify(newValue))
    },
    titleSuggestions(newValue) {
      localStorage.setItem('titleSuggestions', JSON.stringify(newValue))
    },
    genEngagingText(newValue) {
      this.engagingText = newValue
    },
    genPerex(newValue) {
      this.perex = newValue
    },
    genBody(newValue) {
      this.body = newValue
    },
    genTags(newValue) {
      this.tags = newValue
    },
    genTitleSuggestions(newValue) {
      this.titleSuggestions = newValue
    },
  },
}
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

main {
  display: flex;
}
.tags-container {
  font-size: 12px;
  width: 75%;
  padding-left: 22px;
  padding-bottom: 20px;
}

.sidebar-label {
  font-size: 14px;
  font-weight: 600;
  padding: 8px 0 0px 8px;
}

.sidebar-section {
  width: 25%;
  height: 100vh;
  border-left: 1px solid var(--color-border);
}

.article-section {
  width: 75%;
  height: 100vh;
  overflow-y: none;
}

.intro-box {
  width: 96%;
  margin: auto;
  display: flex;
  justify-content: space-between;
  padding: 3%;
}

.suggestions-container {
  padding-bottom: 6px;
  border-bottom: 1px solid var(--color-border);
}

/* TEXTAREA */
.textarea-container {
  display: flex;
  flex-direction: column;
  width: 96%;
  margin: auto;
}

textarea {
  background-color: white;
  border-radius: 5px;
  resize: none;
  outline: none;
  caret-color: black;
  padding: 10px 3%;
  color: var(--color-text);
  border: 0;
}

textarea:focus,
textarea:hover {
  background-color: var(--color-block);
}

.headline {
  font-size: 1.75rem;
  font-weight: 900;
}

.topic-box {
  padding: 0px 3%;
  text-transform: uppercase;
  font-weight: 700;
  color: var(--color-text-haze);
}

.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: auto;
  gap: 6px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 12%;
}

.page-wrapper {
  display: flex;
  width: 90%;
  gap: 2%;
  margin: auto;
  flex-direction: row;
  color: var(--color-text);
}

.filler {
  padding: 32px;
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
  width: 90%;
  background-color: var(--color-block);
  color: var(--color-text);
  border: 0px;
  border-radius: 5px;
  padding: 8px;
  text-align: left;
  cursor: pointer;
  margin: 8px 6px 2px 8px;
  font-size: 12px;
}

.title-btn:hover {
  background-color: var(--color-block-hover);
}

.action-bar {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 10px;
  margin-bottom: 80px;
}

.title-suggestion-wrapper {
  display: flex;
  width: 23%;
  flex-direction: column;
}

.m-title-suggestion-wrapper {
  display: none;
}

.title-suggestion-label {
  text-wrap: nowrap;
  overflow: hidden;
}

.regenerate-wrapper {
  border: 0 0 0 20px solid black;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: 8px;
}

.regenerate-button {
  background-color: transparent;
  opacity: 0.75;
  color: var(--color-text);
  border: none;
  font-size: 18px;
  cursor: pointer;
}

.textarea-wrapper {
  display: flex;
  width: 60%;
  flex-direction: column;
}

/* BUTTONS */

.buttons-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  border-bottom: 1px solid var(--color-border);
  padding: 20px 16px;
}

.btn {
  border-radius: 10px;
  cursor: pointer;
}

.btn-primary {
  background-color: var(--color-accent);
  padding: 8px 10px;
  border: none;
  color: var(--color-text-dark-bg);
}

.btn-secondary {
  background-color: transparent;
  padding: 8px 10px;
  border: 1px solid black;
}


.topic-container {
  display: flex;
  justify-content: center;
  width: 75%;
}

#topicBox {
  margin: 10px 0;
  width: 47.5%; /* 0.95 * 50% */
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  margin-bottom: 2px;
}

.word-counter {
  font-size: 12px;
  opacity: 0.5;
}

.time-to-read, .back-button {
  font-size: 12px;
  opacity: 0.5;
}

.tag-input {
  border: none;
  border-radius: 5px;
  padding-left: 1%;
  background-color: rgba(76, 76, 83, 0.75);
  color: white;
  outline: none;
}

.tags {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  white-space: nowrap;
  flex-wrap: wrap;
  gap: 8px 8px;
  margin-top: 1%;
  margin-bottom: 1%;
}

.close-icon {
  font-size: 16px;
  display: inline-flex;
  align-items: center;
  line-height: 1;
  cursor: pointer;
}

.close-icon:hover {
  color: var(--color-accent);
}

.add-icon {
  cursor: pointer;
}

.add-icon:hover {
  color: var(--color-accent);
}

.tags div {
  background-color: var(--color-block);
  color: var(--color-text);
  border: 0px;
  border-radius: 5px;
  padding: 4px 8px;
  text-align: left;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.source-wrapper {
  max-width: 100%;
  overflow: hidden;
  white-space: nowrap;
}

.url {
  display: inline-block;
  max-width: 100%;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  color: inherit;
  background-color: var(--color-block);
  border-radius: 5px;
  padding: 6px 8px;
}

.word-count-time-to-read-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}

.button {
  border: 0px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 12px;
  padding: 10px;
  cursor: pointer;
}

.export-to-external-system {
  background-color: #d9d9d9;
  color: var(--color-text);
}

.export-button {
  background-color: var(--color-accent);
  color: var(--color-text-dark-bg);
  border: 0px;

  transition: box-shadow 0.4s ease;
}

.export-button:hover {
  box-shadow: 0 0 8px var(--color-accent);
}

.title {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin: auto;
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

/* UTILITY */
.bold {
  font-weight: bold;
}

@media (max-width: 480px) {
  .title-suggestion-wrapper {
    display: none;
  }

  .textarea-wrapper {
    width: 98%;
    margin: 0;
  }

  .export-button {
    width: 100%;
    height: 42px;
    margin-bottom: 40px;
  }

  .m-title-suggestion-wrapper {
    display: block;
  }

  #topicBox {
    width: 90%;
    padding-right: 0;
    text-wrap: pretty;
  }
}
</style>

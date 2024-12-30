<template>
  <main>
    <ProgressBar :active-page="3"></ProgressBar>
    <div class="loading-container" v-show="articleStore.loading">
      <LoadingSpinner></LoadingSpinner>
      Generating article...
    </div>

    <!-- TOPIC -->
     <div class="topic-container">
    <h2 id="topicBox" class="title" v-show="!articleStore.loading">
      {{ selectedTopic }}
    </h2>
    </div>


    <div class="page-wrapper">
      <div class="textarea-wrapper">
        <div class="textarea-container" v-show="!articleStore.loading">
          <div class="header-container">
            <h3 class="header-container">Title</h3>
            <p class="word-counter">Word count: {{ titleWordCount }}</p>
          </div>
          <div class="textarea-copy-wrapper">
            <span
              class="material-icons copy-icon"
              @click="copyText('title-textarea')"
              title="Copy text to clipboard"
              >content_copy</span
            >
            <textarea
              id="title-textarea"
              v-model="title"
              @input="autoResize"
            ></textarea>
          </div>
        </div>

        <!-- MOBILE - TITLE SUGGESTION - TEMPORARY -->
        <div class="m-title-suggestion-wrapper" v-show="!articleStore.loading">
          <div class="regenerate-wrapper" v-show="!articleStore.loading">
            <h3 class="header-container" v-show="!articleStore.loading">
              Title suggestions
            </h3>
            <AiContent></AiContent>
            <button
              class="material-icons regenerate-button"
              title="Regenerate"
              @click="regenTitleSuggestions"
            >
              autorenew
            </button>
          </div>

          <button
            v-for="(suggestion, index) in titleSuggestions"
            :key="index"
            class="title-btn"
            @click="copyTitle(suggestion)"
          >
            {{ suggestion }}
          </button>
        </div>

        <div class="textarea-container" v-show="!articleStore.loading">
          <div class="header-container">
            <div class="regenerate-wrapper">
              <h3 class="header-container">Engaging text</h3>

              <button
                class="material-icons regenerate-button"
                title="Regenerate"
                @click="regenEngagingText"
              >
                autorenew
              </button>
            </div>
            <p class="word-counter">Word count: {{ engagingTextWordCount }}</p>
          </div>
          <div class="textarea-copy-wrapper">
            <span
              class="material-icons copy-icon"
              @click="copyText('engaging-textarea')"
              title="Copy text to clipboard"
              >content_copy</span
            >
            <textarea
              id="engaging-textarea"
              v-model="engagingText"
              @input="autoResize"
            ></textarea>
          </div>
        </div>

        <div class="textarea-container" v-show="!articleStore.loading">
          <div class="header-container">
            <div class="regenerate-wrapper">
              <h3 class="header-container">Perex</h3>

              <button
                class="material-icons regenerate-button"
                title="Regenerate"
                @click="regenPerex"
              >
                autorenew
              </button>
            </div>
            <p class="word-counter">Word count: {{ perexWordCount }}</p>
          </div>
          <div class="textarea-copy-wrapper">
            <span
              class="material-icons copy-icon"
              @click="copyText('perex-textarea')"
              title="Copy text to clipboard"
              >content_copy</span
            >
            <textarea
              id="perex-textarea"
              v-model="perex"
              @input="autoResize"
            ></textarea>
          </div>
        </div>

        <div class="textarea-container" v-show="!articleStore.loading">
          <div class="header-container">
            <div class="regenerate-wrapper">
              <h3 class="header-container">Body</h3>

              <button
                class="material-icons regenerate-button"
                title="Regenerate"
                @click="regenBody"
              >
                autorenew
              </button>
            </div>
            <div class="word-count-time-to-read-wrapper">
              <p class="time-to-read">Time to read: {{ timeToRead }}</p>
              <p class="word-counter">Word count: {{ bodyWordCount }}</p>
            </div>
          </div>
          <div class="textarea-copy-wrapper">
            <span
              class="material-icons copy-icon"
              @click="copyText('body-textarea')"
              title="Copy text to clipboard"
              >content_copy</span
            >
            <textarea
              id="body-textarea"
              v-model="body"
              @input="autoResize"
            ></textarea>
          </div>
        </div>

        <div class="tags-container" v-show="!articleStore.loading">
          <div class="regenerate-wrapper">
            <h3 class="header-container">Tags</h3>

            <button
              class="material-icons regenerate-button"
              title="Regenerate"
              @click="regenTags"
            >
              autorenew
            </button>
          </div>
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

        <div class="source-wrapper" v-show="!articleStore.loading">
          <h3 class="header-container">Original Source</h3>
          <a :href="originalUrl" class="url">{{ originalUrl }}</a>
        </div>

        <!-- ACTION BAR -- EXPORT -->
        <div class="action-bar" v-show="!articleStore.loading">
          <button class="export-to-external-system button">
            Export to external system
          </button>
          <button class="export-button button" @click="exportText">
            Export to TXT
          </button>
        </div>
      </div>

      <!-- TITLE SUGGESTION -->
      <div class="title-suggestion-wrapper" v-show="!articleStore.loading">
        <div class="header-container">
          <div class="regenerate-wrapper">
            <h3
              class="header-container title-suggestion-label"
              v-show="!articleStore.loading"
            >
              Title suggestions
            </h3>
            <AiContent></AiContent>
          </div>
          <button
            class="material-icons regenerate-button"
            title="Regenerate"
            @click="regenTitleSuggestions"
          >
            autorenew
          </button>
        </div>

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
  </main>
</template>

<script lang="ts">
import { useArticleStore } from '@/stores/articleStore'
import ProgressBar from '@/components/ProgressBar.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import AiContent from '@/components/AiContent.vue'

export default {
  setup() {
    const articleStore = useArticleStore()
    return { articleStore }
  },
  components: {
    ProgressBar,
    LoadingSpinner,
    AiContent,
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
  width: 75%;
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
  width: 100%;
  background-color: var(--color-block);
  color: var(--color-text);
  border: 0px;
  border-radius: 5px;
  padding: 8px;
  text-align: left;
  cursor: pointer;
  margin-bottom: 10px;
}

.title-btn:hover {
  background-color: rgba(217, 217, 217, 1);
}

.action-bar {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 10px;
  margin-bottom: 80px;
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

.time-to-read {
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
  gap: 10px 10px;
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

button {
  font-weight: 500;
}

.export-to-external-system {
  background-color: #D9D9D9;
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

textarea {
  background-color: var(--color-block);
  border-radius: 5px;
  resize: none;
  outline: none;
  caret-color: black;
  padding: 10px;
  color: var(--color-text);
  border: 0;
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

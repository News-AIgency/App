<template>
  <main>
    <ProgressBar :active-page="3"></ProgressBar>
    <div class="loading-container" v-show="articleStore.loading">
      <LoadingSpinner></LoadingSpinner>
      Generating article...
    </div>
    <div class="page-wrapper">
      <div class="textarea-wrapper">
        <h2 class="title" v-show="!articleStore.loading">
          {{ selectedTopic }}
        </h2>

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

        <div class="action-bar" v-show="!articleStore.loading">
          <button class="export-button" @click="exportText">Export</button>
        </div>
      </div>

      <div class="title-suggestion-wrapper" v-show="!articleStore.loading">
        <h2 class="filler"></h2>
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
        var hash_tag = this.newTag.trim()
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
    genTitleSuggestions(newValue) {
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
  margin-top: 6px;
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
  width: 50%;
  flex-direction: column;
  margin-right: 2%;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  margin-top: 1%;
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
  background-color: rgba(76, 76, 83, 0.75);
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
  background-color: rgba(76, 76, 83, 0.75);
  border-radius: 5px;
  padding: 6px 8px;
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
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin: auto;
  margin-top: 4%;
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

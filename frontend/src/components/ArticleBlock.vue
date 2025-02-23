<template>
  <div class="block-label-container">
    <textarea
      :class="['article-block', type]"
      v-model="internalText"
      @input="autoResize"
      ref="textarea"
    >
    </textarea>
    <div class="block-panel">
      <div class="block-label">{{ type }}</div>
      <div class="block-actions">
        <button class="block-action-btn material-icons regenerate-button" title="Regenerate" @click="regenerateText">autorenew</button>
        <button class="block-action-btn material-icons content_copy" title="Copy"></button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import ArticleService from '@/services/ArticleService';
import { useArticleStore } from '@/stores/articleStore';

export default {
  name: 'ArticleBlock',
  props: {
    text: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      internalText: this.text,
    }
  },
  watch: {
    text(newVal) {
      this.internalText = newVal
      this.$nextTick(() => {
        this.autoResize({ target: this.$refs.textarea })
      })
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.autoResize({ target: this.$refs.textarea })
    })
  },
  methods: {
    autoResize(event: Event) {
      const target = event.target as HTMLTextAreaElement
      target.style.height = 'auto'
      target.style.height = `${target.scrollHeight}px`
    },
    async regenerateText() {
      try {
        const articleStore = useArticleStore()
        let response;

        if (this.type == "Engaging Text") {
          response = await ArticleService.regenerateEngagingText(articleStore.url, articleStore.selectedTopic, this.internalText, articleStore.title);
          this.internalText = response.data.engaging_text;
          console.log("Enganging text regenerated");
        } else if (this.type == "Perex") {
          response = await ArticleService.regeneratePerex(articleStore.url, articleStore.selectedTopic, this.internalText, articleStore.title);
          this.internalText = response.data.perex;
          console.log("Perex regenerated");
        } else if (this.type == "Body") {
          console.log("Body regenration called");
          response = await ArticleService.regenerateBody(articleStore.url, articleStore.selectedTopic, this.internalText, articleStore.title);
          this.internalText = response.data.body;
          console.log("Body regenerated");
        } else {
          console.error("Unknown type of block");
        }

        this.$nextTick(() => {
        this.autoResize({ target: this.$refs.textarea })
      })
      } catch (error) {
        console.error(error)
      }
    },
  },
}
</script>

<style scoped>
.block-label-container {
  color: var(--color-text-haze);
  font-size: 12px;
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  margin-bottom: 10px;
  gap: 4px;
}
.block-panel {
  width: 15%;
  max-height: max-content;
}
.block-label {
  background-color: var(--vt-c-white);
  border-radius: 10px;
  border: 1px solid var(--color-border);
  padding: 2px 6px;
}
.article-block {
  background-color: white;
  border-radius: 5px;
  resize: none;
  outline: none;
  caret-color: black;
  padding: 10px 3%;
  color: var(--color-text);
  border: 0;
  width: 85%;
}

.article-block:focus,
.article-block:hover {
  background-color: var(--color-block);
}
.block-actions {
  display: flex;
  justify-content: start;
  gap: 2px;
}

.block-action-btn {
  background-color: var(--color-block);
  border: 0;
  border-radius: 5px;
  color: var(--color-text-haze);
  cursor: pointer;
  font-size: 0.75rem;
  outline: none;
  padding: 4px;
  margin-top: 2px;
}
</style>

<template>
  <main>
    <ProgressBar :currentStep="currentStep"></ProgressBar>
    <ErrorMessage class="error-message" v-if="topicsStore.error" />
    <div class="topic-selection" v-if="!topicsStore.error">
      <h2 class="title" >Custom topic</h2>
      <div class="custom-topic-container">
        <input
          type="text"
          placeholder="Enter custom topic"
          class="topic-input"
          v-model="customTopic"
        />
        <button
          class="custom-topic-button"
          :disabled="!customTopic.trim()"
          @click.prevent="selectTopic(customTopic)"
        >
          <span class="material-icons">arrow_forward</span>
        </button>
      </div>
      <div class="or-divider">OR</div>

      <div class="ai-gen-content">
        <h2 class="title">Topic Suggestions</h2>
        <AiContent></AiContent>
      </div>

      <form class="topics">
        <button
          v-for="(topic, index) in topics"
          :key="index"
          @click.prevent="selectTopic(topic)"
          class="topic-button"
        >
          <span class="topic-num">{{ index + 1 }}</span>
          <p class="topic-label">{{ topic }}</p>
          <span class="material-icons forward-arrow">arrow_forward</span>
        </button>
        <div class="loading-container" v-show="topicsStore.loading">
          <LoadingSpinner></LoadingSpinner>
          Generating topics...
        </div>

      </form>
    </div>
  </main>
</template>

<script lang="ts">
import { useArticleStore } from '@/stores/articleStore'
import { useTopicsStore } from '../stores/topicsStore'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import AiContent from '@/components/AiContent.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
  setup() {
    const articleStore = useArticleStore()
    const topicsStore = useTopicsStore()
    return { topicsStore, articleStore }
  },
  components: {
    LoadingSpinner,
    ProgressBar,
    AiContent,
    ErrorMessage
  },
  data() {
    return {
      selectedTopic: '',
      customTopic: '',
      currentStep: 2,
    }
  },
  mounted() {
    this.loadFromLocalStorage()
  },
  computed: {
    topics() {
      return this.topicsStore.getTopics
    },
  },
  methods: {
    async selectTopic(topic: string) {
      this.selectedTopic = topic
      const articleStore = useArticleStore()
      articleStore.selectedTopic = topic

      try {
        articleStore.fetchArticle()
        this.$router.push('/article')
      } catch (error) {
        console.error('Failed to fetch article: ', error)
        articleStore.error = true
      }
    },
    loadFromLocalStorage() {
      if (localStorage.getItem('generatedTopics') != null) {
        const topics = localStorage.getItem('generatedTopics')
        this.topicsStore.topics = topics ? JSON.parse(topics) : []
      }
    },
  },
  watch: {
    selectedTopic(newValue) {
      localStorage.setItem('selectedTopic', newValue)
    },
    topics(newValue) {
      localStorage.setItem('generatedTopics', JSON.stringify(newValue))
    },
  },
}
</script>

<style scoped lang="scss">
@media screen and (max-device-width: 480px) {
  .title {
    font-size: 20px !important;
    margin-bottom: 2%;
  }

  .or-divider {
    margin: 10px 0px !important;
  }

  .topics {
    display: flex;
    flex-direction: column;
  }

  .topic-num {
    color: var(--color-text);
    padding: 0 15px 0 15px !important;
  }

  .topics .forward-arrow {
    display: none;
  }
}

.error-message {
  margin: auto;
  padding: 20px;
  text-align: center;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.ai-gen-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

.topic-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 20px;
}

.custom-topic-container {
  width: 60%;
  min-width: 320px;
  display: flex;
  flex-direction: row;
  gap: 10px;
  margin-top: 1%;
}

.custom-topic-button {
  aspect-ratio: 1/1;
  height: 58px;
  background-color: #E8E9E9;
  border: 0px transparent;
  border-radius: 5px;
  color: var(--color-text);
  cursor: pointer;
}

.custom-topic-button:disabled {
  background-color: var(--color-block);
  cursor: not-allowed;
}

.topic-input {
  width: 100%;
  background-color: var(--color-block);
  border: 0px transparent;
  border-radius: 5px;
  padding-left: 16px;
  outline: none;
  caret-color: white;
  color: var(--color-text-haze);
  height: 58px;
}

.or-divider {
  margin: 20px 0px;
  opacity: 0.75;
}

.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: auto;
  gap: 6px;
  color: var(--color-text);
  margin-top: 20px;
}

.title {
  color: var(--color-text);
  font-size: 1.5em;
  font-weight: bold;
}

.topics {
  display: flex;
  flex-direction: column;
  width: 60%;
  max-width: 80%;
  min-width: 320px;
  margin-top: 1%;
  gap: 16px;
}

.topic-button {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  position: relative;
  font-size: 16px;
  width: 100%;
  height: 58px;
  border-radius: 5px;
  border: 0px transparent;
  background-color: var(--color-block);
  color: var(--color-text);
}

.topic-label {
  width: 80%;
  text-align: left;
}

.forward-arrow {
  color: var(--color-text);
  font-size: 24px;
  opacity: 0;
  position: absolute;
  right: 2%;
  transition: 0.3s ease;
}

.topic-num {
  width: auto;
  height: auto;
  padding: 10px 20px;
  color: var(--color-text);
  text-align: center;
  font-weight: bold;
}

@media (hover: hover) {
  .topic-button:hover {
    background-color: var(--color-block-hover);
    transition: 0.3s ease;
    cursor: pointer;
    box-shadow:
      0 2px 2px 0 rgba(0, 0, 0, 0.1),
      0 2px 10px 0 rgba(0, 0, 0, 0.06);

      .forward-arrow {
        opacity: 1;
      }
  }
}

// up to you i guess, ci chces ,aby tam ten arrow svietil na dotykovych obrazovkach
@media (hover: none) {
  .topic-button .forward-arrow {
    opacity: 1;
  }
}
</style>

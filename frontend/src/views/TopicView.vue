<template>
  <main>
    <ProgressBar :active-page="2"></ProgressBar>
    <div class="topic-selection">
      <h2 class="title">Custom topic</h2>
      <div class="custom-topic-container">
        <input type="text" placeholder="Enter custom topic" class="topic-input" v-model="customTopic" />
        <button class="custom-topic-button" :disabled="!customTopic.trim()" @click.prevent="selectTopic(customTopic)">
          <span class="material-icons">arrow_forward</span>
        </button>
      </div>
      <div class="or-divider">OR</div>
      <h2 class="title">Topic Suggestions (AI)</h2>

      <form class="topics">
        <button v-for="(topic, index) in topics" :key="index" @click.prevent="selectTopic(topic)" class="topic-button">
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
import ProgressBar from '@/components/ProgressBar.vue';

export default {
  setup() {
    const articleStore = useArticleStore()
    const topicsStore = useTopicsStore()
    return { topicsStore, articleStore }
  },
  components: {
    LoadingSpinner,
    ProgressBar,
  },
  data() {
    return {
      selectedTopic: '',
      customTopic: '',
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
      console.log("TOPIC: ", topic);
      this.selectedTopic = topic;
      const articleStore = useArticleStore();
      articleStore.selectedTopic = topic;

      try {
        articleStore.fetchArticle();
        this.$router.push('/article');
      } catch (error) {
        console.error("Failed to fetch article: ", error);
      }
    },
    loadFromLocalStorage() {
      if (localStorage.getItem('generatedTopics') != null) {
        const topics = localStorage.getItem('generatedTopics');
        this.topicsStore.topics = topics ? JSON.parse(topics) : [];
      }
    }
  },
  watch: {
    selectedTopic(newValue) {
      localStorage.setItem('selectedTopic', newValue)
    },
    topics(newValue) {
      localStorage.setItem("generatedTopics", JSON.stringify(newValue))
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

.custom-topic-container {
  width: 60%;
  display: flex;
  flex-direction: row;
  gap: 10px;
  margin-top: 1%;
}

.custom-topic-button {
  aspect-ratio: 1/1;
  height: 58px;
  background-color: rgba(212, 217, 228, 0.16);
  border: 0px transparent;
  border-radius: 5px;
  color: var(--color-text);
  cursor: pointer;
}

.custom-topic-button:disabled {
  background-color: rgba(212, 217, 228, 0.2);
  cursor: not-allowed;
}

.topic-input {
  width: 100%;
  background-color: rgba(212, 217, 228, 0.16);
  border: 0px transparent;
  border-radius: 5px;
  padding-left: 16px;
  outline: none;
  caret-color: white;
  color: rgba(255, 255, 255, 0.7);
  height: 58px;
  margin-left: 2%;
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
  color: rgba(255, 255, 255, 0.5);
  margin-top: 20px;
}

.title {
  color: var(--color-text);
  font-size: 2em;
  font-weight: bold;
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
  background-color: #38383e;
  color: rgba(255, 255, 255, 1);
}

.topic-label {
  text-align: left;
}

.topic-button:hover {
  background-color: #9f00ff;
  transition: 0.3s ease;
  cursor: pointer;
  box-shadow:
    0 6px 10px 0 rgba(0, 0, 0, 0.2),
    0 6px 20px 0 rgba(0, 0, 0, 0.19);
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

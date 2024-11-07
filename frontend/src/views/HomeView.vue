<template>
  <main>
    <ProgressBar :active-page="TEST"></ProgressBar>
    <form>
      <p class="input-heading">Enter URL below</p>
      <p class="input-subheading">to generate topic ideas</p>
      <div class="url-input-container">
        <input type="url" placeholder="Enter URL to an article" class="url-input" v-model="inputURL">
        <span class="material-icons paste-icon" @click="pasteUrl">content_paste</span>
      </div>
      <div class="error-container">{{ error_text }}</div>
      <button @click.prevent="sendURL" class="generate-btn">Generate</button>
    </form>
  </main>
</template>

<script lang="ts">
import { useTopicsStore } from '@/stores/topicsStore'
import { useArticleStore } from '@/stores/articleStore';
import ProgressBar from '../components/ProgressBar.vue'

export default {
  name: "HomeView",
  data() {
    return {
      inputURL: "",
      TEST: 1,
      error_text: "",
    };
  },
  components: {
    ProgressBar,
  },
  mounted() {
    localStorage.clear();
  },
  methods: {
    isValidUrl(string: string) {
      if (string.length == 0) {
        this.error_text = "URL field cannot be empty"
        return false;
      }
      try {
        new URL(string);
        return true;
      } catch (error) {
        console.error('Invalid URL: ', error);
        this.error_text = "Invalid URL format";
        return false;
      }
    },

    async sendURL() {
      try {
        if (!this.isValidUrl(this.inputURL)) {
          console.error("Invalid URL");
          return
        }
        this.goToTopics(this.inputURL);
      } catch (error) {
        console.error('Error at sendURL: ', error);
      }
    },

    async goToTopics(url: string) {
      const topicsStore = useTopicsStore();
      const articleStore = useArticleStore();
      articleStore.url = url;
      localStorage.setItem('originalUrl', url);

      try {
        topicsStore.fetchTopics(this.inputURL);
        this.$router.push('/topics');
      } catch (error) {
        console.error("Failed to fetch topics: ", error);
      }
    },

    async pasteUrl() {
      const text = await navigator.clipboard.readText();
      this.inputURL += text;
    },
  },
}
</script>

<style scoped>
.url-input-container {
  margin: auto;
  width: 40%;
  max-width: 700px;
  min-width: 300px;
  height: 3em;
  border: 2px solid;
  border-color: #545454;
  border-radius: 5px;
  background-color: rgba(212, 217, 228, 0.16);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.url-input {
  width: 90%;
  background-color: transparent;
  border: 0px transparent;
  padding-left: 16px;
  outline: none;
  caret-color: white;
  color: rgba(255, 255, 255, 0.7);
}

.error-container {
  margin-top: 12px;
  display: block;
  height: 12px;
  line-height: 10px;
  overflow: hidden;
  color: var(--color-error);
  font-size: 12px;
}

.paste-icon {
  position: relative;
  padding: 10px 16px;
  opacity: 50%;
  cursor: pointer;
  user-select: none;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2em;
}

.generate-btn {
  background-color: var(--color-accent);
  color: var(--color-text);
  border: 0px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 12px;
  padding: 10px;
  margin-top: 24px;
  cursor: pointer;

  transition: box-shadow 0.4s ease;
}

.generate-btn:hover {
  box-shadow: 0 0 8px #9F00FF;
}

.input-heading {
  font-size: 24px;
}

.input-subheading {
  font-size: 16px;
  padding-bottom: 40px;
  opacity: 0.75;
}
</style>

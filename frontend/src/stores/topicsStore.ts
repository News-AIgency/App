import {defineStore} from 'pinia';
import axios from 'axios';

export const useTopicsStore = defineStore('topics', {
  state: () => ({
    topics: ["Topic1", "Topic2"] as string[],
  }),
  getters: {
    getTopics(): string[] {
      return this.topics
    }
  },
  actions: {
    async fetchTopics(url: string) {
      try {

        const response = await axios.post('http://localhost:8000/article/topics', {url: url});
        this.topics = response.data.topics;

      } catch (error) {
        console.error(error)
      }
    }
  }
});

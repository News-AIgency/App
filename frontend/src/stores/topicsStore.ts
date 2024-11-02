import {defineStore} from 'pinia';
// import axios from 'axios';

import TopicsService from '@/services/TopicsService'

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
    async fetchTopics() {
      try {

        // const response = await axios.post('http://localhost:8000/article/topics', {url: url});
        this.topics = (await TopicsService.topics()).data.topics

      } catch (error) {
        console.error(error)
      }
    }
  }
});

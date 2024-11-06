import {defineStore} from 'pinia';
// import axios from 'axios';

import TopicsService from '@/services/TopicsService'

export const useTopicsStore = defineStore('topics', {
  state: () => ({
    topics: [],
    loading: false,
  }),
  getters: {
    getTopics(): string[] {
      return this.topics
    }
  },
  actions: {
    async fetchTopics(url: string) {
      try {

        // const response = await axios.post('http://localhost:8000/article/topics', {url: url});
        this.loading = true;
        this.topics = (await TopicsService.topics(url)).data.topics

      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false;
      }
    }
  }
});

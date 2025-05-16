import {defineStore} from 'pinia';
// import axios from 'axios';

import TopicsService from '@/services/TopicsService'

export const useTopicsStore = defineStore('topics', {
  state: () => ({
    topics: [],
    loading: false,
    error: false,
  }),
  getters: {
    getTopics(): string[] {
      return this.topics
    }
  },
  actions: {
    async fetchTopics(url: string) {
      try {
        this.loading = true;
        const response = await TopicsService.topics(url);
        this.topics = response.data.topics;
        this.error = false;
      } catch (error) {
        this.error = true;
        console.error("Topics error:", error);
      } finally {
        this.loading = false;
      }
    }
  }
});

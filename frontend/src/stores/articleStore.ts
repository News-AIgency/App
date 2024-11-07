import { defineStore } from 'pinia';
import ArticleService from '@/services/ArticleService';

export const useArticleStore = defineStore('article', {
  state: () => ({
    selectedTopic: "" as string,
    title: "" as string,
    titleSuggestions: [] as string[],
    engagingText: "" as string,
    tags: [] as string[],
    perex: "" as string,
    body: "" as string,
    url: "" as string,
    loading: false,
  }),
  getters: {
    getTitleSuggestions(): string[] {
      return this.titleSuggestions;
    },
    getEngagingText(): string {
      return this.engagingText;
    },
    getPerex(): string {
      return this.perex;
    },
    getBody(): string {
      return this.body;
    },
    getTags(): string[] {
      return this.tags;
    }
  },
  actions: {
    async fetchArticle() {
      try {
        this.loading = true;
        const response = await ArticleService.article(this.url, this.selectedTopic)
        this.titleSuggestions = response.data.headlines;
        this.engagingText = response.data.engaging_text;
        this.perex = response.data.perex;
        this.body = response.data.article;
        this.tags = response.data.tags;

      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false;
      }
    }
  }
});

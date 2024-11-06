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
    url: "" as string
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
        const response = await ArticleService.article(this.url, this.selectedTopic)
        this.titleSuggestions = response.data.headlines;
        this.engagingText = response.data.engaging_text;
        this.perex = response.data.perex;
        this.body = response.data.article;
        this.tags = response.data.tags;

      } catch (error) {
        console.error(error)
      }
    }
  }
});

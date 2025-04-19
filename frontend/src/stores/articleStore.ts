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
    articleId: 0,
    loading: false,
  }),
  getters: {
    getTitleSuggestions(): string[] {
      return this.titleSuggestions;
    },
    getTitle(): string {
      return this.title;
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
        this.titleSuggestions = response.data.article.headlines;
        this.title = response.data.article.headlines[0];
        this.engagingText = response.data.article.engaging_text;
        this.perex = response.data.article.perex;
        this.body = response.data.article.article;
        this.tags = response.data.article.tags;
        this.articleId = response.data.id;
        
        //TEST CI DOBRE RETURNUJEM DATA OHLADOM GRAFU NA FE
        console.log("Graph Metadata:");
        console.log("  gen_graph:", response.data.article.gen_graph);
        console.log("  graph_type:", response.data.article.graph_type);
        console.log("  graph_data:", response.data.article.graph_data);
        
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false;
      }
    }
  }
});

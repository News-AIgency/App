import {defineStore} from 'pinia';
import axios from 'axios';

export const useArticleStore = defineStore ('article', {
  state: () => ({
    selectedTopic: "" as string,
    title: "" as string,
    titleSuggestions: ["Priemerné ceny pohonných látok v SR vzrástli o 2 centy za liter", "Ceny benzínov a nafty zaznamenali najvyššiu hodnotu od septembra", "Spotrebitelia platili za motorovú naftu v priemere 1,420 eura za liter"] as string[],
    perex: "" as string,
    body: "" as string,
    url: "" as string
  }),
  actions: {
    async fetchArticle(url: string, topic: string) {
      try {
        const response = await axios.post('Link na article generate endpoint', {url: url, topic: topic});

        this.title = response.data.title;
        this.perex = response.data.perex;
        this.body = response.data.body;
        this.url = url;

      } catch (error) {
        console.error(error)
      }
    }
  }
});

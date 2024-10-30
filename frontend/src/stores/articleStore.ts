import {defineStore} from 'pinia';

export const useArticleStore = defineStore ('article', {
  state: () => ({
    selectedTopic: "" as string,
    title: "" as string,
    titleSuggestions: [] as string[],
    perex: "" as string,
    body: "" as string,
    url: "" as string
  }),
});

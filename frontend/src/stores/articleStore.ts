import {defineStore} from 'pinia';

export const useArticleStore = defineStore ('article', {
  state: () => ({
    selectedTopic: "" as string,
    title: "" as string,
    titleSuggestions: ["Priemerné ceny pohonných látok v SR vzrástli o 2 centy za liter", "Ceny benzínov a nafty zaznamenali najvyššiu hodnotu od septembra", "Spotrebitelia platili za motorovú naftu v priemere 1,420 eura za liter"] as string[],
    perex: "" as string,
    body: "" as string,
    url: "" as string
  }),
});

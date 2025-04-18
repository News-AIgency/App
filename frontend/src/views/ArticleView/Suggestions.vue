<template>
    <div class="suggestions-container">
        <div class="suggestions-label-container"><p class="sidebar-label">Headline suggestions</p><button class=" material-icons regenerate-button" title="Regenerate" @click="regenerateSuggestions">autorenew</button></div>
        <button
            v-for="(suggestion, index) in titleSuggestions"
            :key="index"
            class="title-btn"
            @click="copyTitle(suggestion)"
            >
            {{ suggestion }}
        </button>
    </div>
</template>


<script lang="ts">
import type { PropType } from 'vue';

export default {
    name: 'Suggestions',
    props: {
        regenerateSuggestions: {
            type: Function as PropType<() => Promise<void>>,
            required: true
        },
        copyTitle: {
            type: Function as PropType<(title: string) => void>,
            required: true
        },
        titleSuggestions: {
            type: Array as PropType<string[]>,
            required: true
        }
    }

}
</script>


<style lang="scss" scoped>
.suggestions-container {
  padding: 0 .25rem 6px;
  border-bottom: 1px solid var(--color-border);
}

.suggestions-label-container {
  display: flex;
  justify-content: start;
  align-items: center;
  padding: 8px 0 0px 8px;
  gap: 8px
}

.title-btn {
  background-color: var(--color-block);
  color: var(--color-text);
  border: 0px;
  border-radius: 5px;
  padding: 8px;
  text-align: left;
  cursor: pointer;
  margin: 8px 6px 2px 8px;
  font-size: 12px;

  &:hover {
    background-color: var(--color-block-hover);
  }
}

.regenerate-button {
  background-color: transparent;
  opacity: 0.75;
  color: var(--color-text);
  border: none;
  font-size: 18px;
  cursor: pointer;
}
</style>
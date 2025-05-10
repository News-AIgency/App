<template>
  <div class="toggle-switch">
    <label class="switch">
      <input type="checkbox" v-model="articleStore.stormEnabled"/>
      <span class="slider round"></span>
    </label>
    <div class="label-container">
      <span class="label">STORM</span
      ><span class="material-icons icon-info"
        >info</span>
      <div class="tooltip">Enable STORM to search for similar articles to improve the result.</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useArticleStore } from '@/stores/articleStore'

export default defineComponent({
  name: 'ToggleSwitch',
  setup() {
    const articleStore = useArticleStore()

    return {
      articleStore,
    }
  },
})
</script>

<style scoped>
.toggle-switch {
  margin-top: 4px;
  display: flex;
}
.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: -2px;
  bottom: 0;
  background-color: var(--color-block);
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: '';
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: rgb(209, 213, 228);
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.label-container {
  display: inline-flex;
  flex-direction: row;
  align-items: center;
  margin-left: 8px;

}

.label {
  color: var(--color-text);
  opacity: 0.5;
  font-size: 12px;
}

.icon-info {
  display: inline-block;
  font-size: 12px;
  position: relative;
  opacity: 0.5;
  cursor: default;
  padding: 4px;
}

.tooltip {
  position: absolute;
  width: 160px;
  background-color: #eceef550;
  color: var(--color-text-haze);
  text-align: center;
  border-radius: 5px;
  padding: 5px;
  z-index: 100;
  transform: translateX(50%);
  opacity: 0;
  transition: opacity 0.8s;
  border: 1px solid rgb(202, 206, 223);
  font-size: 12px;
  visibility: hidden;
  transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;

  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px); /* for safari */
  box-shadow: 0 2px 4px rgba(32, 33, 34, 0.1);
}

.icon-info:hover  + .tooltip {
  visibility: visible;
  opacity: 1;
}
</style>

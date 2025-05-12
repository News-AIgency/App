<template>
  <transition name="popup">
  <div class="popup-container" v-if="visible">
    <p class="text">You have unsaved changes</p>
    <div class="buttons-container">
      <button class="discard-btn" @click="discardChanges">Discard</button
      ><button class="save-btn">Save changes</button>
    </div>
  </div>
</transition>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'SaveChangePopup',
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    discardChanges() {
      this.$emit('discard')
    },
  },
})
</script>

<style scoped>
.text {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
/* buttons */
.buttons-container {
  display: flex;
  gap: 10px;
}

.discard-btn {
  background-color: transparent;
  border: none;
  padding: 8px 10px;
  cursor: pointer;
  color: var(--color-text-haze);
}

.discard-btn:hover {
  text-decoration: underline;
}

.save-btn {
  background-color: var(--color-green);
  color: white;
  border: none;
  padding: 8px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.save-btn:hover {
  background-color: var(--color-green-hover);
}

/* main container */
.popup-container {
  width: clamp(300px, 50%, 500px);
  display: flex;
  justify-content: space-between;
  position: fixed;
  bottom: 10px;
  position: absolute;
  left: 50%;
  translate: -50%;
  background-color: white;
  color: var(--color-text);
  padding: 10px 20px;
  border-radius: 15px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  text-align: center;
}
/* transition classes */
.popup-enter-active, .popup-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.popup-enter-from, .popup-leave-to {
  opacity: 0;
  transform: translateY(100%);
}

.popup-enter-to, .popup-leave-from {
  opacity: 1;
  transform: translateY(0);
}

</style>

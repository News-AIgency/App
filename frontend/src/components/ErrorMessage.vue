<template>
  <div class="error-message">
    <h1>Something went wrong! 😢</h1>
    <p>You can start from beginning, if error occurs try again later.</p>
    <button class="btn" @click="goHome"><span class="material-icons keyboard_backspace back-icon"></span>Start Over</button>
  </div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';

export default {
  name: 'ErrorMessage',
  setup() {
    const router = useRouter();

    const goHome = () => {
      router.push('/');
    };

    return {
      goHome,
    };
  }
}</script>

<style scoped>
.back-icon {
  font-size: 14px;
}
.btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: var(--color-block);
  margin-top: 10px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  padding: 8px 10px;
  font-size: 12px;
}

.btn:hover {
  background-color: var(--color-block-hover);
}
</style>

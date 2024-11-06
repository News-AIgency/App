<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="page-wrapper">
  <nav class="navbar">
    <a class="navbar-logo">News <span class="text-accent">AI</span>gency</a>
    <a>Contact Us</a>
  </nav>
  <RouterView/>
  <footer class="footer-container">
    <p>News AIgency</p>
    <p>2024</p>
  </footer>
</div>
</template>

<style scoped>
.navbar {
  color: var(--color-text);
}


.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  padding-bottom: 2.5rem;
}


.footer-container {
  display: flex;
  margin: auto;
  margin-top: 20px;
  padding-top: 20px;
  margin-bottom: 20px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;

  font-size: 16px;
  opacity: 0.5;
}
footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 2.5rem;

}
</style>

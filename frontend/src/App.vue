<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'

const router = useRouter();

function goToStart() {
  router.push('/');
}

function mailTo() {
  var mail = document.createElement('a');
  mail.href = "mailto:tptim042024@gmail.com";
  mail.click();
}
</script>

<template>
  <div class="page-wrapper">
    <nav class="navbar">
      <a class="navbar-logo" @click="goToStart">News <span class="text-accent">AI</span>gency</a>
      <a class="contact-us" @click="mailTo">Contact Us</a>
    </nav>
    <RouterView />
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

.navbar-logo {
  cursor: pointer;
}

.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  padding-bottom: 2.5rem;
}

.contact-us {
  cursor: pointer;
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


<template>
  <div class="page-wrapper">
    <nav class="navbar">
      <!-- <a class="navbar-logo" @click="goToStart"
        >WR<span class="text-accent">AI</span>TE</a
      > -->
      <img src="../public/logo.svg" alt="WrAIte XMAS logo <3">
      <div class="navbar-item"><a href="">Home</a></div>
      <div class="navbar-item"><a href="">Organization</a></div>
      <div class="navbar-item"><a href="">History</a></div>
      <a class="contact-us" @click="mailTo">Contact Us</a>
    </nav>
    <div class="content-wrapper"><RouterView /></div>
  </div>
</template>

<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'

const router = useRouter()

function goToStart() {
  router.push('/')
}

function mailTo() {
  window.location.href = 'mailto:tptim042024@gmail.com'
}
</script>

<style scoped>
@media screen and (max-device-width: 480px) {
  .navbar {
    gap: 10%;
  }

  .navbar-logo {
    font-size: 22px;
  }
}

.navbar {
  display: flex;
  flex-direction: column;
  justify-content: start;
  gap: 8px;
  color: var(--color-text);
  width: 25%;
  height: 100vh;
}

.navbar-logo {
  cursor: pointer;
}
.navbar-item {
  background-color: var(--color-block);
  border-radius: 10px;
  padding: 8px 4px;
  width: 170px;
}

.navbar-item a {
  color: var(--color-text-haze);
  font-weight: 600;
  text-decoration: none;
}

.page-wrapper {
  display: flex;
  flex-direction: row;
  min-height: 100vh;
  position: relative;
  padding-bottom: 2.5rem;
}

.content-wrapper {
  width: 100%;
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

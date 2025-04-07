<template>
  <div class="page-wrapper">
    <nav class="navbar">
      <div class="menu-container">
        <a class="navbar-logo" @click="goToStart"
          >WR<span class="text-accent">AI</span>TE</a
        >
        <!-- <img
          clas>s="navbar-logo"
          src="../public/logo.svg"
          @click="goToStart"
          alt="WrAIte XMAS logo <3"
        /> -->
        <a href="" class="navbar-item">
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M3 13h1v7c0 1.103.897 2 2 2h12c1.103 0 2-.897 2-2v-7h1a1 1 0 0 0 .707-1.707l-9-9a1 1 0 0 0-1.414 0l-9 9A1 1 0 0 0 3 13m7 7v-5h4v5zm2-15.586l6 6V15l.001 5H16v-5c0-1.103-.897-2-2-2h-4c-1.103 0-2 .897-2 2v5H6v-9.586z"
            /></svg
          ><span class="label">Home</span>
        </a>
        <!-- <div class="navbar-item">
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            width="24px"
            height="24px"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="#898989"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 21V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5m-4 0h4"
            /></svg
          ><a href="">Organization</a>
        </div> -->
        <a href="history" class="navbar-item">
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            width="24px"
            height="24px"
            viewBox="0 0 24 24"
          >
            <path
              fill="#898989"
              d="M12 21q-3.15 0-5.575-1.912T3.275 14.2q-.1-.375.15-.687t.675-.363q.4-.05.725.15t.45.6q.6 2.25 2.475 3.675T12 19q2.925 0 4.963-2.037T19 12t-2.037-4.962T12 5q-1.725 0-3.225.8T6.25 8H8q.425 0 .713.288T9 9t-.288.713T8 10H4q-.425 0-.712-.288T3 9V5q0-.425.288-.712T4 4t.713.288T5 5v1.35q1.275-1.6 3.113-2.475T12 3q1.875 0 3.513.713t2.85 1.924t1.925 2.85T21 12t-.712 3.513t-1.925 2.85t-2.85 1.925T12 21m1-9.4l2.5 2.5q.275.275.275.7t-.275.7t-.7.275t-.7-.275l-2.8-2.8q-.15-.15-.225-.337T11 11.975V8q0-.425.288-.712T12 7t.713.288T13 8z"
            /></svg
          ><span class="label">History</span>
        </a>
      </div>
      <div class="footer-container">
        <a class="contact-us" @click="mailTo">Contact Us</a>
        <div class="footer">WRAITE<br />2025</div>
      </div>
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
    margin: auto;
  }
}

.navbar {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 8px;
  color: var(--color-text);
  width: 20%;
  height: 100vh;
  position: fixed; /* to prevent scroll */
  left: 0;
  top: 0;
}

.menu-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.navbar-logo {
  font-size: 30px;
  margin: auto;
  cursor: pointer;
}
.navbar-item {
  background-color: var(--color-block);
  border-radius: 10px;
  padding: 8px 4px;
  width: 170px;
  display: flex;
  justify-content: start;
  align-items: center;
}

.navbar-item{
  text-decoration: none;
  color: var(--color-text-haze);
}

.icon {
  fill: var(--color-text-haze);
  margin: 0 10px 0 4px;
}

.navbar-item a {
  color: var(--color-text-haze);
  font-weight: 700;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.navbar-item .icon {
  display: flex;
  align-items: center;
}

.navbar-item:hover {
  background-color: var(--color-block-hover);
}

.page-wrapper {
  display: flex;
  flex-direction: row;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.content-wrapper {
  background-color: rgb(255, 255, 255);
  margin: 30px 30px 30px 0px;
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 80%;
  min-height: calc(100vh - 60px);
  margin-left: 20%; /* the size of the sidebar */
  overflow-y: auto;
}

.contact-us {
  cursor: pointer;
}

.footer-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  gap: 4px;
}

.footer {
  text-align: center;
  font-size: 12px;
  opacity: 0.5;
}

.label {
  font-weight: 600;
}
</style>

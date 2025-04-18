<template>
  <div class="page-wrapper" v-if="showNavbar">
    <Navbar></Navbar>
    <div class="content-wrapper"><RouterView /></div>
  </div>
  <RouterView v-if="!showNavbar"/>
</template>

<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import { computed } from 'vue';
import Navbar from './components/Navbar.vue';

const route = useRoute();
const showNavbar = computed(() => route.path !== '/team');
</script>

<style scoped lang="scss">
.page-wrapper {
  display: flex;
  flex-direction: row;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.content-wrapper {
  background-color: rgb(255, 255, 255);
  width: 80%;
  min-height: calc(100vh - 60px);
  overflow-y: auto;
  flex-grow: 1;
}

@media screen and (min-device-width: 1025px) {
  .content-wrapper {
    margin: 30px 30px 30px 0;
    border-radius: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
}

</style>

<template>
   <div class="loading-state">
  <div class="loading"></div>
</div>
</template>

<style>
.loading-state {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.loading {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.25);
  border-top-color: var(--color-accent);
  animation: loading 1s linear infinite;
}
@keyframes loading {
  to {
    transform: rotate(360deg);
  }
}

</style>

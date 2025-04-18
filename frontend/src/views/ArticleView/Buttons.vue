<template>
    <div class="buttons-container">
        <button class="btn-primary btn"><span class="material-icons publish"></span>Publish</button>
        <button class="btn-secondary btn"><span class="material-icons send"></span>Share</button>
    </div>
</template>



<script lang="ts">
export default {
    name: 'Buttons'
}
</script>

<style lang="scss" scoped>
.btn {
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 10px;
  cursor: pointer;

  span {
    font-size: 14px;
  }

  &-primary {
    background-color: var(--color-accent);
    padding: 8px 10px;
    border: none;
    color: var(--color-text-dark-bg);
  }

  &-secondary {
    background-color: transparent;
    padding: 8px 10px;
    border: 1px solid black;
  }
}
</style>
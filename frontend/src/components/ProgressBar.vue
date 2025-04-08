<template>
  <div class="container">
    <div class="step-container">
      <div class="step-num" :class="['step', { active: currentStep == 1 }]">
        STEP 1
      </div>
      <span class="step-text" :class="['step', { active: currentStep == 1 }]"
        >Enter source URL</span
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <path
          fill="currentColor"
          d="M9.575 12L5.7 8.1q-.275-.275-.288-.687T5.7 6.7q.275-.275.7-.275t.7.275l4.6 4.6q.15.15.213.325t.062.375t-.062.375t-.213.325l-4.6 4.6q-.275.275-.687.288T5.7 17.3q-.275-.275-.275-.7t.275-.7zm6.6 0L12.3 8.1q-.275-.275-.288-.687T12.3 6.7q.275-.275.7-.275t.7.275l4.6 4.6q.15.15.213.325t.062.375t-.062.375t-.213.325l-4.6 4.6q-.275.275-.687.288T12.3 17.3q-.275-.275-.275-.7t.275-.7z"
        />
      </svg>
      <div class="step-num" :class="['step', { active: currentStep == 2 }]">
        STEP 2
      </div>
      <span class="step-text" :class="['step', { active: currentStep == 2 }]"
        >Select article topic</span
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <path
          fill="currentColor"
          d="M9.575 12L5.7 8.1q-.275-.275-.288-.687T5.7 6.7q.275-.275.7-.275t.7.275l4.6 4.6q.15.15.213.325t.062.375t-.062.375t-.213.325l-4.6 4.6q-.275.275-.687.288T5.7 17.3q-.275-.275-.275-.7t.275-.7zm6.6 0L12.3 8.1q-.275-.275-.288-.687T12.3 6.7q.275-.275.7-.275t.7.275l4.6 4.6q.15.15.213.325t.062.375t-.062.375t-.213.325l-4.6 4.6q-.275.275-.687.288T12.3 17.3q-.275-.275-.275-.7t.275-.7z"
        />
      </svg>
      <div class="step-num" :class="['step', { active: currentStep == 3 }]">
        STEP 3
      </div>
      <span class="step-text" :class="['step', { active: currentStep == 3 }]"
        >Edit and export your article</span
      >
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'ProgressBar',
  props: {
    currentStep: Number,
  },
}
</script>

<style scoped lang="scss">
svg {
  opacity: 0.5;
}
.container {
  padding-top: 20px;
  margin: auto;
  width: 100%;
  font-size: 0.75rem;
}
.step-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px;
}

.step-num {
  background-color: var(--color-block-inactive);
  padding: 6px 12px;
  border-radius: 20px;
  color: var(--color-text-haze);
  font-weight: bold;
}

.step-num.active {
  background-color: var(--color-block);
  color: var(--color-text);
}

.step-text {
  color: rgba(0, 0, 0, 0.5);
}

.step-text.active {
  color: var(--text-black);
}

@media screen and (max-device-width: 1024px) { // mozno sa to pomesti aj na mensie obrazovky, idk
  .step-text {
    display: none;
  }
  .container {
    padding-top: 68px;
  }
}
</style>

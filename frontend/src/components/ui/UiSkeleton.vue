<script setup>
defineProps({
  width: {
    type: String,
    default: '100%',
  },
  height: {
    type: String,
    default: '1rem',
  },
})
</script>

<template>
  <span class="ui-skeleton" :style="{ width, height }" aria-hidden="true"></span>
</template>

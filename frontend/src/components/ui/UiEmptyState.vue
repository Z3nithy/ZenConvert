<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  announce: {
    type: Boolean,
    default: true,
  },
})
</script>

<template>
  <div class="ui-empty-state" :aria-live="announce ? 'polite' : 'off'">
    <slot name="icon" />
    <h2 class="ui-empty-state__title">{{ title }}</h2>
    <p v-if="description" class="ui-empty-state__description">{{ description }}</p>
    <div v-if="$slots.action"><slot name="action" /></div>
  </div>
</template>

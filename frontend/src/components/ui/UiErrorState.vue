<script setup>
defineProps({
  title: {
    type: String,
    default: 'Não foi possível carregar',
  },
  description: {
    type: String,
    required: true,
  },
  announce: {
    type: Boolean,
    default: true,
  },
})
</script>

<template>
  <section
    class="ui-error-state"
    :role="announce ? 'alert' : undefined"
    :aria-live="announce ? undefined : 'off'"
  >
    <h2 class="ui-error-state__title">{{ title }}</h2>
    <p class="ui-error-state__description">{{ description }}</p>
    <div v-if="$slots.action"><slot name="action" /></div>
  </section>
</template>

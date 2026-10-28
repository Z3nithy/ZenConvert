<script setup>
defineProps({
  variant: {
    type: String,
    default: 'neutral',
    validator: (value) => ['neutral', 'success', 'warning', 'danger'].includes(value),
  },
})
</script>

<template>
  <span class="ui-badge" :class="`ui-badge--${variant}`"><slot /></span>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <article class="ui-card">
    <header v-if="title || description || $slots.header" class="ui-card__header">
      <slot name="header">
        <h2 v-if="title" class="ui-card__title">{{ title }}</h2>
        <p v-if="description" class="ui-card__description">{{ description }}</p>
      </slot>
    </header>
    <slot />
    <footer v-if="$slots.footer" class="ui-card__footer">
      <slot name="footer" />
    </footer>
  </article>
</template>

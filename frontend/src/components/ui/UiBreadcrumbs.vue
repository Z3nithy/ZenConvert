<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    validator: (items) =>
      items.every((item) => item && typeof item.label === 'string' && item.label.length > 0),
  },
  label: {
    type: String,
    default: 'Navegação estrutural',
  },
})
</script>

<template>
  <nav class="ui-breadcrumbs" :aria-label="label">
    <ol class="ui-breadcrumbs__list">
      <li v-for="(item, index) in items" :key="`${item.label}-${index}`">
        <a
          v-if="item.href && index < items.length - 1"
          class="ui-breadcrumbs__link"
          :href="item.href"
        >
          {{ item.label }}
        </a>
        <span
          v-else
          :class="index === items.length - 1 ? 'ui-breadcrumbs__current' : undefined"
          :aria-current="index === items.length - 1 ? 'page' : undefined"
        >
          {{ item.label }}
        </span>
        <span v-if="index < items.length - 1" class="ui-breadcrumbs__separator" aria-hidden="true">
          /
        </span>
      </li>
    </ol>
  </nav>
</template>

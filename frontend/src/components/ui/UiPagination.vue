<script setup>
import { ChevronLeft, ChevronRight } from '@lucide/vue'
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true,
  },
  pageCount: {
    type: Number,
    required: true,
    validator: (value) => Number.isInteger(value) && value >= 1,
  },
  label: {
    type: String,
    default: 'Paginação',
  },
})

const emit = defineEmits(['update:modelValue'])
const visiblePages = computed(() => {
  const start = Math.max(1, Math.min(props.modelValue - 2, props.pageCount - 4))
  const end = Math.min(props.pageCount, start + 4)
  return Array.from({ length: end - start + 1 }, (_, index) => start + index)
})

function goTo(page) {
  if (page >= 1 && page <= props.pageCount && page !== props.modelValue) {
    emit('update:modelValue', page)
  }
}
</script>

<template>
  <nav class="ui-pagination" :aria-label="label">
    <button
      class="ui-pagination__button"
      type="button"
      aria-label="Página anterior"
      :disabled="modelValue <= 1"
      @click="goTo(modelValue - 1)"
    >
      <ChevronLeft :size="18" :stroke-width="1.75" aria-hidden="true" />
    </button>
    <span v-if="visiblePages[0] > 1" class="ui-pagination__ellipsis" aria-hidden="true">…</span>
    <button
      v-for="page in visiblePages"
      :key="page"
      class="ui-pagination__button"
      type="button"
      :aria-label="`Página ${page}`"
      :aria-current="page === modelValue ? 'page' : undefined"
      @click="goTo(page)"
    >
      {{ page }}
    </button>
    <span
      v-if="visiblePages[visiblePages.length - 1] < pageCount"
      class="ui-pagination__ellipsis"
      aria-hidden="true"
    >
      …
    </span>
    <button
      class="ui-pagination__button"
      type="button"
      aria-label="Próxima página"
      :disabled="modelValue >= pageCount"
      @click="goTo(modelValue + 1)"
    >
      <ChevronRight :size="18" :stroke-width="1.75" aria-hidden="true" />
    </button>
  </nav>
</template>

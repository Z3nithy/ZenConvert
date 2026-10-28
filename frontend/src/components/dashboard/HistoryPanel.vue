<script setup>
import { History, Trash2 } from '@lucide/vue'
import UiButton from '@/components/ui/UiButton.vue'
import { formatSize } from '@/utils/files'

defineProps({
  items: { type: Array, required: true },
  persistent: { type: Boolean, default: true },
})
defineEmits(['clear'])

const formatter = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
</script>

<template>
  <section class="history" aria-labelledby="history-title">
    <div class="history__heading">
      <div>
        <p class="history__eyebrow">02 / HISTÓRICO</p>
        <h2 id="history-title">Últimas conversões</h2>
      </div>
      <UiButton v-if="items.length" variant="ghost" size="sm" @click="$emit('clear')">
        <Trash2 :size="14" aria-hidden="true" /> Limpar histórico
      </UiButton>
    </div>

    <p v-if="!items.length" class="history__empty">
      <History :size="16" aria-hidden="true" />
      Nenhuma conversão ainda. As próximas aparecerão aqui.
    </p>

    <ol v-else class="history__list">
      <li v-for="item in items" :key="item.id">
        <span class="history__names">
          <span class="history__name">{{ item.name }}</span>
          <span class="history__arrow" aria-hidden="true">→</span>
          <span class="history__output">{{ item.output }}</span>
        </span>
        <span class="history__meta">
          {{ item.tool }} · {{ formatSize(item.size) }} ·
          <time :datetime="item.at">{{ formatter.format(new Date(item.at)) }}</time>
        </span>
      </li>
    </ol>

    <p class="history__note">
      {{
        persistent
          ? 'Guardado apenas neste navegador. Os arquivos não são armazenados.'
          : 'Não foi possível salvar o histórico neste navegador.'
      }}
    </p>
  </section>
</template>

<style scoped>
.history {
  padding-block: 0 var(--space-10);
}

.history__heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: var(--space-5);
  margin-bottom: var(--space-4);
}

.history__eyebrow {
  margin: 0;
  color: var(--color-green-300);
  font-family: var(--font-mono);
  font-size: 0.6875rem;
  letter-spacing: 0.1em;
}

.history h2 {
  margin: var(--space-2) 0 0;
  font-size: var(--text-xl);
  font-weight: var(--font-weight-semibold);
  letter-spacing: var(--tracking-tight);
}

.history__empty {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin: 0;
  padding: var(--space-5);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-lg);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
}

.history__list {
  display: grid;
  margin: 0;
  padding: 0;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  list-style: none;
}

.history__list li {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-1) var(--space-4);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface-raised);
}

.history__list li + li {
  border-top: 1px solid var(--color-border);
}

.history__names {
  display: flex;
  min-width: 0;
  flex: 1 1 16rem;
  align-items: baseline;
  gap: var(--space-2);
  font-size: var(--text-sm);
}

.history__name {
  min-width: 0;
  overflow: hidden;
  color: var(--color-text-secondary);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history__arrow {
  color: var(--color-gray-400);
}

.history__output {
  min-width: 0;
  overflow: hidden;
  color: var(--color-green-300);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history__meta {
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
}

.history__note {
  margin: var(--space-3) 0 0;
  color: var(--color-text-muted);
  font-size: 0.6875rem;
}

@media (max-width: 36rem) {
  .history__heading {
    align-items: flex-start;
    flex-direction: column;
    gap: var(--space-2);
  }
}
</style>

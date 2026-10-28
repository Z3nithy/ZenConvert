<script setup>
defineProps({
  title: { type: String, required: true },
  status: { type: String, default: '' },
  titleTag: { type: String, default: 'span' },
  titleId: { type: String, default: undefined },
})
</script>

<template>
  <div class="terminal-bar">
    <span class="terminal-bar__lights" aria-hidden="true"
      ><span></span><span></span><span></span
    ></span>
    <component :is="titleTag" :id="titleId" class="terminal-bar__title">{{ title }}</component>
    <span v-if="status" class="terminal-bar__status">
      <span class="terminal-bar__dot" aria-hidden="true"></span>{{ status }}
    </span>
    <slot />
  </div>
</template>

<style scoped>
.terminal-bar {
  display: flex;
  min-height: 2.75rem;
  align-items: center;
  gap: var(--space-3);
  padding-inline: var(--space-4);
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  font-size: 0.625rem;
}

.terminal-bar__lights {
  display: inline-flex;
  gap: 0.375rem;
}

.terminal-bar__lights span {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--color-gray-700);
}

.terminal-bar__lights span:first-child {
  background: var(--color-green-500);
}

.terminal-bar__title {
  min-width: 0;
  flex: 1;
  margin: 0;
  overflow: hidden;
  color: var(--color-text-muted);
  font-size: inherit;
  font-weight: 400;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.terminal-bar__status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-green-300);
}

.terminal-bar__dot {
  width: 0.4375rem;
  height: 0.4375rem;
  flex: 0 0 auto;
  border-radius: 50%;
  background: var(--color-green-400);
  box-shadow: 0 0 10px rgb(105 216 135 / 38%);
}
</style>

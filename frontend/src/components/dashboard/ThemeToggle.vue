<script setup>
import { Moon, Sun } from '@lucide/vue'
import { useTheme } from '@/composables/useTheme'

const { theme, toggleTheme } = useTheme()
</script>

<template>
  <button
    class="ui-icon-button theme-toggle"
    type="button"
    :aria-label="`Ativar tema ${theme === 'dark' ? 'claro' : 'escuro'}`"
    :title="`Ativar tema ${theme === 'dark' ? 'claro' : 'escuro'}`"
    @click="toggleTheme"
  >
    <Sun v-if="theme === 'dark'" :size="18" aria-hidden="true" />
    <Moon v-else :size="18" aria-hidden="true" />
  </button>
</template>

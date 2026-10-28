import { ref } from 'vue'

const STORAGE_KEY = 'zenconvert:theme'
const theme = ref(readThemePreference())

function readThemePreference() {
  try {
    return localStorage.getItem(STORAGE_KEY) === 'light' ? 'light' : 'dark'
  } catch {
    return 'dark'
  }
}

function applyTheme(value) {
  theme.value = value
  document.documentElement.dataset.theme = value

  try {
    localStorage.setItem(STORAGE_KEY, value)
  } catch {
    // Theme switching remains available for the current page if storage is disabled.
  }
}

export function initializeTheme() {
  applyTheme(theme.value)
}

export function useTheme() {
  function toggleTheme() {
    applyTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  return { theme, toggleTheme }
}

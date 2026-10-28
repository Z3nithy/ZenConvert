import { ref } from 'vue'

const STORAGE_KEY = 'zenconvert:history:v1'
const MAX_ITEMS = 20

function isValid(item) {
  return (
    item &&
    typeof item.id === 'string' &&
    typeof item.name === 'string' &&
    typeof item.output === 'string' &&
    typeof item.tool === 'string' &&
    typeof item.size === 'number' &&
    typeof item.at === 'string'
  )
}

function load() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]')
    return Array.isArray(parsed) ? parsed.filter(isValid).slice(0, MAX_ITEMS) : []
  } catch {
    return []
  }
}

/** Histórico local: guarda só metadados, nunca o conteúdo dos arquivos. */
export function useConversionHistory() {
  const items = ref(load())
  const persistent = ref(true)

  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value))
      persistent.value = true
    } catch {
      persistent.value = false
    }
  }

  function add({ name, output, tool, size }) {
    const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
    const entry = { id, name, output, tool, size, at: new Date().toISOString() }
    items.value = [entry, ...items.value].slice(0, MAX_ITEMS)
    save()
  }

  function clear() {
    items.value = []
    save()
  }

  return { items, persistent, add, clear }
}

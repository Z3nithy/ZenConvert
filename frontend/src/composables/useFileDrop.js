import { onBeforeUnmount, ref } from 'vue'

function dropTargetOf(event) {
  return event.target instanceof Element
    ? (event.target.closest('[data-drop-target]')?.dataset.dropTarget ?? null)
    : null
}

function hasFiles(event) {
  return Array.from(event.dataTransfer?.types ?? []).includes('Files')
}

/** Arrastar e soltar arquivos em qualquer ponto da janela. */
export function useFileDrop(onDrop) {
  const isDragging = ref(false)
  const dropTarget = ref(null)
  let depth = 0

  function reset() {
    depth = 0
    isDragging.value = false
    dropTarget.value = null
  }

  function onEnter(event) {
    if (!hasFiles(event)) return
    event.preventDefault()
    depth += 1
    isDragging.value = true
  }

  function onOver(event) {
    if (!hasFiles(event)) return
    event.preventDefault()
    event.dataTransfer.dropEffect = 'copy'
    isDragging.value = true
    dropTarget.value = dropTargetOf(event)
  }

  function onLeave(event) {
    if (!hasFiles(event)) return
    depth = Math.max(0, depth - 1)
    if (depth === 0) reset()
  }

  function onDropEvent(event) {
    if (!hasFiles(event)) return
    event.preventDefault()
    const target = dropTargetOf(event)
    const files = Array.from(event.dataTransfer.files)
    reset()
    if (files.length) onDrop(files, target)
  }

  window.addEventListener('dragenter', onEnter)
  window.addEventListener('dragover', onOver)
  window.addEventListener('dragleave', onLeave)
  window.addEventListener('drop', onDropEvent)
  onBeforeUnmount(() => {
    window.removeEventListener('dragenter', onEnter)
    window.removeEventListener('dragover', onOver)
    window.removeEventListener('dragleave', onLeave)
    window.removeEventListener('drop', onDropEvent)
  })

  return { isDragging, dropTarget }
}

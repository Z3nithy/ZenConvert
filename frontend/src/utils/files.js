export function getExtension(filename) {
  const index = filename.lastIndexOf('.')
  return index === -1 ? '' : filename.slice(index + 1).toLowerCase()
}

export function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

/**
 * Descobre quais destinos aceitam todos os arquivos reconhecidos.
 * Arquivos de formato desconhecido são devolvidos em `unsupported`.
 */
export function detectDestinations(files, tools) {
  const supported = []
  const unsupported = []
  for (const file of files) {
    const extension = getExtension(file.name)
    if (tools.some((tool) => tool.extensions.includes(extension))) supported.push(file)
    else unsupported.push(file)
  }
  const destinations = tools.filter((tool) =>
    supported.every((file) => tool.extensions.includes(getExtension(file.name))),
  )
  return { supported, unsupported, destinations: supported.length ? destinations : [] }
}

function uniqueName(name, used) {
  if (!used.has(name)) return name
  const dot = name.lastIndexOf('.')
  const base = dot > 0 ? name.slice(0, dot) : name
  const extension = dot > 0 ? name.slice(dot) : ''
  let counter = 2
  while (used.has(`${base} (${counter})${extension}`)) counter += 1
  return `${base} (${counter})${extension}`
}

export function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.append(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

/** Gera e baixa um ZIP; `fflate` só é carregado quando o recurso é usado. */
export async function downloadZip(items, zipName) {
  const { zipSync } = await import('fflate')
  const used = new Set()
  const files = {}
  for (const { filename, blob } of items) {
    const name = uniqueName(filename, used)
    used.add(name)
    files[name] = new Uint8Array(await blob.arrayBuffer())
  }
  triggerDownload(new Blob([zipSync(files)], { type: 'application/zip' }), zipName)
}

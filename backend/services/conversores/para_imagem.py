import io
import zipfile

import pypdfium2 as pdfium
from PIL import Image, UnidentifiedImageError

from .erros import ConversaoError

ORIGENS = {"pdf", "png", "jpg", "jpeg", "webp", "gif", "avif"}
MAX_PAGINAS = 50
MIMES = {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp"}
FORMATO_PIL = {"png": "PNG", "jpg": "JPEG", "webp": "WEBP"}


def _codificar(imagem: Image.Image, formato: str) -> bytes:
    if formato == "jpg":
        imagem = imagem.convert("RGB")
    saida = io.BytesIO()
    imagem.save(saida, FORMATO_PIL[formato])
    return saida.getvalue()


def _paginas_pdf(conteudo: bytes) -> list[Image.Image]:
    try:
        documento = pdfium.PdfDocument(conteudo)
    except Exception as erro:
        raise ConversaoError("PDF inválido ou protegido por senha.") from erro
    try:
        total = len(documento)
        if total > MAX_PAGINAS:
            raise ConversaoError(f"O PDF excede o limite de {MAX_PAGINAS} páginas.", 413)
        return [documento[i].render(scale=2).to_pil() for i in range(total)]
    finally:
        documento.close()


def converter(extensao: str, conteudo: bytes, formato: str) -> tuple[bytes, str, str]:
    if extensao == "pdf":
        imagens = _paginas_pdf(conteudo)
    else:
        try:
            imagem = Image.open(io.BytesIO(conteudo))
            imagem.load()
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as erro:
            raise ConversaoError("Imagem inválida ou formato não suportado.") from erro
        imagens = [imagem]

    if len(imagens) == 1:
        return _codificar(imagens[0], formato), MIMES[formato], formato

    saida = io.BytesIO()
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as pacote:
        for numero, pagina in enumerate(imagens, start=1):
            pacote.writestr(f"pagina-{numero:03d}.{formato}", _codificar(pagina, formato))
    return saida.getvalue(), "application/zip", "zip"

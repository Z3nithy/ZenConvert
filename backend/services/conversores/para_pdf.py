import io
import shutil
import subprocess
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, UnidentifiedImageError
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from .erros import ConversaoError
from .tabular import ler_linhas
from .texto import ler_blocos

MIME = "application/pdf"
IMAGENS = {"png", "jpg", "jpeg", "webp", "gif", "avif"}
TEXTOS = {"txt", "md", "html", "htm"}
ORIGENS = (
    {"docx", "doc", "pptx", "ppt", "csv", "tsv", "xlsx", "xls", "json", "yaml", "yml", "xml"}
    | IMAGENS
    | TEXTOS
)


def _texto(extensao: str, conteudo: bytes) -> bytes:
    estilos = getSampleStyleSheet()
    elementos = []
    for tipo, texto in ler_blocos(extensao, conteudo):
        estilo = estilos["BodyText"] if tipo == "p" else estilos[f"Heading{tipo[1]}"]
        elementos.append(Paragraph(escape(texto), estilo))
    saida = io.BytesIO()
    SimpleDocTemplate(saida, pagesize=A4).build(elementos)
    return saida.getvalue()


def _office(extensao: str, conteudo: bytes) -> bytes:
    programa = shutil.which("soffice") or shutil.which("libreoffice")
    if not programa:
        raise ConversaoError(
            "Conversão de documentos Word para PDF requer o LibreOffice instalado no servidor.", 503
        )
    with tempfile.TemporaryDirectory() as pasta:
        origem = Path(pasta) / f"origem.{extensao}"
        origem.write_bytes(conteudo)
        try:
            subprocess.run(
                [programa, "--headless", "--convert-to", "pdf", "--outdir", pasta, str(origem)],
                check=True,
                capture_output=True,
                timeout=90,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as erro:
            raise ConversaoError("Não foi possível converter o documento para PDF.") from erro
        resultado = Path(pasta) / "origem.pdf"
        if not resultado.exists():
            raise ConversaoError("Não foi possível converter o documento para PDF.")
        return resultado.read_bytes()


def _tabela(linhas) -> bytes:
    if not linhas:
        raise ConversaoError("O arquivo não possui dados para converter.")
    colunas = max(len(linha) for linha in linhas)
    estilo = getSampleStyleSheet()["BodyText"]
    estilo.fontSize = 8
    estilo.leading = 10
    dados = [
        [Paragraph(escape(str(v)), estilo) for v in linha] + [""] * (colunas - len(linha))
        for linha in linhas
    ]
    saida = io.BytesIO()
    pagina = landscape(A4) if colunas > 5 else A4
    documento = SimpleDocTemplate(saida, pagesize=pagina, leftMargin=24, rightMargin=24)
    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e4f5ea")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    documento.build([tabela])
    return saida.getvalue()


def _imagem(conteudo: bytes) -> bytes:
    try:
        imagem = Image.open(io.BytesIO(conteudo))
        imagem.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as erro:
        raise ConversaoError("Imagem inválida ou formato não suportado.") from erro
    saida = io.BytesIO()
    imagem.convert("RGB").save(saida, "PDF")
    return saida.getvalue()


def converter(extensao: str, conteudo: bytes) -> tuple[bytes, str, str]:
    if extensao in {"docx", "doc", "pptx", "ppt"}:
        dados = _office(extensao, conteudo)
    elif extensao in IMAGENS:
        dados = _imagem(conteudo)
    elif extensao in TEXTOS:
        dados = _texto(extensao, conteudo)
    else:
        dados = _tabela(ler_linhas(extensao, conteudo))
    return dados, MIME, "pdf"

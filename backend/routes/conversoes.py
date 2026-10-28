import re
from pathlib import PurePath
from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import Response

from core.config import MAX_UPLOAD_MB
from enums import FormatoImagem, FormatoTexto
from schemas import ConversoesDisponiveis, FormatosSuportados
from services.conversores import (
    ORIGENS_POR_DESTINO,
    ConversaoError,
    para_csv,
    para_excel,
    para_imagem,
    para_json,
    para_pdf,
    para_texto,
    para_word,
    para_xml,
    para_yaml,
)

router = APIRouter(prefix="/api/conversoes", tags=["Conversões"])

ArquivoEntrada = Annotated[UploadFile, File(description="Arquivo de origem a ser convertido.")]


def _ler_upload(arquivo: UploadFile, origens_aceitas: set[str]) -> tuple[str, str, bytes]:
    nome = PurePath(arquivo.filename or "").name
    extensao = nome.rsplit(".", 1)[-1].lower() if "." in nome else ""
    if extensao not in origens_aceitas:
        aceitos = ", ".join(f".{e}" for e in sorted(origens_aceitas))
        raise HTTPException(415, f"Formato de origem não suportado. Aceitos: {aceitos}.")

    limite = MAX_UPLOAD_MB * 1024 * 1024
    conteudo = arquivo.file.read(limite + 1)
    if len(conteudo) > limite:
        raise HTTPException(413, f"O arquivo excede o limite de {MAX_UPLOAD_MB} MB.")
    if not conteudo:
        raise HTTPException(400, "O arquivo enviado está vazio.")
    return nome.rsplit(".", 1)[0], extensao, conteudo


def _resposta(base: str, resultado: tuple[bytes, str, str]) -> Response:
    dados, mime, extensao = resultado
    base_segura = re.sub(r"[^\w\- ]", "_", base, flags=re.UNICODE).strip() or "arquivo"
    nome = f"{base_segura}.{extensao}"
    return Response(
        content=dados,
        media_type=mime,
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(nome)}"},
    )


def _executar(arquivo: UploadFile, origens: set[str], conversor) -> Response:
    base, extensao, conteudo = _ler_upload(arquivo, origens)
    try:
        return _resposta(base, conversor(extensao, conteudo))
    except ConversaoError as erro:
        raise HTTPException(erro.status_code, erro.mensagem) from erro


@router.get("", response_model=ConversoesDisponiveis, summary="Lista as conversões disponíveis")
def listar_conversoes():
    return ConversoesDisponiveis(
        limite_upload_mb=MAX_UPLOAD_MB,
        conversoes=[
            FormatosSuportados(
                destino=destino,
                origens=origens,
                parametros=["formato"] if destino in ("imagem", "texto") else [],
            )
            for destino, origens in ORIGENS_POR_DESTINO.items()
        ],
    )


@router.post("/word", summary="Converte PDF, planilhas, JSON, CSV ou imagens para Word (.docx)")
def para_docx(arquivo: ArquivoEntrada):
    return _executar(arquivo, para_word.ORIGENS, para_word.converter)


@router.post("/excel", summary="Converte CSV, JSON ou Word (tabelas) para Excel (.xlsx)")
def para_xlsx(arquivo: ArquivoEntrada):
    return _executar(arquivo, para_excel.ORIGENS, para_excel.converter)


@router.post("/pdf", summary="Converte Word, planilhas, JSON, CSV ou imagens para PDF")
def para_pdf_rota(arquivo: ArquivoEntrada):
    return _executar(arquivo, para_pdf.ORIGENS, para_pdf.converter)


@router.post("/json", summary="Converte CSV, Excel ou Word (tabelas) para JSON")
def para_json_rota(arquivo: ArquivoEntrada):
    return _executar(arquivo, para_json.ORIGENS, para_json.converter)


@router.post("/imagem", summary="Converte PDF ou imagens para PNG, JPG ou WEBP")
def para_imagem_rota(
    arquivo: ArquivoEntrada,
    formato: Annotated[FormatoImagem, Query(description="Formato da imagem gerada.")] = FormatoImagem.PNG,
):
    return _executar(
        arquivo,
        para_imagem.ORIGENS,
        lambda extensao, conteudo: para_imagem.converter(extensao, conteudo, formato.value),
    )


@router.post("/csv", summary="Converte Excel, JSON, YAML, XML ou Word (tabelas) para CSV")
def para_csv_rota(arquivo: ArquivoEntrada):
    return _executar(arquivo, para_csv.ORIGENS, para_csv.converter)


@router.post("/yaml", summary="Converte CSV, Excel, JSON, XML ou Word (tabelas) para YAML")
def para_yaml_rota(arquivo: ArquivoEntrada):
    return _executar(arquivo, para_yaml.ORIGENS, para_yaml.converter)


@router.post("/xml", summary="Converte CSV, Excel, JSON, YAML ou Word (tabelas) para XML")
def para_xml_rota(arquivo: ArquivoEntrada):
    return _executar(arquivo, para_xml.ORIGENS, para_xml.converter)


@router.post("/texto", summary="Converte Word, PDF, PPTX, HTML, Markdown ou TXT para TXT, MD ou HTML")
def para_texto_rota(
    arquivo: ArquivoEntrada,
    formato: Annotated[FormatoTexto, Query(description="Formato de texto gerado.")] = FormatoTexto.TXT,
):
    return _executar(
        arquivo,
        para_texto.ORIGENS,
        lambda extensao, conteudo: para_texto.converter(extensao, conteudo, formato.value),
    )

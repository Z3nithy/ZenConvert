import re
import xml.etree.ElementTree as ET
from typing import Any

from .erros import ConversaoError
from .tabular import ler_dados, serializavel

ORIGENS = {"csv", "tsv", "xlsx", "xls", "json", "yaml", "yml", "docx"}
MAX_PROFUNDIDADE = 100


def _tag(nome: Any) -> str:
    limpo = re.sub(r"[^\w.-]", "_", str(nome), flags=re.UNICODE).strip("_.-") or "item"
    return limpo if re.match(r"[^\W\d]", limpo, flags=re.UNICODE) else f"_{limpo}"


def _valor(pai: ET.Element, nome: str, valor: Any, nivel: int) -> None:
    if nivel > MAX_PROFUNDIDADE:
        raise ConversaoError("A estrutura é profunda demais para XML.")
    if isinstance(valor, list):
        for item in valor:
            _valor(pai, nome, item, nivel + 1)
        return
    elemento = ET.SubElement(pai, nome)
    if isinstance(valor, dict):
        for chave, filho in valor.items():
            if str(chave).startswith("@"):
                elemento.set(_tag(str(chave)[1:]), str(filho))
            elif chave == "#text":
                elemento.text = str(filho)
            else:
                _valor(elemento, _tag(chave), filho, nivel + 1)
    elif valor is not None:
        elemento.text = str(valor).lower() if isinstance(valor, bool) else str(valor)


def converter(extensao: str, conteudo: bytes) -> tuple[bytes, str, str]:
    dados = serializavel(ler_dados(extensao, conteudo))
    if dados in (None, [], {}):
        raise ConversaoError("O arquivo não possui dados para converter.")

    if isinstance(dados, dict) and len(dados) == 1:
        nome, valor = next(iter(dados.items()))
        raiz = ET.Element("_")
        _valor(raiz, _tag(nome), valor, 0)
        elemento = raiz[0]
    else:
        elemento = ET.Element("dados")
        if isinstance(dados, list):
            _valor(elemento, "registro", dados, 0)
        elif isinstance(dados, dict):
            for chave, valor in dados.items():
                _valor(elemento, _tag(chave), valor, 1)
        else:
            _valor(elemento, "valor", dados, 0)
    try:
        ET.indent(elemento)
        texto = ET.tostring(elemento, encoding="unicode")
    except RecursionError as erro:
        raise ConversaoError("A estrutura é profunda demais para XML.") from erro
    return ('<?xml version="1.0" encoding="UTF-8"?>\n' + texto).encode("utf-8"), "application/xml", "xml"

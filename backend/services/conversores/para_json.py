import json

from .erros import ConversaoError
from .tabular import ler_dados, serializavel

ORIGENS = {"csv", "tsv", "xlsx", "xls", "yaml", "yml", "xml", "docx"}


def converter(extensao: str, conteudo: bytes) -> tuple[bytes, str, str]:
    dados = serializavel(ler_dados(extensao, conteudo))
    if dados in (None, [], {}):
        raise ConversaoError("O arquivo não possui dados para converter.")
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    return texto.encode("utf-8"), "application/json", "json"

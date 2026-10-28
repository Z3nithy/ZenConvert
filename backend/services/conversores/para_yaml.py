import yaml

from .erros import ConversaoError
from .tabular import ler_dados, serializavel

ORIGENS = {"csv", "tsv", "xlsx", "xls", "json", "xml", "docx"}


def converter(extensao: str, conteudo: bytes) -> tuple[bytes, str, str]:
    dados = serializavel(ler_dados(extensao, conteudo))
    if dados in (None, [], {}):
        raise ConversaoError("O arquivo não possui dados para converter.")
    texto = yaml.safe_dump(dados, allow_unicode=True, sort_keys=False, default_flow_style=False)
    return texto.encode("utf-8"), "application/yaml", "yaml"

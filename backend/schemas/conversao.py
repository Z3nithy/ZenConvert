from pydantic import BaseModel


class FormatosSuportados(BaseModel):
    destino: str
    origens: list[str]
    parametros: list[str] = []


class ConversoesDisponiveis(BaseModel):
    limite_upload_mb: int
    conversoes: list[FormatosSuportados]

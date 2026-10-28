class ConversaoError(Exception):
    """Falha de conversão com status HTTP associado."""

    def __init__(self, mensagem: str, status_code: int = 422):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code

"""
Testes para a função buscar_cotacao, que extrai a cotação e data de moedas usando o Google.
"""

from botcity.maestro import BotMaestroSDK

from app.busca_cotacao import buscar_cotacao


class DummyBot:
    """
    DummyBot simula o comportamento do WebBot para testes offline sem navegador real.
    """

    def find_element(self, selector, by):
        """
        Simula a busca de elementos na página, retornando elementos fictícios.
        """

        class DummyElement:
            """
            Simula um elemento de input ou texto na página.
            """

            def __init__(self, text="5,00"):
                self.text = text

            def clear(self):
                """
                Simula a limpeza do texto no campo de input.
                """

            def send_keys(self, value):
                """
                Simula o envio de texto para o campo de input.
                """

        if "APjFqb" in selector:
            return DummyElement()
        if "updatable-data-column" in selector:
            return DummyElement("5,00")
        return DummyElement("11 de junho de 2025")

    def enter(self):
        """
        Simula o pressionamento da tecla ENTER.
        """

    driver = None


class DummyMaestro(BotMaestroSDK):
    """
    DummyMaestro herda de BotMaestroSDK para compatibilidade com a função buscar_cotacao.
    Simula o envio de artefatos durante testes.
    """

    def post_artifact(self, **kwargs):
        """
        Simula o envio de artefato, ignorando qualquer chamada real.
        """


def test_buscar_cotacao_sucesso():
    """
    Testa se a função buscar_cotacao retorna os valores esperados com o bot simulado.

    Pré-condições:
    - O bot retorna valores fixos para cotação e data.
    - Maestro simulado aceita post_artifact.

    Pós-condição:
    - A cotação deve ser '5,00'.
    - A data deve ser uma string contendo 'junho' ou '2025'.
    """
    bot = DummyBot()
    maestro = DummyMaestro()

    class DummyExecution:
        """
        Simula a execução de uma tarefa, com um task_id fictício.
        """

        task_id = "123"

    cotacao, data = buscar_cotacao(bot, "dólar", maestro, DummyExecution())
    assert cotacao == "5,00"
    assert isinstance(data, str)
    assert "2025" in data or "junho" in data

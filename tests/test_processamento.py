"""
Testes para a função processar_moedas, que itera sobre moedas e busca suas cotações.
"""

import pandas as pd
from botcity.maestro import BotMaestroSDK

from app.processamento_moedas import processar_moedas


class DummyBot:
    """
    Simula o WebBot com respostas fixas para os testes de cotações.
    """

    def find_element(self, selector, by):
        """
        Simula a busca de elementos na pagina, retornando um elemento com texto fixo.
        """

        class DummyElement:
            """
            Simula um elemento de input com texto fixo.
            """

            def __init__(self, text="5,00"):
                self.text = text

            def clear(self):
                """
                Simula a limpeza do campo de input.
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
        Simula o pressionamento da tecla Enter.
        """

    driver = None


class DummyMaestro(BotMaestroSDK):
    """
    DummyMaestro herda de BotMaestroSDK para compatibilidade com a função buscar_cotacao.
    Simula o envio de artefatos durante testes.
    """

    def new_log_entry(self, **kwargs):
        """
        Simula a criacao de uma nova entrada de log, ignorando qualquer chamada real.
        """

    def post_artifact(self, **kwargs):
        """
        Simula o envio de artefato, ignorando qualquer chamada real.
        """


class DummyExecution:
    """
    Simula a execução de uma tarefa, com um task_id fictício.
    """

    task_id = "123"


def test_processar_moedas():
    """
    Testa o processamento de múltiplas moedas com respostas simuladas.
    Deve retornar 2 processados, 0 falhas e DataFrame atualizado com cotações.
    """
    bot = DummyBot()
    maestro = DummyMaestro()
    execution = DummyExecution()

    df = pd.DataFrame(
        {"Moeda": ["dólar", "euro"], "Cotação": ["", ""], "Data": ["", ""]}
    )

    df_result, processados, falhas = processar_moedas(bot, df, maestro, execution)

    assert processados == 2
    assert falhas == 0
    assert df_result["Cotação"].iloc[0] == "5,00"
    assert df_result["Data"].iloc[0] != ""

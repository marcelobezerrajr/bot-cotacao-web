import pytest
from app.cotacao import buscar_cotacao


class DummyBot:
    def find_element(self, selector, by):
        class DummyElement:
            def __init__(self, text="5,00"):
                self.text = text

            def clear(self):
                pass

            def send_keys(self, value):
                pass

        if "APjFqb" in selector:
            return DummyElement()
        elif "updatable-data-column" in selector:
            return DummyElement("5,00")
        return DummyElement("11 de junho de 2025")

    def enter(self):
        pass

    driver = None


class DummyMaestro:
    def post_artifact(self, **kwargs):
        pass


def test_buscar_cotacao_sucesso():
    bot = DummyBot()
    maestro = DummyMaestro()

    class DummyExecution:
        task_id = "123"

    cotacao, data = buscar_cotacao(bot, "dólar", maestro, DummyExecution())
    assert cotacao == "5,00"
    assert isinstance(data, str)

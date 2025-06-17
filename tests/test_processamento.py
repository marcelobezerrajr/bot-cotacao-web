import pandas as pd
from app.processamento_moedas import ProcessamentoDadosMoedas


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
    def new_log_entry(self, **kwargs):
        pass

    def post_artifact(self, **kwargs):
        pass


class DummyExecution:
    task_id = "123"


def test_processar_moedas():
    bot = DummyBot()
    maestro = DummyMaestro()
    execution = DummyExecution()
    df = pd.DataFrame(
        {"Moeda": ["dólar", "euro"], "Cotação": ["", ""], "Data": ["", ""]}
    )

    df_result, processados, falhas = ProcessamentoDadosMoedas.processar_moedas(
        bot, df, maestro, execution
    )

    assert processados == 2
    assert falhas == 0
    assert df_result["Cotação"].iloc[0] == "5,00"

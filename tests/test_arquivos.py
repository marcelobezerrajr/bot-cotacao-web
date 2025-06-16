import pytest
import pandas as pd
from app.arquivos import carregar_dados_csv


class DummyBot:
    def get_resource_abspath(self, filename):
        return f"resources/{filename}"


def test_carregar_dados_csv_sucesso():
    bot = DummyBot()
    df = carregar_dados_csv(bot, "moedas.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_carregar_dados_csv_arquivo_nao_encontrado():
    bot = DummyBot()
    with pytest.raises(FileNotFoundError):
        carregar_dados_csv(bot, "inexistente.csv")

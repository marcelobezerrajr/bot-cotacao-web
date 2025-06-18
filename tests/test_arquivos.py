import pandas as pd
import pytest

from app.manipula_arquivos import ManipulaArquivosCSVExcel


class DummyBot:
    def get_resource_abspath(self, filename):
        return f"resources/{filename}"


def test_carregar_dados_csv_sucesso():
    bot = DummyBot()
    df = ManipulaArquivosCSVExcel.carregar_dados_csv(bot, "moedas.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_carregar_dados_csv_arquivo_nao_encontrado():
    bot = DummyBot()
    with pytest.raises(FileNotFoundError):
        ManipulaArquivosCSVExcel.carregar_dados_csv(bot, "inexistente.csv")

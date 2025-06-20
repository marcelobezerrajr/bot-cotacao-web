"""
Testes para a classe ManipulaArquivosCSVExcel, responsável por ler e salvar arquivos CSV e Excel.
"""

import pandas as pd
from app.manipula_arquivos import ManipulaArquivosCSVExcel


def test_carregar_dados_csv_sucesso():
    """
    Testa se o carregamento de um arquivo CSV existente retorna um DataFrame válido e não vazio.
    O arquivo 'moedas.csv' deve estar presente na pasta 'resources' com a coluna 'Moeda'.
    """
    manipulador = ManipulaArquivosCSVExcel()
    df = manipulador.carregar_dados_csv("moedas.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Moeda" in df.columns


def test_carregar_dados_csv_arquivo_nao_encontrado():
    """
    Testa se o carregamento de um arquivo inexistente retorna um DataFrame vazio.
    """
    manipulador = ManipulaArquivosCSVExcel()
    df = manipulador.carregar_dados_csv("inexistente.csv")
    assert df.empty

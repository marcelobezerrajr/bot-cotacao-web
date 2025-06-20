"""
Manipulacao de arquivos CSV e Excel.
"""

import logging
from pathlib import Path

import pandas as pd


class ManipulaArquivosCSVExcel:
    """
    Classe para manipulação de arquivos, incluindo carregamento de CSV e salvamento em Excel.
    """

    def __init__(self, base_dir: str = "resources") -> None:
        """
        Inicializa a classe e define o caminho base para os arquivos.
        :param base_dir: Diretório base para leitura/gravação.
        """
        self.base_dir = Path(base_dir)
        self.caminho_csv = None
        self.caminho_excel = None

    def carregar_dados_csv(self, nome_arquivo: str) -> pd.DataFrame:
        """
        Carrega os dados de um arquivo CSV em um DataFrame do pandas.

        :param nome_arquivo: Nome do arquivo CSV.

        :return: DataFrame contendo os dados.

        :raises FileNotFoundError: Se o arquivo não for encontrado.
        :raises Exception: Para outros erros ao ler o CSV.
        """
        self.caminho_csv = self.base_dir / nome_arquivo
        try:
            df = pd.read_csv(self.caminho_csv)
            if "Moeda" not in df.columns:
                raise ValueError("Coluna 'Moeda' não encontrada no CSV.")
            logging.info("%d registros carregados de %s.", len(df), self.caminho_csv)
            return df
        except FileNotFoundError:
            logging.error("Arquivo CSV não encontrado: %s", self.caminho_csv)
            return pd.DataFrame()
        except Exception as e:
            logging.exception(
                "Erro inesperado ao ler o CSV %s: %s", self.caminho_csv, e
            )
            raise

    def salvar_dados_excel(self, df: pd.DataFrame, nome_arquivo: str) -> Path:
        """
        Salva o DataFrame em um arquivo Excel.

        :param df: DataFrame a ser salvo.
        :param nome_arquivo: Nome do arquivo de saída.
        """
        self.caminho_excel = self.base_dir / nome_arquivo
        self.caminho_excel.parent.mkdir(parents=True, exist_ok=True)

        if df.empty:
            logging.warning("DataFrame está vazio. Nenhum dado será salvo.")
        else:
            df.to_excel(self.caminho_excel, index=False)
            logging.info("Arquivo salvo em: %s", self.caminho_excel)

        return self.caminho_excel

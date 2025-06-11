from pathlib import Path
import pandas as pd
import logging


def carregar_dados_csv(bot, nome_arquivo: str) -> pd.DataFrame:
    """
    Carrega os dados de um arquivo CSV em um DataFrame do pandas.

    :param bot: Instância do WebBot para resolver caminho do recurso.
    :param nome_arquivo: Nome do arquivo CSV.
    :return: DataFrame contendo os dados.
    :raises FileNotFoundError: Se o arquivo não for encontrado.
    :raises Exception: Para outros erros ao ler o CSV.
    """
    caminho = Path(bot.get_resource_abspath(nome_arquivo))
    try:
        df = pd.read_csv(caminho)
        if "Moeda" not in df.columns:
            raise ValueError("Coluna 'Moeda' não encontrada no CSV.")
        logging.info(f"{len(df)} registros carregados de '{nome_arquivo}'.")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao ler '{nome_arquivo}': {e}")


def salvar_dados_excel(df: pd.DataFrame, nome_arquivo: str):
    """
    Salva o DataFrame em um arquivo Excel.

    :param df: DataFrame a ser salvo.
    :param bot: Instância do WebBot para resolver o caminho.
    :param nome_arquivo: Nome do arquivo de saída.
    """
    caminho = Path("resources") / nome_arquivo
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(caminho, index=False)
    logging.info(f"Arquivo salvo em: {caminho}")

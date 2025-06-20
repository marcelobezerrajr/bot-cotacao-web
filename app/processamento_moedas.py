"""
Processa uma lista de moedas.
"""

import pandas as pd
from botcity.maestro import AlertType, BotMaestroSDK
from botcity.web import WebBot

from app.busca_cotacao import buscar_cotacao


def processar_moedas(
    bot: WebBot, df: pd.DataFrame, maestro: BotMaestroSDK, execution
) -> tuple[pd.DataFrame, int, int]:
    """
    Processa as moedas do DataFrame, buscando suas cotações.

    :param bot: Instância do WebBot.
    :param df: DataFrame contendo as moedas.
    :param maestro: Instância do BotMaestroSDK.
    :param execution: Instância do AutomationTask.
    :return: Tupla com DataFrame atualizado, total de processados e falhas.
    """
    processados = falhas = 0

    for i, linha in df.iterrows():
        moeda = linha["Moeda"]
        try:
            cotacao, data = buscar_cotacao(bot, moeda, maestro, execution)
            df.at[i, "Cotação"] = cotacao
            df.at[i, "Data"] = data
            processados += 1

            maestro.new_log_entry(
                activity_label="Consulta-Cotacao",
                values={"Moeda": moeda, "Cotação": cotacao, "Data": data},
            )
        except ValueError as e:
            maestro.alert(
                task_id=execution.task_id,
                title=f"Dados Inválidos para Moeda: {moeda}",
                message=f"Falha ao buscar cotação: {e}. Verifique os dados de entrada.",
                alert_type=AlertType.ERROR,
            )
            falhas += 1

    return df, processados, falhas

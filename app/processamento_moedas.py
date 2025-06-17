from botcity.web import WebBot
from botcity.maestro import BotMaestroSDK, AutomationTask
from typing import Tuple
import pandas as pd
import logging

from app.busca_cotacao import BuscarCotacao


class ProcessamentoDadosMoedas:
    """
    Classe responsável por processar os dados das moedas, preenchendo cotações e datas.
    """

    def processar_moedas(
        bot: WebBot, df: pd.DataFrame, maestro: BotMaestroSDK, execution: AutomationTask
    ) -> Tuple[pd.DataFrame, int, int]:
        """
        Processa o DataFrame para preencher cotações e datas das moedas.

        :param bot: Instância do WebBot.
        :param df: DataFrame contendo as moedas.
        :param maestro: Instância do BotMaestroSDK.
        :param execution: Instância do AutomationTask.

        :return: Tupla contendo o DataFrame atualizado, número de registros processados e falhas.

        :raises Exception: Se ocorrer um erro ao processar as moedas.
        """

        processados = 0
        falhas = 0

        for index, row in df.iterrows():
            moeda = row.get("Moeda")
            if not moeda:
                logging.warning(f"[Linha {index}] Registro está incompleto.")
                falhas += 1
                continue

            try:
                logging.info(f"[Linha {index}] Processando moeda: {moeda}")
                cotacao, data = BuscarCotacao.buscar_cotacao(
                    bot, moeda, maestro, execution
                )
                df.at[index, "Cotação"] = cotacao
                df.at[index, "Data"] = data
                processados += 1

                maestro.new_log_entry(
                    activity_label="Consulta-Cotacao",
                    values={"moeda": moeda, "cotacao": cotacao, "data": data},
                )
            except Exception as e:
                logging.error(f"[Linha {index}] Falha ao processar {moeda}: {e}")
                falhas += 1

        return df, processados, falhas

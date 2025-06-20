"""
Busca a cotacao de uma moeda no Google.
"""

from typing import Tuple

from botcity.maestro import BotMaestroSDK
from botcity.web import By, WebBot

from utils.screenshot_error import screenshot_error


def buscar_cotacao(
    bot: WebBot, moeda: str, maestro: BotMaestroSDK, execution
) -> Tuple[str, str]:
    """
    Realiza uma busca no Google para obter cotação e data da moeda.

    :param bot: Instância do WebBot.
    :param moeda: Nome da moeda.
    :param maestro: Instância do BotMaestroSDK.
    :param execution: Instância do AutomationTask.
    :return: Tupla com cotação e data.
    :raises RuntimeError: Em caso de falha ao localizar elementos.
    """
    try:
        # pesquisa = bot.find_element('//*[@id="APjFqb"]', By.XPATH)
        pesquisa = bot.find_element("#APjFqb", By.CSS_SELECTOR)
        pesquisa.clear()
        pesquisa.send_keys(f"Cotação do {moeda} hoje")
        bot.enter()

        cotacao = bot.find_element(
            # '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]',
            # By.XPATH,
            "#knowledge-currency__updatable-data-column > div.b1hJbf >"
            " div.dDoNo.ikb4Bb.gsrt.GDBPqd > span.DFlfde.SwHCTb",
            By.CSS_SELECTOR,
        ).text

        data = bot.find_element(
            # '//*[@id="knowledge-currency__updatable-data-column"]/div[2]/span[1]',
            # By.XPATH,
            "#knowledge-currency__updatable-data-column > div.k0Rg6d.hqAUc > span:nth-child(1)",
            By.CSS_SELECTOR,
        ).text

        return cotacao, data

    except RuntimeError as e:
        screenshot_path = screenshot_error(bot.driver, f"Erro_{moeda}")
        maestro.post_artifact(
            task_id=execution.task_id,
            artifact_name=f"Erro - {moeda}",
            filepath=screenshot_path,
        )
        raise RuntimeError(f"Erro ao buscar cotação da moeda {moeda}: {e}") from e

from botcity.web import WebBot, By
from botcity.maestro import BotMaestroSDK, AutomationTask
from utils.screenshot_error import screenshot_error
from typing import Tuple


def buscar_cotacao(
    bot: WebBot, moeda: str, maestro: BotMaestroSDK, execution: AutomationTask
) -> Tuple[str, str]:
    """
    Realiza uma busca no Google para obter cotação e data da moeda.

    :param bot: Instância do WebBot.
    :param moeda: Nome da moeda.
    :return: Tupla com cotação e data.
    :raises RuntimeError: Em caso de falha ao localizar elementos.
    """
    try:
        pesquisa = bot.find_element('//*[@id="APjFqb"]', By.XPATH)
        pesquisa.clear()
        pesquisa.send_keys(f"Cotação do {moeda} hoje")
        bot.enter()

        cotacao = bot.find_element(
            '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]',
            By.XPATH,
        ).text

        data = bot.find_element(
            '//*[@id="knowledge-currency__updatable-data-column"]/div[2]/span[1]',
            By.XPATH,
        ).text

        return cotacao, data

    except Exception as e:
        screenshot_path = screenshot_error(bot.driver, f"Erro_{moeda}")
        maestro.post_artifact(
            task_id=execution.task_id,
            artifact_name=f"Erro - {moeda}",
            filepath=screenshot_path,
        )
        raise RuntimeError(f"Erro ao buscar cotação da moeda {moeda}: {e}")

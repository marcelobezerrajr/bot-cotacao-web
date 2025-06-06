import logging
from botcity.web import WebBot, Browser, By
from botcity.plugins.csv import BotCSVPlugin
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Dict, Tuple

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BotMaestroSDK.RAISE_NOT_CONNECTED = False


def carregar_dados_csv(bot: WebBot, nome_arquivo: str) -> List[Dict[str, str]]:
    """
    Lê um arquivo CSV localizado nos recursos do projeto e retorna os dados como uma lista de dicionários.

    :param bot: Instância do WebBot usada para resolver o caminho do recurso.
    :param nome_arquivo: Nome do arquivo CSV a ser lido.
    :return: Lista de dicionários com os dados do CSV.
    :raises FileNotFoundError: Se o arquivo não for encontrado.
    :raises Exception: Para erros genéricos na leitura do arquivo.
    """
    caminho = bot.get_resource_abspath(nome_arquivo)
    planilha = BotCSVPlugin()
    try:
        dados = planilha.read(caminho).as_dict()
        logging.info(f"{len(dados)} registros carregados de '{nome_arquivo}'.")
        return dados
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao ler '{nome_arquivo}': {e}")


def buscar_cotacao(bot: WebBot, moeda: str) -> Tuple[str, str]:
    """
    Realiza uma pesquisa no Google para obter a cotação e a data atual da moeda fornecida.

    :param bot: Instância do WebBot usada para interagir com o navegador.
    :param moeda: Nome da moeda a ser consultada.
    :return: Tupla com (cotação, data).
    :raises RuntimeError: Em caso de falha ao buscar a cotação.
    """
    try:
        pesquisa = bot.find_element('//*[@id="APjFqb"]', By.XPATH)
        pesquisa.clear()
        pesquisa.send_keys(f"Cotação do {moeda} hoje")
        bot.enter()
        bot.wait(500)

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
        raise RuntimeError(f"Erro ao buscar cotação da moeda {moeda}: {e}")


def salvar_dados_csv(bot: WebBot, planilha: BotCSVPlugin, nome_arquivo: str) -> None:
    """
    Salva os dados da planilha em um arquivo CSV.

    :param bot: Instância do WebBot usada para resolver o caminho do arquivo.
    :param planilha: Instância do BotCSVPlugin com os dados atualizados.
    :param nome_arquivo: Nome do arquivo de saída.
    """
    caminho_saida = bot.get_resource_abspath(nome_arquivo)
    planilha.write(caminho_saida)
    logging.info(f"Arquivo salvo em: {caminho_saida}")


def processar_moedas(
    bot: WebBot, planilha: BotCSVPlugin, dados: List[Dict[str, str]]
) -> Tuple[int, int]:
    """
    Processa a lista de moedas, busca as cotações e atualiza a planilha com os resultados.

    :param bot: Instância do WebBot.
    :param planilha: Instância do BotCSVPlugin a ser preenchida.
    :param dados: Lista de dicionários com os dados das moedas.
    :return: Tupla com (quantidade de processados, quantidade de falhas).
    """
    processados = 0
    falhas = 0

    for i, linha in enumerate(dados):
        moeda = linha.get("Moeda")
        if not moeda:
            logging.warning(f"Registro na linha {i} está incompleto.")
            falhas += 1
            continue

        try:
            logging.info(f"Processando: {moeda}")
            cotacao, data = buscar_cotacao(bot, moeda)
            planilha.set_entry("Moeda", i, moeda)
            planilha.set_entry("Cotação", i, cotacao)
            planilha.set_entry("Data", i, data)
            processados += 1
        except Exception as e:
            logging.error(f"Falha ao processar {moeda}: {e}")
            falhas += 1

    return processados, falhas


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()
    logging.info(f"Tarefa Maestro ID: {execution.task_id}")

    bot = WebBot()
    bot.headless = execution.parameters.get("headless", "false").lower() == "true"
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

    total = 0
    processados = 0
    falhas = 0

    planilha = BotCSVPlugin()

    try:
        dados = carregar_dados_csv(bot, "moedas.csv")
        total = len(dados)
    except Exception as e:
        logging.critical(str(e))
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.FAILED,
            message=str(e),
            total_items=total,
            processed_items=processados,
            failed_items=falhas,
        )
        return

    logging.info("Iniciando busca no Google...")
    bot.browse("https://www.google.com")
    bot.wait(1000)

    processados, falhas = processar_moedas(bot, planilha, dados)

    salvar_dados_csv(bot, planilha, "moedas_atualizadas.csv")

    bot.wait(1000)
    bot.stop_browser()

    status = (
        AutomationTaskFinishStatus.SUCCESS
        if falhas == 0
        else AutomationTaskFinishStatus.FAILED
    )
    mensagem = (
        "Bot finalizado com sucesso."
        if falhas == 0
        else f"Bot finalizado com {falhas} falhas."
    )

    maestro.finish_task(
        task_id=execution.task_id,
        status=status,
        message=mensagem,
        total_items=total,
        processed_items=processados,
        failed_items=falhas,
    )


if __name__ == "__main__":
    main()

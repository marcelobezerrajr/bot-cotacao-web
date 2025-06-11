import logging
import pandas as pd
from typing import Tuple
from botcity.web import WebBot, Browser, By
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager
from utils.screenshot_error import screenshot_error

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BotMaestroSDK.RAISE_NOT_CONNECTED = False


def carregar_dados_csv(bot: WebBot, nome_arquivo: str) -> pd.DataFrame:
    """
    Carrega os dados de um arquivo CSV em um DataFrame do pandas.

    :param bot: Instância do WebBot para resolver caminho do recurso.
    :param nome_arquivo: Nome do arquivo CSV.
    :return: DataFrame contendo os dados.
    :raises FileNotFoundError: Se o arquivo não for encontrado.
    :raises Exception: Para outros erros ao ler o CSV.
    """
    caminho = bot.get_resource_abspath(nome_arquivo)
    try:
        df = pd.read_csv(caminho)
        logging.info(f"{len(df)} registros carregados de '{nome_arquivo}'.")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao ler '{nome_arquivo}': {e}")


def buscar_cotacao(bot: WebBot, moeda: str) -> Tuple[str, str]:
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
        screenshot_error(bot.driver, f"Erro {moeda}")
        raise RuntimeError(f"Erro ao buscar cotação da moeda {moeda}: {e}")


def salvar_dados_excel(df: pd.DataFrame, bot: WebBot, nome_arquivo: str) -> None:
    """
    Salva o DataFrame em um arquivo Excel.

    :param df: DataFrame a ser salvo.
    :param bot: Instância do WebBot para resolver o caminho.
    :param nome_arquivo: Nome do arquivo de saída.
    """
    caminho = bot.get_resource_abspath(nome_arquivo)
    df.to_excel(caminho, index=False)
    logging.info(f"Arquivo salvo em: {caminho}")


def processar_moedas(
    bot: WebBot, df: pd.DataFrame, maestro: BotMaestroSDK, execution: AutomationTask
) -> Tuple[pd.DataFrame, int, int]:
    processados = 0
    falhas = 0

    for i, row in df.iterrows():
        moeda = row.get("Moeda")
        if not moeda:
            logging.warning(f"Registro na linha {i} está incompleto.")
            falhas += 1
            continue

        try:
            maestro.alert(
                task_id=execution.task_id,
                title=f"Consultando {moeda}",
                message=f"Buscando cotação da moeda: {moeda}...",
                alert_type=AlertType.INFO,
            )

            logging.info(f"Processando: {moeda}")
            cotacao, data = buscar_cotacao(bot, moeda)
            df.at[i, "Cotação"] = cotacao
            df.at[i, "Data"] = data
            processados += 1

            maestro.new_log_entry(
                activity_label="Consulta-Cotacao",
                values={
                    "moeda": moeda,
                    "cotacao": cotacao,
                    "data": data,
                },
            )

        except Exception as e:
            logging.error(f"Falha ao processar {moeda}: {e}")
            falhas += 1

    return df, processados, falhas


def main() -> None:
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

    try:
        maestro.alert(
            task_id=execution.task_id,
            title="Iniciando o processo",
            message="Carregando dados do arquivo CSV...",
            alert_type=AlertType.INFO,
        )

        df = carregar_dados_csv(bot, "moedas.csv")
        total = len(df)
    except Exception as e:
        logging.critical(str(e))
        bot.save_screenshot("erro.png")

        maestro.alert(
            task_id=execution.task_id,
            title="Erro ao carregar dados",
            message=str(e),
            alert_type=AlertType.ERROR,
        )

        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.FAILED,
            message=str(e),
            total_items=total,
            processed_items=processados,
            failed_items=falhas,
        )
        return

    maestro.alert(
        task_id=execution.task_id,
        title="Acessando Google",
        message="Abrindo navegador para buscar as cotações...",
        alert_type=AlertType.INFO,
    )

    bot.browse("https://www.google.com")
    bot.wait(2000)

    maestro.alert(
        task_id=execution.task_id,
        title="Iniciando busca",
        message="Consultando cotações de moedas...",
        alert_type=AlertType.INFO,
    )

    df, processados, falhas = processar_moedas(bot, df, maestro, execution)

    salvar_dados_excel(df, bot, "moedas_atualizadas.xlsx")

    bot.wait(2000)
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

    maestro.alert(
        task_id=execution.task_id,
        title="Processo finalizado",
        message=mensagem,
        alert_type=AlertType.INFO if falhas == 0 else AlertType.WARNING,
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

from botcity.web import WebBot, Browser
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager
from app.arquivos import carregar_dados_csv, salvar_dados_excel
from app.processamento import processar_moedas
import logging
import tempfile

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()
    logging.info(f"Tarefa Maestro ID: {execution.task_id}")

    bot = WebBot()
    bot.browser = Browser.CHROME
    bot.headless = True
    bot.driver_path = ChromeDriverManager().install()

    user_data_dir = tempfile.mkdtemp()

    bot.extra_options = [
        "--headless=new",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        f"--user-data-dir={user_data_dir}",
    ]

    total = processados = falhas = 0

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

        maestro.error(task_id=execution.task_id, exception=e, screenshot="erro.png")

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

    bot.browse("https://www.google.com")
    bot.wait(2000)

    maestro.alert(
        task_id=execution.task_id,
        title="Iniciando busca",
        message="Consultando cotações de moedas...",
        alert_type=AlertType.INFO,
    )

    df, processados, falhas = processar_moedas(bot, df, maestro, execution)
    salvar_dados_excel(df, "moedas_atualizadas.xlsx")

    maestro.post_artifact(
        task_id=execution.task_id,
        artifact_name="Cotações atualizadas",
        filepath=bot.get_resource_abspath("resources/moedas_atualizadas.xlsx"),
    )

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
        alert_type=AlertType.INFO if falhas == 0 else AlertType.WARN,
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

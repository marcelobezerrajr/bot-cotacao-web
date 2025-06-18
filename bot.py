import logging

from botcity.maestro import AlertType, AutomationTaskFinishStatus, BotMaestroSDK
from botcity.web import WebBot

from app.bot_anonimo import ConfiguraBotAnonimo
from app.manipula_arquivos import ManipulaArquivosCSVExcel
from app.processamento_moedas import ProcessamentoDadosMoedas

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()
    logging.info(f"Tarefa Maestro ID: {execution.task_id}")

    bot = WebBot()
    ConfiguraBotAnonimo.configurar_bot_anonimo(bot)

    total = processados = falhas = 0

    try:
        maestro.alert(
            task_id=execution.task_id,
            title="Iniciando o processo",
            message="Carregando dados do arquivo CSV...",
            alert_type=AlertType.INFO,
        )

        df = ManipulaArquivosCSVExcel.carregar_dados_csv(bot, "moedas.csv")
        total = len(df)
    except Exception as e:
        logging.critical(str(e))

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

    df, processados, falhas = ProcessamentoDadosMoedas.processar_moedas(
        bot, df, maestro, execution
    )
    ManipulaArquivosCSVExcel.salvar_dados_excel(df, "moedas_atualizadas.xlsx")

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

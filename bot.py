"""
Bot para buscar cotacoes de moedas no Google e salvar em Excel.
"""

import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from botcity.maestro import AlertType, AutomationTaskFinishStatus, BotMaestroSDK
from botcity.web import WebBot

from app.bot_anonimo import configurar_bot_anonimo
from app.manipula_arquivos import ManipulaArquivosCSVExcel
from app.processamento_moedas import processar_moedas

log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / f"bot_cotacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

BotMaestroSDK.RAISE_NOT_CONNECTED = False  # type: ignore


class BotCotacao:
    """
    Bot para buscar cotacoes de moedas no Google e salvar em Excel.
    """

    def __init__(self):
        """
        Inicializa o BotMaestroSDK com as configurações do BotCity Maestro.
        """
        logging.info("Iniciando o Bot de Cotações de Moedas...")
        self.maestro = BotMaestroSDK.from_sys_args()
        self.execution = self.maestro.get_execution()
        logging.info("Tarefa Maestro ID: %s", self.execution.task_id)

        self.bot = WebBot()
        configurar_bot_anonimo(self.bot)

    def main(self):
        """
        Função principal que executa o bot para buscar cotações de moedas.
        """

        total = processados = falhas = 0

        try:
            self.maestro.alert(
                task_id=self.execution.task_id,
                title="Iniciando o processo",
                message="Carregando dados do arquivo CSV...",
                alert_type=AlertType.INFO,
            )

            manipulador = ManipulaArquivosCSVExcel()
            df = manipulador.carregar_dados_csv("moedas.csv")
            total = len(df)

        except FileNotFoundError as e:
            logging.critical("Arquivo CSV não encontrado: %s", e)

            self.maestro.error(
                task_id=int(self.execution.task_id), exception=e, screenshot="erro.png"
            )
            self.maestro.alert(
                task_id=self.execution.task_id,
                title="Arquivo CSV não encontrado",
                message=str(e),
                alert_type=AlertType.ERROR,
            )

        except pd.errors.ParserError as e:
            logging.critical("Erro ao processar o CSV: %s", e)
            self.maestro.error(
                task_id=int(self.execution.task_id), exception=e, screenshot="erro.png"
            )
            self.maestro.alert(
                task_id=self.execution.task_id,
                title="Erro de leitura CSV",
                message="Erro ao ler ou processar o arquivo CSV.",
                alert_type=AlertType.ERROR,
            )

        except (OSError, ValueError) as e:
            logging.critical("Erro inesperado: %s", e)
            self.maestro.error(
                task_id=int(self.execution.task_id), exception=e, screenshot="erro.png"
            )
            self.maestro.alert(
                task_id=self.execution.task_id,
                title="Erro inesperado",
                message=str(e),
                alert_type=AlertType.ERROR,
            )

        else:
            self.bot.browse("https://www.google.com")
            self.bot.wait(2000)

        self.maestro.alert(
            task_id=self.execution.task_id,
            title="Iniciando busca",
            message="Consultando cotações de moedas...",
            alert_type=AlertType.INFO,
        )

        df, processados, falhas = processar_moedas(
            self.bot, df, self.maestro, self.execution
        )

        caminho_excel = manipulador.salvar_dados_excel(df, "moedas_atualizadas.xlsx")

        caminho_absoluto = self.bot.get_resource_abspath(str(caminho_excel))
        if caminho_absoluto:
            self.maestro.post_artifact(
                task_id=int(self.execution.task_id),
                artifact_name="Cotações atualizadas",
                filepath=caminho_absoluto,
            )
        else:
            logging.warning(
                "Caminho absoluto para o arquivo não encontrado. Artefato não enviado."
            )

        self.bot.wait(2000)
        self.bot.stop_browser()

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

        self.maestro.alert(
            task_id=self.execution.task_id,
            title="Processo finalizado",
            message=mensagem,
            alert_type=AlertType.INFO if falhas == 0 else AlertType.WARN,
        )

        self.maestro.finish_task(
            task_id=self.execution.task_id,
            status=status,
            message=mensagem,
            total_items=total,
            processed_items=processados,
            failed_items=falhas,
        )

        logging.info("Bot finalizado com status: %s", status.name)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    bot = BotCotacao()
    bot.main()

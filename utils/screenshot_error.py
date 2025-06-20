"""
Captura de screenshots em caso de erros.
"""

import os
from datetime import datetime


def screenshot_error(driver, error_message):
    """
    Captura uma screenshot da página atual no navegador em caso de erro.

    :param driver: Instância do driver do navegador.
    :param error_message: Nome ou descrição do erro.
    :return: Caminho completo do arquivo de screenshot salvo.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"resources/screenshot_{error_message}_{timestamp}.png"
    driver.save_screenshot(nome_arquivo)

    print(f"Screenshot salva {nome_arquivo}")
    return os.path.abspath(nome_arquivo)

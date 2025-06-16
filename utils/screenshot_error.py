def screenshot_error(driver, error_message) -> str:
    """
    Faz uma captura de tela da janela atual do navegador e a salva com a mensagem de erro como parte do nome do arquivo.

    :param driver: A instância do Selenium WebDriver.
    :param error_message: Uma string contendo a mensagem de erro a ser incluída no nome do arquivo da captura de tela.

    :return: Caminho da captura de tela salva.
    """
    import time

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_error_message = "".join(c if c.isalnum() else "_" for c in error_message)
    screenshot_filename = f"screenshot_{timestamp}_{safe_error_message}.png"
    driver.save_screenshot(screenshot_filename)

    print(f"Screenshot saved as {screenshot_filename}")
    return screenshot_filename

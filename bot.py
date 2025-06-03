"""
WARNING:

Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
in order to get all the dependencies on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the dependencies.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at
https://documentation.botcity.dev/tutorials/python-automations/web/
"""

# Import for the Web Bot
from botcity.web import WebBot, Browser, By
from botcity.plugins.csv import BotCSVPlugin

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Import for the Web Driver Manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    planilha = BotCSVPlugin()

    dados = planilha.read(bot.get_resource_abspath("moedas.csv")).as_dict()
    print(f"Dados lidos do CSV: {dados}")

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path = ChromeDriverManager().install()

    # Opens the Google website.
    bot.browse("https://www.google.com")

    # Implement here your logic...

    for index, linha in enumerate(dados):
        pesquisa = bot.find_element("APjFqb", By.ID)
        pesquisa.clear()
        pesquisa.send_keys(f"cotação do {linha['moeda']} hoje")
        bot.enter()

        cotacao = bot.find_element(
            '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]',
            By.XPATH,
        )
        print(f"Valor da cotação do {linha['moeda']} hoje: {cotacao.text}")

        data = bot.find_element(".k0Rg6d.hqAUc > span:nth-child(1)", By.CSS_SELECTOR)
        print(f"Data da cotação do {linha['moeda']} hoje: {data.text}")

        planilha.set_entry("cotacao", index, cotacao.text)
        planilha.set_entry("data", index, data.text)

    planilha.write(bot.get_resource_abspath("moedas_atualizadas.csv"))

    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Bot Cotação Moedas finalizado com sucesso.",
        total_items=0,
        processed_items=0,
        failed_items=0,
    )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == "__main__":
    main()

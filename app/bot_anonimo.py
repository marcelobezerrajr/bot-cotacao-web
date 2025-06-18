import tempfile

from botcity.web import Browser
from webdriver_manager.chrome import ChromeDriverManager


class ConfiguraBotAnonimo:
    """
    Classe para configurar o WebBot para rodar de forma anônima e headless com Google Chrome.
    """

    def configurar_bot_anonimo(bot, user_data_dir=None):
        """
        Configura o WebBot para rodar de forma anônima e headless com Google Chrome.

        :param bot: Instância do WebBot a ser configurada.
        :param user_data_dir: Caminho opcional para o diretório de perfil do usuário.
                            Se não for informado, será criado um temporário.
        """

        if user_data_dir is None:
            user_data_dir = tempfile.mkdtemp()

        bot.browser = Browser.CHROME
        bot.headless = True
        bot.driver_path = ChromeDriverManager().install()

        bot.extra_options = [
            "--headless=new",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-gpu",
            "--window-size=1920,1080",
            "--lang=pt-BR",
            f"--user-data-dir={user_data_dir}",
            "--user-agent=Chrome/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        ]

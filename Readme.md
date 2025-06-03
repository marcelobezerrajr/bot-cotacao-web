# Bot de Cotação de Moedas com Python e BotCity 🤖

Este projeto é um bot de automação criado com [BotCity](https://botcity.dev/) que realiza buscas no Google para obter a cotação atual de diferentes moedas, com base em uma planilha CSV de entrada. Os resultados são extraídos e salvos em uma nova planilha CSV, automatizando completamente o processo de pesquisa de valores de câmbio.

## 🚀 Funcionalidades

- Leitura de uma planilha CSV com a lista de moedas.
- Abertura do navegador e busca da cotação de cada moeda no Google.
- Extração do valor da cotação e da data.
- Escrita dos dados atualizados em uma nova planilha CSV.
- Integração com o BotCity Maestro para gestão de tarefas automatizadas.

## 🛠️ Tecnologias Utilizadas

- Python
- BotCity Web SDK
- BotCity Maestro SDK
- Selenium WebDriver (gerenciado pelo `webdriver-manager`)
- Google Chrome
- CSV Plugin do BotCity
